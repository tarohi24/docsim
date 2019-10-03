from pathlib import Path
from more_itertools import flatten
import unittest
from typing import List

from docsim.converters.aan import AANConverter
from docsim.models import ColDocument, QueryDocument
from docsim.settings import data_dir


class AANConverterTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(AANConverterTest, self).__init__(*args, **kwargs)
        self.converter: AANConverter = AANConverter()
        self.source_dir: Path = data_dir.joinpath('aan/orig/collection')
        self.docs: List[ColDocument] = list(flatten(
            [self.converter.to_document(
                self.source_dir.joinpath(f'{docid}.txt'))
             for docid in ['D07-1026', 'D07-1016', ]]))
        self.queries: List[QueryDocument] = list(flatten(
            [self.converter.to_query_dump(
                self.source_dir.joinpath(f'{docid}.txt'))
             for docid in ['D07-1026', 'D07-1016', ]]))

    def test_get_title(self):
        assert self.docs[0].title.value == 'Instance Based Lexical Entailment for Ontology Population'

    def test_get_docid(self):
        assert self.docs[0].docid.value == 'D07-1026'
        assert self.queries[0].docid == 'D07-1026'

    def test_get_tags(self):
        self.assertListEqual(
            self.docs[0].tags.value,
            ['D07'])
        self.assertListEqual(
            self.queries[0].tags,
            ['D07'])

    def test_get_text(self):
        assert self.docs[0].text.value.split()[:3] == 'Proceedings of the'.split()
        assert self.queries[0].text.split()[:3] == 'Proceedings of the'.split()

    def test_get_paras(self):
        pass
