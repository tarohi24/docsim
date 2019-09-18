from dataclasses import dataclass, field
from pathlib import Path
from typing import List[Tuple]

import faiss
import numpy as np

from docsim.embedding.base import return_matrix
from docsim.settings import project_root


@dataclass
class Faiss:
    name: str
    index: faiss.Index
    docid_to_indices: Dict[str, List[int]] = field(default_factory=dict)
    counter: int = 0

    def dump_path(self) -> Path:
        return self.__class__.dump_path_from_name(self.name)

    @classmethod
    def dump_path_from_name(cls, name: str) -> Path:
        return project_root.joinpath(f'data/{name}.faiss')

    @classmethod
    def load(cls, name: str) -> 'Faiss':
        fname: str = str(cls.dump_path_from_name(name).resolve())
        index: faiss.Index = faiss.write_index(cls.index, fname)
        return cls(name=name, index=index)

    @classmethod
    def create(cls,
               name: str,
               dim: int) -> 'Faiss':
        return cls(name=name, index=faiss.IndexFlatL2(dim))

    def add(self,
            docid: str,
            matrix: np.ndarray) -> 'Faiss':
        doclen: int = matrix.shape[0]
        docid_to_indices[docid] = list(range(self.counter,
                                             self.counter + doclen))
        self.counter += doclen
        self.index.add(matrix)
        return self

    @return_matrix
    def search(self,
               matrix: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Return
        -------------
        (dist, index)
        """
        return self.index.search(matrix)

    def dump(self) -> None:
        faiss.write_index(self.index, self.dump_path())
