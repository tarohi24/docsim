from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Generator, List

from docsim.elas import models
from docsim.ir.converters import base
from docsim.ir.models import ColDocument, ColParagraph, QueryDocument

ATTRS: List[str] = [
    'DOC',  # Document
    'DOCNO',  # Document identifier (*)
    'APP-NO',  # Application number
    'APP-DATE',  # Application date
    'PUB-NO',  # Publication number
    'PUB-TYPE',  # Publication type
    'PAT-NO',  # Patent number
    'PAT-TYPE',  # Patent type (**)
    'PUB-DATE',  # Publication date
    'PRI-IPC',  # Primary IPC
    'IPC-VER',  # IPC version
    'PRI-USPC',  # Primary USPC
    'PRIORITY',  # Priority information
    'CITATION',  # Citation(s) (***)
    'INVENTOR',  # Inventor(s)
    'ASSIGNEE',  # Assignee(s)
    'TITLE',  # Title
    'ABST',  # Abstract
    'SPEC',  # Specification
    'CLAIM',  # Claim(s)
]


@dataclass
class NTCIRConverter(base.Converter):

    def _to_attr_dict(self, line: str) -> Dict[str, str]:
        if line[-1] == '\n':
            line: str = line[:-1]  # noqa

        doc: Dict[str, str] = {
            attr: body
            for attr, body
            in zip(ATTRS, line.split('\t'))
        }
        return doc

    def to_document(self,
                    fpath: Path) -> Generator[ColDocument, None, None]:
        with open(fpath, 'r') as fin:
            for line in fin.readlines():
                doc: Dict[str, str] = self._to_attr_dict(line)
                docid: str = doc['DOCNO']
                tags: List[str] = [doc['PRI-IPC'], ]
                title: str = doc['TITLE']
                # NOTE: text is the abstract
                text: str = doc['SPEC']
                yield ColDocument(docid=models.KeywordField(docid),
                                  title=models.TextField(title),
                                  text=models.TextField(text),
                                  tags=models.KeywordListField(tags))

    def to_paragraph(self,
                     fpath: Path) -> List[ColParagraph]:
        raise NotImplementedError('This is an abstract method.')

    def to_query_dump(self,
                      fpath: Path) -> List[QueryDocument]:
        raise NotImplementedError('This is an abstract method.')
