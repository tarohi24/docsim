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
from tqdm import tqdm
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
    def _rec_error(embs: np.ndarray,
                   keyword_embs: np.ndarray,
                   cand_emb: np.ndarray) -> float:
        """
        Reconstruct error. In order to enable unittests, two errors are
        implemented individually.
        """
        if keyword_embs.ndim == 2:
            dims: np.ndarray = np.append(keyword_embs, cand_emb)
        else:
            dims: np.ndarray = np.array([cand_emb])  # type: ignore
        maxes: np.ndarray = np.amax(np.dot(embs, dims.T), axis=1)
        return (1 - maxes).mean()

    @staticmethod
    def _cent_sim_error(keyword_embs: np.ndarray,
                        cand_emb: np.ndarray) -> float:
        if keyword_embs.ndim == 1:
            return 0
        return np.dot(keyword_embs, cand_emb)

    def calc_error(self,
                   embs: np.ndarray,
                   keyword_embs: np.ndarray,
                   cand_emb: np.ndarray) -> float:
        rec_error: float = self._rec_error(embs, keyword_embs, cand_emb)
        cent_sim_error: float = self._cent_sim_error(keyword_embs, cand_emb)

        return rec_error + self.param.coef * cent_sim_error

    def _get_keywords(self,
                      tokens: List[str],
                      embs: np.ndarray,
                      keyword_embs: np.ndarray,
                      n_remains: int) -> List[str]:
        if n_remains == 0:
            return []
        errors: List[float] = [self.calc_error(embs=embs,
                                               keyword_embs=keyword_embs,
                                               cand_emb=embs[i])
                               for i in range(len(tokens))]
        argmin: int = np.argmin(errors)
        keyword: str = tokens[argmin]
        new_keyword_emb = embs[argmin]
        residual_inds = [(t != keyword) for t in tokens]
        print(keyword)
        return [keyword] + self._get_keywords(
            tokens=[t for t, is_valid in zip(tokens, residual_inds) if is_valid],
            embs=embs[residual_inds, :],
            keyword_embs=np.append(keyword_embs, new_keyword_emb),
            n_remains=(n_remains - 1)
        )

    def get_keywords(self,
                     tokens: List[str]) -> List[str]:
        matrix: np.ndarray = mat_normalize(
            self.fasttext.embed_words(tokens))  # (n_tokens, n_dim)
        return self._get_keywords(
            tokens=tokens,
            embs=matrix,
            keyword_embs=np.array([]),
            n_remains=self.param.n_words)

    def to_trec_result(self,
                       doc: ColDocument,
                       es_result: EsResult) -> TRECResult:
        res: TRECResult = TRECResult(
            query_docid=doc.docid,
            scores=es_result.get_scores()
        )
        return res

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
