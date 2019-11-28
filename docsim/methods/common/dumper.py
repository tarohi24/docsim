from pathlib import Path
from typing import List

from docsim.methods.common.types import Context, TRECResult
from docsim.models import ColDocument
from docsim.settings import results_dir


def get_dump_dir(context: Context) -> Path:
    path: Path = results_dir.joinpath(
        f"{context.es_index}/{context.method}/{context.runname}")
    try:
        path.mkdir(parents=True)
    except FileExistsError:
        pass
    return path


def dump_prel(res: TRECResult,
              context: Context) -> None:
    path: Path = get_dump_dir(context=context).joinpath('pred.prel')
    with open(path, 'a') as fout:
        fout.write(res.to_prel())
        fout.write('\n')


def dump_keywords(keywords: List[str],
                  doc: ColDocument,
                  context: Context) -> None:
    path: Path = get_dump_dir(context=context).joinpath('keywords.txt')
    with open(path, 'a') as fout:
        fout.write(','.join(keywords))
        fout.write('\n')
