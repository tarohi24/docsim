from dataclasses import dataclass
import json
import requests
from typing import Any, Dict, List

import numpy as np

from docsim.embedding.base import Model, return_vector, return_matrix
from docsim.settings import nlpserver_url


@dataclass
class Bert(Model):
    dim: int = 1024
    server_url: str = nlpserver_url + '/embed_bert'

    @return_vector
    def embed(self, word: str) -> np.ndarray:
        pass

    @return_matrix
    def embed_words(self,
                    words: List[str]) -> np.ndarray:
        body: Dict[str, Any] = {'text_batch': words}
        response: requests.Response = requests.post(self.server_url, data=body)
        mat: np.ndarray = np.array(json.loads(response.text)['embeddings'])
        return mat
