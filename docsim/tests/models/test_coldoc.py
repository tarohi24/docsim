import pytest

from docsim.models import ColDocument


def test_coldoc_init():
    ColDocument(
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


def test_invalid_coldoc():
    # docid -> id
    json_str: str = """
    {"id": "EP111", "title": "hello", "text": "hi this is the body", "tags": ["C90B"]}
    """
    with pytest.raises(KeyError):
        ColDocument.from_json(json_str)


def test_docid_access():
    json_str: str = """
    {"docid": "EP111", "title": "hello", "text": "hi this is the body", "tags": ["C90B"]}
    """
    doc: ColDocument = ColDocument.from_json(json_str)
    assert doc.docid == 'EP111'
