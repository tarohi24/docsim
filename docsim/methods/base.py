from dataclasses import dataclass
from pathlib import Path
import sys
from typing import List

from tqdm import tqdm

from docsim.elas.search import EsResult, EsSearcher
from docsim.trec import RankItem, TRECConverter
from docsim.models import QueryDataset, QueryDocument
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
class Searcher:
    query_dataset: QueryDataset
    param: Param
    trec_converter: TRECConverter
    is_fake: bool

    def retrieve(self, query: QueryDocument) -> RankItem:
        raise NotImplementedError('This is an abstract class.')

    def run(self) -> None:
        items: List[RankItem] = []
        for query in tqdm(self.query_dataset.queries):
            res: RankItem = self.retrieve(query)
            items.append(res)

            # dump result
            if not self.is_fake:
                self.dump_trec(res)

    def dump_trec(self, item: RankItem) -> None:
        self.trec_converter.incremental_dump(item)

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
