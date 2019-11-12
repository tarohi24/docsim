import pytest

from docsim.models import ColDocument


@pytest.fixture
def json_str() -> str:
    s: str = """
    {"docid": "EP111", "title": "hello", "text": "hi this is the body", "tags": ["C90B"]}
    """
    return s


def test_coldoc_init():
    ColDocument(
        docid='EP111',
        title='hello',
        text='hi this is the body',
        tags=['C90B', ]
    )


def test_coldoc_from_json(json_str):
    ColDocument.from_json(json_str)


def test_invalid_coldoc():
    s: str = """
    {"id": "EP111", "title": "hello", "text": "hi this is the body", "tags": ["C90B"]}
    """
    with pytest.raises(KeyError):
        ColDocument.from_json(s)


def test_docid_access(json_str):
    doc: ColDocument = ColDocument.from_json(json_str)
    assert doc.docid == 'EP111'
