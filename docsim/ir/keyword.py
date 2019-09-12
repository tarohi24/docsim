"""
Keyword search
"""
from dataclasses import dataclass
from typing import List

from docsim import text
from docsim.doc_models import Document
from docsim.rank import RankItem
from docsim.ir.base import Searcher


@dataclass
class KeywordBaseline(Searcher):
    n_words: int
    es_index: str
    
    def retrieve(self, query: Document) -> RankItem:
        filters: List[Filter] = [
            text.LowerFilter(),
            text.StopWordRemover(),
            text.RegexRemover(),
            text.TFFilter(n_words=self.n_words)]
        q_words: List[str] = text.TextProcessor(text=query.body)
        # search elasticsearch
