from dataclasses import dataclass
import json
from pathlib import Path

from dataclasses_jsonschema import JsonSchemaMixin

from docsim.dataset import Dataset


@dataclass
class DocumentID:
    dataset: Dataset
    docid: str

    def __eq__(self, another):
        if isinstance(another, DocumentID):
            return (self.dataset == another.dataset)\
                and (self.docid == another.docid)
        else:
            return False

    def __hash__(self):
        return hash(tuple(self.dataset, self.docid))

    def __str__(self):
        return f'{dataset}_{docid}'


@dataclass
class Document(JsonSchemaMixin):
    docid: DocumentID
    body: str


@dataclass
class EmbeddedDocument(Document, JsonSchemaMixin):
    mat: ary
    model: str

    def normalize(self) -> ary:
        norm: float =  np.linalg.norm(self.mat, axis=1)
        return (mat.T / norm).T


@dataclass
class EmbeddedDocumentList(JsonSchemaMixin):
    docs: List[EmbeddedDocument]

    @classmethod
    def get_filepath(cls,
                     dataset,
                     doctype: str = 'qeury') -> Path:
        cachedir: Path = dataset.get_cachedir()
        return cachedir.joinpath(f'{doctype}.json')

    @classmethod
    def load_cache(cls,
                   dataset: Dataset,
                   doctype: str = 'query') -> EmbeddedDocumentList:
        fpaht: Path = cls.get_filepath(dataset=dataset, doctype=doctype)
        with open(fpath, 'r') as fin:
            dic: Dict = json.load(fin)
        return EmbeddedDocumentList.from_dict(dic)

    def dump(self,
             dataset: Dataset,
             doctype: str) -> None:
        fpaht: Path = cls.get_filepath(dataset=dataset, doctype=doctype)
        with open(fpath, 'w') as fin:
            dic: Dict = json.dump(self.to_dict(), fin)
