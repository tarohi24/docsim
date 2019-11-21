from typing import List

import pytest

from docsim.elas.search import EsResult, EsResultItem
from docsim.methods.common.types import TRECResult
from docsim.methods.methods.keywords import KeywordParam, KeywordBaseline



@pytest.fixture
def param() -> KeywordParam:
    param: KeywordParam = KeywordParam(n_words=2)
    return param


@pytest.fixture
def method(param, context):
    method: KeywordBaseline = KeywordBaseline(context=context, param=param)
    return method


@pytest.fixture
def sample_hits():
    res = EsResult([
        EsResultItem.from_dict(
            {'_source': {'docid': 'EP200'}, '_score': 3.2}),
    ])
    return res


def test_extract_query_from_text(method, text):
    keywords: List[str] = method._extract_keywords_from_text(text=text)
    assert keywords == ['test', 'danger', ]


def test_extract_keyword(method, doc):
    keywords: List[str] = method.extract_keywords(doc=doc)
    assert keywords == ['test', 'danger', ]


def test_search(mocker, method, doc, sample_hits):
    mocker.patch('docsim.settings.es', 'foo')
    mocker.patch('docsim.elas.search.EsSearcher.search',
                 return_value=sample_hits)
    trec_res: TRECResult = method.retrieve(doc=doc)
    assert trec_res.query_docid == 'EP111'
    assert trec_res.scores == {'EP200': 3.2}


def test_flow_creation(mocker, method, sample_hits):
    mocker.patch('docsim.settings.es', 'foo')
    mocker.patch('docsim.elas.search.EsSearcher.search',
                 return_value=sample_hits)
    method.create_flow().run()
