"""
Basic module for initializing
"""
from dataclasses import dataclass, field
import json
import logging
from pathlib import Path
from typing import Dict, Generator, Iterable, List

from tqdm import tqdm

from docsim.converters.base import Converter, DummyConverter
from docsim.elas.client import EsClient
from docsim.models import ColDocument, ColParagraph, QueryDataset, QueryDocument
from docsim.settings import data_dir


logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


@dataclass
class Dataset:
    converter: Converter = field(default_factory=DummyConverter)

    @property
    def mapping_fpath(self) -> Path:
        raise NotImplementedError('This is an abstract class')

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
                    pbar_fails[ename] = tqdm(
                        position=len(pbar_fails), desc=ename)
                pbar_fails[ename].update(1)
                logger.error('Bulk insert: failes')
            else:
                logger.info('Bulk insert: succeed')


@dataclass
class E2EConverter:
    """end-to-end converter"""
    dataset: Dataset
    name: str

    def dump_query(self) -> None:
        qlist: List[QueryDocument] = sum(
            [list(self.dataset.converter.to_query_dump(fpath))
             for fpath in self.dataset.iter_query_files()],
            []
        )
        dic: Dict = QueryDataset(name=self.name, queries=qlist).to_dict()
        fpath: Path = data_dir.joinpath(f'{self.name}/query/dump.json')
        with open(fpath, 'w') as fout:
            json.dump(dic, fout)

    def insert_col(self) -> None:
        es_client: EsClient = EsClient(
            es_index=self.name,
            item_cls=ColDocument)
        es_client.bulk_insert(self.dataset.iter_converted_docs())

    def create_name_mappings(self) -> None:
        mpg: Dict[str, str] = self.dataset.create_name_mapping()
        try:
            with open(self.dataset.mapping_fpath, 'w') as fout:
                json.dump(mpg, fout)
        except FileNotFoundError:
            logger.info(f'{self.name}: name mappings are not necessary...')
            pass

    def run(self) -> None:
        logger.info(f'{self.name}: dumping queries...')
        self.dump_query()
        logger.info(f'{self.name}: creating mappings...')
        self.create_name_mappings()
        logger.info(f'{self.name}: creating mappings...')
        self.insert_col()
