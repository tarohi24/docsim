"""
Module for generating GT for classification
"""
import argparse
from typing import Dict, List

from docsim.clf import ClfResult
from docsim.models import QueryDataset

parser = argparse.ArgumentParser()
parser.add_argument('-d',
                    '--dataset',
                    nargs=1,
                    type=str,
                    help='The name of the dataset')


if __name__ == '__main__':
    args = parser.parse_args()
    ds: str = args.dataset[0]
    dataset: QueryDataset = QueryDataset.load_dump(name=ds)
    gt: Dict[str, List[str]] = {
        qd.docid: qd.tags
        for qd in dataset.queries
    }
    gt: ClfResult = ClfResult(
        dataset_name=ds,
        method_name='gt',
        result=gt)
    gt.dump()
