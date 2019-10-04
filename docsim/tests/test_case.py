import logging
from pathlib import Path
from unittest import TestCase

from docsim.settings import project_root, results_dir


class DocsimTestCase(TestCase):
    """
    Now inheritance seems to fail...
    Don't use this.
    """
    TESTS_ROOT = project_root.joinpath('tests')

    def __init__(self, *args, **kwargs):
        super(DocsimTestCase, self).__init__(*args, **kwargs)
        self.logger = logging.getLogger()

    def clean_results(self):
        # assertion to prevent from deleting from production results
        assert results_dir != project_root.joinpath('results')
        for task in ('ir', 'clf'):
            if results_dir.joinpath(task).exists():
                clefdir: Path = results_dir.joinpath(task).joinpath('clef')
                for fpath in clefdir.glob('*.prel'):
                    fpath.unlink()
                for fpath in clefdir.glob('*.json'):
                    fpath.unlink()

                clefdir.rmdir()
                results_dir.joinpath(task).rmdir()

    def tearDown(self):
        self.clean_results()
