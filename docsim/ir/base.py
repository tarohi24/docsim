"""
Base class definition
"""
from dataclasses import dataclass
import logging
from numbers import Real
from operator import itemgetter
from pathlib import Path
import traceback
from typing import Dict, Iterable, List, Tuple

from docsim.dataset import Dataset
from docsim.doc_models import Docuemnt, DocumentID


logger = logging.getLogger(__file__)
T = TypeVar('T')


def ignore_exception(func: Callable[..., T],
                     exceptions: Tuple[Type[Exception]]) -> Optional[T]:
    """
    Decorator
    """
    def wrapper(*args, **kwargs):
        try:
            val: T = func(*args, **kwargs)
            return val
        except exceptions as e:
            logger.error(e, exc_info=True)
            return
    return wrapper


@dataclass
class Searcher:
    dataset: Dataset
    queries: List[Document]
    runname: str

    def retrieve(self, query: Document) -> RankItem:
        raise NotImplementedError('This is an abstract class.')

    def run(self) -> None:
        items: List[RankItem] = [res
                                 for res
                                 in [retrieve(query) for query in self.queries]
                                 if res is not None]
        trec: TRECConverter = TRECConverter(
            items=items,
            dataset=self.dataset,
            runname=self.runname,
            is_ground_truth=False)
        trec.dump()
