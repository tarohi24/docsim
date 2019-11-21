"""
extract keywords -> do search
"""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
import re
from typing import ClassVar, List, Pattern, Set, Type  # type: ignore

from nltk.corpus import stopwords as nltk_sw
from nltk.tokenize import RegexpTokenizer
from typedflow.flow import Flow
from typedflow.nodes import TaskNode

from docsim.elas.search import EsResult, EsSearcher
from docsim.models import ColDocument
from docsim.methods.common.methods import Method
from docsim.methods.common.types import Param, TRECResult


stopwords: Set[str] = set(nltk_sw.words('english'))
tokenizer: RegexpTokenizer = RegexpTokenizer(r'\w+|\$[\d\.]+|\S+')
not_a_word_pat: Pattern = re.compile(r'^[^a-z0-9]*$')


@dataclass
class KeywordParam(Param):
    n_words: int

    @classmethod
    def from_args(cls, args) -> KeywordParam:
        return KeywordParam(n_words=args.n_keywords)


@dataclass
class KeywordBaseline(Method[KeywordParam]):
    param_type: ClassVar[Type] = KeywordParam

    def get_retrieve_node(self) -> TaskNode[ColDocument, TRECResult]:
        node: TaskNode[ColDocument, TRECResult] = TaskNode(func=self.retrieve)
        return node

    def _extract_keywords_from_text(self, text: str) -> List[str]:
        # lower and tokenize
        tokens: List[str] = tokenizer.tokenize(text.lower())
        # remove stopwords
        tokens: List[str] = [w for w in tokens if w not in stopwords]  # type: ignore
        tokens: List[str] = [w for w in tokens  # type: ignore
                             if not_a_word_pat.match(w) is None
                             and not w.isdigit()]
        counter: Counter = Counter(tokens)
        keywords: List[str] = [w for w, _ in counter.most_common(self.param.n_words)]
        return keywords

    def extract_keywords(self, doc: ColDocument) -> List[str]:
        return self._extract_keywords_from_text(text=doc.text)

    def search(self, doc: ColDocument) -> EsResult:
        searcher: EsSearcher = EsSearcher(es_index=self.context.es_index)
        keywords: List[str] = self.extract_keywords(doc=doc)
        candidates: EsResult = searcher\
            .initialize_query()\
            .add_query(terms=keywords, field='text')\
            .add_size(self.context.n_docs)\
            .add_filter(terms=doc.tags, field='tags')\
            .add_source_fields(['text'])\
            .search()
        return candidates

    def to_trec_result(self,
                       doc: ColDocument,
                       es_result: EsResult) -> TRECResult:
        res: TRECResult = TRECResult(
            query_docid=doc.docid,
            scores=es_result.get_scores()
        )
        return res

    def retrieve(self, doc: ColDocument) -> TRECResult:
        es_result: EsResult = self.search(doc=doc)
        trec_result: TRECResult = self.to_trec_result(doc=doc, es_result=es_result)
        return trec_result

    def create_flow(self) -> Flow:
        task_node: TaskNode[ColDocument, TRECResult] = self.get_retrieve_node()
        (self.load_node > task_node)('loader')
        (task_node > self.dump_node)('res')
        flow: Flow = Flow(dump_nodes=[self.dump_node, ])
        return flow
