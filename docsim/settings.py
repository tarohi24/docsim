from pathlib import Path
import os

from elasticsearch import Elasticsearch


project_root: Path = Path(os.environ['PROJECT_ROOT'])

is_test: bool = bool(int(os.environ['IS_TEST']))
test_dir: Path = project_root.joinpath('docsim/tests')
root: Path = test_dir if is_test else project_root

data_dir: Path = root.joinpath('data')
models_dir: Path = root.joinpath('models')
results_dir: Path = root.joinpath('results')
param_dir: Path = root.joinpath('params')
cache_dir: Path = root.joinpath('cache')
trec_dir: Path = root.joinpath('trec_dir')


# Elasticsearch
es: Elasticsearch = Elasticsearch(
    os.environ['ES_URL'] if not is_test else 'localhost'
)

# nlpserver
nlpserver_url: str = os.environ['NLPSERVER_URL']
