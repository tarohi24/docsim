"""
Standalone script for IR Experiment
"""
from typing import Dict, Type

from docsim.ir import methods
from docsim.ir.methods.base import Searcher
from docsim.ir.models import QueryDataset


searcher_classes: Dict[str, Type[Searcher]] = {
    'keyword': methods.keyword.KeywordBaseline,
}

def main(ds_name: str, runname: str) -> None:
    query_dataset: QueryDataset = QueryDataset.load_dump(name=ds_name)
    searcher_cls: Type[Searcher] = searcher_classes[runname]
    searcher: Searcher = searcher_cls(query_dataset=query_dataset,
                                      runname=runname)
    searcher.run()
