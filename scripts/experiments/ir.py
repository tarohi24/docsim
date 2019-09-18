"""
Standalone script for IR Experiment
"""
import argparse
import json
from pathlib import Path
from typing import Dict, Type, Tuple

# methods
from docsim.ir.methods.keyword import KeywordBaseline, KeywordBaselineParam
from docsim.ir.methods.paa import PAA, PAAParam

from docsim.ir.methods.base import Searcher, Param
from docsim.ir.models import QueryDataset
from docsim.ir.trec import TRECConverter
from docsim.settings import project_root


parser = argparse.ArgumentParser()
parser.add_argument('dataset',
                    type=str,
                    help='The name of the dataset')
parser.add_argument('runname',
                    type=str,
                    help='Module name')
parser.add_argument('param_file',
                    type=str,
                    help='A parameter file')


searcher_classes: Dict[str, Tuple[Type[Searcher], Type[Param]]] = {
    'keyword': (KeywordBaseline, KeywordBaselineParam),
    'paa': (PAA, PAAParam),
}


def main(ds_name: str,
         runname: str,
         param_file: Path) -> None:
    query_dataset: QueryDataset = QueryDataset.load_dump(name=ds_name)
    searcher_cls, param_cls = searcher_classes[runname]

    # load param
    with open(project_root.joinpath(param_file), 'r') as fin:
        param_dict: Dict = json.load(fin)
    param: Param = param_cls.from_dict(param_dict)
    trec_converter: TRECConverter = TRECConverter(
        method_name=searcher_cls.method_name(),
        dataset_name=query_dataset.name)

    # initialize fpath
    try:
        trec_converter.get_fpath().unlink()
    except FileNotFoundError:
        pass
    searcher: Searcher = searcher_cls(query_dataset=query_dataset,
                                      param=param,
                                      trec_converter=trec_converter)

    # execute
    searcher.run()
    trec_converter.get_fpath().chmod('-w')


if __name__ == '__main__':
    args = parser.parse_args()
    main(args.dataset, args.runname, Path(args.param_file))
