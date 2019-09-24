"""
Format citation.txt (the format is in https://github.com/tarohi24/docsim/issues/33)
into prels format specified by TREC eval
"""
from pathlib import Path
from typing import List, Tuple

from docsim.settings import project_root


def extract_citations(fpath: Path) -> List[Tuple[str, str]]:
    with open(fpath, 'r') as fin:
        lines: List[List[str]] = [line.split() for line in fin.read().splitlines()]

    citations: List[Tuple[str, str]] = [(line[0], line[2]) for line in lines]
    return citations


def dump_citations_as_rels(citations: List[Tuple[str, str]],
                           out_fpath: Path) -> None:
    with open(out_fpath, 'w') as fout:
        for frm, to in citations:
            fout.write(f'{frm}\tQ0\t{to}\t1\n')


if __name__ == '__main__':
    in_file: Path = project_root.joinpath('data/aan/orig/citations.txt')
    out_file: Path = project_root.joinpath('results/ir/aan/en.valid.qrels')
    citations: List[Tuple[str, str]] = extract_citations(in_file)
    dump_citations_as_rels(citations, out_file)
