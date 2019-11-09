"""
Query loader
"""
from pathlib import Path
from typing import Generator

from docsim.models import ColDocument
from docsim.settings import data_dir


def query_load_file(dataset: str) -> Generator[ColDocument, None, None]:
    qpath: Path = data_dir.joinpath(f'{dataset}/query/dump.bulk')
    with open(qpath) as fin:
        doc: ColDocument = ColDocument.from_json(fin.readline())
        yield doc
