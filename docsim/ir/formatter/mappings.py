from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List

import numpy as np

from docsim.elas.fields import models


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
