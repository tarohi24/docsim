from dataclasses import dataclass

import fasttext
import numpy as np

from docsim.embedding.base import Model, return_vector
from docsim.settings import project_root


@dataclass
class Fasttext(Model):
    model = fasttext.load_model(
        str(project_root.joinpath('models/fasttext/wiki.en.bin').resolve()))

    @return_vector
    def embed_paragraph(self, para: str) -> np.ndarray:
        return self.model.get_sentence_vector(para)

    @classmethod
    @return_vector
    def load_collection_dump(cls,
                             docid: str) -> np.ndarray:
        pass
