"""
Module for conducting an experiment
"""
from dataclasses import dataclass
import json
from typing import Dict, Generic, TypeVar

from docsim.methods.base import Method, Param
from docsim.models import QueryDataset
from docsim.settings import project_root


T_met = TypeVar('T_met', bound=Method)
T_par = TypeVar('T_par', bound=Param)


@dataclass
class Experimenter(Generic[T_met, T_par]):
    param_file: str
    dataset: QueryDataset
    runname: str
    is_fake: bool

    def load_param(self) -> T_par:
        with open(project_root.joinpath(self.param_file), 'r') as fin:
            param_dict: Dict = json.load(fin)
        param: T_par = T_par.from_dict(param_dict)
        return param

    def run(self) -> None:
        method: T_met = T_met(
            query_dataset=self.dataset,
            param=self.load_param(),
            if_fake=self.is_fake)
        method.run()
