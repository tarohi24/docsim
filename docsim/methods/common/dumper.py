from pathlib import Path
from typing import TypedDict

from docsim.settings import results_dir


def Result(TypedDict):
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


def get_dump_path(dataset: str,
                  method: str,
                  runname: str) -> Path:
    return results_dir.joinpath(f'{dataset}/{method}/{runname}.prel')
