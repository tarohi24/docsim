from pathlib import Path
from typing import Set

import pytest
import xml.etree.ElementTree as ET

from docsim.initialize.converters.ntcir import NTCIRConverter
from docsim.initialize.ntcir.query import loading, replace_tab
from docsim.settings import data_dir


converter: NTCIRConverter = NTCIRConverter()


def test_load_queries():
    lst: Set[Path] = set([path.name for path in loading()])
    assert lst == {'1001', '1002', '1003'}


@pytest.fixture
def root() -> ET.Element:
    path: Path = data_dir.joinpath(f'ntcir/orig/query/1001')
    return replace_tab(path)


def test_get_docid(root):
    assert converter._get_docid(root) == '200106296192'
