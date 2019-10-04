from pathlib import Path
from typing import Dict, Type
from unittest.mock import MagicMock

from docsim.methods.base import Param, Method
from docsim.methods.keyword import KeywordBaseline, KeywordBaselineParam
from docsim.ir import TRECConverter
from docsim.models import QueryDataset, RankItem
from docsim.settings import results_dir
from docsim.tests.test_case import DocsimTestCase


class BaseMethodTest(DocsimTestCase):

    def __init__(self, *args, **kwargs):
        super(BaseMethodTest, self).__init__(*args, **kwargs)
        self.param: Param = Param()
        self.method_cls: Type[Method] = Method
        self.query_dataset: QueryDataset = QueryDataset.load_dump(name='clef')
        self.trec_converter: TRECConverter = TRECConverter(
            method_name=self.method_cls.method_name(),
            dataset_name=self.query_dataset.name)
        self.method: Method = Method(query_dataset=self.query_dataset,
                                     param=self.param,
                                     is_fake=False)

    def setUp(self):
        results_dir.joinpath('ir/clef').mkdir(parents=True)
        results_dir.joinpath('clf/clef').mkdir(parents=True)

    def test_method_name(self):
        assert self.method_cls.method_name() == 'base'

    def test_subclass_method_name(self):
        param: KeywordBaselineParam = KeywordBaselineParam(n_words=2)
        sc: KeywordBaseline = KeywordBaseline(query_dataset=self.query_dataset,
                                              param=param,
                                              is_fake=True)
        assert sc.method_name() == 'keyword'

    def test_query_words(self):
        text: str = '''This is Test test; test. for for for patent patent,'''
        self.assertListEqual(
            ['test', 'patent', ],
            self.method.get_query_words(text, n_words=2))

    def test_run(self):
        prel_path: Path = self.trec_converter.get_fpath()
        assert not prel_path.exists()
        dummy_score: Dict[str, float] = {
            'ABC': 33,
            'TREC': 12,
        }
        rankitem: RankItem = RankItem(
            query_id='dummy',
            scores=dummy_score)
        method: Method = Method(query_dataset=self.query_dataset,
                                param=self.param,
                                is_fake=False)
        method.apply = MagicMock(return_value=rankitem)
        method.run()

        assert prel_path.exists()
        with open(prel_path, 'r') as fin:
            lines = fin.read().splitlines()
        assert len(lines) == (len(dummy_score) * len(self.query_dataset))
        # clearn file in order to use rm_dir
        prel_path.unlink()
