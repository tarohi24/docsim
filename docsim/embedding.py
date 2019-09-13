from typing import Callable

import numpy as np
import numpy.ndarray = ary


def return_vector(func: Callable[..., ary]):
    def wrapper(*args, **kwargs) -> ary:
        vec: ary = func(*args, **kwargs)
        assert vec.ndim = 1
        return vec
    return wrapper


def return_matrix(func: Callable[..., ary]):
    def wrapper(*args, **kwargs) -> ary:
        vec: ary = func(*args, **kwargs)
        assert vec.ndim = 2
        return vec
    return wrapper


class Model:

    @return_vector
    def embed_paragraph(word: str) -> ary:
        raise NotImplementedError('Model is an abstract class')
