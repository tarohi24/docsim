import argparse

from docsim.experiment import Experimenter, method_classes
from docsim.models import QueryDataset


parser = argparse.ArgumentParser()
parser.add_argument('-d',
                    '--dataset',
                    nargs=1,
                    type=str,
                    help='The name of the dataset')
parser.add_argument('-r',
                    '--runname',
                    nargs=1,
                    type=str,
                    help='Module name')
parser.add_argument('-p',
                    '--param_file',
                    nargs=1,
                    type=str,
                    help='A parameter file')
parser.add_argument('-f',
                    '--fake',
                    nargs='?',
                    default=None,
                    help="Specify this flag when you won't save the result")


def main(ds_name: str,
         runname: str,
         param_file: str,
         is_fake: bool) -> None:
    dataset: QueryDataset = QueryDataset.load_dump(name=ds_name)
    method_cls, param_cls = method_classes[runname]
    exp: Experimenter = Experimenter(
        met_cls=method_cls,
        par_cls=param_cls,
        param_file=param_file,
        dataset=dataset,
        runname=runname,
        is_fake=is_fake)
    exp.run()


if __name__ == '__main__':
    args = parser.parse_args()
    is_fake: bool = True if args.fake is not None else False
    main(ds_name=args.dataset[0],
         runname=args.runname[0],
         param_file=args.param_file[0],
         is_fake=is_fake)
