from dataclasses import dataclass
import logging
from pathlib import Path
import re
import sys
from typing import List, Optional, TypeVar
import xml.etree.ElementTree as ET

from docsim.elas import models
from docsim.ir.converters.base import Converter
from docsim.ir.models import ColDocument, ColParagraph, QueryDocument

logger = logging.getLogger(__file__)
T = TypeVar('T')


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


@dataclass
class CLEFConverter(Converter):

    def _get_docid(self,
                   root: ET.Element) -> str:
        docid: str = root.attrib['ucid'].replace('-', '')
        return docid

    def _get_tags(self,
                  root: ET.Element) -> List[str]:
        tags_field: str = 'bibliographic-data/technical-data/classifications-ipcr/classification-ipcr'
        tags_orig: List[ET.Element] = root.findall(tags_field)
        tags: List[str] = [t.text.split()[0] for t in tags_orig if t.text is not None]
        return list(set(tags))

    def _get_title(self,
                   root: ET.Element) -> str:
        title: str = find_text_or_default(
            root=root,
            xpath="bibliographic-data/technical-data/invention-title[@lang='EN']",
            default='')
        return title

    def _get_text(self,
                  root: ET.Element) -> str:
        desc_root: ET.Element = get_or_raise_exception(
            root.find("description[@lang='EN']"))
        desc: str = ' '.join(desc_root.itertext()).replace('\n', ' ')
        return desc

    def get_paragraph_list(self,
                           root: ET.Element) -> List[str]:
        desc_root: Optional[ET.Element] = root.find("description")
        if desc_root is None:
            raise CannotSplitText('root is not found')
        ps: List[ET.Element] = [tag for tag in desc_root.findall('p') if tag is not None]
        if len(ps) > 1:
            return [d.text for d in ps if d.text is not None]
        elif len(ps) == 1:
            try:
                pre_text: str = get_or_raise_exception(ps[0].find('pre')).text.replace('\\n', '\n')  # noqa
                splitted = re.split('\n{2,}', pre_text)
                return splitted
            except NoneException:
                li: List[ET.Element] = ps[0].findall('sl/li')
                return [d.text for d in li if d.text is not None]
        raise CannotSplitText('No condition is matched')

    def to_document(self,
                    fpath: Path) -> List[ColDocument]:
        root: ET.Element = ET.parse(str(fpath.resolve())).getroot()

        docid: str = self._get_docid(root)
        tags: List[str] = self._get_tags(root)
        title: str = self._get_title(root)
        text: str = self._get_text(root)
        return [ColDocument(docid=models.KeywordField(docid),
                            title=models.TextField(title),
                            text=models.TextField(text),
                            tags=models.KeywordListField(tags))]

    def to_paragraph(self,
                     fpath: Path) -> List[ColParagraph]:
        root: ET.Element = ET.parse(str(fpath.resolve())).getroot()
        # text
        try:
            paras: List[str] = self.get_paragraph_list(root)
        except Exception as e:
            logger.warning(e, exc_info=True)
            logger.warning('Could not find description field in the original XML.')
        if len(paras) == 0:
            logger.warning('No paragraphs found.')
            return []

        docid: str = self._get_docid(root)
        tags: List[str] = self._get_tags(root)

        return [
            ColParagraph(docid=models.KeywordField(docid),
                         paraid=models.IntField(paraid),
                         text=models.TextField(para),
                         tags=models.KeywordListField(tags))
            for paraid, para in enumerate(paras)]

    def to_query_dump(self,
                      fpath: Path) -> List[QueryDocument]:
        root: ET.Element = ET.parse(str(fpath.resolve())).getroot()

        try:
            paras: List[str] = self.get_paragraph_list(root)
        except Exception as e:
            logger.warning(e, exc_info=True)
            return []
        if len(paras) == 0:
            logger.warning('No paragraphs found.')
            return []

        docid: str = self._get_docid(root)
        tags: List[str] = self._get_tags(root)

        return [
            QueryDocument(docid=docid,
                          paras=paras,
                          tags=tags)]


if __name__ == '__main__':
    converter = CLEFConverter()
    fpath: Path = Path(sys.argv[1])
    print(converter.to_document(fpath))
