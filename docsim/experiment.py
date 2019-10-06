"""
Module for conducting an experiment
"""
from dataclasses import dataclass
import json
from typing import Dict, Generic, Type, TypeVar, Tuple

# methods
from docsim.methods.keyword import KeywordBaseline, KeywordBaselineParam
from docsim.methods.norm import Norm, NormParam
from docsim.methods.paa import PAA, PAAParam
from docsim.methods.wmd import WMD, WMDParam

from docsim.methods.base import Method, Param
from docsim.models import QueryDataset
from docsim.settings import project_root

T_met = TypeVar('T_met', bound=Method)
T_par = TypeVar('T_par', bound=Param)

method_classes: Dict[str, Tuple[Type[Method], Type[Param]]] = {
    'keyword': (KeywordBaseline, KeywordBaselineParam),
    'norm': (Norm, NormParam),
    'paa': (PAA, PAAParam),
    'wmd': (WMD, WMDParam),
}


@dataclass
class Experimenter(Generic[T_met, T_par]):
    met_cls: Type[T_met]
    par_cls: Type[T_par]
    param_file: str
    dataset: QueryDataset
    runname: str
    is_fake: bool

    def load_param(self) -> T_par:
        with open(project_root.joinpath(self.param_file), 'r') as fin:
            param_dict: Dict = json.load(fin)
        param: T_par = self.par_cls.from_dict(param_dict)
        return param

    def run(self) -> None:
        method: T_met = self.met_cls(
            query_dataset=self.dataset,
            param=self.load_param(),
            is_fake=self.is_fake)
        method.run()
