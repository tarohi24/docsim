import argparse

from docsim.methods.common.flow import MethodProperty
from docsim.methods.common.types import Context


def get_default_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--n_docs',
                        nargs=1,
                        type=int,
                        default=100)
    parser.add_argument('--es_index',
                        nargs=1,
                        type=str)
    parser.add_argument('--runname',
                        nargs=1,
                        type=str)
    return parser


def create_prop_from_args(args,
                          method_name: str) -> MethodProperty:
    context: Context = Context(
        es_index=args.es_index,
        method=method_name,
        runname=args.runname,
        n_docs=args.n_docs)
    mprop: MethodProperty = MethodProperty(context=context)
    return mprop
