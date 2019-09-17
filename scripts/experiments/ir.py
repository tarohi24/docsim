"""
Standalone script for IR Experiment
"""
import sys
from typing import Dict, Type

# methods
from docsim.ir.methods.keyword import KeywordBaseline

from docsim.ir.methods.base import Searcher, Param
from docsim.ir.models import QueryDataset



searcher_classes: Dict[str, Tuple[Type[Param], Type[Searcher]] = {
    'keyword': (KeywordBaselineParam, KeywordBaseline),
}

def main(ds_name: str, runname: str) -> None:
    query_dataset: QueryDataset = QueryDataset.load_dump(name=ds_name)
    searcher_cls: Type[Searcher] = searcher_classes[runname]
    searcher: Searcher = searcher_cls(query_dataset=query_dataset,
                                      runname=runname)
    searcher.run()


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
