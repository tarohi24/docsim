import pytest
import numpy as np

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


def test_flow(fuzzy):
    fuzzy.create_flow().typecheck()


def test_get_all_tokens(fuzzy, doc):
    assert fuzzy.get_all_tokens(doc) == 'test test test danger danger da_'.split()


def test_rec_error(fuzzy):
    func = fuzzy._rec_error
    mat: np.ndarray = np.zeros((10, 300))
    centroids: np.ndarray = np.zeros((1, 300))
    assert func(mat, centroids) == 0

    # illegal type
    centroids: np.ndarray = np.zeros(300)
    with pytest.raises(np.AxisError):
        func(mat, centroids)

    mat: np.ndarray = np.array([
        np.zeros(300),
        np.ones(300)
    ])
    centroids = np.zeros((1, 300))
    np.testing.assert_almost_equal(func(mat, centroids), np.sqrt(300) / 2)


def test_cent_sim_error(fuzzy):
    func = fuzzy._cent_sim_error
    centroids = np.zeros((1, 300))
    with pytest.warns(RuntimeWarning):
        assert np.isnan(func(centroids))
    centroids = np.ones((1, 300))
    np.testing.assert_almost_equal(func(centroids), 1)
