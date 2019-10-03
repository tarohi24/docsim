from dataclasses import dataclass
from number import Real
from pathlib import Path
import sys
from typing import Dict, List

from tqdm import tqdm

from docsim.clf import ClfResult
from docsim.elas.search import EsResult, EsSearcher
from docsim.trec import TRECConverter
from docsim.models import RankItem, QueryDataset, QueryDocument
from docsim.text import (
    Filter,
    TextProcessor,
    LowerFilter,
    StopWordRemover,
    RegexRemover,
    TFFilter
)


class Param:
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

    def run_retrieve(self,
                     query: QueryDocument,
                     trec_converter: TRECConverter) -> None:
        for query in tqdm(self.query_dataset.queries):
            ri: RankItem = self.apply(query)
            scores: Dict[str, Real] = ri.get_doc_scores()
            # dump result
            if not self.is_fake:
                self.dump_trec(query_id=query.docid,
                               scores=scores,
                               trec_converter=trec_converter)

    def run_clf(self, query: QueryDocument) -> RankItem:
        clf_res: ClfResult = ClfResult(
            dataset_name=self.query_dataset.name,
            method_name=self.__class__.method_name)
        for query in tqdm(self.query_dataset.queries):
            ri: RankItem = self.apply(query)
            clf_res.result[query.docid] = ri.pred_tags(n_top=3)
            # dump result
            if not self.is_fake:
                clf_res.dump()

    def dump_trec(self,
                  query_id: str,
                  scores: Dict[str, Real],
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
            .add_source_fields(['text', ])\
            .add_filter(terms=query_doc.tags, field='tags')\
            .search()
        return res
