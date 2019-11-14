from dataclasses import dataclass
import json
import requests
from typing import Any, Dict

import numpy as np

from docsim.embedding.base import Model, return_vector
from docsim.settings import nlpserver_url


@dataclass
class Elmo(Model):
    dim: int = 1024
    server_url: str = str(nlpserver_url.joinpath('embed_elmo').resolve())

    @return_vector
    def embed(self, word: str) -> np.ndarray:
        body: Dict[str, Any] = {'text': word}
        response: requests.Response = requests.post(self.server_url, data=body)
        vec: np.ndarray = np.array(json.loads(response.text)['embeddings'])[0]
        return vec
