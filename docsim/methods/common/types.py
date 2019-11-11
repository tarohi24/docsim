from typing import TypedDict  # type: ignore


class BaseParam(TypedDict):
    es_index: str
    method: str
    runname: str
    n_docs: int
