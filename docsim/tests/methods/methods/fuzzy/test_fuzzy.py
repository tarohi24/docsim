from pathlib import Path
from typing import Dict, List

import pytest
import numpy as np

from docsim.settings import data_dir

from docsim.tests.embedding.fasttext import FTMock
from docsim.tests.methods.methods.base import context, text, doc  # noqa
from docsim.methods.methods.fuzzy.fuzzy import get_keywords


@pytest.fixture(autouse=True)
def mock_ft(mocker):
    mocker.patch('docsim.methods.methods.fuzzy.naive.FuzzyNaive.FastText', new=FTMock)


@pytest.fixture
def sample_embeddings() -> Dict[str, np.ndarray]:
    embdir: Path = data_dir.joinpath('embs')
    with open(embdir.joinpath('fasttext_vocab.txt')) as fin:
        vocabs: List[str] = fin.read().splitlines()
    mat: np.ndarray = np.load(str(embdir.joinpath('fasttext_embs.npy').resolve()))
    return {word: ary for word, ary in zip(vocabs, mat)}


def test_get_keywords(mocker, sample_embeddings):
    tokens = ['software', 'license', 'program', 'terms', 'code']
    mocker.patch('docsim.tests.embedding.fasttext.FTMock.embed_words',
                 return_value=np.array([sample_embeddings[w] for w in tokens]))
    assert set(get_keywords(tokens)) == {'software', 'license'}
