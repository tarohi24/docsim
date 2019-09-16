from dataclasses import dataclass
from more_itertools import flatten
from numbers import Real
from operator import itemgetter
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from docsim.ir.models import QueryDataset


@dataclass
class RankItem:
    """
    both a prediction result or a ground truth
    recall, precision and ap considere self as a ground truth
    """
    query_id: str
    scores: Dict[str, Real]

    def get_ranks(self) -> List[str]:
        return [docid for docid, _ in sorted(self.scores.items(),
                                             key=itemgetter(1))]


@dataclass
class TRECConverter:
    query_dataset: QueryDataset
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
