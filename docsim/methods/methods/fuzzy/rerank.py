from collections import Counter
from dataclasses import dataclass, field
from typing import ClassVar, Dict, List, Type

import numpy as np

from docsim.embedding.base import mat_normalize
from docsim.embedding.fasttext import FastText
from docsim.methods.common.methods import Method
from docsim.methods.common.pre_filtering import load_cols
from docsim.methods.common.types import TRECResult
from docsim.models import ColDocument

from docsim.methods.methods.fuzzy.param import FuzzyParam
from docsim.methods.methods.fuzzy.fuzzy import get_keywords
from docsim.methods.methods.fuzzy.tokenize import get_all_tokens


@dataclass
class FuzzyReranker(Method[FuzzyParam]):
    param_type: ClassVar[Type] = FuzzyParam
    fasttext: FastText = field(init=False)

    def __post_init__(self):
        super(FuzzyReranker, self).__post_init__()
        self.fasttext: FastText = FastText()

    def get_cols(self,
                 query: ColDocument) -> List[ColDocument]:
        """
        Get documents cached by keywrod search
        """
        docid: str = query.docid
        cols: List[ColDocument] = load_cols(
            docid=docid,
            dataset=self.context.es_index)
        return cols

    def embed_words(self,
                    tokens: List[str]) -> np.ndarray:
        matrix: np.ndarray = mat_normalize(
            self.fasttext.embed_words(tokens))  # (n_tokens, n_dim)
        return matrix

    def extract_keywords(self,
                         mat: np.ndarray,
                         tokens: List[str]) -> List[str]:
        """
        Given embeddint matrix mat (n_tokens * n_dim) and tokens (list (n_tokens)),
        calculate keyword tokens
        """
        return get_keywords(
            tokens=tokens,
            embs=mat,
            keyword_embs=np.array([]),
            n_remains=self.param.n_words,
            coef=self.param.coef)

    def _get_nns(self,
                 mat: np.ndarray,
                 keyword_embs: np.ndarray) -> List[int]:
        """
        Given embedding matrix mat, Get nearest keywords in keyword_embs

        Return
        -----
        list (len = mat.shape[0]) of nearest embedding's indexes
        """
        nns: List[int] = np.amax(
            np.dot(mat, keyword_embs.T), axis=1).tolist()
        return nns

    def to_fuzzy_bows(self,
                      mat: np.ndarray,
                      keyword_embs: np.ndarray) -> np.ndarray:
        """
        Generate a FuzzyBoW vector according to keyword_embs

        Return
        -----
        1D array whose item[i] is the normalized frequency of ith keyword
        """
        nns = self._get_nns(mat=mat, keyword_embs=keyword_embs)
        counter: Counter = Counter(nns)
        counts: List[int] = [counter[i] if i in counter else 0
                             for i in range(keyword_embs.shape[0])]
        return np.array(counts) / np.sum(counts)

    def get_collection_fuzzy_bows(self,
                                  cols: List[ColDocument],
                                  keyword_embs: np.ndarray) -> Dict[str, np.ndarray]:
        bow_dict: Dict[str, np.ndarray] = dict()
        for doc in cols:
            tokens: List[str] = get_all_tokens(doc)
            embs: np.ndarray = mat_normalize(self.embed_words(tokens))
            bow: np.ndarray = self.to_fuzzy_bows(mat=embs,
                                                 keyword_embs=keyword_embs)
            bow_dict[doc.docid] = bow
        return bow_dict

    def match(self,
              query_doc: ColDocument,
              query_bow: np.ndarray,
              col_bows: Dict[str, np.ndarray]) -> TRECResult:
        """
        Yet this only computes cosine similarity as the similarity.
        There's room for adding other ways.
        """
        scores: Dict[str, float] = {docid: np.dot(query_bow, bow)
                                    for docid, bow in col_bows.items()}
        return TRECResult(query_docid=query_doc.docid,
                          scores=scores)
