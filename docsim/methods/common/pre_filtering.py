"""
Loader of pre-filtered texts and embeddings
"""
from pathlib import Path

import numpy as np

from docsim.settings import cache_dir


def get_emb_loader(docid: str,
                   dataset: str,
                   model: str) -> Dict[str, np.ndarray]:
    """
    Return
    -----
    A list of matrix (n_sentences * dim)
    """
    dirpath: Path = cache_dir.joinpath(f'{dataset}/{model}/{docid}')
    dic: List[np.ndarray] = {
        p.stem: np.load(str(p.resolve()))
        for p in dirpath.glob('*.npy')
    }
    return dic
