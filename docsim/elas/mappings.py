from dataclasses import dataclass
from numbers import Real

import numpy as np
import numpy.ndarray as ary


class Mapping:
    @classmethod
    def mapping(cls) -> Dict:
        raise NotImplementedError('This is an abstract class.')


@dataclass
class TextField(Mapping):
    text: str

    @classmethod
    def mapping(cls) -> Dict:
        return {
            'type': 'text',
            'analyzer': 'english'
        }

@dataclass
class TagField(Mapping):
    tags: List[str]

    @classmethod
    def mapping(cls) -> Dict:
        return {
            'type': 'keyword'
        }


@dataclass
class VectorField(Mapping):
    """
    yet supported
    """
    vec: ary

    @classmethod
    def mapping(cls) -> Dict:
        return {
            'type': 'dense_vector'
        }
    

@dataclass
class BaseMapping(JsonSchemaMixin):
    """
    Attributes
    ------------
    text
        body
    tags
        used for pre-filtering
    """
    text: TextField
    tags: List[str]
    embedding: List[Real]

    def to_mapping(cls) -> Dict:
        schema: Dict = cls.json_schema()
        return ToMappingConverter().convert(schema)
