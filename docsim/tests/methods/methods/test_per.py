import pytest

from docsim.elas.search import EsResult, EsResultItem
from docsim.methods.common.types import Context
from docsim.methods.methods.per import Per, PerParam, Stragegy
from docsim.models import ColDocument

from docsim.tests.embedding.fasttext import FTMock


@pytest.fixture
def param() -> PerParam:
    param: PerParam = PerParam(n_words=2,
                               strategy=Stragegy['PESSIMICTIC'])
    return param


@pytest.fixture
def context() -> Context:
    return {
        'n_docs': 3,
        'es_index': 'dummy',
        'method': 'keyword',
        'runname': '40',
    }


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


@pytest.fixture
def per(mocker, param, mprop) -> Per:
    mocker.patch('docsim.methods.methods.per.FastText', new=FTMock)
    return Per(param=param, mprop=mprop)


@pytest.fixture
def sample_hits():
    res = EsResult([
        EsResultItem.from_dict(
            {'_source': {'docid': 'EP200', 'text': 'hello world'}, '_score': 3.2}),
    ])
    return res
