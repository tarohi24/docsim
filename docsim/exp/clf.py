"""
Module for classification
"""
from __future__ import annotations  # noqa
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
        return self.__class__.get_fpath_from(dataset_name=self.dataset_name,
                                             method_name=self.method_name)

    @classmethod
    def get_fpath_from(cls,
                       dataset_name: str,
                       method_name: str) -> Path:
        return results_dir.joinpath(f'clf/{dataset_name}/{method_name}.json')

    @classmethod
    def load(cls,
             dataset_name: str,
             method_name: str) -> ClfResult:
        with open(cls.get_fpath_from(dataset_name, method_name)) as fin:
            dic: Dict = json.load(fin)
        return cls.from_dict(dic)

    def dump(self) -> None:
        with open(self.get_fpath(), 'w') as fout:
            json.dump(self.to_dict(), fout)


@dataclass
class Evaluator:
    """
    Abstract method
    """
    def eval(self,
             pred: ClfResult,
             gt: ClfResult) -> float:
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

    def eval(self,
             pred: ClfResult,
             gt: ClfResult) -> float:
        keys: Set[str] = set(pred.result.keys()) & set(gt.result.keys())
        lst: List[bool] = [
            len(set(pred.result[key][:self.n_top]) & set(gt.result[key][:self.n_top])) > 0
            for key in keys]
        return np.mean([1.0 if acc else 0.0 for acc in lst])

    def __repr__(self) -> str:
        return f'acc@{self.n_top}'
