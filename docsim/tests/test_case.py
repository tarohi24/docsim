import logging
from unittest import TestCase

from docsim.settings import project_root


class DocsimTestCase(TestCase):
    """
    Now inheritance seems to fail...
    Don't use this.
    """
    TESTS_ROOT = project_root.joinpath('tests')

    def __init__(self, *args, **kwargs):
        super(DocsimTestCase, self).__init__(*args, **kwargs)
        self.logger = logging.getLogger()

    def setUp(self, *args, **kwargs):
        super(DocsimTestCase, self).setUp()
        pass
