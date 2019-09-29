import json
import sys
from typing import Dict, List

from docsim.settings import es, data_dir


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
    dataset: str = sys.argv[1]
    with open(data_dir.joinpath(f'{dataset}/en.qrel')) as fin:
        lines: List[str] = fin.read().splitlines()

    with open(data_dir.joinpath(f'{dataset}/name_mapping.json')) as fin:
        mapping: Dict[str, str] = json.load(fin)

    with open(data_dir.joinpath(f'{dataset}/en.valid.qrel'), 'w') as fout:
        for line in lines:
            items: List[str] = line.split()
            docid: str = items[2].replace('-', '')
            if check_existence(docid, dataset):
                query_docid: str = mapping[items[0]].replace('-', '')
                fout.write(f'{query_docid} {items[1]} {docid} {items[3]}\n')
