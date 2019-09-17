from dataclasses import dataclass
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
                                             key=itemgetter(1))]


@dataclass
class TRECConverter:
    method_name: str
    is_ground_truth: bool = False

    def get_fpath(self) -> Path:
        ext: str = 'qrel' if self.is_ground_truth else 'prel'
        return project_root.joinpath(f'results/ir/{self.method_name}.{ext}')

    def format_item(self,
                    item: RankItem) -> List[Tuple[str, ...]]:

        return [
            (str(item.query_id), docid, str(score), self.method_name)
            for docid, score
            in sorted(item.scores.items(), key=itemgetter(1), reverse=True)
        ]

    def incremental_dump(self,
                         item: RankItem) -> None:
        records: List[Tuple[str, ...]] = self.format_item(item)
        with open(self.get_fpath(), 'a') as fout:
            fout.write('\n'.join(['\t'.join(rec) for rec in records]))
            fout.write('\n')
