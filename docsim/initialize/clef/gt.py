"""
Generate ground truth labels
load original qrel -> map a key to the new key -> dump new qrel
"""
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Dict, List, Optional, Match, Tuple


def loading() -> List[str]:
    """
    Return
    -----
    e.g. "PAC-1 0 EP-0971326-B1 1"
    """
    path: Path = Path.home().joinpath('clef/PAC-Qrels/PAC_qrels_21_EN.txt')
    with open(path) as fin:
        lines: List[str] = fin.read().splitlines()
    return lines


def load_mapping() -> Dict[str, str]:

    def _parse(line: str) -> Tuple[str, str]:
        # accepts a line such as "PAC-119_EP-1258304-A1.xml"
        eps_op: Optional[Match[str]] = re.match(
            r'(PAC-\d+)_EP-(\d+)-([A-Z][0-9]).xml', line)
        assert eps_op is not None
        eps: Match[str] = eps_op
        return (eps.group(1), f'EP{eps.group(2)}{eps.group(3)}')

    pac_eps: List[str] = [
        p.name for p in Path.home().joinpath('clef/topics').glob('PAC-*.xml')]
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
