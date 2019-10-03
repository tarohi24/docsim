"""
Principal Angle Analysis
"""
from dataclasses import dataclass, field
from typing import Dict, List

from dataclasses_jsonschema import JsonSchemaMixin
import numpy as np
import scipy

from docsim.elas.search import EsResult
from docsim.embedding.base import return_matrix
from docsim.embedding.fasttext import FastText
from docsim.methods.base import Searcher, Param
from docsim.models import RankItem, QueryDocument
from docsim.text import Filter, TextProcessor


@dataclass
class PAAParam(Param, JsonSchemaMixin):
    n_words: int


@dataclass
class PAA(Searcher):
    param: PAAParam
    fasttext: FastText = field(default_factory=FastText.create)

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
        filters: List[Filter] = self.get_default_filtes(
            n_words=self.param.n_words)
        processor: TextProcessor = TextProcessor(filters=filters)
        candidates: EsResult = self.filter_by_terms(
            text=query_doc.text,
            n_words=self.param.n_words,
            size=size)

        pre_filtered_text: Dict[str, str] = {
            hit.docid: hit.source['text']
            for hit in candidates.hits}

        q_matrix: np.ndarray = self.embed_words(processor.apply(query_doc.text))

        scores: Dict[str, float] = dict()
        for docid, text in pre_filtered_text.items():
            words: List[str] = processor.apply(text)
            mat: np.ndarray = self.embed_words(words)
            score: float = self.paa(mat, q_matrix)
            scores[docid] = score

        return RankItem(query_id=query_doc.docid, scores=scores)
