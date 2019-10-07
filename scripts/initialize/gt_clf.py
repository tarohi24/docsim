"""
Module for generating GT for classification
"""
import argparse
import json
from typing import Dict, List

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
    
    with open(dataset.get_clf_gt_path(), 'w') as fout:
        json.dump(gt, fout)
