from pathlib import Path
import unittest
from typing import List

from docsim.ir.converters.ntcir import NTCIRConverter
from docsim.ir.models import ColDocument, ColParagraph, QueryDocument
from docsim.settings import project_root


class NTCIRConverterTest(unittest.TestCase):
    source_dir: Path = project_root.joinpath('docsim/tests/ir/converters/source')

    def __init__(self, *args, **kwargs):
        super(NTCIRConverterTest, self).__init__(*args, **kwargs)
        self.converter: NTCIRConverter = NTCIRConverter()
        self.test_file: Path = NTCIRConverterTest.source_dir.joinpath('sample.txt')
        self.docs: List[ColDocument] = list(self.converter.to_document(self.test_file))

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
