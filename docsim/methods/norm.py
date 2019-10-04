"""
Text Similarity Estimation Based on Word Embeddings and
MatrixNorms for Targeted Marketing. NAACL. 2019
"""
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from dataclasses_jsonschema import JsonSchemaMixin
import numpy as np

from docsim.elas.search import EsResult, EsSearcher
from docsim.embedding.base import return_matrix
from docsim.embedding.fasttext import FastText
from docsim.methods.base import Method, Param
from docsim.models import RankItem, QueryDocument
from docsim.text import Filter, TextProcessor


@dataclass
class NormParam(Param, JsonSchemaMixin):
    n_words: int  # used for pre-filtering
    norm: str


@dataclass
class Norm(Method):
    param: NormParam
    fasttext: FastText = field(default_factory=FastText.create)

    @classmethod
    def method_name(cls) -> str:
        return 'norm'

    @return_matrix
    def embed_words(self,
                    words: List[str]) -> np.ndarray:
        return np.array([self.fasttext.embed(w) for w in words])

    def norm(self,
             A: np.ndarray,
             B: np.ndarray) -> float:
        assert A.shape[1] == B.shape[1]
        aa: float = np.linalg.norm(np.dot(A, A.T), ord=self.param.norm)
        bb: float = np.linalg.norm(np.dot(B, B.T), ord=self.param.norm)
        ab: float = np.linalg.norm(np.dot(A, B.T), ord=self.param.norm)
        return ab / np.sqrt(aa * bb)

    def retrieve(self,
                 query_doc: QueryDocument,
                 size: int = 100) -> RankItem:
        filters: List[Filter] = self.get_default_filtes(
            n_words=self.param.n_words)
        processor: TextProcessor = TextProcessor(filters=filters)
        q_words: List[str] = processor.apply(query_doc.text)
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

        tokens_dict: Dict[Tuple[str, str], List[str]] = {
            hit.get_id_and_tag(): processor.apply(hit.source['text'])
            for hit in candidates.hits
        }

        scores: Dict[Tuple[str, str], float] = dict()
        for key, words in tokens_dict.items():
            mat: np.ndarray = self.embed_words(words)
            scores[key] = -self.norm(mat, q_matrix)

        return RankItem(query_id=query_doc.docid, scores=scores)
