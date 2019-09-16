from pathlib import Path
from typing import Iterable

from docsim.ir.models import IRDocument, IRParagraph


class Converter:
    """
    convert something into IRBase
    """
    def to_irdocument(self, fpath: Path) -> Iterable[IRDocument]:
        raise NotImplementedError('This is an abstract class.')

    def to_irparagraph(self,
                       docs: Iterable[IRDocument]) -> Iterable[IRParagraph]:
        raise NotImplementedError('This is an abstract class.')
