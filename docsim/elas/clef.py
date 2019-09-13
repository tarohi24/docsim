from dataclasses import dataclass
import logging
from pathlib import Path
import re
from tqdm import tqdm
from typing import Generator, List, Optional, TypeVar
import xml.etree.ElementTree as ET

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
        text: str = get_or_raise_exception(content.text)
    except NoneException:
        return default
    return text


def get_paragraph_list(root: ET.Element) -> List[str]:
    desc_root: Optional[ET.Element] = root.find("description[@lang='EN']")
    if desc_root is None:
        logger.debug('root is not found')
        return []
    ps: List[ET.Element] = [tag for tag in desc_root.findall('p') if tag is not None]
    if len(ps) > 1:
        return [d.text for d in ps if d.text is not None]
    elif len(ps) == 1:
        try:
            pre_text: str = get_or_raise_exception(
                ps[0].find('pre')).text.replace('\\n', '\n')  # noqa
            splitted = re.split('\n{2,}', pre_text)
            return splitted
        except NoneException:
            li: List[ET.Element] = ps[0].findall('sl/li')
            return [d.text for d in li if d.text is not None]
    logger.debug('No condition is matched')
    return []


@dataclass
class CLEFConverter(mpgs.Converter):
    pbar_succ = tqdm(position=0, desc='success')
    pbar_fail = tqdm(position=1, desc='fail')

    def generate_irbase(self,
                        fpath: Path) -> Generator[IRBase, None, None]:
        root: ET.Element = ET.parse(str(fpath.resolve())).getroot()

        # docid
        try:
            docid: str = root.attrib['ucid'].replace('-', '')
        except KeyError:
            self.pbar_fail.update(1)
            logger.warning('DocID not found')

        # text
        try:
            paras: List[str] = get_paragraph_list(root)
        except Exception:
            logger.warning('Could not find description field in the original XML.')
            self.pbar_fail.update(1)
            return

        if len(paras) == 0:
            logger.warning('No paragraphs found.')
            self.pbar_fail.update(1)
            return

        logger.info('XML successfully parsed')
        title: str = find_text_or_default(
            root=root,
            xpath="bibliographic-data/technical-data/invention-title[@lang='EN']",
            default='')
        tags_field: str = 'bibliographic-data/technical-data/classifications-ipcr'
        tags_orig: List[ET.Element] = root.findall(tags_field)
        tags: List[str] = [t.text.split()[0] for t in tags_orig if t.text is not None]

        for paraid, para in enumerate(paras):
            self.pbar_succ.update(1)
            yield mpgs.IRBase(
                docid=mpgs.KeywordField(docid),
                paraid=mpgs.IntField(paraid),
                title=mpgs.TextField(title),
                text=mpgs.TextField(para),
                tags=mpgs.KeywordListField(tags))
