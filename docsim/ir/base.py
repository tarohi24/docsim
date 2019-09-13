"""
Base class definition
"""
from dataclasses import dataclass
import logging
import traceback

from docsim.doc_models import Docuemnt
from docsim.rank import RankItem, TRECConverter


logger = logging.getLogger(__file__)
T = TypeVar('T')


def ignore_exception(func: Callable[..., T]) -> Optional[T]:
    def wrapper(*args, **kwargs):
        try:
            val: T = func(*args, **kwargs)
            return val
        except Exception as e:
            logger.error(e, exc_info=True)
            return


@dataclass
class Searcher:
    dataset: Dataset
    queries: List[Document]
    runname: str

    @ignore_exception
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
