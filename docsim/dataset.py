from abc import ABCMeta, abstractmethod

import numpy as np
ary = np.ndarray


@dataclass
class Document(ABCMeta):
    docid: str
    body: str


@dataclass
class EmbeddedQuery(Document):
    mat: ary
    model: str
    

    def normalize(self) -> ary:
        norm: float =  np.linalg.norm(self.mat, axis=1)
        return (mat.T / norm).T

    


@dataclass
class QueryDocument:
    body: str
    
    
    

class QueryDataset(ABCMeta):
    """
    pass
    """
    
    


class CLEFDataset
