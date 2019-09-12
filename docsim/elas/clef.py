from dataclasses import dataclass
import logging
from pathlib import Path
import xml.etree.ElementTree as ET

from docsim.elas import mappings as mpgs


logger = logging.getLogger(__file__)
T = TypeVar('T')


def find_or_default(root: ET.Element,
                    xpath: str,
                    default: str) -> str:
    content: Optional[T] = root.find(xpath)
    return content.text if content is not None else default


@dataclass
class CLEFConverter(mpgs.Converter):
    xml_fpath: Path

    def convert(self) -> IRBase:
        root: ET.Element = ET.parse(str(self.xml_fpath.resolve())).get_root()

        # docid
        try:
            docid: str = root.attrib['ucid'].replace('-', '')
        except KeyError as e:
            logger.warning('DocID not found')
            
        # text
        text: str = find_or_default(
            root=root,
            xpath="bibliographic-data/description[@lang='EN']",
            default='')
        title: str = find_or_default(
            root=root,
            xpaht="bibliographic-data/technical-data/invention-title[@lang='EN']",
            default='')
        tags_field: str = 'bibliographic-data/technical-data/classifications-ipcr'
        tags: List[str] = [t.text.split()[0] for t in root.findall(tags_field)]
    
        return mpgs.IRBase(
            docid=mpgs.KeywordField(docid),
            title=mpgs.TextField(title),
            text=mpgs.TextField(text),
            tags=mpgs.TagsField(tags))

@dataclass
class CLEFInser
