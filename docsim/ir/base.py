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


@dataclass
class RankItem:
    """
    both a prediction result or a ground truth
    recall, precision and ap considere self as a ground truth
    """
    query_id: DocumentID
    scores: Dict[DocumentID, Real]

    def get_ranks(self) -> List[DocumentID]:
        return [docid for docid, _ in sorted(self.scores.items(),
                                             key=itemgetter(1))]


@dataclass
class TRECConverter:
    dataset: Dataset
    runname: str
    is_ground_truth: bool = False

    def get_fpath(self) -> Path:
        ext: str = 'qrel' if self.is_ground_truth else 'prel'
        return self.dataset.get_result_dir().joinpath(f'{self.runname}.{ext}')

    def format(self,
               items: Iterable[RankItem]) -> List[Tuple[str, ...]]:
        """
        Convert items to TREC-eval input format
        """
        return list(
            flatten([
                [
                    (str(item.query_id), docid, str(score), self.runname)
                    for docid, score
                    in sorted(item.scores.items(), key=itemgetter(1), reverse=True)
                ]
                for item in items
            ])
        )

    def dump(self,
             items: Iterable[RankItem],
             ignore_existence: bool = False) -> None:
        records: List[Tuple[str, ...]] = self.format(items)
        fpath: Path = self.get_fpath()
        if not ignore_existence:
            if fpath.exists():
                raise AssertionError(f'File exists. {fpath}')
        with open(self.get_fpath(), 'w') as fout:
            fout.write('\n'.join(['\t'.join(rec) for rec in records]))
