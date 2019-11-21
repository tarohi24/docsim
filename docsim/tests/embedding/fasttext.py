from dataclasses import dataclass

import numpy as np


@dataclass
class FTMock:
    dim: int = 300

    def embed(self, word: str) -> np.ndarray:
        return np.random.rand(self.dim)
