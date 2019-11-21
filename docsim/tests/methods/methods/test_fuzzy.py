import pytest
import numpy as np

from docsim.methods.methods.fuzzy import FuzzyParam, Fuzzy
from docsim.embedding.base import mat_normalize

from docsim.tests.embedding.fasttext import FTMock
from docsim.tests.methods.methods.base import context, text, doc  # noqa


@pytest.fixture(autouse=True)
def mock_ft(mocker):
    mocker.patch('docsim.methods.methods.fuzzy.FastText', new=FTMock)


@pytest.fixture
def param() -> FuzzyParam:
    return FuzzyParam(
        n_words=2,
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

    mat: np.ndarray = mat_normalize(
        np.array([
            np.full(300, 2),
            np.ones(300)
        ])
    )
    sims: np.ndarray = np.dot(mat, mat.T)
    np.testing.assert_almost_equal(func(sims, [1]), 0)


def test_cent_sim_error(fuzzy):
    func = fuzzy._cent_sim_error
    mat: np.ndarray = mat_normalize(
        np.array([
            np.ones(300),
            np.ones(300),
            np.ones(300),
        ])
    )
    sims: np.ndarray = np.dot(mat, mat.T)
    # 0 if len(ind) == 0
    np.testing.assert_almost_equal(func(sims, [1, ]), 0)
    np.testing.assert_almost_equal(func(sims, [1, 2]), 1)


def test_get_keywords(mocker, fuzzy):
    sims: np.ndarray = np.array([
        [1, 0.3, 0.8],
        [0.3, 1, 0.2],
        [0.8, 0.2, 1]
    ])
    sims_mock = mocker.MagicMock(return_value=sims)
    mocker.patch('docsim.methods.methods.fuzzy.Fuzzy.get_sim_matrix', sims_mock)
    tokens = ['software', 'license', 'program']
    assert fuzzy.get_keywords(tokens) == ['software', 'license']
