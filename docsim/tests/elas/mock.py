from unittest.mock import MagicMock

import pytest

from docsim.elas.searcher import EsSearcher


@pytest.fixture
def es_result() -> EsResult:
    hits: List[EsResultItem] = 


def searcher_mock() -> EsSearcher:
    es_index: str = 'dummy'
    mock = MagicMock(spec_set=EsSearcher(es_index=es_index, es=None))
    mock.search.return_value  =: 
