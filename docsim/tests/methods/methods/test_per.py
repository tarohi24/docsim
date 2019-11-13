import pytest

from docsim.methods.common.types import Context
from docsim.methods.common.methods import MethodProperty
from docsim.methods.methods.per import Per, PerParam, Stragegy

from docsim.tests.embedding.fasttext import FastText


@pytest.fixture
def param() -> PerParam:
    param: PerParam = PerParam(n_words=2, strategy=Stragegy['PESSIMICTIC'])
    return param


@pytest.fixture
def mprop() -> MethodProperty:
    context: Context = {
        'n_docs': 3,
        'es_index': 'dummy',
        'method': 'keyword',
        'runname': '40',
    }
    mprop: MethodProperty = MethodProperty(context=context)
    return mprop


@pytest.fixture
def per(mocker, param, mprop) -> Per:
    mocker.patch('docsim.methods.methods.per.FastText', new=FastText)
    return Per(param=param, mprop=mprop)


def test_init(per):
    assert per.kb.param.n_words == 2
