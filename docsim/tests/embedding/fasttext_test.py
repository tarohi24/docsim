import pytest

from docsim.embedding.fasttext import FastText
from docsim.settings import project_root
from docsim.tests.test_case import DocsimTestCase


def get_fasttext_model() -> FastText:
    return FastText.create()


class FastTextTest(DocsimTestCase):

    def __init__(self, *args, **kwargs):
        super(FastTextTest, self).__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls):
        cls.model: FastText = get_fasttext_model()

    def test_get_embedding(self):
        word: str = 'hello'
        FastTextTest.model.embed(word)      
