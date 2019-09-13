from dataclasses import dataclass
from typing import Any, Dict, List

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
    paraid: IntField
    title: TextField
    text: TextField
    tags: KeywordListField

    @classmethod
    def mapping(cls) -> Dict:
        return {
            'properties': {
                'docid': KeywordField.mapping(),
                'paraid': IntField.mapping(),
                'title': TextField.mapping(),
                'text': TextField.mapping(),
                'tags': KeywordListField.mapping(),
            }
        }

    def to_dict(self) -> Dict:
        docid_val: str = self.docid.to_elas_value()
        paraid_val: int = self.paraid.to_elas_value()
        return {
            '_id': '{}-{}'.format(docid_val, str(paraid_val)),
            'docid': docid_val,
            'paraid': paraid_val,
            'title': self.title.to_elas_value(),
            'text': self.text.to_elas_value(),
            'tags': self.tags.to_elas_value(),
        }


class Converter:
    """
    convert something into IRBase
    """
    def to_irbase(self, fpath: Path) -> Iterable[IRBase]:
        raise NotImplementedError('This is an abstract class.')
