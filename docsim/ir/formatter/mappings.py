from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable

from docsim.elas.fields import models
from docsim.elas.models import EsItem


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
    docid: models.KeywordField  # unique key
    paraid: models.IntField
    title: models.TextField
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
