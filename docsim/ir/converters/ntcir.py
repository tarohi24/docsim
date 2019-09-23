from dataclasses import dataclass
from pathlib import Path
from typing import Generator, List
import xml.etree.ElementTree as ET

from docsim.elas import models
from docsim.ir.converters import base
from docsim.ir.models import ColDocument, ColParagraph, QueryDocument


@dataclass
class NTCIRConverter(base.Converter):

    def _get_title(self,
                   root: ET.Element) -> str:
        title: str = base.find_text_or_default(root, 'TITLE', '')
        return title

    def _get_docid(self,
                   root: ET.Element) -> str:
        def convert_docid(orig: str) -> str:
            """
            >>> converters('PATENT-US-GRT-1993-05176894')
            '199305176894'
            """
            return ''.join(orig.split('-')[-2:])

        docid: str = base.find_text_or_default(root, 'DOCNO', '')
        return convert_docid(docid)

    def _get_tags(self,
                  root: ET.Element) -> List[str]:
        def convert_tags(orig: str) -> List[str]:
            """
            >>> convert_tags('C01C 03/16')
            'C01C'
            """
            return orig.split(' ')[:1]

        clfs: str = base.find_text_or_default(root, 'PRI-IPC', '')
        return convert_tags(clfs)

    def _get_text(self,
                  root: ET.Element) -> str:
        text: str = base.find_text_or_default(root, 'SPEC', '')
        return text

    def _get_paragraph_list(self,
                            root: ET.Element) -> List[str]:
        """
        NOTE: is it possible to separate NTCIR patent into paragraphs?
        """
        raise NotImplementedError('Yet implemented.')

    def to_document(self,
                    fpath: Path) -> Generator[ColDocument, None, None]:
        with open(fpath, 'r') as fin:
            lines: List[str] = [line\
                                .replace('<tab>', '\t')\
                                .replace('"', '&quot;')\
                                .replace("&", "&amp;")\
                                .replace("\"", "&quot;")
                                for line in fin.read().splitlines()]

        for line in lines:
            root: ET.Element = ET.fromstring(line)
            docid: str = self._get_docid(root)
            tags: List[str] = self._get_tags(root)
            title: str = self._get_title(root)
            text: str = self._get_text(root)
            yield ColDocument(docid=models.KeywordField(docid),
                              title=models.TextField(title),
                              text=models.TextField(text),
                              tags=models.KeywordListField(tags))

    def to_paragraph(self,
                     fpath: Path) -> List[ColParagraph]:
        raise NotImplementedError('Yet implemented.')

    def to_query_dump(self,
                      fpath: Path) -> List[QueryDocument]:
        raise NotImplementedError('Yet implemented.')
