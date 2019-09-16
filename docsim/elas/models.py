from dataclasses import dataclass
from typing import Any, Dict, List

import numpy as np


class Field:
    @classmethod
    def mapping(cls) -> Dict:
        raise NotImplementedError('This is an abstract class.')

    def to_elas_value(self) -> Any:
        raise NotImplementedError('This is an abstract class.')


class EsItem:
    """
    Elasticsearch mapping
    """
    unique_key_field: Field

    @classmethod
    def mapping(cls) -> Dict:
        raise NotImplementedError('This is an abstract class.')

    def to_dict(self) -> Dict:
        raise NotImplementedError('This is an abstract class.')


@dataclass
class IntField(Field):
    value: int

    @classmethod
    def mapping(cls) -> Dict:
        return {
            'type': 'integer',
        }

    def to_elas_value(self) -> int:
        return self.value


@dataclass
class TextField(Field):
    text: str

    @classmethod
    def mapping(cls) -> Dict:
        return {
            'type': 'text',
            'analyzer': 'english'
        }

    def to_elas_value(self) -> str:
        return self.text


@dataclass
class KeywordField(Field):
    keyword: str

    @classmethod
    def mapping(cls) -> Dict:
        return {
            'type': 'keyword',
        }

    def to_elas_value(self) -> str:
        return self.keyword


@dataclass
class KeywordListField(Field):
    keywords: List[str]

    @classmethod
    def mapping(cls) -> Dict:
        return {
            'type': 'keyword'
        }

    def to_elas_value(self) -> List[str]:
        return self.keywords


@dataclass
class FasttextVectorField(Field):
    vec: np.ndarray

    @classmethod
    def mapping(cls) -> Dict:
        return {
            'type': 'dense_vector',
            'dim': 300
        }

    def to_elas_value(self) -> List[float]:
        return self.vec.tolist()
