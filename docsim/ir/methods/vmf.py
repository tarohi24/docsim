"""
von Mises Fisher distribution
"""
from dataclasses import dataclass, field
from typing import Dict, List

from dataclasses_jsonschema import JsonSchemaMixin
import numpy as np
import scipy
from spherecluster import VonMisesFisherMixture

from docsim.elas.search import EsResult, EsSearcher
from docsim.embedding.base import return_matrix, mat_normalize
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
class VMFParam(Param, JsonSchemaMixin):
    n_words: int
    es_index: str


@dataclass
class VMF(Searcher):
    param: VMFParam
    fasttext: FastText = field(default_factory=FastText.create)

    @classmethod
    def method_name(cls) -> str:
        return 'paa'

    @return_matrix
    def embed_words(self,
                    words: List[str]) -> np.ndarray:
        return np.array([self.fasttext.embed(w) for w in words])

    def vmf(self,
            vec: np.ndarray,
            mu: np.ndarray,
            kappa: float) -> float:
        """
        DEPRECATE: overflow frequently happens
        """
        n: int = 300
        i: float = scipy.special.jv(n // 2 - 1, kappa)
        c1: float = np.power(2 * np.pi, -n // 2)
        k: float = np.power(kappa, n // 2 - 1)
        c: float = c1 * k / i
        score: float = c * np.exp(kappa * np.dot(mu.T, vec))
        return score

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
        searcher: EsSearcher = EsSearcher(es_index=self.param.es_index)
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
            mat: np.ndarray = mat_normalize(self.embed_words(words))

            model: VonMisesFisherMixture = VonMisesFisherMixture(
                n_clusters=1,
                posterior_type='soft')
            model.fit(mat_normalize(mat))
            mu: np.ndarray = model.cluster_centers_[0]
            kappa: float = model.concentrations_[0]

            probs: float = np.sum([self.vmf(vec=vec, mu=mu, kappa=kappa) for vec in q_matrix])
            scores[docid] = probs

        return RankItem(query_id=query_doc.docid, scores=scores)
