from dataclasses import dataclass
from numbers import Real
from operator import itemgetter
from typing import Dict, List, Iterable

from dataclasses_jsonschema import JsonSchemaMixin
from more_itertools import flatten

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

def to_trec(items: Iterable[RankItem],
            runname: str = 'STANDARD') -> List[str, str, Real]:
    """
    Convert items to TREC-eval input format
    """
    return list(
        flatten([
            [
                (str(item.query_id), docid, score, runname)
                for docid, score
                in sorted(item.scores.items(), key=itemgetter(1), reverse=True)
            ]
            for item in items
        ])
    )
