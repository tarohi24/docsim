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
class KeywordField(Mapping):
    keyword: str

    @classmethod
    def mapping(cls) -> Dict:
        return {
            'type': 'keyword',
        }

@dataclass
class TagsField(Mapping):
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
class IRBase:
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
