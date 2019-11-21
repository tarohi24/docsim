import pytest

from docsim.methods.methods.fuzzy import FuzzyParam, Fuzzy

from docsim.tests.embedding.fasttext import FTMock
from docsim.tests.methods.methods.base import context, text, doc  # noqa


@pytest.fixture(autouse=True)
def mock_ft(mocker):
    mocker.patch('docsim.methods.methods.fuzzy.FastText', new=FTMock)


@pytest.fixture
def param() -> FuzzyParam:
    return FuzzyParam(
        n_words=3,
        model='fasttext',
        coef=1
    )


@pytest.fixture
def fuzzy(mocker, param, context) -> Fuzzy:
    return Fuzzy(param=param, context=context)


def test_init(fuzzy):
    assert fuzzy.param.coef == 1
