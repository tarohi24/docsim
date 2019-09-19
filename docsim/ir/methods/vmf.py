"""
von Mises Fisher distribution
"""
from dataclasses import dataclass, field
from typing import Dict, List

from dataclasses_jsonschema import JsonSchemaMixin
import numpy as np
from spherecluster import VonMisesFisherMixture
from spherecluster.von_mises_fisher_mixture import _vmf_log

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
        # c: float = np.pow(2 * pi, -n / 2} *  kappa^{n/2-1}
        score = np.exp(kappa * np.dot(mu.T, x))
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

        # fit distribution
        model: VonMisesFisherMixture = VonMisesFisherMixture(
            n_clusters=1,
            posterior_type='soft')
        model.fit(mat_normalize(q_matrix))
        mu: np.ndarray = model.cluster_centers_[0]
        kappa: float = model.concentrations_[0]

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
            probs: float = np.sum(vmf.prob(mat_normalize(mat)))
            scores[docid] = probs

        return RankItem(query_id=query_doc.docid, scores=scores)
