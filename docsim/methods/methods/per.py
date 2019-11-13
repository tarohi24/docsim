from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import (
    Callable, ClassVar, Dict, List, Type, TypedDict, TypeVar)

import numpy as np
from typedflow.flow import Flow
from typedflow.tasks import Task
from typedflow.nodes import TaskNode

from docsim.elas.search import EsResult, EsSearcher
from docsim.embedding.base import return_matrix
from docsim.embedding.fasttext import FastText
from docsim.methods.common.methods import Method
from docsim.methods.common.types import Param, P, TRECResult
from docsim.methods.methods.keywords import KeywordBaseline, KeywordParam
from docsim.models import ColDocument


T = TypeVar('T')
K = TypeVar('K')


class Stragegy(Enum):
    PESSIMICTIC = 1
    OPTIMISTIC = 2


@dataclass
class PerParam(Param):
    n_words: int
    strategy: Stragegy

    @classmethod
    def from_args(cls, args) -> PerParam:
        return PerParam(n_words=args.n_words,
                        strategy=Stragegy[args.strategy])


@dataclass
class Per(Method[PerParam]):
    param_type: ClassVar[Type[P]] = PerParam
    kb: KeywordBaseline = field(init=False)
    fasttext: FastText = field(init=False)

    def __post_init__(self):
        self.kb: KeywordBaseline = KeywordBaseline(
            mprop=self.mprop,
            param=KeywordParam(n_words=self.param.n_words))
        self.fasttext: FastText = FastText()

    def pre_flitering(self,
                      doc: ColDocument) -> List[str]:
        cands: List[str] = [item.docid for item
                            in self.kb.search(doc=doc).hits]
        return cands

    @return_matrix
    def _embed_keywords(self,
                        keywords: List[str]) -> np.ndarray:
        ary: np.ndarray = np.array([self.fasttext.embed(word)
                                    for word in keywords])
        return ary

    def embed_cands(self,
                    docids: List[str]) -> Dict[str, np.ndarray]:
        searcher: EsSearcher = EsSearcher(es_index=self.mprop.context['es_index'])
        res: EsResult = searcher\
            .initialize_query()\
            .add_query(terms=docids, field='docid')\
            .add_size(len(docids))\
            .add_source_fields(['text', ])\
            .search()
        id_texts: Dict[str, str] = {  # type: ignore
            item.docid: item.source['text']
            for item in res.hits
        }
        embeddings: Dict[str, np.ndarray] = {
            docid: self._embed_keywords(
                self.kb._extract_keywords_from_text(text=text))
            for docid, text in id_texts.items()
        }
        return embeddings

    def embed_query(self,
                    doc: ColDocument) -> np.ndarray:
        keywords: List[str] = self.kb.extract_keywords(doc=doc)
        embeddings: np.ndarray = self._embed_keywords(keywords)
        return embeddings

    class QandC(TypedDict):
        query_doc: ColDocument
        query_emb: np.ndarray
        col_emb: Dict[str, np.ndarray]

    def _projection_norm(self,
                         vec: np.ndarray,
                         bases: np.ndarray) -> float:
        """
        compute the norm of a vector which is a projection of vec
        into bases space
        Note: assert that each vectors are unit vectors (norm == 1.0)

        Parameters
        -----
        vec: 1D
        bases: 2D (n_base, dim)
        """
        # compute norm for each vecs
        comps: np.ndarray = np.dot(bases, vec)
        assert comps.shape == (len(bases), )
        norm: float = np.linglg.norm(comps)
        return norm

    def score(self,
              qandc: QandC) -> TRECResult:
        norms: Dict[str, float] = {
            docid: self._projection_norm(qandc['query_emb'], mat)
            for docid, mat in qandc['col_emb'].items()
        }
        res: TRECResult = TRECResult(
            query_docid=qandc['query_doc'].docid,
            scores=norms)
        return res

    @staticmethod
    def get_node(func: Callable[[T], K],
                 arg_type: Type[T]) -> TaskNode[T, K]:
        task: Task[T, K] = Task(func=func)
        node: TaskNode[T, K] = TaskNode(task=task, arg_type=arg_type)
        return node

    def create_flow(self):
        node_filter: TaskNode[ColDocument, List[str]] = self.get_node(
            func=self.pre_flitering,
            arg_type=ColDocument)
        node_get_text: TaskNode[List[str], Dict[str, np.ndarray]] = self.get_node(
            func=self.embed_cands,
            arg_type=List[str])
        node_query: TaskNode[ColDocument, List[str]] = self.get_node(
            func=self.embed_query,
            arg_type=ColDocument)
        node_score: TaskNode[self.QandC, TRECResult] = self.get_node(
            func=self.score,
            arg_type=self.QandC)

        # define the topology
        node_filter.set_upstream_node('load', self.mprop.load_node)
        node_get_text.set_upstream_node('filter', node_filter)
        node_query.set_upstream_node('load', self.mprop.load_node)

        node_score.set_upstream_node('col_emb', node_get_text)
        node_score.set_upstream_node('query_doc', self.mprop.load_node)
        node_score.set_upstream_node('query_emb', node_query)

        self.mprop.dump_node.set_upstream_node('score', node_score)

        flow: Flow = Flow(dump_nodes=[self.mprop.dump_node, ])
        return flow
