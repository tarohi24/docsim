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
