"""
Keyword search
"""
from dataclasses import dataclass

from dataclasses_jsonschema import JsonSchemaMixin

from docsim.elas.search import EsResult
from docsim.methods.base import Method, Param
from docsim.models import QueryDocument
from docsim.models import RankItem


@dataclass
class KeywordBaselineParam(Param, JsonSchemaMixin):
    n_words: int


@dataclass
class KeywordBaseline(Method):
    param: KeywordBaselineParam

    def apply(self,
              query_doc: QueryDocument,
              size: int = 100) -> RankItem:
        # search elasticsearch
        res: EsResult = self.filter_by_terms(query_doc=query_doc,
                                             n_words=self.param.n_words,
                                             size=size)
        return res.to_rank_item(query_id=query_doc.docid)
