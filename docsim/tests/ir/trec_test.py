import unittest
from typing import Dict

from docsim.ir.trec import RankItem
from docsim.testing import DocsimTestCase


class TestRankItem(DocsimTestCase):
    
    def setUp(self):
        super().setUp()
        self.dummy_score: Dict[str, float] = {
            'ABC': 33,
            'TREC': 12,
        }

    def test_get_ranks(self):
        rankitem: RankItem = RankItem(
            query_id='dummy',
            scores=self.dummy_score)
        unittest.assertListEqual(
            ['ABC', 'TREC', ],
            rankitem.get_ranks())
