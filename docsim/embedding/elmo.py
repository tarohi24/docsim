from dataclasses import dataclass, field
from typing import List

from allennlp.modules.elmo import Elmo as Ai2ElMo
from allennlp.modules.elmo import batch_to_ids
import numpy as np

from docsim.embedding.base import Model, return_vector
from docsim.settings import models_dir


@dataclass
class ElMo(Model):
    model: Ai2ElMo = field(init=False)

    def __post_init__(self):
        options_file: str = str(
            models_dir.joinpath(
                'elmo/elmo_2x4096_512_2048cnn_2xhighway_options.json').resolve())
        weight_file: str = str(
            models_dir.joinpath(
                'elmo/elmo_2x4096_512_2048cnn_2xhighway_weights.hdf5').resolve())
        self.model: Ai2ElMo = Ai2ElMo(options_file, weight_file, 2, dropout=0)
        self.dim: int = 1024

    @return_vector
    def embed(self, word: str) -> np.ndarray:
        sentences: List[List[str]] = [[word, ], ]
        character_ids = batch_to_ids(sentences)
        return self.model(character_ids)
