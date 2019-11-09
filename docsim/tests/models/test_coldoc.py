import pytest

from docsim.models import ColDocument


def test_coldoc_init():
    ColDocument._create_doc_from_values(
        docid='EP111',
        title='hello',
        text='hi this is the body',
        tags=['C90B', ]
    )


def test_coldoc_from_json():
    json_str: str = """
    {"docid": "EP111", "title": "hello", "text": "hi this is the body", "tags": ["C90B"]}
    """
    ColDocument.from_json(json_str)
