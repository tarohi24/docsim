from typing import Dict, List, Set

import pytest
import numpy as np

from docsim.models import ColDocument
from docsim.methods.methods.fuzzy.param import FuzzyParam
from docsim.methods.methods.fuzzy.rerank import FuzzyRerank
from docsim.tests.methods.methods.base import context  # noqa

from docsim.tests.embedding.fasttext import FTMock


@pytest.fixture
def param() -> FuzzyParam:
    return FuzzyParam(
        n_words=3,
        model='fasttext',
        coef=1,
    )


@pytest.fixture
def model(param, context) -> FuzzyRerank:  # noqa
    return FuzzyRerank(param=param, context=context)


def get_tokens() -> List[str]:
    tokens: List[str] = 'hello world everyone'.split()
    return tokens
    

@pytest.fixture(autouse=True)
def mock_ft(mocker):
    mocker.patch('docsim.methods.methods.fuzzy.rerank.FastText', new=FTMock)


def test_embed_words(model):
    mat = model.embed_words(get_tokens())
    assert mat.ndim == 2
    norms = np.linalg.norm(mat, axis=1)
    # assert mat is normalized
    np.testing.assert_array_almost_equal(norms, np.ones(mat.shape[0]))


def test_get_kembs(model):
    mat = model.embed_words(get_tokens())
    embs = model.get_kembs(mat)
    assert set(model._get_nns(mat, embs)) == {0, 1, 2}


def test_fuzzy_bows(mocker, model):
    mat = model.embed_words(get_tokens())
    embs = model.get_kembs(mat)
    bow: np.ndarray = model.to_fuzzy_bows(mat, embs)
    ones: np.ndarray = np.ones(embs.shape[0])
    np.testing.assert_array_almost_equal(bow, ones / np.sum(ones))

    # 2 keywords
    mocker.patch.object(model.param, 'n_words', 2)
    embs = model.get_kembs(mat)
    assert embs.shape[0] == 2
    sorted_sims: np.ndarray = np.sort(model.to_fuzzy_bows(mat, embs))
    desired = np.sort([2 / 3, 1 / 3])
    np.testing.assert_array_almost_equal(sorted_sims, desired)


def test_match(mocker, model):
    mat = model.embed_words(get_tokens())
    embs = model.get_kembs(mat)
    assert embs.shape[0] == 3
    qbow: np.ndarray = model.to_fuzzy_bows(mat, embs)
    cols: List[ColDocument] = [
        ColDocument(docid='a', tags=[], text='hello world everyone', title=''),
        ColDocument(docid='b', tags=[], text='this is a pen', title=''),
    ]
    col_bows: Dict[str, np.ndarray] = model.get_collection_fuzzy_bows(cols, embs)

    qdoc = mocker.MagicMock()
    qdoc.docid = 'query'
    res = model.match(query_doc=qdoc,
                      query_bow=qbow,
                      col_bows=col_bows)
    assert res.scores['a'] > res.scores['b']


def test_get_cols(mocker, model):
    mocker.patch.object(model.context, 'es_index', 'clef')
    qdoc = mocker.MagicMock()
    qdoc.docid = 'EP1288722A2'
    ids: Set[str] = set(d.docid for d in model.get_cols(query=qdoc))
    assert set(ids) == {'EP0762208B1', 'EP0762208A2', 'EP1096314A1'}


def test_typecheck(model):
    flow = model.create_flow()
    flow.typecheck()
