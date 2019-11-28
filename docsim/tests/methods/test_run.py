from pathlib import Path
from typing import List, TypeVar

import pytest

from docsim.methods.run import get_method, parse
from docsim.methods.methods.keywords import KeywordBaseline
from docsim.settings import param_dir


P = TypeVar('P')


@pytest.fixture
def sample_yaml() -> Path:
    path: Path = param_dir.joinpath('sample.yaml')
    return path


def test_get_method():
    assert get_method('keywords') == KeywordBaseline
    with pytest.raises(KeyError):
        get_method('dummy')


def test_parse(sample_yaml):
    lst: List[P] = parse(sample_yaml)
    assert len(lst) == 1
    assert lst[0].context.n_docs == 100
    assert lst[0].context.es_index== 'clef'
    assert lst[0].context.method == 'keywords'
    assert lst[0].context.runname == '40'
    assert lst[0].param.n_words == 40
