from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar, Dict, List, Type

from docsim.elas.search import EsResult, EsSearcher
from docsim.embedding.fasttext import FastText
from docsim.methods.common.methods import Method
from docsim.methods.common.types import Param, P
from docsim.methods.methods.keywords import KeywordBaseline, KeywordParam


class Stragegy(Enum):
    PESSIMICTIC = 1
    OPTIMISTIC = 2


@dataclass
class PerParam(Param):
    n_words: int
    strategy: Stragegy

    @classmethod
    def from_args(cls, args) -> PerParam:
        return PerParam(n_words=args.n_words,
                        strategy=Stragegy[args.strategy])


@dataclass
class Per(Method[PerParam]):
    param_type: ClassVar[Type[P]] = PerParam
    kb: KeywordBaseline = field(init=False)
    fasttext: FastText = field(init=False)

    def __post_init__(self):
        self.kb: KeywordBaseline = KeywordBaseline(
            mprop=self.mprop,
            param=KeywordParam(n_words=self.param.n_words))
        self.fasttext: FastText = FastText()

    def get_text_from_elas(self,
                           docids: List[str]) -> Dict[str, str]:
        searcher: EsSearcher = EsSearcher(es_index=self.mprop.context['es_index'])
        res: EsResult = searcher\
            .initialize_query()\
            .add_query(terms=docids, field='docid')\
            .add_size(len(docids))\
            .add_source_fields(['text', ])\
            .search()
        id_texts: Dict[str, str] = {  # type: ignore
            item.docid: item.source['text']
            for item in res.hits
        }
        return id_texts
