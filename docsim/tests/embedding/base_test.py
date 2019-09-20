import numpy as np
import pytest

from docsim.embedding.base import return_vector, return_matrix, InvalidShape
from docsim.tests.test_case import DocsimTestCase


class EmbeddingBaseTest(DocsimTestCase):

    def __init__(self, *args, **kwargs):
        super(EmbeddingBaseTest, self).__init__(*args, **kwargs)

    def setUp(self):
        super(EmbeddingBaseTest, self).setUp()
        self.vec: np.ndarray = np.arange(6)
        self.mat: np.ndarray = np.arange(6).reshape(2, 3)

    @return_vector
    def identity_vec_mapping(self, x: np.ndarray):
        return x

    @return_matrix
    def identity_mat_mapping(self, x: np.ndarray):
        return x

    def test_return_vector(self):
        with pytest.raises(InvalidShape):
            self.identity_vec_mapping(self.mat)

        np.testing.assert_array_equal(
            self.identity_vec_mapping(self.vec),
            self.vec)

    def test_return_mat(self):
        with pytest.raises(InvalidShape):
            self.identity_mat_mapping(self.vec)

        np.testing.assert_array_equal(
            self.identity_mat_mapping(self.mat),
            self.mat)
