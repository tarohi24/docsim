"""
Query loader
"""
from pathlib import Path
from typing import Generator

from typedflow.tasks import DataLoader
from typedflow.nodes import LoaderNode

from docsim.models import ColDocument
from docsim.settings import data_dir


__all__ = ['loader_node', ]


def query_load_file(dataset: str) -> Generator[ColDocument, None, None]:
    qpath: Path = data_dir.joinpath(f'{dataset}/query/dump.bulk')
    with open(qpath) as fin:
        doc: ColDocument = ColDocument.from_json(fin.readline())  # type: ignore
        yield doc


def loader_node(dataset: str) -> LoaderNode[ColDocument]:
    queries: Generator[ColDocument, None, None] = query_load_file(dataset=dataset)
    loader: DataLoader[ColDocument] = DataLoader(gen=queries,
                                                 batch_size=1)
    node: LoaderNode[ColDocument] = LoaderNode(loader)
    return node
