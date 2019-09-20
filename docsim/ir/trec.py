from dataclasses import dataclass
import math
from numbers import Real
from operator import itemgetter
from pathlib import Path
from typing import Dict, List, Tuple

from docsim.settings import project_root


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
                                             key=itemgetter(1),
                                             reverse=True)]


@dataclass
class TRECConverter:
    dataset_name: str
    method_name: str

    def get_fpath(self) -> Path:
        return project_root.joinpath(f'results/ir/{self.dataset_name}/{self.method_name}.prel')

    def format_item(self,
                    item: RankItem) -> List[Tuple[str, ...]]:
        return [
            (str(item.query_id), 'Q0', docid, str(rank + 1), str(math.floor(score)), self.method_name)
            for rank, (docid, score)
            in enumerate(sorted(item.scores.items(), key=itemgetter(1), reverse=True))
        ]

    def incremental_dump(self,
                         item: RankItem) -> None:
        records: List[Tuple[str, ...]] = self.format_item(item)
        with open(self.get_fpath(), 'a') as fout:
            fout.write('\n'.join([' '.join(rec) for rec in records]))
            fout.write('\n')
