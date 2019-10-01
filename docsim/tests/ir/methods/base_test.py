import unittest
from typing import Type

from docsim.ir.methods.base import Param, Searcher
from docsim.ir.methods.keyword import KeywordBaseline, KeywordBaselineParam
from docsim.ir.trec import TRECConverter
from docsim.ir.models import QueryDataset


class BaseMethodTest(unittest.TestCase):

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
                                           is_fake=True)

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
