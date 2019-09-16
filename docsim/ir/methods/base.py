from dataclasses import dataclass
from typing import List

from docsim.ir.trec import RankItem, TRECConverter
from docsim.ir.models import QueryDataset, QueryDocument


@dataclass
class Searcher:
    query_dataset: QueryDataset
    runname: str

    def retrieve(self, query: QueryDocument) -> RankItem:
        raise NotImplementedError('This is an abstract class.')

    def run(self) -> None:
        items: List[RankItem] = [res
                                 for res
                                 in [self.retrieve(query) for query in self.dataset.queries]
                                 if res is not None]
        trec: TRECConverter = TRECConverter(
            items=items,
            query_dataset=self.query_dataset,
            runname=self.runname,
            is_ground_truth=False)
        trec.dump()
