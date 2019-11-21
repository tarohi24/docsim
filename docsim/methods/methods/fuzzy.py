"""
Available only for fasttext
"""
from __future__ import annotations
from dataclasses import dataclass, field
from itertools import product
import re
import warnings
from typing import ClassVar, List, Pattern, Set, Type, TypedDict

from nltk.corpus import stopwords as nltk_sw
from nltk.tokenize import RegexpTokenizer
import numpy as np
from typedflow.flow import Flow
from typedflow.nodes import TaskNode

from docsim.elas.search import EsResult, EsSearcher
from docsim.embedding.base import mat_normalize
from docsim.embedding.fasttext import FastText
from docsim.methods.common.methods import Method
from docsim.methods.common.types import Param, TRECResult
from docsim.models import ColDocument
from docsim.methods.common.pre_filtering import load_cols


stopwords: Set[str] = set(nltk_sw.words('english'))
tokenizer: RegexpTokenizer = RegexpTokenizer(r'\w+|\$[\d\.]+|\S+')
not_a_word_pat: Pattern = re.compile(r'^[^a-z0-9]*$')


@dataclass
class FuzzyParam(Param):
    n_words: str
    model: str
    coef: float

    @classmethod
    def from_args(cls, args) -> FuzzyParam:
        param: FuzzyParam = FuzzyParam(n_words=args.n_words,
                                       model=args.model,
                                       coef=args.coef)
        return param


class ScoringArg(TypedDict):
    query_doc: ColDocument
    keywords: List[str]


class Fuzzy(Method[FuzzyParam]):
    param_type: ClassVar[Type] = FuzzyParam
    fasttext: FastText = field(init=False)

    def __post_init__(self):
        super(Fuzzy, self).__post_init__()
        self.fasttext: FastText = FastText()

    def get_docid(self, doc: ColDocument) -> str:
        return doc.docid

    def get_cols(self, doc: ColDocument) -> List[ColDocument]:
        docid: str = doc.docid
        cols: List[ColDocument] = load_cols(
            docid=docid,
            dataset=self.context.es_index)
        return cols

    def get_all_tokens(self,
                       doc: ColDocument) -> List[str]:
        tokens: List[str] = tokenizer.tokenize(doc.text.lower())
        # remove stopwords
        tokens: List[str] = [w for w in tokens if w not in stopwords]  # type: ignore
        tokens: List[str] = [w for w in tokens  # type: ignore
                             if not_a_word_pat.match(w) is None
                             and not w.isdigit()]
        return tokens

    @staticmethod
    def _rec_error(sims: np.ndarray,
                   ind: List[int]) -> float:
        """
        Reconstruct error. In order to enable unittests, two errors are
        implemented individually.
        """
        assert len(ind) > 0
        indices: np.ndarray = np.isin(np.arange(sims.shape[0]), ind)
        reduced_sims: np.ndarray = sims[:, indices]  # (n_tokens, n_cents)
        maxes: np.ndarray = np.amax(reduced_sims, axis=1)
        if all(maxes == 1):
            warnings.warn('Probably all elements in sims are zero?')
        return (1 - maxes).mean()

    @staticmethod
    def _cent_sim_error(sims: np.ndarray,
                        ind: List[int]) -> float:
        """
        Similarity among bases

        Parameters
        -----
        sims
            2D (n_tokens, n_tokens)
        ind
            dimension indices of sims
        """
        if len(ind) < 2:
            return 0
        cent_sim_error: float = np.mean([sims[(i, j)]
                                         for i, j in product(ind, ind)])
        return cent_sim_error

    def calc_error(self,
                   sims: np.ndarray,
                   ind: List[int]) -> float:
        rec_error: float = self._rec_error(sims, ind)
        cent_sim_error: float = self._cent_sim_error(sims, ind)
        return rec_error + self.param.coef * cent_sim_error

    def get_sim_matrix(self,
                       tokens: List[str]) -> np.ndarray:
        """
        isolate from get_keywords due to easy testing
        """
        matrix: np.ndarray = mat_normalize(
            self.fasttext.embed_words(tokens))  # (n_tokens, n_dim)
        sim_matrix: np.ndarray = np.dot(matrix, matrix.T)  # (n_tokens, n_tokens)
        return sim_matrix

    def get_keywords(self,
                     tokens: List[str]) -> List[str]:
        sim_matrix: np.ndarray = self.get_sim_matrix(tokens=tokens)
        keyword_inds: List[int] = []
        keywords: Set[str] = set()

        for _ in range(self.param.n_words):
            errors: List[float] = [self.calc_error(sims=sim_matrix,
                                                   ind=keyword_inds + [i])
                                   for i in range(sim_matrix.shape[0])
                                   if i not in keyword_inds
                                   and tokens[i] not in keywords]
            argmin = np.argmin(errors)
            keyword_inds = np.append(keyword_inds, argmin)
            keywords.add(tokens[argmin])
        print(keywords)
        return list(keywords)

    def match(self,
              args: ScoringArg) -> TRECResult:
        searcher: EsSearcher = EsSearcher(es_index=self.context.es_index)
        candidates: EsResult = searcher\
            .initialize_query()\
            .add_query(terms=args['keywords'], field='text')\
            .add_size(self.context.n_docs)\
            .add_filter(terms=args['query_doc'].tags, field='tags')\
            .add_source_fields(['text'])\
            .search()
        trec_result: TRECResult = self.to_trec_result(doc=args['query_doc'], es_result=candidates)
        return trec_result

    def create_flow(self):
        node_get_tokens: TaskNode[ColDocument, List[str]] = TaskNode(func=self.get_all_tokens)
        (node_get_tokens < self.load_node)('doc')

        node_get_keywords: TaskNode[List[str], List[str]] = TaskNode(func=self.get_keywords)
        (node_get_tokens > node_get_keywords)('tokens')

        node_match: TaskNode[ScoringArg, TRECResult] = TaskNode(func=self.match)
        (node_match < self.load_node)('query_doc')
        (node_match < node_get_keywords)('keywords')

        (self.dump_node < node_match)('task')

        flow: Flow = Flow(dump_nodes=[self.dump_node, ])
        return flow
