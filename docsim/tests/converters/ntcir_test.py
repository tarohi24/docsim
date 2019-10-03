from pathlib import Path
import unittest
from typing import List

from docsim.ir.converters.ntcir import NTCIRConverter
from docsim.ir.models import ColDocument, QueryDocument
from docsim.settings import data_dir


class NTCIRConverterTest(unittest.TestCase):
    source_dir: Path = data_dir.joinpath('ntcir')

    def __init__(self, *args, **kwargs):
        super(NTCIRConverterTest, self).__init__(*args, **kwargs)
        self.converter: NTCIRConverter = NTCIRConverter()
        self.test_file: Path = NTCIRConverterTest.source_dir.joinpath('orig/collection/sample.txt')
        self.docs: List[ColDocument] = list(self.converter.to_document(self.test_file))
        self.queries: List[QueryDocument] = [
            self.converter.to_query_dump(
                NTCIRConverterTest.source_dir.joinpath(f'orig/query/100{i}.xml'))[0]
            for i in range(1, 4)]

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
