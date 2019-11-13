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


def get_res() -> TRECResult:
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


def test_to_prel():
    res = get_res()
    assert res.to_prel() == """EP111 Q0 EP102 1 2.0 STANDARD
EP111 Q0 EP101 2 1.0 STANDARD
EP111 Q0 EP100 3 0.0 STANDARD"""


def test_dump(context):
    res = get_res()
    data: List[TRECResult] = [res, ]
    batch: Batch[TRECResult] = Batch(batch_id=0, data=data)

    path: Path = get_dump_path(context)
    try:
        path.unlink()
    except FileNotFoundError:
        pass
    dump_prel(batch=batch, context=context)
    with open(path) as fin:
        out: List[str] = fin.read().splitlines()
    assert out == ['EP111 Q0 EP102 1 2.0 STANDARD',
                   'EP111 Q0 EP101 2 1.0 STANDARD',
                   'EP111 Q0 EP100 3 0.0 STANDARD']
    path.unlink()


def test_dump_with_fault(context):
    data: List[Union[TRECResult, FaultItem]] = [FaultItem(), ]
    batch: Batch[TRECResult] = Batch(batch_id=0, data=data)

    path: Path = get_dump_path(context)
    try:
        path.unlink()
    except FileNotFoundError:
        pass
    dump_prel(batch=batch, context=context)
    with open(path) as fin:
        out: List[str] = fin.read().splitlines()
    assert out == ['', ]
    path.unlink()
