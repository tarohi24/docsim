from dataclasses import dataclass
from pathlib import Path
from typing import Dict, TypedDict  # type: ignore

from typedflow.batch import Batch
from typedflow.tasks import Dumper
from typedflow.nodes import DumpNode

from docsim.settings import results_dir


@dataclass
class TRECResult:
    query_docid: str
    scores: Dict[str, float]

    def to_prel(self) -> str:
        return '\n'.join([f"{self.query_docid} 0 {key} {score}"
                          for key, score in self.scores.items()])


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


def dump_prel(batch: Batch[TRECResult],
              param: DumpParam) -> None:
    path: Path = get_dump_path(param=param)
    with open(path, 'a') as fout:
        for res in batch.data:
            fout.write(res.to_prel())


def dumper_node(batch: Batch[TRECResult],
                param: DumpParam) -> DumpNode[TRECResult]:
    dumper: Dumper[TRECResult] = Dumper(func=dump_prel)
    dump_node: DumpNode[TRECResult] = DumpNode(dumper=dumper)
    return dump_node
