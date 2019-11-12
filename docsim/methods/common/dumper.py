from pathlib import Path
from typing import Union

from typedflow.batch import Batch
from typedflow.exceptions import FaultItem
from typedflow.tasks import Dumper
from typedflow.nodes import DumpNode

from docsim.methods.common.types import Context, TRECResult
from docsim.settings import results_dir, is_test


def get_dump_path(context: Context) -> Path:
    path: Path = results_dir.joinpath(
        f"{context['es_index']}/{context['method']}/{context['runname']}.prel")
    try:
        path.parent.mkdir(parents=True)
    except FileExistsError:
        pass
    return path


def dump_prel(batch: Batch[Union[TRECResult, FaultItem]],
              context: Context) -> None:
    path: Path = get_dump_path(context=context)
    if batch.batch_id == 0 and path.exists():
        if not is_test:
            path.unlink()
    with open(path, 'a') as fout:
        for res in batch.data:
            if not isinstance(res, FaultItem):
                fout.write(res.to_prel())
        fout.write('\n')


def get_dump_node(context: Context) -> DumpNode[TRECResult]:
    dumper: Dumper[TRECResult] = Dumper(
        func=lambda batch: dump_prel(batch, context=context))
    dump_node: DumpNode[TRECResult] = DumpNode(dumper=dumper,
                                               arg_type=TRECResult)
    return dump_node
