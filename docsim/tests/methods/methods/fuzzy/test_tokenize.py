from docsim.methods.methods.fuzzy.tokenize import get_all_tokens
from docsim.tests.methods.methods.base import doc  # noqa


def test_get_all_tokens(doc):  # noqa
    assert get_all_tokens(doc) == 'test test test danger danger da_'.split()
