"""
Keyword search
"""
from dataclasses import dataclass
from typing import List

from dataclasses_jsonschema import JsonSchemaMixin

from docsim import text
from docsim.elas.search import EsResult, EsSearcher
from docsim.ir.methods.base import Searcher, Param
from docsim.ir.models import QueryDocument
from docsim.ir.trec import RankItem
from docsim.text import Filter


@dataclass
class KeywordBaselineParam(Param, JsonSchemaMixin):
    n_words: int


@dataclass
class KeywordBaseline(Searcher):
    param: KeywordBaselineParam

    @classmethod
    def method_name(cls) -> str:
        return 'keyword'

    def retrieve(self,
                 query_doc: QueryDocument,
                 size: int = 100) -> RankItem:
        filters: List[Filter] = [
            text.LowerFilter(),
            text.StopWordRemover(),
            text.RegexRemover(),
            text.TFFilter(n_words=self.param.n_words)]
        q_words: List[str] = text.TextProcessor(filters=filters)\
            .apply(query_doc.text)
        # search elasticsearch
        searcher: EsSearcher = EsSearcher(es_index=self.query_dataset.name)
        res: EsResult = searcher\
            .initialize_query()\
            .add_query(terms=q_words, field='text')\
            .add_size(size)\
            .add_filter(terms=query_doc.tags, field='tags')\
            .search()
        return res.to_rank_item(query_id=query_doc.docid)
