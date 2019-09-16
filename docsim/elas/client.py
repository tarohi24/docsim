"""
Client module
"""
from dataclasses import dataclass
import logging
from typing import Dict, Iterable, Type

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from elasticsearch.helpers import streaming_bulk

from docsim.elas.models import EsItem
from docsim.settings import es


logger = logging.getLogger(__file__)


class IndexCreateError(Exception):
    pass


@dataclass
class EsClient:
    es_index: str
    item_cls: Type[EsItem]
    es: Elasticsearch = es

    def create_index(self) -> None:
        ack: Dict = self.es.indices.create(
            index=self.es_index,
            body={'mappings': self.item_cls.mapping()})
        logger.info(ack)

    def delete_index(self) -> None:
        try:
            self.es.indices.delete(index=self.es_index)
        except NotFoundError:
            logger.info(f'{self.es_index} does not exist')

    def bulk_insert(self,
                    items: Iterable[EsItem]) -> None:
        """
        CAUTION: This initializes the index.
        """
        def iter_items(items: Iterable[EsItem]) -> Iterable[Dict]:
            for item in items:
                yield item.to_dict()

        self.delete_index()
        self.create_index()

        for ok, response in streaming_bulk(es,
                                           iter_items(items),
                                           index=self.es_index,
                                           chunk_size=100):
            if not ok:
                logger.warn('Bulk insert: fails')
        self.es.indices.refresh()
