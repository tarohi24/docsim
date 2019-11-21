"""
Available only for fasttext
"""
from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import ClassVar, List, Pattern, Set, Type, TypedDict

from nltk.corpus import stopwords as nltk_sw
from nltk.tokenize import RegexpTokenizer
import numpy as np
from typedflow.flow import Flow
from typedflow.nodes import TaskNode

from docsim.elas.search import EsResult, EsSearcher
from docsim.embedding.base import mat_normalize, return_vector
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


@dataclass
class Fuzzy(Method[FuzzyParam]):
    param_type: ClassVar[Type] = FuzzyParam
    fasttext: FastText = field(init=False)

    def __post_init__(self):
        self.fasttext: FastText = FastText()

    def get_docid(self, doc: ColDocument) -> str:
        return doc.docid

    def get_cols(self, doc: ColDocument) -> List[ColDocument]:
        docid: str = doc.docid
        cols: List[ColDocument] = load_cols(
            docid=docid,
            dataset=self.mprop.context['es_index'])
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

    def calc_error(self,
                   mat: np.ndarray,
                   centroids: np.ndarray) -> float:
        if centroids.ndim == 1:
            centroids = centroids.reshape(-1, 300)
        ind: List[int] = np.argmax(np.dot(mat, centroids.T), axis=1)
        rec_error: float = np.mean(np.linalg.norm(mat - mat[ind, :], axis=1))
        cent_sim_error: float = np.dot(centroids, centroids.T).mean()
        return rec_error + self.param.coef * cent_sim_error

    @return_vector
    def get_keywords(self,
                     tokens: List[str]) -> List[str]:
        """
        Parameters
        -----
        matrix: 2D array (n_words, dim)

        Return
        -----
        1D vector (n_words)
        """
        matrix: np.ndarray = self.fasttext.embed_words(tokens)
        norm_mat: np.ndarray = mat_normalize(matrix)
        keyword_inds: np.ndarray = np.array([]).astype(int)
        keywords: Set[str] = set()
        for _ in range(self.param.n_words):
            print('HI')
            centroids: np.ndarray = norm_mat[keyword_inds]
            errors: List[float] = [
                self.calc_error(
                    norm_mat[~np.isin(
                        np.arange(norm_mat.shape[0]),
                        np.append(keyword_inds, i)
                    )],
                    np.append(centroids, norm_mat[i])
                )
                for i in range(norm_mat.shape[0])
                if tokens[i] not in keywords
            ]
            argmin = np.argmin(errors)
            keyword_inds = np.append(keyword_inds, argmin)
            keywords.add(tokens[argmin])
        print(keywords)
        return list(keywords)

    class ScoringArg(TypedDict):
        query_doc: ColDocument
        keywords: List[str]

    def match(self,
              args: ScoringArg) -> TRECResult:
        searcher: EsSearcher = EsSearcher(es_index=self.mprop.context['es_index'])
        candidates: EsResult = searcher\
            .initialize_query()\
            .add_query(terms=args['keywords'], field='text')\
            .add_size(self.mprop.context['n_docs'])\
            .add_filter(terms=args['query_doc'].tags, field='tags')\
            .add_source_fields(['text'])\
            .search()
        trec_result: TRECResult = self.to_trec_result(doc=args['query_doc'], es_result=candidates)
        return trec_result

    def create_flow(self):
        loader: LoaderNode[ColDocument] =a
        node_get_tokens: TaskNode[ColDocument, List[str]] = TaskNode(func=self.get_all_tokens)
        node_get_keywords: TaskNode[List[str], List[str]] = TaskNode(func=self.get_keywords)
        (node_get_tokens > node_get_keywords)('tokens')
        node_get_tokens.set_upstream_node('query_doc', self.mprop.load_node)
        node_get_keywords.set_upstream_node('tokens', node_get_tokens)

        node_match: TaskNode[self.ScoringArg, TRECResult] = self.get_node(
            func=self.match,
            arg_type=self.ScoringArg)

        node_match.set_upstream_node('query_doc', self.mprop.load_node)
        node_match.set_upstream_node('keywords', node_get_keywords)

        self.mprop.dump_node.set_upstream_node('task', node_match)
        flow: Flow = Flow(dump_nodes=[self.mprop.dump_node, ])
        return flow
