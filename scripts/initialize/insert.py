import sys

from docsim.dataset import Dataset
from docsim.elas.clef import CLEFConverter
from docsim.elas.index import EsClient
from docsim.elas.mappings import Converter


dataset_dict: Dict[str, Dataset] = {
    'clef': Dataset('clef')
}

converters: Dict[str, Converter] = {
    'clef': CLEFConverter(),
}

es_indices: Dict[str, str] = {
    'clef': 'clef',
}


if __name__ == '__main__':
    ds_name: str = sys.argv[1]
    dataset: Dataset = dataset_dict[ds_name]
    converter: Converter = converters[ds_name]
    es_clinet: EsClient = 
