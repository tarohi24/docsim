"""
Tests for experiment.py
"""
from docsim.experiment import Experimenter
from docsim.methods.keyword import KeywordBaseline, KeywordBaselineParam
from docsim.models import QueryDataset
from docsim.settings import results_dir
from docsim.tests.test_case import DocsimTestCase


class ExperimenterTest(DocsimTestCase):

    def __init__(self, *args, **kwargs):
        super(ExperimenterTest, self).__init__(*args, **kwargs)
        # used as dummies
        self.param_file: str = 'params/keyword/40.json'
        self.dataset: QueryDataset = QueryDataset.load_dump('clef')
        self.runname: str = 'keyword'

    def setUp(self, *args, **kwargs):
        super(ExperimenterTest, self).setUp(*args, **kwargs)
        assert results_dir.joinpath('ir/clef').mkdir(parents=True)
        assert results_dir.joinpath('clf/clef').mkdir(parents=True)

    def test_load_param_which_exists(self):
        exp: Experimenter = Experimenter(
            met_cls=KeywordBaseline,
            par_cls=KeywordBaselineParam,
            param_file=self.param_file,
            dataset=self.dataset,
            runname=self.runname,
            is_fake=True)
        assert type(exp.load_param()) == KeywordBaselineParam

    def test_run(self):
        exp: Experimenter = Experimenter(
            met_cls=KeywordBaseline,
            par_cls=KeywordBaselineParam,
            param_file=self.param_file,
            dataset=self.dataset,
            runname=self.runname,
            is_fake=False)
        exp.run()
        assert results_dir.joinpath('ir/clef/keyword.prel')
        assert results_dir.joinpath('clf/clef/keyword.json')
