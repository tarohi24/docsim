import sys

from docsim.dataset import Dataset, dataset_dict
from docsim.elas.index import EsClient
from docsim.elas.mappings import IRBase


def main(ds_name: str) -> None:
    dataset: Dataset = dataset_dict[ds_name]
    es_client: EsClient(
        es_index=dataset.es_index,
        item_cls=IRBase)
    items: Generator[IRBase, None, None] = {
        dataset.converter.generate_irbase(fpath)
        for fpath in dataset.original_files()
    }
    es_client.bulk_insert(items)


if __name__ == '__main__':
    main(sys.argv[1])
