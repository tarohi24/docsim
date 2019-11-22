"""
Available only for fasttext
"""
from __future__ import annotations
from dataclasses import dataclass, field
from itertools import product
import logging
import re
import warnings
from typing import ClassVar, List, Pattern, Set, Type, TypedDict

import numpy as np
from tqdm import tqdm
from typedflow.flow import Flow
from typedflow.nodes import TaskNode

from docsim.elas.search import EsResult, EsSearcher
from docsim.embedding.base import mat_normalize
from docsim.embedding.fasttext import FastText
from docsim.methods.common.methods import Method
from docsim.methods.common.types import TRECResult
from docsim.models import ColDocument
from docsim.methods.common.pre_filtering import load_cols

from docsim.methods.methods.fuzzy.param import FuzzyParam
from docsim.methods.methods.fuzzy.fuzzy import get_keywords
from docsim.methods.methods.fuzzy.tokenize import get_all_tokens


logger = logging.getLogger(__file__)


class ScoringArg(TypedDict):
    query_doc: ColDocument
    keywords: List[str]


@dataclass
class FuzzyNaive(Method[FuzzyParam]):
    param_type: ClassVar[Type] = FuzzyParam
    fasttext: FastText = field(init=False)

    def __post_init__(self):
        super(FuzzyNaive, self).__post_init__()
        self.fasttext: FastText = FastText()

    def extract_keywords(self,
                         tokens: List[str]) -> List[str]:
        matrix: np.ndarray = mat_normalize(
            self.fasttext.embed_words(tokens))  # (n_tokens, n_dim)
        return get_keywords(
            tokens=tokens,
            embs=matrix,
            keyword_embs=np.array([]),
            n_remains=self.param.n_words,
            coef=self.param.coef)

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
        node_get_tokens: TaskNode[ColDocument, List[str]] = TaskNode(func=get_all_tokens)
        (node_get_tokens < self.load_node)('doc')

        node_get_keywords: TaskNode[List[str], List[str]] = TaskNode(func=self.extract_keywords)
        (node_get_tokens > node_get_keywords)('tokens')

        node_match: TaskNode[ScoringArg, TRECResult] = TaskNode(func=self.match)
        (node_match < self.load_node)('query_doc')
        (node_match < node_get_keywords)('keywords')

        (self.dump_node < node_match)('task')

        flow: Flow = Flow(dump_nodes=[self.dump_node, ])
        return flow
