import argparse
import asyncio
from pathlib import Path
from typing import Dict, List, Type

import yaml
from typedflow.flow import Flow

from docsim.methods.common.types import Context, P
from docsim.methods.common.methods import MethodProperty, M

# methods
from docsim.methods.methods import keywords


def get_method(method_name: str) -> Type[M]:
    if method_name == 'kewords':
        return keywords.KeywordBaselines
    else:
        raise KeyError(f'{method_name} is not found')


def parse(path: Path) -> List[M]:
    with open(path) as fin:
        data: Dict = yaml.load(fin, Loader=yaml.Loader)
    n_docs: int = data['n_docs']
    es_index: str = data['es_index']
    method_name: str = data['method']
    method_type: Type[M] = get_method(method_name)
    param_type: Type[P] = method_type.param_type

    lst: List[M] = []
    for p in data['params']:
        runname: str = p['name']
        context: Context = Context({
            'n_docs': n_docs,
            'es_index': es_index,
            'method': method_name,
            'runname': runname
        })
        mprop: MethodProperty = MethodProperty(context=context)
        del p['name']
        param: P = param_type(**p)
        method: M = method_type(mprop=mprop, param=param)
        lst.append(method)
    return lst


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('paramfile',
                        metavar='F',
                        type=Path,
                        nargs=1,
                        help='A yaml file')
    args = parser.parse_args()
    methods: List[M] = parse(args.paramfile)
    for met in methods:
        flow: Flow = met.create_flow()
        asyncio.run(flow.run())
