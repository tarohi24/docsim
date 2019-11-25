from dataclasses import dataclass, field
from typing import Dict, List

import fasttext
import numpy as np
from tqdm import tqdm

from docsim.embedding.base import Model, return_matrix, return_vector
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

    @return_matrix
    def embed_words(self,
                    words: List[str]) -> np.ndarray:
        emb_caches: Dict[str, np.ndarray] = dict()
        for w in tqdm(words, desc='embedding words...', leave=True):
            if w not in emb_caches:
                emb_caches[w] = self.embed(w)
        return np.array([emb_caches[w] for w in words])
