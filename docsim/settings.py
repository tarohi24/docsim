from pathlib import Path
import os

from elasticsearch import Elasticsearch


project_root: Path = Path(os.environ['PROJECT_ROOT'])

# Elasticsearch
es: Elasticsearch = Elasticsearch(os.environ['ES_URL'])
