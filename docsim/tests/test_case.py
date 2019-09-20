import logging
from unittest import TestCase

from docsim.settings import project_root


class DocsimTestCase(TestCase):
    """
    Not dataclass. Therefore the following variables are class variables.
    """
    TESTS_ROOT = project_root.joinpath('tests')

    def __init__(self):
        self.logger = logging.getLogger()

    def setUp(self):
        super().setUp()
        self.logger.basicConfig(
            format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
            level=logging.DEBUG)
