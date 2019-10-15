import argparse
from dataclasses import dataclass, field
import logging
import json
from pathlib import Path
from typing import Dict, Generator, Iterable, List, Type
import xml.etree.ElementTree as ET

from tqdm import tqdm

from docsim.elas.client import EsClient
from docsim.converters.base import Converter, DummyConverter, find_text_or_default, get_or_raise_exception
from docsim.converters.aan import AANConverter
from docsim.converters.clef import CLEFConverter
from docsim.converters.ntcir import NTCIRConverter
from docsim.models import ColDocument, ColParagraph, QueryDataset, QueryDocument
from docsim.settings import data_dir

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('-d',
                    '--dataset',
                    nargs=1,
                    type=str,
                    help='The name of the dataset')
parser.add_argument('-o',
                    '--operations',
                    nargs='+',
                    type=str,
                    help='Operations')
parser.add_argument('-f', '--fake',
                    nargs='?',
                    default=None,
                    help="Specify this flag when you won't save the result")


class Dataset:
    converter: Converter = field(default_factory=DummyConverter)

    @property
    def mapping_fpath(self) -> Path:
        return data_dir.joinpath(f'ntcir/name_mapping.json')

    def iter_orig_files(self) -> Iterable[Path]:
        raise NotImplementedError('This is an abstract class')

    def iter_query_files(self) -> Iterable[Path]:
        raise NotImplementedError('This is an abstract class')

    def create_name_mapping(self) -> Dict[str, str]:
        raise NotImplementedError('This is an abstract class')

    def iter_converted_docs(self) -> Generator[ColParagraph, None, None]:
        pbar_succ: tqdm = tqdm(position=0, desc='Success')
        pbar_fails: Dict[str, tqdm] = dict()
        converter: Converter = self.converter
        for fpath in self.iter_orig_files():
            try:
                for doc in converter.to_document(fpath):
                    yield doc
                    pbar_succ.update(1)
            except Exception as e:
                ename: str = type(e).__name__
                if ename == 'NameError':
                    logger.exception(e, exc_info=True)
                if ename not in pbar_fails:
                    pbar_fails[ename] = tqdm(position=len(pbar_fails), desc=ename)
                pbar_fails[ename].update(1)
                logger.error('Bulk insert: failes')
            else:
                logger.info('Bulk insert: succeed')


@dataclass
class CLEFDataset(Dataset):
    converter: Converter = field(default_factory=CLEFConverter)

    def iter_orig_files(self) -> Generator[Path, None, None]:
        return data_dir.joinpath(f'clef/orig/collection').glob(f'**/*.xml')

    def iter_query_files(self) -> Generator[Path, None, None]:
        return data_dir.joinpath(f'clef/orig/query').glob(f'**/*.xml')


@dataclass
class NTCIRDataset(Dataset):
    converter: Converter = field(default_factory=NTCIRConverter)

    @property
    def mapping_fpath(self) -> Path:
        return data_dir.joinpath(f'ntcir/name_mapping.json')

    def iter_orig_files(self) -> Generator[Path, None, None]:
        return data_dir.joinpath(f'ntcir/orig/collection').glob(f'**/*.xml')

    def iter_query_files(self) -> Generator[Path, None, None]:
        return data_dir.joinpath(f'ntcir/orig/query').glob(f'**/*.xml')

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


@dataclass
class AANDataset(Dataset):
    converter: Converter = field(default_factory=AANConverter)

    def iter_orig_files(self) -> Generator[Path, None, None]:
        return data_dir.joinpath(f'aan/orig/collection').glob(f'*.txt')

    def iter_query_files(self) -> Generator[Path, None, None]:
        return self.iter_orig_files()


dataset_dict: Dict[str, Type[Dataset]] = {
    'clef': CLEFDataset,
    'ntcir': NTCIRDataset,
    'aan': AANDataset,
}


def main(ds_name: str,
         operations: Iterable[str]) -> None:
    ds_cls: Type[Dataset] = dataset_dict[ds_name]
    dataset: Dataset = ds_cls()
    if 'doc' in operations:
        es_client: EsClient = EsClient(
            es_index=ds_name,
            item_cls=ColDocument)
        es_client.bulk_insert(dataset.iter_converted_docs())

    if 'para' in operations:
        raise NotImplementedError('Para is not prepared')

    if 'query' in operations:
        qlist: List[QueryDocument] = sum(
            [dataset.converter.to_query_dump(fpath) for fpath in dataset.iter_query_files()],
            []
        )
        dic: Dict = QueryDataset(name=ds_name, queries=qlist).to_dict()
        with open(data_dir.joinpath(f'{ds_name}/query/dump.json'), 'w') as fout:
            json.dump(dic, fout)

    if 'mapping' in operations:
        mpg: Dict[str, str] = dataset.create_name_mapping()
        with open(dataset.mapping_fpath, 'w') as fout:
            json.dump(mpg, fout)


if __name__ == '__main__':
    args = parser.parse_args()
    main(args.dataset[0], args.operations)
