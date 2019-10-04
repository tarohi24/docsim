import argparse

from docsim.experiment import Experimenter, method_classes
from docsim.ir.models import QueryDataset


parser = argparse.ArgumentParser()
parser.add_argument('dataset',
                    type=str,
                    help='The name of the dataset')
parser.add_argument('runname',
                    type=str,
                    help='Module name')
parser.add_argument('param_file',
                    type=str,
                    help='A parameter file')
parser.add_argument('-f', '--fake',
                    nargs='?',
                    default=None,
                    help="Specify this flag when you won't save the result")


def main(ds_name: str,
         runname: str,
         param_file: str,
         is_fake: bool) -> None:
    dataset: QueryDataset = QueryDataset.load_dump(name=ds_name)
    searcher_cls, param_cls = method_classes[runname]
    exp: Experimenter = Experimenter(
        param_file=param_file,
        dataset=dataset,
        runname=runname,
        is_fake=is_fake)
    exp.run()


if __name__ == '__main__':
    args = parser.parse_args()
    is_fake: bool = True if args.fake is not None else False
    main(ds_name=args.dataset,
         runname=args.runname,
         param_file=args.param_file,
         is_fake=is_fake)
