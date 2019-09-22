from pathlib import Path
from typing import Iterable, List

from docsim.ir.models import ColDocument, ColParagraph, QueryDocument


class NoneException(Exception):
    pass


class CannotSplitText(Exception):
    pass


def get_or_raise_exception(obj: Optional[T]) -> T:
    if obj is None:
        raise NoneException
    else:
        return obj


def find_text_or_default(root: ET.Element,
                         xpath: str,
                         default: str) -> str:
    try:
        content: ET.Element = get_or_raise_exception(root.find(xpath))
    except NoneException:
        return default
    try:
        text: str = get_or_raise_exception(content.text)
    except NoneException:
        return default
    return text


class Converter:
    """
    convert something into IRBase
    """
    def to_document(self, fpath: Path) -> Iterable[ColDocument]:
        raise NotImplementedError('This is an abstract class.')

    def to_paragraph(self, fpath: Path) -> Iterable[ColParagraph]:
        raise NotImplementedError('This is an abstract class.')

    def to_query_dump(self, fpath: Path) -> List[QueryDocument]:
        raise NotImplementedError('This is an abstract class.')
