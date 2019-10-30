"""
Generate labels (qrels, gt)
"""
from pathlib import Path
from typing import List

import faust

from docsim.converters.clef import CLEFConverter
from docsim.models import QueryDocument
from docsim.settings import data_dir


app = faust.App('clef_labels', broker='kafka://broker:9092')
labels: List[str] 

