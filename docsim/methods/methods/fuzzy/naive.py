"""
Available only for fasttext
"""
from __future__ import annotations
from dataclasses import dataclass, field
import logging
from typing import ClassVar, List, Type

import numpy as np
from typedflow.flow import Flow
from typedflow.nodes import TaskNode

from docsim.elas.search import EsResult, EsSearcher
from docsim.embedding.base import mat_normalize
from docsim.embedding.fasttext import FastText
from docsim.methods.common.methods import Method
from docsim.methods.common.types import TRECResult
from docsim.models import ColDocument

from docsim.methods.methods.fuzzy.param import FuzzyParam
from docsim.methods.methods.fuzzy.fuzzy import get_keyword_embs
from docsim.methods.methods.fuzzy.tokenize import get_all_tokens


logger = logging.getLogger(__file__)


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
        k_embs: np.ndarray = get_keyword_embs(
            tokens=tokens,
            embs=matrix,
            keyword_embs=None,
            n_remains=self.param.n_words,
            coef=self.param.coef)
        indices: List[int] = [i for i, is_valid
                              in enumerate(np.sum(matrix - k_embs, axis=1) == 0)
                              if is_valid]
        return list(set([tokens[i] for i in indices]))

    def to_trec_result(self,
                       doc: ColDocument,
                       es_result: EsResult) -> TRECResult:
        res: TRECResult = TRECResult(
            query_docid=doc.docid,
            scores=es_result.get_scores()
        )
        return res

    def match(self,
              query_doc: ColDocument,
              keywords: List[str]) -> TRECResult:
        searcher: EsSearcher = EsSearcher(es_index=self.context.es_index)
        candidates: EsResult = searcher\
            .initialize_query()\
            .add_query(terms=keywords, field='text')\
            .add_size(self.context.n_docs)\
            .add_filter(terms=query_doc.tags, field='tags')\
            .add_source_fields(['text'])\
            .search()
        trec_result: TRECResult = self.to_trec_result(doc=query_doc, es_result=candidates)
        return trec_result

    def create_flow(self):
        node_get_tokens: TaskNode[List[str]] = TaskNode(func=get_all_tokens)
        (node_get_tokens < self.load_node)('doc')

        node_get_keywords: TaskNode[List[str]] = TaskNode(func=self.extract_keywords)
        (node_get_tokens > node_get_keywords)('tokens')

        node_match: TaskNode[TRECResult] = TaskNode(func=self.match)
        (node_match < self.load_node)('query_doc')
        (node_match < node_get_keywords)('keywords')

        (self.dump_node < node_match)('res')

        flow: Flow = Flow(dump_nodes=[self.dump_node, ])
        return flow
