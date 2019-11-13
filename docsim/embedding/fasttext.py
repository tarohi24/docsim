from dataclasses import dataclass, field

import fasttext
import numpy as np

from docsim.embedding.base import Model, return_vector
from docsim.settings import models_dir


@dataclass
class FastText(Model):
    model: fasttext.FastText._FastText = field(init=False)

    def __post_init__(self):
        self.model = fasttext.load_model(
            str(models_dir.joinpath('fasttext/cc.en.300.bin').resolve()))
        self.dim: int = 300

    @return_vector
    def embed(self, word: str) -> np.ndarray:
        return self.model.get_word_vector(word)
