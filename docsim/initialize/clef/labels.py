"""
Generate labels (qrels, gt)
"""
from pathlib import Path
import re
from typing import Dict, List

import faust


app = faust.App('clef_labels', broker='kafka://broker:9092')
pac_to_docid_mapping: Dict[int, str] = dict()
topic_pattern = re.compile(r'PAC-(\d+)_EP-(\d+)-([A-Z0-9]{2})')
qrel_dict = app.Table('clef_labels_qrel', default=list)


def load_mapping():
    directory: Path = Path.home().joinpath('clef/topics')
    for topic_path in directory.glob('*.xml'):
        fname: str = topic_path.stem()
        match = topic_pattern.match(fname)
        if match is None:
            raise AssertionError()
        pac_to_docid_mapping[int(match.group(1))] = f'EP{match.group(2)}{match.group(3)}'


class Qrel(faust.Record):
    query: str
    rel: str


@app.timer(1)
async def load_original_qrel():
    path: Path = Path.home().joinpath('clef/PAC-Qrels/PAC_qrels_21_EN.txt')
    with open(path) as fin:
        lines: List[str] = [line.split(' ') for line in fin.read().splitlines()]
    async for line in lines:
        pacid: int = int(line[0][4:])
        docid: str = pac_to_docid_mapping[pacid]
        relid: str = line[2].replace('-', '')
        qrel: Qrel = Qrel(query=docid, rel=relid)
        await dump_qrels.send(qrel)


@app.agent
async def dump_qrels(qrels: faust.Stream[Qrel]):
    async for qrel in qrels:
        qrel_dict[qrel.query].append(qrel.rel)


if __name__ == '__main__':
    load_mapping()
    app.main()
