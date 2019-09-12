from dataclasses import dataclass
from pathlib import Path

import numpy as np

from docsim.settings import project_root

ary = np.ndarray


@dataclass
class Dataset:
    name: str

    def get_data_dir(self) -> Path:
        return project_root.joinpath(f'data/{self.name}')

    def get_result_dir(self) -> Path:
        return project_root.joinpath(f'result/{self.name}')

    def __eq__(self, another):
        if isinstance(another, Dataset):
            return self.name == another.name
        else:
            return False

    def __hash__(self):
        return hash(self.name)


datasets = (
    Dataset('clef'),
    Dataset('ntcir'),
)
