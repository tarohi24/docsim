from dataclasses import dataclass
import logging
from pathlib import Path
import sys
from typing import Dict, List, Tuple
import xml.etree.ElementTree as ET

import nltk

from docsim.elas import models
from docsim.converters.base import (
    Converter
)
from docsim.models import ColDocument, ColParagraph, QueryDocument
from docsim.settings import data_dir

logger = logging.getLogger(__file__)
with open(data_dir.joinpath('aan/orig/citations.txt'), 'r') as fin:
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

    def _get_info(self,
                  fpath: Path) -> Tuple[str, List[str], str, str]:
        docid: str = fpath.stem
        tags: List[str] = [docid.split('-')[0], ]  # the first alphabet
        try:
            title: str = title_dic[docid]
        except KeyError:
            logger.warn(f'The title of {docid} is not found')
            title: str = ''  # type: ignore
        with open(fpath, 'r') as fin:
            text: str = fin.read()
        return docid, tags, title, text

    def to_document(self,
                    fpath: Path) -> List[ColDocument]:
        docid, tags, title, text = self._get_info(fpath)
        return [ColDocument(docid=models.KeywordField(docid),
                            title=models.TextField(title),
                            text=models.TextField(text),
                            tags=models.KeywordListField(tags))]

    def to_paragraph(self,
                     fpath: Path) -> List[ColParagraph]:
        pass

    def to_query_dump(self,
                      fpath: Path) -> List[QueryDocument]:
        """
        NOTE: paras are made by sent_tokenizer
        """
        docid, tags, _, text = self._get_info(fpath)
        tokenized: List[str] = nltk.sent_tokenize(text)
        return [QueryDocument(docid=docid,
                              paras=tokenized,
                              tags=tags)]


if __name__ == '__main__':
    converter = AANConverter()
    fpath: Path = Path(sys.argv[1])
    print(converter.to_document(fpath))
