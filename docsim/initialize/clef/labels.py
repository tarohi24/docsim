"""
Generate labels (qrels, gt)
"""
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Dict, Iterable, List

from docsim.settings import data_dir


pac_to_docid_mapping: Dict[int, str] = dict()
topic_pattern = re.compile(r'PAC-(\d+)_EP-(\d+)-([A-Z0-9]{2})')
qrel_dict: Dict[str, list] = defaultdict(list)


def load_mapping():
    directory: Path = Path('/data').joinpath('clef/topics')
    for topic_path in directory.glob('*.xml'):
        fname: str = Path(topic_path).stem
        match = topic_pattern.match(fname)
        if match is None:
            raise AssertionError()
        pac_to_docid_mapping[int(match.group(1))] = f'EP{match.group(2)}{match.group(3)}'


@dataclass
class Qrel:
    query: str
    rel: str


def load_original_qrel():
    path: Path = Path('/data').joinpath('clef/PAC-Qrels/PAC_qrels_21_EN.txt')
    with open(path) as fin:
        lines: List[str] = [line.split(' ') for line in fin.read().splitlines()]
    qrels: List[str] = []
    for line in lines:
        pacid: int = int(line[0][4:])
        docid: str = pac_to_docid_mapping[pacid]
        relid: str = line[2].replace('-', '')
        qrel: Qrel = Qrel(query=docid, rel=relid)
        qrels.append(qrel)
    return dump_qrels(qrels)


def dump_qrels(qrels: Iterable[Qrel]):
    for qrel in qrels:
        qrel_dict[qrel.query].append(qrel.rel)


if __name__ == '__main__':
    load_mapping()

    with open(data_dir.joinpath('clef/en.qrels'), 'w') as fout:
        for key, lst in qrel_dict.items():
            for item in lst:
                fout.write(f'{key} 1 {item} 1\n')
