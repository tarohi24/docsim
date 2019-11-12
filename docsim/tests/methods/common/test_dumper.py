from pathlib import Path
from typing import Dict, List, Union

import pytest
from typedflow.batch import Batch
from typedflow.exceptions import FaultItem

from docsim.methods.common.dumper import get_dump_path, dump_prel
from docsim.methods.common.types import Context, TRECResult
from docsim.settings import results_dir


@pytest.fixture(scope='module')
def context() -> Context:
    context: Context = {
        'es_index': 'clef',
        'method': 'keyword',
        'runname': '40',
        'n_docs': 10
    }
    yield context


@pytest.fixture(scope='module')
def res() -> TRECResult:
    scores: Dict[str, float] = {
        f'EP10{i}': float(i)
        for i in range(3)
    }
    result: TRECResult = TRECResult(
        query_docid='EP111',
        scores=scores
    )
    return result


def test_path_func(context):
    assert get_dump_path(context)\
        == results_dir.joinpath('clef/keyword/40.prel')


def test_to_prel(res):
    assert res.to_prel() == """EP111 0 EP100 0.0
EP111 0 EP101 1.0
EP111 0 EP102 2.0"""


def test_dump(context, res):
    data: List[TRECResult] = [res, ]
    batch: Batch[TRECResult] = Batch(batch_id=0, data=data)

    dump_prel(batch=batch, context=context)
    path: Path = get_dump_path(context)
    with open(path) as fin:
        out: List[str] = fin.read().splitlines()
    assert out == ['EP111 0 EP100 0.0', 'EP111 0 EP101 1.0', 'EP111 0 EP102 2.0']
    path.unlink()


def test_dump_with_fault(context):
    data: List[Union[TRECResult, FaultItem]] = [FaultItem(), ]
    batch: Batch[TRECResult] = Batch(batch_id=0, data=data)

    dump_prel(batch=batch, context=context)
    path: Path = get_dump_path(context)
    with open(path) as fin:
        out: List[str] = fin.read().splitlines()
    assert out == []
    path.unlink()
