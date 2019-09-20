import logging
from unittest import TestCase

from docsim.settings import project_root


class DocsimTestCase(TestCase):
    """
    Now inheritance seems to fail...
    Don't use this.
    """
    TESTS_ROOT = project_root.joinpath('tests')

    def __init__(self):
        self.logger = logging.getLogger()

    def setUp(self):
        self.logger.basicConfig(
            format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
            level=logging.DEBUG)
