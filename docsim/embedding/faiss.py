from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import faiss
import numpy as np

from docsim.embedding.base import return_matrix
from docsim.settings import project_root


@dataclass
class Faiss:
    name: str
    index: faiss.Index

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
            matrix: np.ndarray) -> 'Faiss':
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
