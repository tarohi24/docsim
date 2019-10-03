from __future__ import annotations  # noqa
from dataclasses import dataclass
import json
from numbers import Real
from operator import itemgetter
from pathlib import Path
from typing import Dict, List, Tuple

from dataclasses_jsonschema import JsonSchemaMixin

from docsim.elas import models
from docsim.settings import data_dir, results_dir
from docsim.utils import uniq


@dataclass
class RankItem:
    """
    both a prediction result or a ground truth
    recall, precision and ap considere self as a ground truth
    """
    query_id: str
    scores: Dict[Tuple[str, str], Real]  # (docid, tag) -> score

    def get_doc_scores(self) -> Dict[str, Real]:
        return {key[0]: score for key, score in self.scores.items()}

    def get_tag_scores(self) -> Dict[str, Real]:
        return {key[1]: score for key, score in self.scores.items()}

    def pred_tag(self,
                 n_top: int) -> List[str]:
        sorted_score: List[str] = [
            tag for tag, _ in sorted(self.get_tag_scores().items(),
                                     key=itemgetter(1),
                                     reverse=True)]
        unique_tags: List[str] = uniq(orig=sorted_score, n_top=n_top)
        return unique_tags


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
        return data_dir.joinpath(f'{name}/query/dump.json')

    @classmethod
    def load_dump(cls, name: str) -> 'QueryDocument':
        with open(cls._get_dump_path(name=name), 'r') as fin:
            dic: Dict = json.load(fin)
        return cls.from_dict(dic)

    def get_result_dir(self) -> Path:
        return results_dir.joinpath(f'{self.name}')

    def __len__(self):
        return len(self.queries)


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

    @classmethod
    def _create_doc_from_values(cls,
                                docid: str,
                                title: str,
                                text: str,
                                tags: List[str]) -> 'ColDocument':
        """
        for testing
        """
        return ColDocument(
            docid=models.KeywordField(docid),
            title=models.TextField(title),
            text=models.TextField(text),
            tags=models.KeywordListField(tags))


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
