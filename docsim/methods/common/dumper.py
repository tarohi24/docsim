from pathlib import Path
from typing import Dict, TypedDict  # type: ignore

from typedflow.batch import Batch
from typedflow.tasks import Dumper
from typedflow.nodes import DumpNode

from docsim.methods.common.dumper import Result as TRECResult
from docsim.settings import results_dir


class Result(TypedDict):
    """
    methods related to this item should be declared
    outside this class because method impl is not allowed by PEP589
    (at runtime, it's just a dict)
    """
    query_docid: str
    scores: Dict[str, float]


def to_prel(res: Result) -> str:
    return '\n'.join([f"{res['query_docid']} 0 {key} {score}"
                      for key, score in res['scores'].items()])


class DumpParam(TypedDict):
    dataset: str
    method: str
    runname: str


def get_dump_path(param: DumpParam) -> Path:
    path: Path = results_dir.joinpath(
        f"{param['dataset']}/{param['method']}/{param['runname']}.prel")
    try:
        path.parent.mkdir(parents=True)
    except FileExistsError:
        pass
    return path


def dump_prel(batch: Batch[Result],
              param: DumpParam) -> None:
    path: Path = get_dump_path(param=param)
    with open(path, 'a') as fout:
        for res in batch.data:
            fout.write(to_prel(res))


def dumper_node(batch: Batch[Result],
                param: DumpParam) -> DumpNode[TRECResult]:
    dumper: Dumper[Result] = Dumper(func=dump_prel)
    dump_node: DumpNode[TRECResult] = DumpNode(dumper=dumper)
    return dump_node
