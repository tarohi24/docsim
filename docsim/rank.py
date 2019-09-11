from dataclasses import dataclass
from operator import itemgetter
from typing import Dict, List, Set


from dataclasses_jsonschema import JsonSchemaMixin

from docsim.dataset import DocumentID


@dataclass
class RankItem:
    """
    both a prediction result or a ground truth
    recall, precision and ap considere self as a ground truth
    """
    query_id: DocumentID
    scores: Dict[DocumentID, float]
    
    def get_ranks(self) -> List[DocumentID]:
        return [docid for docid, _ in sorted(scores.items(),
                                             key=itemgetter(1))]

    def recall(self,
               pred: RankItem,
               n: int) -> float:
        pred_set: Set[DocumentID] = set(pred.get_ranks[:n])
        gt: Set[DocumentID] = set(self.scores.keys())
        return len(pred_set & gt) / len(gt)

    def precision(self,
                  pred: RankItem,
                  n: int) -> float:
        pred_set: Set[DocumentID] = set(pred.get_ranks[:n])
        gt: Set[DocumentID] = set(self.scores.keys())
        return len(pred_set & gt) / n
