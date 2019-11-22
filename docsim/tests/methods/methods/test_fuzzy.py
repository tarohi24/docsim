from pathlib import Path
from typing import Dict, List

import pytest
import numpy as np

from docsim.methods.methods.fuzzy import FuzzyParam, Fuzzy
from docsim.embedding.base import mat_normalize
from docsim.settings import data_dir

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
def fuzzy(mocker, param, context) -> Fuzzy:  # noqa
    return Fuzzy(param=param, context=context)


@pytest.fixture
def sample_embeddings() -> Dict[str, np.ndarray]:
    embdir: Path = data_dir.joinpath('embs')
    with open(embdir.joinpath('fasttext_vocab.txt')) as fin:
        vocabs: List[str] = fin.read().splitlines()
    mat: np.ndarray = np.load(str(embdir.joinpath('fasttext_embs.npy').resolve()))
    return {word: ary for word, ary in zip(vocabs, mat)}


def test_init(fuzzy):
    assert fuzzy.param.coef == 1


def test_flow(fuzzy):
    fuzzy.create_flow().typecheck()


def test_get_all_tokens(fuzzy, doc):  # noqa
    assert fuzzy.get_all_tokens(doc) == 'test test test danger danger da_'.split()


def test_get_keywords(mocker, fuzzy, sample_embeddings):
    tokens = ['software', 'license', 'program', 'terms', 'code']
    mocker.patch('docsim.tests.embedding.fasttext.FTMock.embed_words',
                 return_value=np.array([sample_embeddings[w] for w in tokens]))
    assert set(fuzzy.get_keywords(tokens)) == {'software', 'license'}
