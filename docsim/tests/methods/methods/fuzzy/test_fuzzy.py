from pathlib import Path
from typing import Dict, List

import pytest
import numpy as np

from docsim.settings import data_dir

from docsim.tests.embedding.fasttext import FTMock
from docsim.embedding.base import mat_normalize
from docsim.methods.methods.fuzzy.fuzzy import get_keyword_embs


@pytest.fixture(autouse=True)
def mock_ft(mocker):
    mocker.patch('docsim.methods.methods.fuzzy.naive.FastText', new=FTMock)


@pytest.fixture
def sample_embeddings() -> Dict[str, np.ndarray]:
    embdir: Path = data_dir.joinpath('embs')
    with open(embdir.joinpath('fasttext_vocab.txt')) as fin:
        vocabs: List[str] = fin.read().splitlines()
    mat: np.ndarray = np.load(str(embdir.joinpath('fasttext_embs.npy').resolve()))
    return {word: ary for word, ary in zip(vocabs, mat)}


def test_get_keywords(sample_embeddings):
    tokens = ['software', 'license', 'program', 'terms', 'code']
    embs = mat_normalize(np.array([sample_embeddings[w] for w in tokens]))
    keyword_embs: np.ndarray = get_keyword_embs(
        tokens=tokens,
        embs=embs,
        keyword_embs=None,
        n_remains=2,
        coef=1)
    gt_embs: np.ndarray = embs[[0, 1]]
    assert np.linalg.matrix_rank(keyword_embs - gt_embs) == 1
