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


class Model:

    @return_vector
    def embed_paragraph(cls, para: str) -> np.ndarray:
        raise NotImplementedError('Model is an abstract class')
