from __future__ import annotations
from collections import Counter
from dataclasses import dataclass, field
from enum import Enum
import re
from typing import ClassVar, List, Pattern, Set, Type  # type: ignore

from nltk.corpus import stopwords as nltk_sw
from nltk.tokenize import RegexpTokenizer
from typedflow.flow import Flow
from typedflow.tasks import Task
from typedflow.nodes import TaskNode

from docsim.elas.search import EsResult, EsSearcher
from docsim.models import ColDocument
from docsim.methods.common.methods import Method
from docsim.methods.common.types import Param, TRECResult, P
from docsim.methods.methods.keywords import KeywordBaseline, KeywordParam


class STRATEGY(Enum):
    PERSSIMISTIC = 1
    OPTIMISTIC = 2


@dataclass
class PerParam(Param):
    n_words: int
    strategy: STRATEGY

    @classmethod
    def from_args(cls, args) -> PerParam:
        return PerParam(n_words=args.n_words,
                        strategy=STRATEGY[args.strategy])


@dataclass
class Per(Method[PerParam]):
    param_type: ClassVar[Type[P]] = PerParam
    kb: KeywordBaseline = field(init=False)

    def __post_init__(self):
        self.kb: KeywordBaseline = KeywordBaseline(
            mprop=self.mprop,
            param=KeywordParam(n_words=self.param.n_words))

    def reorder(self,
                doc: ColDocument):
        
