from typing import Dict

from docsim.methods.common.dumper import Result, get_dump_path
from docsim.settings import results_dir


def test_path_func():
    assert get_dump_path(dataset='clef', method='keyword', runname='40')\
        == results_dir.joinpath('clef/keyword/40.prel')
