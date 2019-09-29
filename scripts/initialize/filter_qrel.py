import argparse
import json
from typing import Dict, List

from docsim.settings import es, data_dir


parser = argparse.ArgumentParser()
parser.add_argument('-d',
                    '--dataset',
                    type=str,
                    nargs=1,
                    help='The name of the dataset')
parser.add_argument('-m',
                    '--mapping',
                    action='store_true',
                    default=False,
                    help='Specify to use name mapping')


def check_existence(docid: str,
                    dataset: str) -> bool:
    body: Dict = {
        'query': {
            'match': {
                'docid': docid
            }
        }
    }
    res = es.search(index=dataset, body=body)
    return len(res['hits']['hits']) > 0


if __name__ == '__main__':
    args = parser.parse_args()
    dataset: str = args.dataset[0]
    is_map: bool = args.mapping
    with open(data_dir.joinpath(f'{dataset}/en.qrel')) as fin:
        lines: List[str] = fin.read().splitlines()

    if is_map:
        with open(data_dir.joinpath(f'{dataset}/name_mapping.json')) as fin:
            mapping: Dict[str, str] = json.load(fin)

    with open(data_dir.joinpath(f'{dataset}/en.valid.qrel'), 'w') as fout:
        for line in lines:
            items: List[str] = line.split()
            docid: str = items[2].replace('-', '')
            if check_existence(docid, dataset):
                query_docid: str = mapping[items[0]].replace('-', '') if is_map else items[0]
                fout.write(f'{query_docid} {items[1]} {docid} {items[3]}\n')
