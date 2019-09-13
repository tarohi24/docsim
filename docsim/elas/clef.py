import logging
from pathlib import Path
import xml.etree.ElementTree as ET
from typing import List, Optional, TypeVar

from docsim.elas import mappings as mpgs
from docsim.elas.mappings import IRBase


logger = logging.getLogger(__file__)
T = TypeVar('T')


class NoneException(Exception):
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
        text: Optional[str] = get_or_raise_exception(content.text)
    except NoneException:
        return default
    return text


def get_paragraph_list(root: ET.Element) -> List[str]:
    try:
        desc_root: ET.Element = get_or_raise_exception(root.find("description[@lang='EN']"))
    except NoneException:
        return []
    ps: List[ET.Element] = desc_root.findall('p')
    if len(ps) > 1:
        return [d.text for d in ps]
    elif len(ps) == 1:
        try:
            pre_text: str = get_or_raise_exception(ps[0].find('pre').text, default='')
            return pre_text.replace('\\n', '\n').split('\n\n')
        except:
            li: List[ET.Element] = ps[0].findall('sl/li')
            return [d.text for d in li]
    return []


class CLEFConverter(mpgs.Converter):

    def convert(self,
                xml_fpath: Path) -> IRBase:
        root: ET.Element = ET.parse(str(self.xml_fpath.resolve())).getroot()

        # docid
        try:
            docid: str = root.attrib['ucid'].replace('-', '')
        except KeyError:
            logger.warning('DocID not found')

        # text
        text: str = find_text_or_default(
            root=root,
            xpath="bibliographic-data/description[@lang='EN']",
            default='')
        title: str = find_text_or_default(
            root=root,
            xpath="bibliographic-data/technical-data/invention-title[@lang='EN']",
            default='')
        tags_field: str = 'bibliographic-data/technical-data/classifications-ipcr'
        tags_orig: List[ET.Element] = root.findall(tags_field)
        tags: List[str] = [t.text.split()[0] for t in tags_orig if t.text is not None]

        return mpgs.IRBase(
            docid=mpgs.KeywordField(docid),
            title=mpgs.TextField(title),
            text=mpgs.TextField(text),
            tags=mpgs.TagsField(tags))
