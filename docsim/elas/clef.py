import logging
from pathlib import Path
import xml.etree.ElementTree as ET

from docsim.elas.mappings import Converter, IRBase

logger = logging.getLogger(__file__)
T = TypeVar('T')


def find_or_default(root: ET.Element,
                    xpath: str,
                    default: str) -> str:
    content: Optional[T] = root.find(xpath)
    return content.text if content is not None else default


@dataclass
class CLEFConverter(Converter):
    xml_fpath: Path

    @staticmethod
    
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
        tags_orig: str = find_or_default(
            root=root,
            xpath='bibliographic-data/technical-data/classifications-ipcr')
        
        
        try:
            text: str = root.find("").text.replace('\n', ' ')
        except Exception as e:
            logger.warning('Description not found')

        bib: Optional[ET.Element] = root.find('')
        if bib is not None:
            # title
            try:
                title: str = bib.find("technical-data/invention-title[@lang='EN']").text
            except Exception as e:
                logger.warning('Title not found')

            # patent classification
            if bib is not None:
                try:
                except Exception as e:
                    logger.warning('Classsifications not found')
                    tags: List
            return IRBase(
                docid=docid,
                text=text,
                
        else:
            

            
            
