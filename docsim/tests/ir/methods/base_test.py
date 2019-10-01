import unittest
from unittest.mock import MagicMock
from typing import Type

from docsim.ir.methods.base import Param, Searcher
from docsim.ir.methods.keyword import KeywordBaseline, KeywordBaselineParam
from docsim.ir.trec import RankItem, TRECConverter
from docsim.ir.models import QueryDataset
from docsim.tests.test_case import DocsimTestCase


class BaseMethodTest(DocsimTestCase):

    def __init__(self, *args, **kwargs):
        super(BaseMethodTest, self).__init__(*args, **kwargs)
        self.param: Param = Param()
        self.searcher_cls: Type[Searcher] = Searcher
        self.query_dataset: QueryDataset = QueryDataset.load_dump(name='clef')
        self.trec_converter: TRECConverter = TRECConverter(
            method_name=self.searcher_cls.method_name(),
            dataset_name=self.query_dataset.name)
        self.searcher: Searcher = Searcher(query_dataset=self.query_dataset,
                                           param=self.param,
                                           trec_converter=self.trec_converter,
                                           is_fake=False)

    def test_method_name(self):
        assert self.searcher_cls.method_name() == 'base'

    def test_subclass_method_name(self):
        param: KeywordBaselineParam = KeywordBaselineParam(n_words=2)
        sc: KeywordBaseline = KeywordBaseline(query_dataset=self.query_dataset,
                                              param=param,
                                              trec_converter=self.trec_converter,
                                              is_fake=True)
        assert sc.method_name() == 'keyword'

    def test_query_words(self):
        text: str = '''This is Test test; test. for for for patent patent,'''
        self.assertListEqual(
            ['test', 'patent', ],
            self.searcher.get_query_words(text, n_words=2))

    def test_retrieve(self):
        prel_path: Path = self.trec_converter.get_fpath()
        assert not prel_path.exists()
        dummy_score: Dict[str, float] = {
            'ABC': 33,
            'TREC': 12,
        }
        rankitem: RankItem = RankItem(
            query_id='dummy',
            scores=dummy_score)
        searcher: Searcher = Searcher(query_dataset=self.query_dataset,
                                      param=self.param,
                                      trec_converter=self.trec_converter,
                                      is_fake=True)
        searcher.retrieve = MagicMock(return_value=lambda self, query: rankitem)
        searcher.run()

        assert prel_path.exists()
        with open(prel_path, 'r') as fin:
            lines = fin.read().splitlines()
        assert len(lines) == (len(dummy_score) * len(self.query_dataset))
