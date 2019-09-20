import numpy as np
import pytest

from docsim.embedding.base import return_vector, return_matrix, InvalidShape
from docsim.tests.test_case import DocsimTestCase


class EmbeddingBaseTest(DocsimTestCase):

    @return_vector
    def identity_vec_mapping(self, x: np.ndarray):
        return x

    @return_matrix
    def identity_mat_mapping(self, x: np.ndarray):
        return x

    def test_return_vector(self):
        with pytest.raises(InvalidShape):
            self.identity_vec_mapping(np.arange(6).reshape(2, 3))

    def test_return_mat(self):
        with pytest.raises(InvalidShape):
            self.identity_mat_mapping(np.arange(6))
