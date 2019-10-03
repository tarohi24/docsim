"""
Keyword search
"""
from dataclasses import dataclass

from dataclasses_jsonschema import JsonSchemaMixin

from docsim.elas.search import EsResult
from docsim.methods.base import Searcher, Param
from docsim.models import QueryDocument
from docsim.trec import RankItem


@dataclass
class KeywordBaselineParam(Param, JsonSchemaMixin):
    n_words: int


@dataclass
class KeywordBaseline(Searcher):
    param: KeywordBaselineParam

    def retrieve(self,
                 query_doc: QueryDocument,
                 size: int = 100) -> RankItem:
        # search elasticsearch
        res: EsResult = self.filter_by_terms(text=query_doc.text,
                                             n_words=self.param.n_words,
                                             size=size)
        return res.to_rank_item(query_id=query_doc.docid)
