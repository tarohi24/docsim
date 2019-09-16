from collections import defaultdict
from dataclasses import dataclass
import logging
from pathlib import Path
import sys
from typing import Generator, Iterable, Type

from tqdm import tqdm

from docsim.elas.client import EsClient
from docsim.ir.converters.base import Converter
from docsim.ir.converters.clef import CLEFConverter
from docsim.ir.models import ColDocument
from docsim.settings import project_root

logger = logging.getLogger(__file__)
# logging.disable(logging.CRITICAL)


@dataclass
class Dataset:
    name: str
    
    @property
    def converter(self) -> Converter:
        cls: Type[Converter] = {
            'clef': CLEFConverter
        }[self.name]
        return cls()
    
    def iter_orig_files(self) -> Generator[Path, None, None]:
        return project_root.joinpath(f'data/{self.name}/orig').glob('**/*.xml')

    def iter_converted_docs(self) -> Generator[ColDocument, None, None]:
        pbar_succ = tqdm(position=0)
        pbar_fails = dict()
        converter: Converter = self.converter
        for fpath in self.iter_orig_files():
            try:
                for doc in converter.to_document(fpath):
                    yield doc
            except Exception as e:
                ename: str = type(e).__name__ 
                if ename == 'NameError':
                    logger.exception(e, exc_info=True)
                if ename not in pbar_fails:
                    pbar_fails[ename] = tqdm(position=len(pbar_fails), desc=ename)
                pbar_fails[ename].update(1)
            else:
                pbar_succ.update(1)


def main(ds_name: str) -> None:
    # insert bulk
    dataset: Dataset = Dataset(name=ds_name)
    es_client: EsClient = EsClient(
        es_index=ds_name,
        item_cls=ColDocument)
    es_client.bulk_insert(dataset.iter_converted_docs())


if __name__ == '__main__':
    main(sys.argv[1])
