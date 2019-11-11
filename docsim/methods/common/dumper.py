from dataclasses import dataclass
from pathlib import Path
from typing import Dict  # type: ignore

from typedflow.batch import Batch
from typedflow.tasks import Dumper
from typedflow.nodes import DumpNode

from docsim.methods.common.types import BaseParam
from docsim.settings import results_dir


@dataclass
class TRECResult:
    query_docid: str
    scores: Dict[str, float]

    def to_prel(self) -> str:
        return '\n'.join([f"{self.query_docid} 0 {key} {score}"
                          for key, score in self.scores.items()])


def get_dump_path(param: BaseParam) -> Path:
    path: Path = results_dir.joinpath(
        f"{param['es_index']}/{param['method']}/{param['runname']}.prel")
    try:
        path.parent.mkdir(parents=True)
    except FileExistsError:
        pass
    return path


def dump_prel(batch: Batch[TRECResult],
              param: BaseParam) -> None:
    path: Path = get_dump_path(param=param)
    with open(path, 'a') as fout:
        for res in batch.data:
            fout.write(res.to_prel())


def dump_node(param: BaseParam) -> DumpNode[TRECResult]:
    dumper: Dumper[TRECResult] = Dumper(
        func=lambda batch: dump_prel(batch, param=param))
    dump_node: DumpNode[TRECResult] = DumpNode(dumper=dumper,
                                               arg_type=TRECResult)
    return dump_node
