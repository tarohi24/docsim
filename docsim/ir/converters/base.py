from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from docsim.ir.models import ColDocument, ColParagraph, QueryDocument


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
