"""
Generate ground truth labels
load original qrel -> map a key to the new key -> dump new qrel
"""
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Dict, Generator, List, Optional, Match, Tuple

from typedflow.typedflow import Task, DataLoader, Dumper, Pipeline
from typedflow.utils import dump_to_one_file
from tqdm import tqdm

from docsim.settings import data_dir


def loading() -> Generator[str, None, None]:
    """
    Return
    -----
    e.g. "PAC-1 0 EP-0971326-B1 1"
    """
    path: Path = data_dir.joinpath('clef/orig/gt.qrel')
    with open(path) as fin:
        lines: List[str] = fin.read().splitlines()
    for line in tqdm(lines):
        yield line
    return


def load_mapping() -> Dict[str, str]:

    def _parse(line: str) -> Tuple[str, str]:
        # accepts a line such as "PAC-119_EP-1258304-A1.xml"
        eps_op: Optional[Match[str]] = re.match(
            r'(PAC-\d+)_EP-(\d+)-([A-Z][0-9]).xml', line)
        assert eps_op is not None
        eps: Match[str] = eps_op
        return (eps.group(1), f'EP{eps.group(2)}{eps.group(3)}')

    pac_eps: List[str] = [
        p.name for p in data_dir.joinpath('clef/orig/query/topics').glob('PAC-*.xml')]
    parsed: List[Tuple[str, str]] = [_parse(name) for name in pac_eps]
    dic: Dict[str, str] = {k: v for k, v in parsed}
    return dic


@dataclass
class QrelItem:
    query: str
    target: str
    relevance: int

    def to_json(self) -> str:
        return f'{self.query} 0 {self.target} {str(self.relevance)}'


def parse(line: str,
          mapping: Dict[str, str]) -> QrelItem:
    splitted: List[str] = line.split()
    qi: QrelItem = QrelItem(
        query=mapping[splitted[0]],
        target=splitted[2].replace('-', ''),
        relevance=int(splitted[3]))
    return qi


if __name__ == '__main__':
    mapping: Dict[str, str] = load_mapping()
    gen: Generator[str, None, None] = loading()
    loader: DataLoader = DataLoader[Path](gen=gen)
    parse_task: Task = Task[str, QrelItem](
        func=lambda line: parse(line, mapping=mapping))
    dump_path: Path = data_dir.joinpath('clef/query/gt.qrel')
    dumper: Dumper = Dumper[QrelItem](
        func=lambda batch: dump_to_one_file(batch, dump_path))
    pipeline: Pipeline = Pipeline(
        loader=loader,
        pipeline=[parse_task],
        dumper=dumper)
    pipeline.run()
