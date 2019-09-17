from dataclasses import dataclass
from typing import List

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
