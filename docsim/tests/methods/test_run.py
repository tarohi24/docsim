from pathlib import Path

import pytest

from docsim.methods.run import get_method
from docsim.methods.methods.keywords import KeywordBaseline
from docsim.settings import param_dir


@pytest.fixture
def sample_yaml_file() -> Path:
    path: Path = param_dir.joinpath('sample.yaml')
    return path


def test_get_method():
    assert get_method('keywords') == KeywordBaseline
    with pytest.raises(KeyError):
        get_method('dummy')
