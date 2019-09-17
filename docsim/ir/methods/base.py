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

    @classmethod
    @property
    def method_name(cls) -> str:
        raise NotImplementedError('This is an abstract class.')

    def retrieve(self, query: QueryDocument) -> RankItem:
        raise NotImplementedError('This is an abstract class.')

    def run(self) -> None:
        items: List[RankItem] = []
        for query in tqdm(self.query_dataset.queries):
            res: RankItem = self.retrieve(query)
            items.append(res)

            # dump result
            self.dump_trec(items)

    def dump_trec(self, items: List[RankItem]) -> None:
        trec: TRECConverter = TRECConverter(
            query_dataset=self.query_dataset,
            is_ground_truth=False)
        trec.dump()
