from pathlib import Path
from typing import List

import pytest

from docsim.methods.run import get_method, parse
from docsim.methods.common.methods import M
from docsim.methods.methods.keywords import KeywordBaseline
from docsim.settings import param_dir


@pytest.fixture
def sample_yaml() -> Path:
    path: Path = param_dir.joinpath('sample.yaml')
    return path


def test_get_method():
    assert get_method('keywords') == KeywordBaseline
    with pytest.raises(KeyError):
        get_method('dummy')


def test_parse(sample_yaml):
    lst: List[M] = parse(sample_yaml)
    assert len(lst) == 2
    assert lst[0].mprop.context['n_docs'] == 100
    assert lst[0].mprop.context['es_index'] == 'clef'
    assert lst[0].mprop.context['method'] == 'keywords'
    assert lst[0].mprop.context['runname'] == '40'
    assert lst[1].mprop.context['runname'] == '30'

    assert lst[0].param.n_words == 40
    assert lst[1].param.n_words == 30
