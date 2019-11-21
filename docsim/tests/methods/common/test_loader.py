from typing import Generator

from typedflow.nodes import LoaderNode

from docsim.models import ColDocument
from docsim.methods.common.loader import load_query_files


def node():
    def get_queries() -> Generator[ColDocument, None, None]:
        return load_query_files(dataset='clef')
    node: LoaderNode[ColDocument] = LoaderNode(func=get_queries)
    return node


def test_node_creation():
    node()
