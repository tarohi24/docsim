"""
Module for elasticsaerch
"""
from dataclasses import dataclass
from numbers import Real
from typing import Dict, Type

from dataclasses_jsonschema import JsonSchemaMixin


T_JsonSchemaMixin = TypeVar('T', bound='JsonSchemaMixin')


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
class EsResult():
    hits: List[EsResultItem]

    @classmethod
    def from_dict(cls,
                  data: Dict) -> cls:
        hits: List[Dict] = data['hits']['hits']  # type: ignore
        return [EsResultItem.from_dict(hit) for hit in hits]
