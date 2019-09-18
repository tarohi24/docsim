from dataclasses import dataclass

import fasttext
import numpy as np

from docsim.embedding.base import Model, return_vector
from docsim.settings import project_root


@dataclass
class FastText(Model):
    model: fasttext._FastText

    @classmethod
    def create(cls) -> 'FastText':
        model = fasttext.load_model(
            str(project_root.joinpath('models/fasttext/wiki.en.bin').resolve()))
        return cls(model=model)

    @return_vector
    def embed(self, word: str) -> np.ndarray:
        return self.model.get_word_vector(word)
