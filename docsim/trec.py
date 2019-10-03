from dataclasses import dataclass
import math
from numbers import Real
from operator import itemgetter
from pathlib import Path
from typing import Dict, List, Tuple

from docsim.settings import results_dir


@dataclass
class TRECConverter:
    dataset_name: str
    method_name: str

    def get_fpath(self) -> Path:
        return results_dir.joinpath(f'ir/{self.dataset_name}/{self.method_name}.prel')

    def format_item(self,
                    query_id: str,
                    scores: Dict[str, Real]) -> List[Tuple[str, ...]]:
        return [
            (str(query_id), 'Q0', docid, str(rank + 1), str(math.floor(score)), self.method_name)
            for rank, (docid, score)
            in enumerate(sorted(scores.items(), key=itemgetter(1), reverse=True))
        ]

    def incremental_dump(self,
                         query_id: str,
                         scores: Dict[str, Real]) -> None:
        records: List[Tuple[str, ...]] = self.format_item(query_id, scores)
        with open(self.get_fpath(), 'a') as fout:
            fout.write('\n'.join([' '.join(rec) for rec in records]))
            fout.write('\n')
