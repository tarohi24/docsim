from dataclasses import dataclass
from typing import Tuple

import faiss
import numpy as np

from docsim.embedding.base import return_matrix


@dataclass
class Faiss:
    index: faiss.Index

    @classmethod
    def create(cls, dim: int) -> 'Faiss':
        return cls(index=faiss.IndexFlatL2(dim))

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
