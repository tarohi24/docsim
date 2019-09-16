"""
Module for elasticsaerch
"""
from __future__ import annotations
from dataclasses import dataclass
from numbers import Real
from typing import Dict, List, Type, TypeVar

from dataclasses_jsonschema import JsonSchemaMixin


T_JsonSchemaMixin = TypeVar('T_JsonSchemaMixin', bound='JsonSchemaMixin')
T_EsResult = TypeVar('T_EsResult', bound='EsResult')


@dataclass
class EsResultItem(JsonSchemaMixin):
    elas_id: str
    score: Real
    source: Dict

    @classmethod
    def from_dict(cls: Type[T_JsonSchemaMixin],
                  data: Dict,
                  validate: bool = True) -> T_JsonSchemaMixin:
        new_data: Dict = {
            'elas_id': data['_id'],
            'score': data['_score'],
            'source': data['_source'],
        }
        return super(EsResultItem, cls).from_dict(new_data)


@dataclass
class EsResult:
    hits: List[EsResultItem]

    @classmethod
    def from_dict(cls,
                  data: Dict) -> 'EsResult':
        hits: List[Dict] = data['hits']['hits']  # type: ignore
        return cls([EsResultItem.from_dict(hit) for hit in hits])


@dataclass
class EsSearcher:
    es: EsClient
    es_index: str
    query: Dict = field(default_factory=dict)

    def search(self) -> EsResult:
        res: EsResult = EsResult.from_dict(es.search(index=index, body=self.query))
        return res

    def add_query(self,
                  terms: List[str],
                  field: str,
                  condition: str = 'should') -> EsSearcher:
        """
        modify self.query
        """
        self['query'] = {
            'query': {
                'bool': {
                    condition: [
                        {'match': {field: t}}
                        for t in terms
                    ]
                }
            }
        }
        return self

    def add_size(self,
                 size: int) -> EsSearcher:
        """
        modify self.size
        """
        self.query['size'] = size
        return self

    def add_source_fields(self,
                          source_fields: List[str]) -> EsSearcher:
        """
        modify self._source
        """
        self.query['_source'] = source_fields
        return self

    def add_filter(self,
                   terms: List[str],
                   field: str,
                   condition: str = 'should') -> EsSearcher:
        """
        modify self.query
        """
        self['filter'] = {
            'query': {
                'bool': {
                    condition: [
                        {'match': {field: t}}
                        for t in terms
                    ]
                }
            }
        }
        return self
