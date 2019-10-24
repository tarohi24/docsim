from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Generator
import xml.etree.ElementTree as ET

from docsim.converters.base import find_text_or_default, get_or_raise_exception
from docsim.converters.ntcir import NTCIRConverter
from docsim.initialize.base import Dataset
from docsim.settings import data_dir


@dataclass
class NTCIRDataset(Dataset):
    converter: NTCIRConverter = field(default_factory=NTCIRConverter)

    @property
    def mapping_fpath(self) -> Path:
        return data_dir.joinpath(f'ntcir/name_mapping.json')

    def iter_orig_files(self) -> Generator[Path, None, None]:
        return data_dir.joinpath(f'ntcir/orig/collection').glob(f'**/*')

    def iter_query_files(self) -> Generator[Path, None, None]:
        return data_dir.joinpath(f'ntcir/orig/query').glob(f'**/*')

    def create_name_mapping(self) -> Dict[str, str]:
        mpg: Dict[str, str] = dict()
        for fpath in self.iter_query_files():
            with open(fpath, 'r') as fin:
                xml_body: str = self.converter.escape(fin.read())
            root: ET.Element = ET.fromstring(xml_body)
            topic_num: str = find_text_or_default(root, 'NUM', '')
            doc_root: ET.Element = get_or_raise_exception(root.find('DOC'))
            docid: str = self.converter._get_docid(doc_root)
            if topic_num == '' or docid == '':
                raise AssertionError
            mpg[topic_num] = docid
        return mpg
