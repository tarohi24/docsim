"""
Tests for experiment.py
"""
from docsim.experiment import method_classes, Experimenter
from docsim.methods.keyword import KeywordBaselineParam
from docsim.models import QueryDataset
from docsim.tests.test_case import DocsimTestCase


class ExperimenterTest(DocsimTestCase):

    def __init__(self, *args, **kwargs):
        super(ExperimenterTest, self).__init__(*args, **kwargs)
        # used as dummies
        self.param_file: str = 'params/keyword/40.json'
        self.dataset: QueryDataset = method_classes['keyword']
        self.runname: str = 'keyword'

    def test_load_param_which_exists(self):
        exp: Experimenter = Experimenter(
            param_file=self.param_file,
            dataset=self.dataset,
            runname=self.runname,
            is_fake=True)
        assert type(exp.load_param()) == KeywordBaselineParam
