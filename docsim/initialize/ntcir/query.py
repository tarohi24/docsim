"""
load xml -> parse and extract -> dump into a file (query.bulk)
"""
from pathlib import Path
import re
from typing import Generator, List, Optional
from lxml import etree
import xml.etree.ElementTree as ET

from tqdm import tqdm
from typedflow.flow import Flow
from typedflow.nodes import TaskNode, LoaderNode, DumpNode

from docsim.initialize.converters.ntcir import NTCIRConverter
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
    return ColDocument(docid=docid,
                       title=title,
                       text=text,
                       tags=tags)


if __name__ == '__main__':
    loader_node: LoaderNode[Path] = LoaderNode(func=loading)
    pre_task_node: TaskNode[Path, ET.Element] = TaskNode(func=replace_tab)
    task_node: TaskNode[ET.Element, ColDocument] = TaskNode(func=get_document)
    (task_node < pre_task_node)('pre')

    def dump_to_one_file(doc: ColDocument) -> None:
        with open(data_dir.joinpath('ntcir/query/dump.bulk'), 'a') as fout:
            fout.write(doc.to_json() + '\n')  # noqa

    dump_node: DumpNode[ColDocument] = DumpNode(func=dump_to_one_file)
    flow: Flow = Flow(dump_nodes=[dump_node, ])
    flow.run()
