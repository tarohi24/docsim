"""
Split a file which contains multiple XML roots
"""
import argparse
from pathlib import Path
from typing import Generator, List

from tqdm import tqdm


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-i',
                    dest='input_file',
                    type=str,
                    help='Input file path')
parser.add_argument('-o',
                    dest='output_dir',
                    type=str,
                    help='Output Directory')


def iter_docs(fpath) -> Generator[List[str], None, None]:
    lst: List[str] = []
    with open(fpath, 'r') as fin:
        for line in fin.readlines():
            line = line[:-1]
            lst.append(line)
            if line == '</DOC>':
                yield lst


if __name__ == '__main__':
    args = parser.parse_args()
    print(args.input_file)
    in_path: Path = Path(args.input_file)
    assert in_path.exists()

    out_dir: Path = Path(args.output_dir)
    assert out_dir.exists()
    assert len(list(out_dir.glob('*'))) == 0  # contains no files

    for i, doc in tqdm(enumerate(iter_docs(in_path))):
        with open(out_dir.joinpath(f'{i}.xml'), 'w') as fout:
            fout.write('\n'.join(doc))
