"""
extract keywords -> do search ------> embedding -----> dump embedding
                              \\----> dump texts
"""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import (
    Callable, ClassVar, Dict, List, Type, TypedDict, TypeVar)

import numpy as np
from nltk.tokenize import sent_tokenize
from typedflow.batch import Batch
from typedflow.flow import Flow
from typedflow.tasks import Task, Dumper
from typedflow.nodes import TaskNode, DumpNode, LoaderNode

from docsim.elas.search import EsSearcher
from docsim.embedding.base import Model as EmbedModel
from docsim.embedding.fasttext import FastText
from docsim.embedding.bert import Bert
from docsim.embedding.elmo import Elmo
from docsim.methods.common.methods import Method
from docsim.methods.common.types import P
from docsim.methods.methods.keywords import KeywordBaseline, KeywordParam
from docsim.models import ColDocument
from docsim.settings import cache_dir


T = TypeVar('T')
K = TypeVar('K')


@dataclass
class CacheParam:
    n_words: int
    model: str


class Cacher(Method[CacheParam]):
    param_type: ClassVar[Type[P]] = CacheParam
    kb: KeywordBaseline = field(init=False)
    embed_model: EmbedModel = field(init=False)

    def __post_init__(self):
        self.kb: KeywordBaseline = KeywordBaseline(
            mprop=self.mprop,
            param=KeywordParam(n_words=self.param.n_words))
        if self.param.model == 'fasttext':
            self.embed_model: FastText = FastText()
        elif self.param.model == 'elmo':
            self.embed_model: Elmo = Elmo()
        elif self.param.model == 'bert':
            self.embed_model: Elmo = Bert()
        else:
            raise KeyError()

    def get_docid(self,
                  doc: ColDocument) -> str:
        return doc.docid

    def get_filtered_docs(self,
                          doc: ColDocument) -> List[ColDocument]:
        docids: List[str] = [item.docid for item
                             in self.kb.search(doc=doc).hits]
        searcher: EsSearcher = EsSearcher(es_index=self.mprop.context['es_index'])
        docs: List[ColDocument] = searcher\
            .initialize_query()\
            .add_query(terms=docids, field='docid')\
            .add_size(len(docids))\
            .add_source_fields(['text', 'title', 'tags'])\
            .search()\
            .to_docs()
        return docs

    class IDandDocs(TypedDict):
        docid: str
        rel_docs: List[ColDocument]

    def dump_doc(self,
                 batch: Batch[IDandDocs]) -> None:
        for item in batch.data:
            path: Path = cache_dir\
                .joinpath(self.mprop.context['es_index'])\
                .joinpath(self.param.model)\
                .joinpath(f"item['docid'].dump")
            with open(path, 'w') as fout:
                for doc in item['rel_docs']:
                    fout.write(doc.to_json())
                    fout.write('\n')

    def dump_embedding(self,
                       batch: Batch[IDandDocs]) -> None:
        for item in batch.data:
            for doc in item['rel_docs']:
                sents: List[str] = sent_tokenize(doc.text)
                embeddings: np.ndarray = self.embed_model.embed_words(words=sents)
                path: Path = cache_dir\
                    .joinpath(self.mprop.context['es_index'])\
                    .joinpath(self.param.model)\
                    .joinpath(item['docid'])\
                    .joinpath(f"{doc.docid}.npy")
                np.save(str(path.resolve()), embeddings)

    @staticmethod
    def get_node(func: Callable[[T], K],
                 arg_type: Type[T]) -> TaskNode[T, K]:
        task: Task[T, K] = Task(func=func)
        node: TaskNode[T, K] = TaskNode(task=task, arg_type=arg_type)
        return node

    @staticmethod
    def get_dump_node(func: Callable[[T], None],
                      arg_type: Type[T]) -> DumpNode[T]:
        dumper: Dumper[T] = Dumper(func=func)
        node: DumpNode[T] = DumpNode(dumper=dumper)
        return node

    def create_flow(self):
        loader: LoaderNode[ColDocument] = self.mprop.load_node
        node_get_docs: TaskNode[ColDocument, List[ColDocument]] = self.get_node(
            func=self.get_filtered_docs,
            arg_type=ColDocument)
        node_dump_text: DumpNode[IDandDocs] = self.get_dump_node(func=dump_doc)
        node_dump_text.set_upstream_node('docid', loader)
        node_dump_text.set_upstream_node('rel_docs', node_get_docs)
        node_get_docs.set_upstream_node('loader', loader)

        node_encoder: DumpNode[IDandDocs] = self.get_dump_node(func=dump_embedding)
        node_encoder.set_upstream_node('docid', loader)
        node_encoder.set_upstream_node('rel_docs', node_get_docs)

        flow: Flow = Flow(dump_nodes=[node_dump_text, node_encoder])
        return flow
