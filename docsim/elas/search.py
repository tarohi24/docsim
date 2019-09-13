"""
Module for elasticsaerch
"""
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
    index: str
    size: int
    source_field: List[str]

    def search(self, keywords: List[str]) -> EsResult:
        body = {
            'query': {
                'bool': {
                    'should': [
                        {'match': {'documentId.keyword': ucid}}
                        for ucid in doc_ids
                    ]
                }
            },
            'size': len(doc_ids),
            '_source': ['documentId', 'description', ]
        }
        res: EsResult = EsResult.from_dict(es.search(index=index, body=body))
        return res