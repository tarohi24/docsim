from typing import Dict

from docsim.methods.common.dumper import Result, get_dump_path, to_prel
from docsim.settings import results_dir


def test_path_func():
    assert get_dump_path(dataset='clef', method='keyword', runname='40')\
        == results_dir.joinpath('clef/keyword/40.prel')


def test_to_prel():
    scores: Dict[str, float] = {
        f'EP10{i}': float(i)
        for i in range(3)
    }
    res: Result = {
        'query_docid': 'EP111',
        'scores': scores
    }
    assert to_prel(res) == """EP111 0 EP100 0.0
EP111 0 EP101 1.0
EP111 0 EP102 2.0"""
