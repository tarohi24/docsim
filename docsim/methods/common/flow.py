from dataclasses import dataclass, field
from typing import Generic, TypeVar

from typedflow.flow import Flow
from typedflow.nodes import LoaderNode, DumpNode

from docsim.methods.common.dumper import get_dump_node
from docsim.methods.common.loader import get_loader_node
from docsim.methods.common.types import Context, Param, TRECResult
from docsim.models import ColDocument


P = TypeVar('P', bound=Param)


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


@dataclass
class Method(Generic[P]):
    prop: MethodProperty
    param: P

    def create_flow(self):
        ...
