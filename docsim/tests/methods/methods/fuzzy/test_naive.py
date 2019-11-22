import pytest

from docsim.methods.methods.fuzzy.param import FuzzyParam
from docsim.methods.methods.fuzzy.naive import FuzzyNaive
from docsim.tests.methods.methods.base import context  # noqa

from docsim.tests.embedding.fasttext import FTMock


@pytest.fixture
def param() -> FuzzyParam:
    return FuzzyParam(
        n_words=2,
        model='fasttext',
        coef=1,
        strategy='NAIVE'
    )


@pytest.fixture
def fuzzy(mocker, param, context) -> FuzzyNaive:  # noqa
    return FuzzyNaive(param=param, context=context)


@pytest.fixture(autouse=True)
def mock_ft(mocker):
    mocker.patch('docsim.methods.methods.fuzzy.naive.FastText', new=FTMock)


def test_flow(fuzzy):
    fuzzy.create_flow().typecheck()
