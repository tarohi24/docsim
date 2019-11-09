from __future__ import annotations  # noqa
from dataclasses import dataclass
import json
from operator import itemgetter
from pathlib import Path
from typing import Dict, List, Tuple

from dataclasses_json import dataclass_json

from docsim.elas import models
from docsim.settings import data_dir
from docsim.utils.utils import uniq


@dataclass
class RankItem:
    """
    both a prediction result or a ground truth
    recall, precision and ap considere self as a ground truth
    """
    query_id: str
    scores: Dict[Tuple[str, str], float]  # (docid, tag) -> score

    def get_doc_scores(self) -> Dict[str, float]:
        return {key[0]: score for key, score in self.scores.items()}

    def get_tag_scores(self) -> Dict[str, float]:
        return {key[1]: score for key, score in self.scores.items()}

    def pred_tags(self,
                  n_top: int) -> List[str]:
        sorted_score: List[str] = [
            tag for tag, _ in sorted(self.get_tag_scores().items(),
                                     key=itemgetter(1),
                                     reverse=True)]
        unique_tags: List[str] = uniq(orig=sorted_score, n_top=n_top)
        return unique_tags

    def __len__(self) -> int:
        return len(self.scores)


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

    def to_json(self) -> str:
        dic: Dict = self.to_dict()
        return json.dumps(dic)

    @classmethod
    def _create_doc_from_values(cls,
                                docid: str,
                                title: str,
                                text: str,
                                tags: List[str]) -> ColDocument:
        """
        for testing
        """
        return ColDocument(
            docid=models.KeywordField(docid),
            title=models.TextField(title),
            text=models.TextField(text),
            tags=models.KeywordListField(tags))

    @classmethod
    def from_json(cls,
                  jsonstr: str) -> ColDocument:
        dic: Dict = json.loads(jsonstr)
        docid: str = dic['docid']
        title: str = dic['title']
        text: str = dic['text']
        tags: List[str] = dic['tags']
        return cls._create_doc_from_values(
            docid=docid,
            title=title,
            text=text,
            tags=tags)
