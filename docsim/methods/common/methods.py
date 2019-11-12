from __future__ import annotations
from dataclasses import dataclass, field
from typing import ClassVar, Generic, Type, TypeVar  # type: ignore

from typedflow.flow import Flow
from typedflow.nodes import LoaderNode, DumpNode

from docsim.methods.common.dumper import get_dump_node
from docsim.methods.common.loader import get_loader_node
from docsim.methods.common.types import Context, TRECResult
from docsim.models import ColDocument


@dataclass
class MethodProperty:
    context: Context  # independent of methods
    load_node: LoaderNode[ColDocument] = field(init=False)
    dump_node: DumpNode[TRECResult] = field(init=False)

    def __post_init__(self):
        self.load_node: LoaderNode[ColDocument] = get_loader_node(
            context=self.context)
        self.dump_node: DumpNode[TRECResult] = get_dump_node(
            context=self.context)

    def create_flow(self) -> Flow:
        ...


P = TypeVar('P')


@dataclass
class Method(Generic[P]):
    mprop: MethodProperty
    param: P
    param_type: ClassVar[Type[P]] = field(init=False)

    def create_flow(self):
        ...


M = TypeVar('M', bound=Method)
