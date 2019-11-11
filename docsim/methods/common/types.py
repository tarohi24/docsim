from dataclasses import dataclass
from typing import Dict, TypedDict  # type: ignore


@dataclass
class TRECResult:
    query_docid: str
    scores: Dict[str, float]

    def to_prel(self) -> str:
        return '\n'.join([f"{self.query_docid} 0 {key} {score}"
                          for key, score in self.scores.items()])


class Param:
    pass


class Context(TypedDict):
    es_index: str
    method: str
    runname: str
    n_docs: int
