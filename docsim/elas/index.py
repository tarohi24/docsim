"""
Index module
"""
from dataclasses import dataclass
from typing import Iterable

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, streaming_bulk

from docsim.mappings import EsItem
from docsim.settings import es


ItemClass = TypeVar('ItemClass', bound=EsItem)
logger = logging.getLogger(__file__)


class IndexCreateError(Exception):
    pass


@dataclass
class EsIndex:
    es_index: str
    es: Elasticsearch = es
    item_cls: ItemClass

    def create_index(self) -> None:
        ack: Dict = self.es.indices.create(
            index=self.es_index,
            body={'mappings': mappings})
        if 'acknowled' not in ack:
            raise IndexCreateError(f'Index {self.es_index} already exists')
        elif not ack['acknowled']:
            raise IndexCreateError(f'Error when creating index {self.es_index}')
        else:
            return

    def bulk_insert(self, items: Iterable[self.item_cls]) -> None:
        """
        CAUTION: This initializes the index.
        """
        def iter_items(items: Iterable[self.item_cls]) -> Iterable[Dict]:
            for item in items:
                yield item.to_dict()

        try:
            self.es.incides.refresh()
        except IndexCreateError:
            raise AssertionError('Bulk insert fails')

        for ok, response in streaming_bulk(es,
                                           iter_items(items),
                                           index=self.es_index,
                                           chunk_size=100):
            if not ok:
                logger.warn('Bulk insert: fails')
