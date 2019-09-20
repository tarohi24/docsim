from pathlib import Path
import unittest
from typing import List
import xml.etree.ElementTree as ET

from docsim.ir.converters.clef import CLEFConverter
from docsim.settings import project_root


class CLEFConverterTest(unittest.TestCase):

    def to_xml_root(self, docid: str) -> ET.Element:
        """
        Parameters
        ----------
        docid
            EP... *with* '-'
            e.g. EP-0050001-A2
        """
        first: str = docid[3]
        second: str = docid[4:6]
        third: str = docid[6:8]
        forth: str = docid[8:10]

        fpath: Path = project_root.joinpath(
            f'data/clef/orig/collection/00000{first}/{second}/{third}/{forth}/{docid}.xml')

        root: ET.Element = ET.parse(str(fpath.resolve())).getroot()
        return root

    def __init__(self, *args, **kwargs):
        super(CLEFConverterTest, self).__init__(*args, **kwargs)
        self.converter: CLEFConverter = CLEFConverter()
        self.docids: List[str] = [
            'EP-0050001-A2',
        ]
        self.roots: List[ET.Element] = [self.to_xml_root(docid) for docid in self.docids]

    def test_get_title(self):
        titles: List[str] = [
            'A golf aid.',
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
            [['A63B', ], ],
            [self.converter._get_tags(root) for root in self.roots])
