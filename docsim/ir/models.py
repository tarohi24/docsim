from __future__ import annotations  # noqa
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Dict, Iterable, List

from dataclasses_jsonschema import JsonSchemaMixin

from docsim.elas import models
from docsim.ir.converters.base import Converter
from docsim.settings import project_root


@dataclass
class QueryDocument(JsonSchemaMixin):
    docid: str
    paras: List[str]
    tags: List[str]

    @property
    def text(self) -> str:
        return ' '.join(self.paras)


@dataclass
class QueryDataset(JsonSchemaMixin):
    name: str
    queries: List[QueryDocument]

    @classmethod
    def _get_dump_path(cls, name: str) -> Path:
        return project_root.joinpath(f'data/{name}/query/dump.json')

    @classmethod
    def load_dump(cls, name: str) -> 'QueryDocument':
        with open(cls._get_dump_path(name=name), 'r') as fin:
            dic: Dict = json.load(fin)
        return cls.from_dict(dic)

    def get_result_dir(self) -> Path:
        return project_root.joinpath(f'results/{self.name}')

    @classmethod
    def create_dump(cls,
                    name: str,
                    converter: Converter,
                    xml_pathes: Iterable[Path]) -> 'QueryDocument':
        qlist: List[QueryDocument] = sum(
            [converter.to_query_dump(fpath) for fpath in xml_pathes],
            []
        )
        dic: Dict = cls(name=name, queries=qlist).to_dict()
        with open(cls._get_dump_path(name=name), 'w') as fout:
            json.dump(dic, fout)


@dataclass
class ColDocument(models.EsItem):
    docid: models.KeywordField  # unique key
    title: models.TextField
    text: models.TextField
    tags: models.KeywordListField

    @classmethod
    def mapping(cls) -> Dict:
        return {
            'properties': {
                'docid': models.KeywordField.mapping(),
                'title': models.TextField.mapping(),
                'text': models.TextField.mapping(),
                'tags': models.KeywordListField.mapping(),
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


@dataclass
class ColParagraph(models.EsItem):
    docid: models.KeywordField
    paraid: models.IntField
    text: models.TextField
    tags: models.KeywordListField

    @classmethod
    def mapping(cls) -> Dict:
        return {
            'properties': {
                'docid': models.KeywordField.mapping(),
                'paraid': models.IntField.mapping(),
                'title': models.TextField.mapping(),
                'text': models.TextField.mapping(),
                'tags': models.KeywordListField.mapping(),
            }
        }

    def to_dict(self) -> Dict:
        pid: int = self.paraid.to_elas_value()
        did: str = self.docid.to_elas_value()
        return {
            '_id': '{}-{}'.format(did, str(pid)),
            'docid': did,
            'paraid': pid,
            'title': self.title.to_elas_value(),
            'text': self.text.to_elas_value(),
            'tags': self.tags.to_elas_value(),
        }
