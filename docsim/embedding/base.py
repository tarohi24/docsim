from dataclasses import dataclass
from typing import Callable

import numpy as np


def return_vector(func: Callable[..., np.ndarray]):
    def wrapper(*args, **kwargs) -> np.ndarray:
        vec: np.ndarray = func(*args, **kwargs)
        assert vec.ndim == 1
        return vec
    return wrapper


def return_matrix(func: Callable[..., np.ndarray]):
    def wrapper(*args, **kwargs) -> np.ndarray:
        vec: np.ndarray = func(*args, **kwargs)
        assert vec.ndim == 2
        return vec
    return wrapper


@return_matrix
def mat_normalize(mat: np.ndarray) -> np.ndarray:
    assert len(mat.shape) == 2
    norm = np.linalg.norm(mat, axis=1)
    return (mat.T / norm).T


@dataclass
class Model:
    dim: int

    @return_vector
    def embed_paragraph(cls, para: str) -> np.ndarray:
        raise NotImplementedError('Model is an abstract class')
