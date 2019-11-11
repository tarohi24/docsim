"""
extract keywords -> do search
"""
from collections import Counter
from dataclasses import dataclass
import re
from typing import List, Pattern, Set, TypedDict  # type: ignore

from nltk.corpus import stopwords as nltk_sw
from nltk.tokenize import RegexpTokenizer
from typedflow.flow import Flow
from typedflow.tasks import Task
from typedflow.nodes import LoaderNode

from docsim.elas.search import EsResult, EsSearcher
from docsim.models import ColDocument
from docsim.methods.common.dumper import dumper_node
from docsim.methods.common.dumper import TRECResult
from docsim.methods.common.loader import loader_node


stopwords: Set[str] = set(nltk_sw.words('english'))
tokenizer: RegexpTokenizer = RegexpTokenizer(r'\w+|\$[\d\.]+|\S+')
not_a_word_pat: Pattern = re.compile(r'^[^a-z0-9]*$')


class BaseParam(TypedDict):
    n_docs: int
    es_index: str


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
