import argparse
import logging
import sys
from typing import Dict, Type

from docsim.initialize.base import Dataset, E2EConverter
from docsim.initialize.aan import AANDataset
from docsim.initialize.clef import CLEFDataset
from docsim.initialize.ntcir import NTCIRDataset


def main() -> int:
    logger = logging.getLogger(__file__)
    logger.setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('-d',
                        '--dataset',
                        nargs=1,
                        type=str,
                        help='The name of the dataset')
    parser.add_argument('-f', '--fake',
                        nargs='?',
                        default=None,
                        help="Flag when you won't save the result")

    args = parser.parse_args()

    ds_name: str = args.dataset[0]
    dataset_dict: Dict[str, Type[Dataset]] = {
        'clef': CLEFDataset,
        'ntcir': NTCIRDataset,
        'aan': AANDataset,
    }
    cls: Type[Dataset] = dataset_dict[ds_name]
    dataset = cls()
    e2e: E2EConverter = E2EConverter(dataset=dataset, name=ds_name)
    e2e.run()
    return 0


if __name__ == '__main__':
    sys.exit(main())
