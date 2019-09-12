"""
Index module
"""
from dataclasses import dataclass

from elasticsearch import Elasticsearch

from docsim.mappings import Mapping
from docsim.settings import es


@dataclass
class EsIndex:
    es_index: str
    es: Elasticsearch = es

    def create_index(self) -> bool:
        ack: Dict = self.es.indices.create(
            index=self.es_index,
            body={'mappings': mappings})
        return ack['acknowled']

    def bulk_insert(self, List[Mapping]) -> None:
        pass
