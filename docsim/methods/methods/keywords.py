"""
extract keywords -> do search
"""
from __future__ import annotations
import asyncio
from collections import Counter
from dataclasses import dataclass
import re
from typing import List, Pattern, Set  # type: ignore

from nltk.corpus import stopwords as nltk_sw
from nltk.tokenize import RegexpTokenizer
from typedflow.flow import Flow
from typedflow.tasks import Task
from typedflow.nodes import TaskNode

from docsim.elas.search import EsResult, EsSearcher
from docsim.models import ColDocument
from docsim.methods.common.flow import Method, MethodProperty
from docsim.methods.common.types import Param, TRECResult
from docsim.methods.common.argparser import (
    get_default_parser, create_prop_from_args)


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

    def get_retrieve_node(self) -> TaskNode[ColDocument, TRECResult]:
        task: Task[ColDocument, TRECResult] = Task(self.retrieve)
        node: TaskNode[ColDocument, TRECResult] = TaskNode(task=task,
                                                           arg_type=ColDocument)
        return node

    def _extract_keywords_from_text(self, text: str) -> List[str]:
        # lower and tokenize
        tokens: List[str] = tokenizer.tokenize(text.lower())
        # remove stopwords
        tokens: List[str] = [w for w in tokens if w not in stopwords]  # type: ignore
        tokens: List[str] = [w for w in tokens  # type: ignore
                             if not_a_word_pat.match(w) is None]
        counter: Counter = Counter(tokens)
        keywords: List[str] = [w for w, _ in counter.most_common(self.param.n_words)]
        return keywords

    def extract_keywords(self, doc: ColDocument) -> List[str]:
        return self._extract_keywords_from_text(text=doc.text)

    def retrieve(self, doc: ColDocument) -> TRECResult:
        searcher: EsSearcher = EsSearcher(es_index=self.prop.context['es_index'])
        keywords: List[str] = self.extract_keywords(doc=doc)
        candidates: EsResult = searcher\
            .initialize_query()\
            .add_query(terms=keywords, field='text')\
            .add_size(self.prop.context['n_docs'])\
            .add_filter(terms=doc.tags, field='tags')\
            .add_source_fields(['text'])\
            .search()
        res: TRECResult = TRECResult(
            query_docid=doc.docid,
            scores=candidates.get_scores()
        )
        return res

    def create_flow(self) -> Flow:
        task_node: TaskNode[ColDocument, TRECResult] = self.get_retrieve_node()
        self.prop.dump_node.set_upstream_node('task', task_node)
        task_node.set_upstream_node('load', self.prop.load_node)
        flow: Flow = Flow(dump_nodes=[self.prop.dump_node, ])
        return flow


if __name__ == '__main__':
    parser = get_default_parser()
    parser.add_argument('--n-keywords',
                        nargs=1,
                        type=int)
    parser = get_default_parser()
    args = parser.parse_args()
    mprop: MethodProperty = create_prop_from_args(args, method_name='keyword')
    param: KeywordParam = KeywordParam.from_args(args)
    method: KeywordBaseline = KeywordBaseline(param=param, prop=mprop)
    flow: Flow = method.create_flow()
    asyncio.run(flow.run())
