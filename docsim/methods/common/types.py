from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, TypedDict, TypeVar  # type: ignore


@dataclass
class TRECResult:
    query_docid: str
    scores: Dict[str, float]

    def to_prel(self) -> str:
        return '\n'.join([f"{self.query_docid} Q0 {key} {rank} {score} STANDARD"
                          for rank, (key, score)
                          in enumerate(self.scores.items(), 1)])


class Param:

    @classmethod
    def from_args(cls, args) -> Param:
        ...


P = TypeVar('P', bound=Param)


class Context(TypedDict):
    es_index: str
    method: str
    runname: str
    n_docs: int
