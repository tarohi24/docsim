"""
Generate corpus for the specific category
"""
import argparse
from pathlib import Path
from typing import List

from tqdm import tqdm

from docsim.elas.search import EsResult, EsSearcher


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset',
                        type=str,
                        nargs=1)
    parser.add_argument('output',
                        type=str,
                        nargs=1)
    parser.add_argument('tags_file',
                        type=str,
                        nargs=1)
    args = parser.parse_args()
    dataset: str = args.dataset[0]
    tags_file: str = args.tags_file[0]
    output: str = args.output[0]

    tags_path: Path = Path(__file__).parent.joinpath(tags_file)
    with open(tags_path) as fin:
        tags = fin.read().splitlines()

    print(tags)
    res: EsResult = EsSearcher(es_index=dataset)\
        .initialize_query()\
        .add_match_all()\
        .add_query(terms=tags, field='tags')\
        .add_source_fields(['text'])\
        .scroll()

    path: Path = Path(__file__).parent.joinpath(dataset).joinpath(f'{output}.txt')
    with open(path, 'w') as fout:
        for hit in tqdm(res.hits):
            fout.write(hit.source['text'] + '\n')
