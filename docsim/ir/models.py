from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable

from docsim.elas.fields import models
from docsim.elas.models import EsItem
    

class IRDocument(EsItem):
    """
    importable both from dump and from elasticsearch
    """
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
class IRParagraph(EsItem):
    docid: models.KeywordField
    paraid: models.IntField
    text: models.TextField

    @classmethod
    def mapping(cls) -> Dict:
        return {
            'properties': {
                'docid': models.KeywordField.mapping(),
                'paraid': models.IntField.mapping(),
                'text': models.TextField.mapping(),
            }
        }

    def to_dict(self) -> Dict:
        docid_val: str = self.docid.to_elas_value()
        paraid_val: int = self.paraid.to_elas_value()
        return {
            '_id': '{}-{}'.format(docid_val, str(paraid_val)),
            'docid': docid_val,
            'paraid': paraid_val,
            'text': self.text.to_elas_value(),
        }
