from dataclasses import dataclass
from pathlib import Path
from typing import List
import xml.etree.ElementTree as ET

import chardet

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

    def is_valid_text(self,
                      fpath: Path) -> bool:
        """
        EUC_JP -> invalid (we have to get rid of ja docs)
        """
        with open(fpath, 'r') as fin:
            enc: str = chardet.detect(fin.read())['encoding']
        if enc == 'EUC-JP':
            return False
        elif enc == 'ASCII':
            return True
        else:
            raise AssertionError(f'{enc} is unknow')
