"""
Available only for fasttext
"""
from __future__ import annotations
from dataclasses import dataclass, field
import logging
from typing import ClassVar, List, Type, Generator

import numpy as np
from typedflow.flow import Flow
from typedflow.nodes import TaskNode, DumpNode, LoaderNode

from docsim.elas.search import EsResult, EsSearcher
from docsim.embedding.base import mat_normalize
from docsim.embedding.fasttext import FastText
from docsim.methods.common.methods import Method
from docsim.methods.common.types import TRECResult, Context
from docsim.models import ColDocument
from docsim.methods.common.dumper import dump_keywords

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
            embs=matrix,
            keyword_embs=None,
            n_remains=self.param.n_words,
            coef=self.param.coef)
        logger.info(k_embs.sum(axis=1))
        indices: List[int] = [np.argmin(np.linalg.norm(matrix - vec, axis=1))
                              for vec in k_embs]
        logger.info(indices)
        keywords: List[str] = list(set([tokens[i] for i in indices]))
        logger.info(keywords)
        return keywords

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

        def provide_context() -> Generator[Context, None, None]:
            while True:
                yield self.context

        node_get_tokens: TaskNode[List[str]] = TaskNode(func=get_all_tokens)
        (node_get_tokens < self.load_node)('doc')

        node_get_keywords: TaskNode[List[str]] = TaskNode(func=self.extract_keywords)
        (node_get_tokens > node_get_keywords)('tokens')
        keywords_dumper: DumpNode = DumpNode(dump_keywords)
        (keywords_dumper < node_get_keywords)('keywords')
        (keywords_dumper < self.load_node)('doc')
        (keywords_dumper < LoaderNode(provide_context,
                                      batch_size=1))('context')
        node_match: TaskNode[TRECResult] = TaskNode(func=self.match)
        (node_match < self.load_node)('query_doc')
        (node_match < node_get_keywords)('keywords')

        (self.dump_node < node_match)('res')

        flow: Flow = Flow(dump_nodes=[self.dump_node, keywords_dumper])
        return flow
