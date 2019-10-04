import unittest
from typing import Dict, Tuple

from docsim.models import RankItem


class TestRankItem(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestRankItem, self).__init__(*args, **kwargs)
        self.dummy_scores: Dict[Tuple[str, str], float] = {
            # (docid, tag): score
            ('EP1000', 'A'): 33.0,
            ('EP1001', 'A'): 33.0,
            ('EP1002', 'B'): 20.0,
        }
        self.query_id: str = 'EPTopic1000'
        self.ri: RankItem = RankItem(query_id=self.query_id,
                                     scores=self.dummy_scores)

    def test_pred_tags_just_n_top(self):
        pred = self.ri.pred_tags(n_top=2)
        self.assertSetEqual(set(pred), {'A', 'B'})

    def test_pred_tags_less_n_top(self):
        pred = self.ri.pred_tags(n_top=1)
        self.assertSetEqual(set(pred), {'A', })

    def test_pred_tags_more_n_top(self):
        pred = self.ri.pred_tags(n_top=3)
        self.assertSetEqual(set(pred), {'A', 'B'})
