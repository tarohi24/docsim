from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd


@dataclass
class Recall:
    docid: str
    n_items: int
    score: float

    @classmethod
    def from_line(cls, line: str) -> Recall:
        try:
            n_items, docid, score = line.split()
        except ValueError:
            raise ValueError(f'Invalid format: {line}')
        return Recall(
            n_items=int(n_items.replace('recall_', '')),
            docid=docid,
            score=float(score))


def get_uniq_docids(info_list: List[Recall],
                    docids: List[str]) -> List[str]:
    """
    Given info_list, generate docids
    """
    if len(info_list) == 0:
        return docids
    head, *tails = info_list
    if len(docids) > 0:
        docid: str = head.docid
        if docid == docids[-1]:
            return get_uniq_docids(tails, docids)
        else:
            return get_uniq_docids(tails, docids + [docid])
    else:
        return get_uniq_docids(tails, [head.docid])


def to_df(path: Path) -> pd.DataFrame:
    """
    Load a recall file (.trec file which consists of recalls)
    as a pd.DataFrame
    """

    with open(path) as fin:
        info_list: List[Recall] = [Recall.from_line(line)
                                   for line in fin.read().splitlines()]
    docids: List[str] = get_uniq_docids(info_list, [])
    mat: np.ndarray = np.array([recall.score for recall in info_list]).reshape(len(docids), -1)
    return pd.DataFrame(mat,
                        index=docids,
                        columns=[r.n_items for r in info_list[:mat.shape[1]]])
