
import pytest


from docsim.methods.methods.fuzzy import FuzzyParam, Fuzzy
from docsim.methods.common.types import Context
from docsim.methods.common.methods import MethodProperty
from docsim.models import ColDocument

from docsim.tests.embedding.fasttext import FastText as FTMock


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
def text() -> str:
    text: str = 'This is this IS a test. TEST. test; danger Danger da_ is.'
    return text


@pytest.fixture
def doc(text) -> ColDocument:
    doc: ColDocument = ColDocument(
        docid='EP111',
        title='sample',
        text=text,
        tags=['G10P'])
    return doc


@pytest.fixture
def fuzzy(mocker, param, mprop) -> Fuzzy:
    return Fuzzy(param=param, mprop=mprop)


def test_init(fuzzy):
    assert fuzzy.param.coef == 1
