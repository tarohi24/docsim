"""
load -> create an instance -> insert into ES
"""
import logging
from pathlib import Path
from typing import Generator, List
import xml.etree.ElementTree as ET

from elasticsearch.helpers import bulk
from tqdm import tqdm
from typedflow.typedflow import Task, DataLoader, Dumper, Pipeline, Batch

from docsim.converters.clef import CLEFConverter
from docsim.elas import models
from docsim.elas.client import EsClient
from docsim.models import ColDocument
from docsim.settings import data_dir


converter: CLEFConverter = CLEFConverter()
logger = logging.getLogger(__file__)


def loading() -> Generator[Path, None, None]:
    directory: Path = data_dir.joinpath(f'clef/orig/colleciton/EP')
    for path in tqdm(directory.glob(f'**/*.xml')):
        yield path


def get_document(path: Path) -> ColDocument:
    root: ET.Element = ET.parse(str(path.resolve())).getroot()
    docid: str = converter._get_docid(root)
    tags: List[str] = converter._get_tags(root)
    title: str = converter._get_title(root)
    text: str = converter._get_text(root)
    return ColDocument(docid=models.KeywordField(docid),
                       title=models.TextField(title),
                       text=models.TextField(text),
                       tags=models.KeywordListField(tags))


def insert_into_es(doc: Batch[ColDocument],
                   es_client: EsClient) -> None:
    """
    CAUTION: This initializes the index.
    """
    es_client.delete_index()
    es_client.create_index()

    for ok, response in bulk(es_client.es,
                             doc.data,
                             index=es_client.es_index,
                             chunk_size=100):
        if not ok:
            logger.warn('Bulk insert: fails')
    es_client.es.indices.refresh()


if __name__ == '__main__':
    gen: Generator[Path, None, None] = loading()
    loader: DataLoader = DataLoader[Path](gen=gen)
    get_doc_task: Task = Task[Path, ColDocument](func=get_document)
    es_client: EsClient = EsClient(index='clef',
                                   item_cls=ColDocument)
    dumper: Dumper = Dumper[ColDocument](
        func=lambda batch: insert_into_es(batch, es_client=es_client))
    pipeline: Pipeline = Pipeline(
        loader=loader,
        pipeline=[get_doc_task],
        dumper=dumper)
    pipeline.run()
