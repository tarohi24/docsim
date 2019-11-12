"""
load xml -> parse and extract -> dump into a file (query.bulk)
"""
import asyncio
from pathlib import Path
import re
from typing import Generator, List, Optional, Union
from lxml import etree
import xml.etree.ElementTree as ET

from tqdm import tqdm
from typedflow.batch import Batch
from typedflow.exceptions import FaultItem
from typedflow.flow import Flow
from typedflow.nodes import TaskNode, LoaderNode, DumpNode
from typedflow.tasks import Task, DataLoader, Dumper

from docsim.initialize.converters.ntcir import NTCIRConverter
from docsim.elas import models
from docsim.models import ColDocument
from docsim.settings import data_dir

converter: NTCIRConverter = NTCIRConverter()
parser = etree.XMLParser(resolve_entities=False)


def loading() -> Generator[Path, None, None]:
    directory: Path = data_dir.joinpath(f'ntcir/orig/query')
    pathlist: List[Path] = list(directory.glob(r'*'))
    for path in tqdm(pathlist):
        yield path


def replace_tab(path: Path) -> ET.Element:
    with open(path) as fin:
        body: str = fin.read()
    replaced: str = re.sub(
        r'&(.*?);',
        ' ',
        body.replace('<tab>', ' '))
    elem: ET.Element = ET.fromstring(replaced, parser=parser)
    doc_elem: Optional[ET.Element] = elem.find('DOC')
    assert doc_elem is not None
    return doc_elem


def get_document(root: ET.Element) -> ColDocument:
    docid: str = converter._get_docid(root)
    tags: List[str] = converter._get_tags(root)
    title: str = converter._get_title(root)
    text: str = converter._get_text(root)
    return ColDocument(docid=models.KeywordField(docid),
                       title=models.TextField(title),
                       text=models.TextField(text),
                       tags=models.KeywordListField(tags))


def dump_to_one_file(batch: Batch[Union[FaultItem, ColDocument]],
                     path: Path) -> None:
    with open(path, 'a') as fout:
        for item in batch.data:
            if not isinstance(item, FaultItem):
                fout.write(item.to_json() + '\n')


if __name__ == '__main__':
    # loader
    gen: Generator[Path, None, None] = loading()
    loader: DataLoader[Path] = DataLoader(gen=gen)
    loader_node: LoaderNode[Path] = LoaderNode(loader=loader)

    # pre-task
    pre_proc_task: Task[Path, ET.Element] = Task(func=replace_tab)
    pre_task_node: TaskNode[Path, ET.Element] = TaskNode(task=pre_proc_task,
                                                         arg_type=Path)
    pre_task_node.set_upstream_node('loader', loader_node)

    # task
    task: Task[ET.Element, ColDocument] = Task(func=get_document)
    task_node: TaskNode[ET.Element, ColDocument] = TaskNode(task=task,
                                                            arg_type=ColDocument)
    task_node.set_upstream_node('pre', pre_task_node)

    # dump
    dump_path: Path = data_dir.joinpath('ntcir/query/dump.bulk')
    dumper: Dumper = Dumper[ColDocument](
        func=lambda batch: dump_to_one_file(batch, dump_path))
    dump_node: DumpNode[ColDocument] = DumpNode(dumper=dumper,
                                                arg_type=ColDocument)
    dump_node.set_upstream_node('task', task_node)

    flow: Flow = Flow(dump_nodes=[dump_node, ])
    asyncio.run(flow.run())
