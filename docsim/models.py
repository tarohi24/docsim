from __future__ import annotations
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Dict, Generator, List

from dataclasses_jsonschema import JsonSchemaMixin
import numpy as np

from docsim.elas.clef import CLEFConverter
from docsim.elas.mappings import Converter
from docsim.embedding.base import Model, return_matrix
from docsim.settings import project_root


@dataclass
class Dataset:
    name: str
    converter: Converter
    es_index: str

    def list_original_files(self) -> Generator[Path, None, None]:
        return self.get_data_dir().glob('orig/**/*.xml')

    def get_data_dir(self) -> Path:
        return project_root.joinpath(f'data/{self.name}')

    def get_result_dir(self) -> Path:
        return project_root.joinpath(f'result/{self.name}')

    def __eq__(self, another):
        if isinstance(another, Dataset):
            return self.name == another.name
        else:
            return False

    def __hash__(self):
        return hash(self.name)


dataset_dict: Dict[str, Dataset] = {
    'clef': Dataset(
        name='clef',
        converter=CLEFConverter(),
        es_index='clef'),
}


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
        return f'{self.dataset}_{self.docid}'
@dataclass
class Document(JsonSchemaMixin):
    docid: DocumentID
    body: str


@dataclass
class EmbeddedDocument(Document, JsonSchemaMixin):
    mat: np.ndarray
    model: Model

    @return_matrix
    def normalize(self) -> np.ndarray:
        norm: float = np.linalg.norm(self.mat, axis=1)
        return (self.mat.T / norm).T


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
        fpath: Path = cls.get_filepath(dataset=dataset, doctype=doctype)
        with open(fpath, 'r') as fin:
            dic: Dict = json.load(fin)
        return cls.from_dict(dic)

    def dump(self,
             dataset: Dataset,
             doctype: str) -> None:
        fpath: Path = self.__cls__.get_filepath(dataset=dataset, doctype=doctype)
        with open(fpath, 'w') as fin:
            json.dump(self.to_dict(), fin)
