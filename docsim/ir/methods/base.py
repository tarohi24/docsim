@dataclass
class Searcher:
    dataset: Dataset
    queries: List[Document]
    runname: str

    def retrieve(self, query: Document) -> RankItem:
        raise NotImplementedError('This is an abstract class.')

    def run(self) -> None:
        items: List[RankItem] = [res
                                 for res
                                 in [self.retrieve(query) for query in self.queries]
                                 if res is not None]
        trec: TRECConverter = TRECConverter(
            items=items,
            dataset=self.dataset,
            runname=self.runname,
            is_ground_truth=False)
        trec.dump()
