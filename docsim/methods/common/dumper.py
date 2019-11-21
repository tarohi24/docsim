from pathlib import Path

from docsim.methods.common.types import Context, TRECResult
from docsim.settings import results_dir


def get_dump_path(context: Context) -> Path:
    path: Path = results_dir.joinpath(
        f"{context.es_index}/{context.method}/{context.runname}.prel")
    try:
        path.parent.mkdir(parents=True)
    except FileExistsError:
        pass
    return path


def dump_prel(res: TRECResult,
              context: Context) -> None:
    path: Path = get_dump_path(context=context)
    with open(path, 'a') as fout:
        fout.write(res.to_prel())
        fout.write('\n')
