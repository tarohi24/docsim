from pathlib import Path
import unittest
from typing import List

from docsim.ir.converters.aan import AANConverter
from docsim.ir.models import ColDocument, QueryDocument
from docsim.settings import project_root


class AANConverterTest(unittest.TestCase):
    source_dir: Path = project_root.joinpath('docsim/tests/ir/converters/source/aan')

    def __init__(self, *args, **kwargs):
        super(AANConverterTest, self).__init__(*args, **kwargs)
        self.converter: AANConverter = AANConverter()
        self.source_txts: List[Path] = [
            source_dir.joinpath('D07-1026.txt'),
        ]

    def test_get_title(self):
        assert self.docs[0].title.value == 'Process for making improved corrosion preventive zinc cyanamide'

    def test_get_docid(self):
        assert self.docs[0].docid.value == '199305176894'

    def test_get_tags(self):
        self.assertListEqual(
            self.docs[0].tags.value,
            ['C01C'])

    def test_get_text(self):
        assert self.docs[0].text.value.split()[:3] == 'The invention will'.split()

    def test_get_paras(self):
        assert self.queries[0].paras[0].split()[:3] == 'DETAILED DESCRIPTION OF'.split()
        assert self.queries[0].paras[1].split()[:3] == 'On the contrary,'.split()
