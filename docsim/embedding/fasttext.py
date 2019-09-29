from dataclasses import dataclass

import fasttext
import numpy as np

from docsim.embedding.base import Model, return_vector
from docsim.settings import models_dir


@dataclass
class FastText(Model):
    model: fasttext.FastText._FastText

    @classmethod
    def create(cls) -> 'FastText':
        model = fasttext.load_model(
            str(models_dir.joinpath('fasttext/wiki.en.bin').resolve()))
        return cls(dim=300, model=model)  # noqa

    @return_vector
    def embed(self, word: str) -> np.ndarray:
        return self.model.get_word_vector(word)
