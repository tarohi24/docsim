from pathlib import Path
from typing import TypedDict

from docsim.settings import results_dir


def Result(TypedDict):
    query_docid: str
    scores: Dict[str, float]


def get_dump_path(dataset: str,
                  method: str,
                  runname: str) -> Path:
    return results_dir.joinpath(f'{dataset}/{method}/{runname}.prel')
