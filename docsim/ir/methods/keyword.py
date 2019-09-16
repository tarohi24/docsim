"""
Keyword search
"""
from dataclasses import dataclass
from typing import List

from docsim import text
from docsim.elas.search import EsResult, EsSearcher
from docsim.ir.methods.base import Searcher
from docsim.ir.models import QueryDocument
from docsim.ir.trec import RankItem
from docsim.text import Filter


@dataclass
class KeywordBaseline(Searcher):
    n_words: int
    es_index: str

    def retrieve(self,
                 query_doc: QueryDocument,
                 size: int) -> RankItem:
        filters: List[Filter] = [
            text.LowerFilter(),
            text.StopWordRemover(),
            text.RegexRemover(),
            text.TFFilter(n_words=self.n_words)]
        q_words: List[str] = text.TextProcessor(
            text=query_doc.text,
            filters=filters)
        # search elasticsearch
        searcher: EsSearcher = EsSearcher(es_index=self.es_index)
        res: EsResult = searcher\
            .initialize_query()\
            .add_query(terms=q_words, field='text')\
            .add_size(size)\
            .add_filter(terms=query_doc.tags, field='tags')\
            .search()
        return res.to_rank_item(query_id=query_doc.docid)
