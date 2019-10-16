import argparse
import logging
from typing import Dict, Iterable, Type



logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('-d',
                    '--dataset',
                    nargs=1,
                    type=str,
                    help='The name of the dataset')
parser.add_argument('-o',
                    '--operations',
                    nargs='+',
                    type=str,
                    help='Operations')
parser.add_argument('-f', '--fake',
                    nargs='?',
                    default=None,
                    help="Specify this flag when you won't save the result")








dataset_dict: Dict[str, Type[Dataset]] = {
    'clef': CLEFDataset,
    'ntcir': NTCIRDataset,
    'aan': AANDataset,
}


def main(ds_name: str,
         operations: Iterable[str]) -> None:
    ds_cls: Type[Dataset] = dataset_dict[ds_name]
    dataset: Dataset = ds_cls()
    if 'doc' in operations:
        pass

    if 'para' in operations:
        raise NotImplementedError('Para is not prepared')

    if 'query' in operations:
        pass

    if 'mapping' in operations:
        pass


if __name__ == '__main__':
    args = parser.parse_args()
    main(args.dataset[0], args.operations)
