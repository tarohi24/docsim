from dataclasses import dataclass
from numbers import Real

import numpy as np
import numpy.ndarray as ary


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
class TagsField(Field):
    tags: List[str]

    @classmethod
    def mapping(cls) -> Dict:
        return {
            'type': 'keyword'
        }

    def to_elas_value(self) -> List[str]:
        return self.tags


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

    def to_elas_value(self) -> List[float]:
        return self.vec.tolist()


@dataclass
class IRBase(EsItem):
    """
    Attributes
    ------------
    text
        body
    tags
        used for pre-filtering
    """
    docid: KeywordField  # unique key
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

    def to_dict(self) -> Dict:
        return {
            '_id': self.docid.to_elas_value(),
            'docid': self.docid.to_elas_value(),
            'title': self.title.to_elas_value(),
            'text': self.text.to_elas_value(),
            'tags': self.tags.to_elas_value(),
        }


class Converter:
    """
    convert something into IRBase
    """
    def to_irbase(self) -> IRBase:
        raise NotImplementedError('This is an abstract class.')
