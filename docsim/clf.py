"""
Module for classification
"""
from dataclasses import dataclass
from typing import List

import numpy as np


@dataclass
class Evaluator:
    """
    Abstract method
    """
    pred_list: List[List[str]]
    gt_list: List[List[str]]

    def eval(self) -> float:
        raise NotImplementedError('This is an abstract method')

    def __iter__(self):
        return iter(zip(self.pred_list, self.gt_list))


@dataclass
class AccuracyEvaluator(Evaluator):
    n_top: int

    def eval(self) -> float:
        lst: List[bool] = [len(set(pred[:self.n_top]) & set(gt)) > 0 for pred, gt in self]
        return np.mean([1.0 if acc else 0.0 for acc in lst])
