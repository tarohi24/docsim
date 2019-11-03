"""
load xml -> parse and extract -> dump into a file (query.bulk)
"""
from pathlib import Path
import re
from typing import Generator, List
from lxml import etree
import xml.etree.ElementTree as ET

from tqdm import tqdm
from typedflow.typedflow import Task, DataLoader, Dumper, Pipeline
from typedflow.utils import dump_to_one_file

from docsim.converters.ntcir import NTCIRConverter
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
    return elem


def get_document(root: ET.Element) -> ColDocument:
    docid: str = converter._get_docid(root)
    tags: List[str] = converter._get_tags(root)
    title: str = converter._get_title(root)
    text: str = converter._get_text(root)
    return ColDocument(docid=models.KeywordField(docid),
                       title=models.TextField(title),
                       text=models.TextField(text),
                       tags=models.KeywordListField(tags))


if __name__ == '__main__':
    gen: Generator[Path, None, None] = loading()
    loader: DataLoader = DataLoader[Path](gen=gen)
    pre_proc_task: Task = Task[Path, ET.Element](func=replace_tab)
    task: Task = Task[ET.Element, ColDocument](func=get_document)
    dump_path: Path = data_dir.joinpath('ntcir/query/dump.bulk')
    dumper: Dumper = Dumper[ColDocument](
        func=lambda batch: dump_to_one_file(batch, dump_path))
    pipeline: Pipeline = Pipeline(
        loader=loader,
        pipeline=[pre_proc_task, task],
        dumper=dumper)
    pipeline.run()
