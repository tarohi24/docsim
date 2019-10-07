"""
Module for classification
"""
from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Dict, List, Set

from dataclasses_jsonschema import JsonSchemaMixin
import numpy as np

from docsim.settings import results_dir


@dataclass
class ClfResult(JsonSchemaMixin):
    dataset_name: str
    method_name: str
    result: Dict[str, List[str]] = field(default_factory=dict)

    def get_fpath(self) -> Path:
        return results_dir.joinpath(f'clf/{self.dataset_name}/{self.method_name}.json')

    def dump(self) -> None:
        with open(self.get_fpath(), 'w') as fout:
            json.dump(self.to_dict(), fout)

@dataclass
class Evaluator:
    """
    Abstract method
    """

    @classmethod
    @property
    def name(cls) -> str:
        raise NotImplementedError('This is an abstract method')

    def eval(self,
             result: ClfResult,
             gt_list: Dict[str, List[str]]) -> float:
        raise NotImplementedError('This is an abstract method')

    def __iter__(self):
        """
        Keeping order of the iteration is not necessary,
        but it makes easier to debug.
        """
        keys: List[str] = sorted(list(self.result.result.keys()))
        # perhaps it causes KeyError (although it shouldn't)
        return iter([self.gt_list[docid] for docid in keys])


@dataclass
class AccuracyEvaluator(Evaluator):
    n_top: int

    @classmethod
    @property
    def name(cls) -> str:
        return 'acc'

    def eval(self,
             pred: ClfResult,
             gt_list: Dict[str, List[str]]) -> float:
        keys: Set[str] = set(pred.result.keys()) & set(gt_list.keys())
        lst: List[bool] = [
            len(set(pred.result[key][:self.n_top]) & set(gt_list[key][:self.n_top])) > 0
            for key in keys]
        return np.mean([1.0 if acc else 0.0 for acc in lst])
