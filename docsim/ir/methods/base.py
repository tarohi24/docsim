from dataclasses import dataclass
from itertools import groupby
from operator import attrgetter
from typing import Callable, Dict, Hashable, List, Type

from tqdm import tqdm

from docsim.ir.trec import RankItem, TRECConverter
from docsim.ir.models import QueryDataset, QueryDocument


class Param:
    pass


@dataclass
class Searcher:
    query_dataset: QueryDataset
    param: Param

    def retrieve(self, query: QueryDocument) -> RankItem:
        raise NotImplementedError('This is an abstract class.')

    def run(self) -> None:
        items: List[RankItem] = [res
                                 for res
                                 in [self.retrieve(query) for query in tqdm(self.query_dataset.queries)]
                                 if res is not None]
        trec: TRECConverter = TRECConverter(
            items=items,
            query_dataset=self.query_dataset,
            runname=self.runname,
            is_ground_truth=False)
        trec.dump()


@dataclass
class ExperimentManager:
    query_dataset: QueryDataset
    params: List[Param]

    def groupby(self, attr: str) -> Dict[Hashable, List[Param]]:
        key_func: Callable[[Param], Hashable] = attrgetter(attr)
        attr_sorted_params: List[Param] = sorted(self.params, key=key_func)
        return {
            key: list(values)
            for key, values in groupby(attr_sorted_params, key=key_func)
        }

    def run(self,
            searcher_cls: Type[Searcher]) -> None:
        for param in self.params:
            searcher: Searcher = searcher_cls(param=param,
                                              query_dataset=self.query_dataset)
            searcher.run()
