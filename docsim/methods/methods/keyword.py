"""
extract keywords -> do search
"""
from collections import Counter
from dataclasses import dataclass
import re
from typing import List, Pattern, Set  # type: ignore

from nltk.corpus import stopwords as nltk_sw
from nltk.tokenize import RegexpTokenizer
from typedflow.flow import Flow
from typedflow.tasks import Task
from typedflow.nodes import LoaderNode, TaskNode, DumpNode

from docsim.elas.search import EsResult, EsSearcher
from docsim.models import ColDocument
from docsim.methods.common.dumper import TRECResult, dump_node
from docsim.methods.common.loader import loader_node
from docsim.methods.common.types import BaseParam


stopwords: Set[str] = set(nltk_sw.words('english'))
tokenizer: RegexpTokenizer = RegexpTokenizer(r'\w+|\$[\d\.]+|\S+')
not_a_word_pat: Pattern = re.compile(r'^[^a-z0-9]*$')


class KeywordParam(BaseParam):
    n_words: int


def _extract_keywords_from_text(text: str,
                                param: KeywordParam) -> List[str]:
    # lower and tokenize
    tokens: List[str] = tokenizer.tokenize(text.lower())
    # remove stopwords
    tokens: List[str] = [w for w in tokens if w not in stopwords]  # type: ignore
    tokens: List[str] = [w for w in tokens  # type: ignore
                         if not_a_word_pat.match(w) is None]
    counter: Counter = Counter(tokens)
    keywords: List[str] = [w for w, _ in counter.most_common(param['n_words'])]
    return keywords


def extract_keywords(doc: ColDocument,
                     param: KeywordParam) -> List[str]:
    return _extract_keywords_from_text(text=doc.text, param=param)


def retrieve(doc: ColDocument,
             param: KeywordParam) -> TRECResult:
    searcher: EsSearcher = EsSearcher(es_index=param['es_index'])
    keywords: List[str] = extract_keywords(doc=doc, param=param)
    candidates: EsResult = searcher\
        .initialize_query()\
        .add_query(terms=keywords, field='text')\
        .add_size(param['n_docs'])\
        .add_filter(terms=doc.tags, field='tags')\
        .add_source_fields(['text'])\
        .search()
    res: TRECResult = TRECResult(
        query_docid=doc.docid,
        scores=candidates.get_scores()
    )
    return res


def retrieve_node(param: KeywordParam) -> TaskNode[ColDocument, TRECResult]:
    task: Task[ColDocument, TRECResult] = Task(
        func=lambda doc: retrieve(doc, param=param))
    node: TaskNode[ColDocument, TRECResult] = TaskNode(task=task,
                                                       arg_type=ColDocument)
    return node


@dataclass
class KeywordBaseline:
    param: KeywordParam

    def create_flow(self):
        loader: LoaderNode[ColDocument] = loader_node(
            dataset=self.param['es_index'])
        task: Task[ColDocument, TRECResult] = retrieve_node(
            param=self.param)
        dump: DumpNode[TRECResult] = dump_node(param=self.param)
        task.set_upstream_node('loader', loader)
        dump.set_upstream_node('task', task)
        flow: Flow = Flow(dump_nodes=[dump, ])
        return flow
