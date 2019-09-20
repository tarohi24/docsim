import unittest  # noqa
from typing import List

from docsim.elas.client import EsClient
from docsim.ir.models import ColDocument
from docsim.tests.test_case import DocsimTestCase


class TestEsClient(DocsimTestCase):

    def setUp(self, *args, **kwargs):
        super(TestEsClient, self).setUp()
        dummy_index: str = 'dummy'
        self.client: EsClient = EsClient(es_index=dummy_index,
                                         item_cls=ColDocument)
        assert not self.client.es.indices.exists(index=dummy_index)
        self.client.create_index()

        self.docs: List[ColDocument] = [
            ColDocument._create_doc_from_values(
                docid='ABC',
                title='Testing is important',
                text='hi',
                tags=['hi', '1234']),
            ColDocument._create_doc_from_values(
                docid='TREC',
                title='test2',
                text='hi hello',
                tags=['1234', ])
        ]

    def test_bulk_insert(self):
        self.client.bulk_insert(self.docs,
                                create_index=False,
                                delete_index=False)

    def tearDown(self):
        self.client.delete_index()
