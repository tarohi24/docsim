from pathlib import Path
import os

from elasticsearch import Elasticsearch


project_root: Path = Path(os.environ['PROJECT_ROOT'])

is_test: bool = bool(os.environ['IS_TEST'])
if is_test:
    test_dir: Path = project_root.joinpath('docsim/tests')
    data_dir: Path = test_dir.joinpath('data')
    models_dir: Path = test_dir.joinpath('models')
    results_dir: Path = test_dir.joinpath('results')
else:
    data_dir: Path = project_root.joinpath('data')  # noqa
    models_dir: Path = project_root.joinpath('models')  # noqa
    results_dir: Path = project_root.joinpath('results')  # noqa

# Elasticsearch
es: Elasticsearch = Elasticsearch(os.environ['ES_URL'])
