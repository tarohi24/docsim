"""
Principal Angle Analysis
"""
from dataclasses import dataclass, field
from typing import Dict, List

from dataclasses_jsonschema import JsonSchemaMixin
import numpy as np
import scipy

from docsim.elas.search import EsResult, EsSearcher
from docsim.embedding.base import return_matrix
from docsim.embedding.fasttext import FastText
from docsim.ir.methods.base import Searcher, Param
from docsim.ir.models import QueryDocument
from docsim.ir.trec import RankItem
from docsim.text import (
    Filter,
    LowerFilter,
    StopWordRemover,
    RegexRemover,
    TFFilter,
    TextProcessor
)


@dataclass
class PAAParam(Param, JsonSchemaMixin):
    n_words: int


@dataclass
class PAA(Searcher):
    param: PAAParam
    fasttext: FastText = field(default_factory=FastText.create)

    @classmethod
    def method_name(cls) -> str:
        return 'paa'

    @return_matrix
    def embed_words(self,
                    words: List[str]) -> np.ndarray:
        return np.array([self.fasttext.embed(w) for w in words])

    def paa(self,
            A: np.ndarray,
            B: np.ndarray) -> float:
        """
        Projection matrix
        """
        angles: np.ndarray = np.radians(scipy.linalg.subspace_angles(A.T, B.T))
        return np.sqrt(300 - np.sum(np.cos(angles) ** 2))

    def retrieve(self,
                 query_doc: QueryDocument,
                 size: int = 100) -> RankItem:
        filters: List[Filter] = [
            LowerFilter(),
            StopWordRemover(),
            RegexRemover(),
            TFFilter(n_words=self.param.n_words)]
        q_words: List[str] = TextProcessor(filters=filters).apply(query_doc.text)
        q_matrix: np.ndarray = self.embed_words(q_words)

        # pre_filtering
        searcher: EsSearcher = EsSearcher(es_index=self.query_dataset.name)
        candidates: EsResult = searcher\
            .initialize_query()\
            .add_query(terms=q_words, field='text')\
            .add_size(size)\
            .add_filter(terms=query_doc.tags, field='tags')\
            .add_source_fields(['text'])\
            .search()

        pre_filtered_text: Dict[str, str] = {
            hit.docid: hit.source['text']
            for hit in candidates.hits}

        scores: Dict[str, float] = dict()
        for docid, text in pre_filtered_text.items():
            words: List[str] = TextProcessor(filters=filters).apply(text)
            mat: np.ndarray = self.embed_words(words)
            score: float = self.paa(mat, q_matrix)
            print(score)
            scores[docid] = score

        return RankItem(query_id=query_doc.docid, scores=scores)
