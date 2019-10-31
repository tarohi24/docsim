from dataclasses import dataclass
import logging
from pathlib import Path
import sys
from typing import Dict, List

from dataclasses_jsonschema import JsonSchemaMixin
from tqdm import tqdm

from docsim.clf import ClfResult
from docsim.elas.search import EsResult, EsSearcher
from docsim.ir import TRECConverter
from docsim.models import RankItem, QueryDataset, QueryDocument
from docsim.text import (
    Filter,
    TextProcessor,
    LowerFilter,
    StopWordRemover,
    RegexRemover,
    TFFilter
)


class Param(JsonSchemaMixin):
    pass


@dataclass
class Method:
    query_dataset: QueryDataset
    param: Param
    is_fake: bool

    def apply(self,
              query: QueryDocument) -> RankItem:
        """
        Methob body (in common among all tasks)

        Retutn
        -----------
        (key)
            (Docid, tag)
        (value)
            The probability the key emerges.
        """
        raise NotImplementedError('This is an abstract method')

    def clear_results(self,
                      path: Path) -> None:
        try:
            # IR path
            path.unlink()
        except FileNotFoundError:
            pass

    def run(self) -> None:
        logger = logging.getLogger(self.method_name())
        trec_converter: TRECConverter = TRECConverter(
            method_name=self.method_name(),
            dataset_name=self.query_dataset.name)
        clf_res: ClfResult = ClfResult(
            method_name=self.method_name(),
            dataset_name=self.query_dataset.name)

        if not self.is_fake:
            # clear existing result files
            self.clear_results(trec_converter.get_fpath())
            self.clear_results(clf_res.get_fpath())

        qlen: int = len(self.query_dataset.queries)
        for i, query in tqdm(enumerate(self.query_dataset.queries)):
            # loggging
            logger.info(f'Query {i} / {qlen} ...')
            ri: RankItem = self.apply(query)
            ir_scores: Dict[str, float] = ri.get_doc_scores()
            clf_res.result[query.docid] = ri.pred_tags(n_top=len(ri))
            if not self.is_fake:
                logger.info('dumping...')
                self.dump_trec(query_id=query.docid,
                               scores=ir_scores,
                               trec_converter=trec_converter)
                clf_res.dump()

    def dump_trec(self,
                  query_id: str,
                  scores: Dict[str, float],
                  trec_converter: TRECConverter) -> None:
        trec_converter.incremental_dump(query_id, scores)

    @classmethod
    def method_name(cls) -> str:
        return Path(sys.modules[cls.__module__].__file__).stem

    def _get_query_with_custom_filters(self,
                                       text: str,
                                       filters: List[Filter]) -> List[str]:
        q_words: List[str] = TextProcessor(filters=filters)\
            .apply(text)
        return q_words

    def get_default_filtes(self,
                           n_words: int) -> List[Filter]:
        filters: List[Filter] = [
            LowerFilter(),
            SPMFilter(),
            StopWordRemover(),
            RegexRemover(),
            TFFilter(n_words=n_words)]
        return filters

    def get_query_words(self,
                        text: str,
                        n_words: int) -> List[str]:
        filters: List[Filter] = self.get_default_filtes(n_words=n_words)
        return self._get_query_with_custom_filters(text=text,
                                                   filters=filters)

    def filter_by_terms(self,
                        query_doc: QueryDocument,
                        n_words: int,
                        size: int) -> EsResult:
        q_words: List[str] = self.get_query_words(text=query_doc.text,
                                                  n_words=n_words)
        searcher: EsSearcher = EsSearcher(es_index=self.query_dataset.name)
        res: EsResult = searcher\
            .initialize_query()\
            .add_query(terms=q_words, field='text')\
            .add_size(size)\
            .add_source_fields(['text', 'tags', ])\
            .add_filter(terms=query_doc.tags, field='tags')\
            .search()
        return res
