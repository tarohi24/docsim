from dataclasses import dataclass
from numbers import Real
from operator import itemgetter
from typing import Dict, List, Iterable

from dataclasses_jsonschema import JsonSchemaMixin
from more_itertools import flatten

from docsim.dataset import Dataset
from docsim.doc_model import DocumentID


@dataclass
class RankItem:
    """
    both a prediction result or a ground truth
    recall, precision and ap considere self as a ground truth
    """
    query_id: DocumentID
    scores: Dict[DocumentID, Real]
    
    def get_ranks(self) -> List[DocumentID]:
        return [docid for docid, _ in sorted(scores.items(),
                                             key=itemgetter(1))]


@dataclass
def TRECConverter:
    items: items: Iterable[RankItem]
    dataset: Dataset
    runname: str
    is_ground_truth: bool = False

    def get_fpath(self) -> Path:
        ext: str = 'qrel' if is_ground_truth else 'prel'
        return dataset.get_result_dir().joinpath(f'{self.runname}.{ext}')

    def format(self) -> List[Tuple[str, ...]]:
        """
        Convert items to TREC-eval input format
        """
        return list(
            flatten([
                [
                    (str(item.query_id), docid, str(score), runname)
                    for docid, score
                    in sorted(self.item.scores.items(), key=itemgetter(1), reverse=True)
                ]
                for item in items
            ])
        )

    def dump(self,
             ignore_existence: bool = False) -> None:
        records: List[Tuple[str, ...]] = self.format()
        fpath: Path = self.get_fpath()
        if not ignore_existence:
            if fpath.exits():
                raise AssertionError(f'File exists. {fpath}')   
        with open(self.get_fpath(), 'w') as fout:
            fout.write('\n'.join(['\t'.join(rec) for red in records]))
