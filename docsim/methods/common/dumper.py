from pathlib import Path

from typedflow.batch import Batch
from typedflow.tasks import Dumper
from typedflow.nodes import DumpNode

from docsim.methods.common.types import Context, TRECResult
from docsim.settings import results_dir


def get_dump_path(context: Context) -> Path:
    path: Path = results_dir.joinpath(
        f"{context['es_index']}/{context['method']}/{context['runname']}.prel")
    try:
        path.parent.mkdir(parents=True)
    except FileExistsError:
        pass
    return path


def dump_prel(batch: Batch[TRECResult],
              context: Context) -> None:
    path: Path = get_dump_path(context=context)
    with open(path, 'a') as fout:
        for res in batch.data:
            fout.write(res.to_prel())


def get_dump_node(context: Context) -> DumpNode[TRECResult]:
    dumper: Dumper[TRECResult] = Dumper(
        func=lambda batch: dump_prel(batch, context=context))
    dump_node: DumpNode[TRECResult] = DumpNode(dumper=dumper,
                                               arg_type=TRECResult)
    return dump_node
