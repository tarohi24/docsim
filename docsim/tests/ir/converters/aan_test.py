from pathlib import Path
from more_itertools import flatten
import unittest
from typing import List

from docsim.ir.converters.aan import AANConverter
from docsim.ir.models import ColDocument
from docsim.settings import data_dir


class AANConverterTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(AANConverterTest, self).__init__(*args, **kwargs)
        self.converter: AANConverter = AANConverter()
        self.source_txts: List[Path] = list(
            data_dir.joinpath('aan/orig/collection').glob('*.txt'))
        self.docs: List[ColDocument] = list(flatten(
            [self.converter.to_document(fpath) for fpath in self.source_txts]
        ))

    def test_get_title(self):
        assert self.docs[0].title.value == 'Instance Based Lexical Entailment for Ontology Population'

    def test_get_docid(self):
        assert self.docs[0].docid.value == 'D07-1026'

    def test_get_tags(self):
        self.assertListEqual(
            self.docs[0].tags.value,
            ['D07'])

    def test_get_text(self):
        assert self.docs[0].text.value.split()[:3] == 'Proceedings of the'.split()

    def test_get_paras(self):
        pass
