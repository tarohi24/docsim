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
    trec_converter: TRECConverter

    @classmethod
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
            self.dump_trec(res)

    def dump_trec(self, item: RankItem) -> None:
        self.trec_converter.incremental_dump(item)
