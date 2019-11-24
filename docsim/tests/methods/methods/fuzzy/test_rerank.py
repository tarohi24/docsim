from typing import List

import pytest
import numpy as np

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


def test_fuzzy_bows(model):
    mat = model.embed_words(get_tokens())
    embs = model.get_kembs(mat)
    bow: np.ndarray = model.to_fuzzy_bows(mat, embs)
    ones: np.ndarray = np.ones(embs.shape[0])
    np.testing.assert_array_almost_equal(bow, ones / np.sum(ones))
