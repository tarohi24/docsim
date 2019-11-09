from typing import Generator

import pytest
from typedflow.tasks import DataLoader
from typedflow.nodes import LoaderNode

from docsim.models import ColDocument
from docsim.methods.common.loader import query_load_file



def test_query_load_file():
    queries: Generator[ColDocument, None, None] = query_load_file(dataset='clef')
    qdoc: ColDocument = next(queries)
    assert qdoc.docid == 'EP1780094A1'


def dataloader() -> DataLoader[ColDocument]:
    queries: Generator[ColDocument, None, None] = query_load_file(dataset='clef')
    loader: DataLoader[ColDocument] = DataLoader(gen=queries, batch_size=1)
    return loader


def test_dataloader_creation():
    dataloader()


def node():
    loader: DataLoader[ColDocument] = dataloader()
    node: LoaderNode[ColDocument] = LoaderNode(loader)


def test_node_creation():
    node()
