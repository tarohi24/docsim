import numpy as np

ary = np.ndarray


@dataclass
class Dataset:
    name: str

    def __eq__(self, another):
        if isinstance(another, Dataset):
            return self.name == another.name
        else:
            return False

    def __hash__(self):
        return hash(self.name)


datasets = {
    Dataset('clef'),
    Dataset('ntcir'),
)
