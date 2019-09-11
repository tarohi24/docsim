from dataclasses import dataclass

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
