from __future__ import annotations
from dataclasses import dataclass

from docsim.methods.common.types import Param
from docsim.methods.methods.fuzzy.strategy import Strategy


@dataclass
class FuzzyParam(Param):
    n_words: str
    model: str
    coef: float
    strategy: Strategy

    @classmethod
    def from_args(cls, args) -> FuzzyParam:
        param: FuzzyParam = FuzzyParam(n_words=args.n_words,
                                       model=args.model,
                                       coef=args.coef,
                                       strategy=args.strategy)
        return param
