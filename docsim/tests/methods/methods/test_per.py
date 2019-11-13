import pytest

from docsim.elas.search import EsResult, EsResultItem
from docsim.methods.common.types import Context
from docsim.methods.common.methods import MethodProperty
from docsim.methods.methods.per import Per, PerParam, Stragegy
from docsim.models import ColDocument

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
    mocker.patch('docsim.methods.methods.per.FastText', new=FastText)
    return Per(param=param, mprop=mprop)


@pytest.fixture
def sample_hits():
    res = EsResult([
        EsResultItem.from_dict(
            {'_source': {'docid': 'EP200', 'text': 'hello world'}, '_score': 3.2}),
    ])
    return res


def test_init(per):
    assert per.kb.param.n_words == 2


def test_pre_filtering(mocker, sample_hits, per, doc):
    mocker.patch('docsim.elas.search.EsSearcher.search',
                 return_value=sample_hits)
    assert per.pre_flitering(doc=doc) == ['EP200', ]


def test_embed_cands(mocker, sample_hits, per, doc):
    mocker.patch('docsim.elas.search.EsSearcher.search',
                 return_value=sample_hits)
    assert per.embed_cands(docids=['EP200'])['EP200'].shape == (2, 300)
