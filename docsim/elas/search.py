"""
Module for elasticsaerch
"""
from __future__ import annotations
from dataclasses import dataclass, field
from numbers import Real
from typing import Dict, List, TypeVar

from docsim.elas.client import EsClient
from docsim.ir.trec import RankItem
from docsim.settings import es


T_EsResult = TypeVar('T_EsResult', bound='EsResult')


@dataclass
class EsResultItem:
    docid: str
    score: Real
    source: Dict

    @classmethod
    def from_dict(cls,
                  data: Dict) -> 'EsResultItem':
        self = EsResultItem(
            elas_id=data['docid'],
            score=data['_score'],
            source=data['_source']
        )
        return self


@dataclass
class EsResult:
    hits: List[EsResultItem]

    @classmethod
    def from_dict(cls,
                  data: Dict) -> 'EsResult':
        hits: List[Dict] = data['hits']['hits']  # type: ignore
        return cls([EsResultItem.from_dict(hit) for hit in hits])

    def to_rank_item(self,
                     query_id: str) -> RankItem:
        scores: Dict[str, float] = {
            hit.docid: hit.score
            for hit in self.hits}
        return RankItem(query_id=query_id, scores=scores)
        
           
@dataclass
class EsSearcher:
    es_index: str
    query: Dict = field(default_factory=dict)
    es: EsClient = es

    def search(self) -> EsResult:
        res: EsResult = EsResult.from_dict(
            es.search(index=self.es_index, body=self.query))
        return res

    def add_query(self,
                  terms: List[str],
                  field: str = 'text',
                  condition: str = 'should') -> 'EsSearcher':
        """
        modify self.query
        """
        self['query'] = {
            'query': {
                'bool': {
                    condition: [
                        {'match': {field: t}}
                        for t in terms
                    ]
                }
            }
        }
        return self

    def add_size(self,
                 size: int) -> 'EsSearcher':
        """
        modify self.size
        """
        self.query['size'] = size
        return self

    def add_source_fields(self,
                          source_fields: List[str]) -> 'EsSearcher':
        """
        modify self._source
        """
        self.query['_source'] = source_fields
        return self

    def add_filter(self,
                   terms: List[str],
                   field: str = 'tags',
                   condition: str = 'should') -> 'EsSearcher':
        """
        modify self.query
        """
        self['filter'] = {
            'query': {
                'bool': {
                    condition: [
                        {'match': {field: t}}
                        for t in terms
                    ]
                }
            }
        }
        return self
