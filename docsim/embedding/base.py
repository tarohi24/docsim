from dataclasses import dataclass, field
from typing import Callable, List

import numpy as np


class InvalidShape(Exception):
    pass


def return_vector(func: Callable[..., np.ndarray]):
    def wrapper(*args, **kwargs) -> np.ndarray:
        vec: np.ndarray = func(*args, **kwargs)
        if vec.ndim != 1:
            raise InvalidShape()
        return vec
    return wrapper


def return_matrix(func: Callable[..., np.ndarray]):
    def wrapper(*args, **kwargs) -> np.ndarray:
        vec: np.ndarray = func(*args, **kwargs)
        if vec.ndim != 2:
            raise InvalidShape()
        return vec
    return wrapper


@return_matrix
def mat_normalize(mat: np.ndarray) -> np.ndarray:
    assert len(mat.shape) == 2
    norm = np.linalg.norm(mat, axis=1)
    mat: np.ndarray = (mat.T / norm).T
    return mat


@dataclass
class Model:
    """
    The basic class for all embedding models.
    """
    dim: int = field(init=False)

    @return_vector
    def embed(self, word: str) -> np.ndarray:
        raise NotImplementedError('Model is an abstract class')

    @return_matrix
    def embed_words(self,
                    words: List[str]) -> np.ndarray:
        raise NotImplementedError('Model is an abstract class')
