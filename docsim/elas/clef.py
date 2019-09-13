from dataclasses import dataclass
import logging
from pathlib import Path
import xml.etree.ElementTree as ET
from typing import List, Optional, TypeVar

from docsim.elas import mappings as mpgs
from docsim.elas.mappings import IRBase


logger = logging.getLogger(__file__)
T = TypeVar('T')


def find_or_default(root: ET.Element,
                    xpath: str,
                    default: str) -> str:
    content: Optional[ET.Element] = root.find(xpath)
    if content is None:
        return default
    else:
        text: Optional[str] = content.text
        if text is not None:
            return text
        else:
            return default


@dataclass
class CLEFConverter(mpgs.Converter):
    xml_fpath: Path

    def convert(self) -> IRBase:
        root: ET.Element = ET.parse(str(self.xml_fpath.resolve())).getroot()

        # docid
        try:
            docid: str = root.attrib['ucid'].replace('-', '')
        except KeyError:
            logger.warning('DocID not found')

        # text
        text: str = find_or_default(
            root=root,
            xpath="bibliographic-data/description[@lang='EN']",
            default='')
        title: str = find_or_default(
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
