from pathlib import Path
from typing import List

import faust

from docsim.converters.clef import CLEFConverter
from docsim.models import QueryDocument
from docsim.settings import data_dir


app = faust.App('clef', broker='kafka://broker:9092')
converter: CLEFConverter = CLEFConverter()
queries = app.Table('clef_query', default=QueryDocument)


@app.timer(0.5)
async def iter_query_files():
    for path in data_dir.joinpath(f'clef/orig/query').glob(f'**/*.xml'):
        abspath: str = str(path.resolve())
        await query_dump.send(value=abspath)


@app.agent()
async def query_dump(pathes: faust.Stream[str]):
    async for path in pathes:
        docs: List[QueryDocument] = converter.to_query_dump(Path(path))
        for doc in docs:
            queries[doc.docid] = doc


if __name__ == '__main__':
    app.main()
