from unittest.mock import MagicMock
from typing import List

import pytest

from docsim.methods.methods.keyword import (
    KeywordParam, extract_keywords, _extract_keywords_from_text
)
from docsim.models import ColDocument


@pytest.fixture
def param() -> KeywordParam:
    param: KeywordParam = {
        'n_words': 2,
        'n_docs': 3,
    }
    return param


@pytest.fixture
def text() -> str:
    doc: str = 'This is this IS a test. TEST. test; danger Danger da_ is.'
    return doc


@pytest.fixture
def doc(text) -> ColDocument:
    doc: ColDocument = ColDocument(
        docid='EP111',
        title='sample',
        text=text,
        tags=['G10P'])
    return doc


def test_extract_query_from_text(param, text):
    keywords: List[str] = _extract_keywords_from_text(text=text, param=param)
    assert keywords == ['test', 'danger', ]


def test_extract_keyword(param, doc):
    keywords: List[str] = extract_keywords(doc=doc, param=param)
    assert keywords == ['test', 'danger', ]
