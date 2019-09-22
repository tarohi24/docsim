from pathlib import Path
import unittest
from typing import List

import pytest

from docsim.ir.converters.clef import NTCIRConverter
from docsim.settings import project_root


class CLEFConverterTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(NTCIRConverter, self).__init__(*args, **kwargs)
        self.converter: NTCIRConverter = NTCIRConverter()
        self.docids: List[str] = [
            'EP-0050001-A2',
            'EP-1010180-B1'
        ]
        self.roots: List[ET.Element] = [self.to_xml_root(docid) for docid in self.docids]

    def test_get_title(self):
        titles: List[str] = [
            'A golf aid.',
            'A READ-ONLY MEMORY AND READ-ONLY MEMORY DEVICE',
        ]
        self.assertListEqual(
            titles,
            [self.converter._get_title(root) for root in self.roots])

    def test_get_docid(self):
        self.assertListEqual(
            [docid.replace('-', '') for docid in self.docids],
            [self.converter._get_docid(root) for root in self.roots])

    def test_get_tags(self):
        self.assertListEqual(
            [set('A63B'.split()),
             set('H01L G11C'.split())],
            [set(self.converter._get_tags(root)) for root in self.roots])

    def test_get_text(self):
        with pytest.raises(NoneException):
            self.converter._get_text(self.roots[0])

        self.assertListEqual(
            'The present invention'.split(),
            self.converter._get_text(self.roots[1]).split()[:3])

    def test_get_paras(self):
        with pytest.raises(NoneException):
            self.converter.get_paragraph_list(self.roots[0])

        assert len(self.converter.get_paragraph_list(self.roots[1])) == 40
