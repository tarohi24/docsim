from dataclasses import dataclass
from numbers import Real

import numpy as np
import numpy.ndarray as ary


class Field:
    @classmethod
    def mapping(cls) -> Dict:
        raise NotImplementedError('This is an abstract class.')

class Mapping:
    @classmethod
    def mapping(cls) -> Dict:
        raise NotImplementedError('This is an abstract class.')


@dataclass
class TextField(Field):
    text: str

    @classmethod
    def mapping(cls) -> Dict:
        return {
            'type': 'text',
            'analyzer': 'english'
        }


@dataclass
class KeywordField(Field):
    keyword: str

    @classmethod
    def mapping(cls) -> Dict:
        return {
            'type': 'keyword',
        }

@dataclass
class TagsField(Field):
    tags: List[str]

    @classmethod
    def mapping(cls) -> Dict:
        return {
            'type': 'keyword'
        }


@dataclass
class VectorField(Field):
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
class IRBase(Mapping):
    """
    Attributes
    ------------
    text
        body
    tags
        used for pre-filtering
    """
    docid: KeywordField
    title: TextField
    text: TextField
    tags: TagsField
    
    @classmethod
    def mapping(cls) -> Dict:
        return {
            'properties': {
                'docid': KeywordField.mapping(),
                'title': TextField.mapping(),
                'text': TextField.mapping(),
                'tags': TagsField.mapping(),
            }
        }


class Converter:
    """
    convert something into IRBase
    """
    def to_irbase(self) -> IRBase:
        raise NotImplementedError('This is an abstract class.')
