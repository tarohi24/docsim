from dataclasses import dataclass

import numpy as np


ary = np.ndarray


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


@dataclass
class Document:
    docid: DocumentID
    body: str



@dataclass
class EmbeddedDocument(Document):
    mat: ary
    model: str

    def normalize(self) -> ary:
        norm: float =  np.linalg.norm(self.mat, axis=1)
        return (mat.T / norm).T


@dataclass
class Dataset:
    name: str

    def __eq__(self, another):
        if isinstance(another, Dataset):
            return self.name == another.name
        else:
            return False

    def __hash__(self):
        return hash(self.name)
