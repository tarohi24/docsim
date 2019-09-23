from dataclasses import dataclass
import logging
import json
from pathlib import Path
import sys
from typing import Dict, Generator, Iterable, List, Type

from tqdm import tqdm

from docsim.elas.client import EsClient
from docsim.ir.converters.base import Converter
from docsim.ir.converters.clef import CLEFConverter
from docsim.ir.converters.ntcir import NTCIRConverter
from docsim.ir.models import ColDocument, ColParagraph, QueryDataset, QueryDocument
from docsim.settings import project_root

logger = logging.getLogger(__file__)
# logging.disable(logging.CRITICAL)


@dataclass
class Dataset:
    name: str

    @property
    def converter(self) -> Converter:
        cls: Type[Converter] = {
            'clef': CLEFConverter,
            'ntcir': NTCIRConverter,
        }[self.name]
        return cls()

    @property
    def extension(self) -> str:
        ext: str = {
            'clef': 'xml',
            'ntcir': 'txt',
        }[self.name]
        return ext

    def iter_orig_files(self) -> Generator[Path, None, None]:
        return project_root.joinpath(f'data/{self.name}/orig/collection').glob(f'**/*.{self.extension}')

    def iter_query_files(self) -> Generator[Path, None, None]:
        return project_root.joinpath(f'data/{self.name}/orig/query').glob(f'**/*.{self.extension}')

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


def main(ds_name: str,
         operations: Iterable[str]) -> None:
    # insert bulk
    dataset: Dataset = Dataset(name=ds_name)
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
        with open(project_root.joinpath(f'data/{ds_name}/query/dump.json'), 'w') as fout:
            json.dump(dic, fout)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
