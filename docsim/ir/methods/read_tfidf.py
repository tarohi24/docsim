"""
TFIDF for word embeddings
#45
"""
from dataclasses import dataclass, field
from typing import Dict, List

from dataclasses_jsonschema import JsonSchemaMixin
import numpy as np
from scipy import stats

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
class RealTFIDFParam(Param, JsonSchemaMixin):
    n_words: int  # used for pre-filtering


@dataclass
class RealTFIDF(Searcher):
    param: NormParam
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

        tp: TextProcessor = TextProcessor(filters=filters)
        all_text: List[str] = [tp.apply(text) for text in pre_filtered_text.values()]
        kde = np.array([self.embed_words(words) for words in all_text])

        # Like negative sampling, it computes distribution of the collection
        # by samples randomly choosen

        scores: Dict[str, float] = dict()
        for docid, text in pre_filtered_text.items():
            words: List[str] = tp.apply(text)
            mat: np.ndarray = self.embed_words(words)
            scores[docid] = self.prob(kde=kde, mat=mat)

        return RankItem(query_id=query_doc.docid, scores=scores)
