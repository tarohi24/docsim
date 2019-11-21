"""
Query loader
"""
from pathlib import Path
from typing import Generator

from tqdm import tqdm
from typedflow.nodes import LoaderNode

from docsim.methods.common.types import Context
from docsim.models import ColDocument
from docsim.settings import data_dir


__all__ = ['load_query_files', ]


def load_query_files(dataset: str) -> Generator[ColDocument, None, None]:
    qpath: Path = data_dir.joinpath(f'{dataset}/query/dump.bulk')
    pbar = tqdm()
    with open(qpath) as fin:
        while (line := fin.readline()):
            doc: ColDocument = ColDocument.from_json(line)  # type: ignore
            yield doc
            pbar.update(1)
