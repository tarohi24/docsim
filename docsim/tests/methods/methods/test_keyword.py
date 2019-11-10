from typing import List

from docsim.methods.methods.keyword import (
    KeywordParam, extract_keywords_from_text
)


def test_generate_query():
    param: KeywordParam = {
        'n_words': 2,
        'n_docs': 3,
    }
    doc = 'This is this IS a test. TEST. test; danger Danger da_ is.'
    keywords: List[str] = extract_keywords_from_text(text=doc, param=param)
    assert keywords == ['test', 'danger', ]
