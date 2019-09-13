"""
Index module
"""
from dataclasses import dataclass
import logging
from typing import Dict, Iterable, Type

from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
from tqdm import tqdm

from docsim.mappings import EsItem
from docsim.settings import es


logger = logging.getLogger(__file__)


class IndexCreateError(Exception):
    pass


@dataclass
class EsIndex:
    es_index: str
    item_cls: Type[EsItem]
    es: Elasticsearch = es

    def create_index(self) -> None:
        ack: Dict = self.es.indices.create(
            index=self.es_index,
            body={'mappings': self.item_cls.mappings()})
        if 'acknowled' not in ack:
            raise IndexCreateError(f'Index {self.es_index} already exists')
        elif not ack['acknowled']:
            raise IndexCreateError(f'Error when creating index {self.es_index}')
        else:
            return

    def bulk_insert(self,
                    items: Iterable[EsItem]) -> None:
        """
        CAUTION: This initializes the index.
        """
        def iter_items(items: Iterable[EsItem]) -> Iterable[Dict]:
            for item in items:
                yield item.to_dict()

        try:
            self.es.incides.refresh()
        except IndexCreateError:
            raise AssertionError('Bulk insert fails')

        for ok, response in tqdm(streaming_bulk(es,
                                                iter_items(items),
                                                index=self.es_index,
                                                chunk_size=100)):
            if not ok:
                logger.warn('Bulk insert: fails')
