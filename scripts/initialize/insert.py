from pathlib import Path
import sys
from typing import Generator, Iterable

from docsim.dataset import Dataset, dataset_dict
from docsim.elas.index import EsClient
from docsim.elas.mappings import IRBase, Converter


def item_generator(files: Iterable[Path],
                   converter: Converter) -> Generator[IRBase, None, None]:
    for fpath in files:
        for item in converter.generate_irbase(fpath):
            yield item


def main(ds_name: str) -> None:
    dataset: Dataset = dataset_dict[ds_name]
    es_client: EsClient = EsClient(
        es_index=dataset.es_index,
        item_cls=IRBase)
    es_client.bulk_insert(
        item_generator(
            files=dataset.list_original_files(),
            converter=dataset.converter))


if __name__ == '__main__':
    main(sys.argv[1])
