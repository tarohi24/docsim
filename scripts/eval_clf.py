"""
Script for evaluating a clf result (JSON)
"""
import argparse
from typing import List

from docsim import clf


parser = argparse.ArgumentParser()
parser.add_argument('-d',
                    '--dataset',
                    type=str,
                    nargs=1,
                    help='Dataset name')
parser.add_argument('-m',
                    '--method',
                    type=str,
                    nargs=1,
                    help='Method name')


if __name__ == '__main__':
    args = parser.parse_args()
    ds: str = args.dataset[0]
    met: str = args.method[0]
    pred: ClfResult = clf.ClfResult(dataset_name=ds, method_name=met)
    evaluators: List[clf.Evaluator] = [
        clf.AccuracyEvaluator(n_top=3),
    ]

    for evaluator in evaluators:
        print(evaluator.eval(pred,
    
