"""
Keyword search
"""
from dataclasses import dataclass
from typing import List

from docsim import text
from docsim.doc_models import Document
from docsim.elas.search import EsResult, EsSearcher
from docsim.ir.base import RankItem, Searcher
from docsim.text import Filter


@dataclass
class KeywordBaseline(Searcher):
    n_words: int
    es_index: str

    def retrieve(self,
                 query: Document,
                 size: int) -> RankItem:
        filters: List[Filter] = [
            text.LowerFilter(),
            text.StopWordRemover(),
            text.RegexRemover(),
            text.TFFilter(n_words=self.n_words)]
        q_words: List[str] = text.TextProcessor(text=query.body)
        # search elasticsearch
        searcher: EsSearcher = EsSearcher(es_index=self.es_index)
        searcher\
            .add_query(terms=q_words, field='text')\
            .add_size(size)\
            .add_filter(terms=query.
