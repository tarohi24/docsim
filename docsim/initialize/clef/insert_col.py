"""
load a bulk -> insert
"""
import logging
from pathlib import Path
from typing import Generator

from elasticsearch.helpers import streaming_bulk
from tqdm import tqdm

from docsim.settings import data_dir, es


logger = logging.getLogger(__file__)


def loading() -> Generator[str, None, None]:
    directory: Path = data_dir.joinpath(f'clef/dump')
    for path in tqdm(list(directory.glob(f'*.bulk'))):
        with open(path) as fin:
            for line in fin.read().splitlines():
                yield line


if __name__ == '__main__':
    for ok, response in streaming_bulk(es,
                                       loading(),
                                       index='clef',
                                       chunk_size=100):
        if not ok:
            logger.warn('Bulk insert: fails')
    es.indices.refresh()
