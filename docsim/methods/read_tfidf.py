"""
TFIDF for word embeddings
#45
"""
from dataclasses import dataclass, field
from typing import List

from dataclasses_jsonschema import JsonSchemaMixin
import numpy as np
from scipy import stats

from docsim.embedding.base import return_matrix
from docsim.embedding.fasttext import FastText
from docsim.methods.base import Searcher, Param
from docsim.models import QueryDocument, RankItem


@dataclass
class RealTFIDFParam(Param, JsonSchemaMixin):
    n_words: int  # used for pre-filtering


@dataclass
class RealTFIDF(Searcher):
    param: RealTFIDFParam
    fasttext: FastText = field(default_factory=FastText.create)

    @classmethod
    def method_name(cls) -> str:
        return 'real_tfidf'

    @return_matrix
    def embed_words(self,
                    words: List[str]) -> np.ndarray:
        return np.array([self.fasttext.embed(w) for w in words])

    def prob(self,
             kde: stats.gaussian_kde,
             mat: np.ndarray) -> float:
        """
        Estimate probability of mat = summation of "IDF" of vectors in mat
        """
        return kde.pdf(mat).sum()

    def retrieve(self,
                 query_doc: QueryDocument,
                 size: int = 100) -> RankItem:
        pass
