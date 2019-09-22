from dataclasses import dataclass
from typing import List

from docsim.ir.converters import base


@dataclass
class NTCIRConverter(base.Converter):
    def _get_docid(self,
                   root: ET.Element) -> str:
        pass

    def _get_tags(self,
                  root: ET.Element) -> List[str]:
        pass

    def _get_title(self,
                   root: ET.Element) -> str:
        pass

    def _get_text(self,
                  root: ET.Element) -> str:
        pass

    def _get_paragraph_list(self,
                            root: ET.Element) -> List[str]:
        pass
