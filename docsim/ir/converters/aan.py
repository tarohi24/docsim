from dataclasses import dataclass
import logging
from pathlib import Path
import sys
from typing import Dict, List
import xml.etree.ElementTree as ET

from docsim.elas import models
from docsim.ir.converters.base import (
    Converter
)
from docsim.ir.models import ColDocument, ColParagraph, QueryDocument
from docsim.settings import project_root

logger = logging.getLogger(__file__)
with open(project_root.joinpath('data/aan/orig/titles.txt'), 'r') as fin:
    title_dic: Dict[str, str] = {
        line[0]: line[1]
        for line
        in [l.split('\t') for l in fin.read().splitlines()]
    }


@dataclass
class AANConverter(Converter):

    def _get_paragraph_list(self,
                            root: ET.Element) -> List[str]:
        pass

    def to_document(self,
                    fpath: Path) -> List[ColDocument]:
        docid: str = fpath.stem
        tags: List[str] = [docid.split('-')[0], ]  # the first alphabet
        title: str = title_dic[docid]
        with open(fpath, 'r') as fin:
            text: str = fin.read()
        return [ColDocument(docid=models.KeywordField(docid),
                            title=models.TextField(title),
                            text=models.TextField(text),
                            tags=models.KeywordListField(tags))]

    def to_paragraph(self,
                     fpath: Path) -> List[ColParagraph]:
        pass

    def to_query_dump(self,
                      fpath: Path) -> List[QueryDocument]:
        pass


if __name__ == '__main__':
    converter = AANConverter()
    fpath: Path = Path(sys.argv[1])
    print(converter.to_document(fpath))
