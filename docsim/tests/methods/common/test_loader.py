from typing import Generator

import pytest

from docsim.models import ColDocument
from docsim.methods.common.loader import query_load_file


def test_query_load_file():
    queries: Generator[ColDocument, None, None] = query_load_file(dataset='clef')
    for qdoc in queries:
        pass
