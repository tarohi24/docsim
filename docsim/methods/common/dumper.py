from pathlib import Path
from typing import Set

from typedflow.batch import Batch
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


def ask_yes_or_no() -> bool:
    yes: Set[str] = {'yes', 'y', 'ye'}
    no: Set[str] = {'no', 'n'}
    while True:
        ans: str = input().lower()
        if ans in yes:
            return True
        elif ans in no:
            return False


def dump_prel(batch: Batch[TRECResult],
              context: Context) -> None:
    path: Path = get_dump_path(context=context)
    if batch.batch_id == 0 and path.exists():
        if not is_test:
            sure_deletion: bool = ask_yes_or_no()
            if sure_deletion:
                path.unlink()
            else:
                exit(1)
    with open(path, 'a') as fout:
        for res in batch.data:
            fout.write(res.to_prel())


def get_dump_node(context: Context) -> DumpNode[TRECResult]:
    dumper: Dumper[TRECResult] = Dumper(
        func=lambda batch: dump_prel(batch, context=context))
    dump_node: DumpNode[TRECResult] = DumpNode(dumper=dumper,
                                               arg_type=TRECResult)
    return dump_node
