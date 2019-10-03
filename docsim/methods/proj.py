"""
Personalization by projection matrix
"""
from dataclasses import dataclass, field
from typing import Dict, List

from dataclasses_jsonschema import JsonSchemaMixin
import numpy as np

from docsim.elas.search import EsResult, EsSearcher
from docsim.embedding.base import return_matrix
from docsim.embedding.fasttext import FastText
from docsim.methods.base import Searcher, Param
from docsim.models import QueryDocument, RankItem
from docsim.text import (
    Filter,
    LowerFilter,
    StopWordRemover,
    RegexRemover,
    TFFilter,
    TextProcessor
)


@dataclass
class ProjParam(Param, JsonSchemaMixin):
    n_words: int


@dataclass
class Proj(Searcher):
    param: ProjParam
    fasttext: FastText = field(default_factory=FastText.create)

    @classmethod
    def method_name(cls) -> str:
        return 'proj'

    @return_matrix
    def embed_words(self,
                    words: List[str]) -> np.ndarray:
        return np.array([self.fasttext.embed(w) for w in words])

    @return_matrix
    def project(self,
                A: np.ndarray,
                B: np.ndarray) -> np.ndarray:
        """
        return projected A personalized by B
        A @ P = A
        """
        assert A.shape[0] == B.shape[0]
        # generate the projection matrix
        P: np.ndarray = B.T @ np.linalg.inv(B @ B.T) @ B
        personalized_A: np.ndarray = A @ P
        return personalized_A

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
            .add_size(size * 5)\
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
            pers_mat: np.ndarray = self.project(mat, q_matrix)
            diff_m: np.ndarray = pers_mat - q_matrix
            score = -np.linalg.norm(diff_m, axis=1).sum()
            # score = -np.linalg.norm(diff_m.T @ diff_m)
            print(score)
            # score = np.dot(pers_mat.sum(axis=1), bow)
            scores[docid] = score

        return RankItem(query_id=query_doc.docid, scores=scores)
