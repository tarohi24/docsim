from pathlib import Path

import pytest

from docsim.exp.trec_to_pandas import Recall, to_df


def test_recall_loading_lines():
    rec: Recall = Recall.from_line('recall_100              EP1935970A1     0.2609')
    assert rec.docid == 'EP1935970A1'
    assert rec.n_items == 100
    assert rec.score == 0.2609

    # test for invalid lines
    with pytest.raises(ValueError):
        rec: Recall = Recall.from_line('sdafjk')


def test_get_uniq_ids(tmp_path):
    lines =\
        """recall_5                EP1935533A1     0.0000
           recall_10               EP1935533A1     0.0000
           recall_15               EP1935533A1     0.0000
           recall_20               EP1935533A1     0.0000
           recall_30               EP1935533A1     0.0000
           recall_100              EP1935533A1     0.3333
           recall_200              EP1935533A1     0.3333
           recall_500              EP1935533A1     0.3333
           recall_1000             EP1935533A1     0.3333
           recall_5                EP1935970A1     0.0000
           recall_10               EP1935970A1     0.0000
           recall_15               EP1935970A1     0.0435
           recall_20               EP1935970A1     0.0435
           recall_30               EP1935970A1     0.0435
           recall_100              EP1935970A1     0.2609
           recall_200              EP1935970A1     0.2609
           recall_500              EP1935970A1     0.2609
           recall_1000             EP1935970A1     0.2609
           recall_5                EP1936625A2     0.0000
           recall_10               EP1936625A2     0.0000
           recall_15               EP1936625A2     0.0000
           recall_20               EP1936625A2     0.0000
           recall_30               EP1936625A2     0.0000
           recall_100              EP1936625A2     0.0000
           recall_200              EP1936625A2     0.0000
           recall_500              EP1936625A2     0.0000
           recall_1000             EP1936625A2     0.0000"""

    path: Path = tmp_path.joinpath('sample.trec')
    with open(path, 'w') as fout:
        for l in lines:
            fout.write(l)
    df = to_df(path)
    assert df.index.tolist() == 'EP1935533A1 EP1935970A1 EP1936625A2'.split()
    assert df.columns.tolist() == [5, 10, 15, 20, 30, 100, 200, 500, 1000]
