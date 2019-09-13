from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Generator

from docsim.elas.clef import CLEFConverter
from docsim.elas.mappings import Converter
from docsim.settings import project_root


@dataclass
class Dataset:
    name: str
    converter: Converter
    es_index: str

    def list_original_files(self) -> Generator[Path, None, None]:
        return self.get_data_dir().glob('orig/**/*.xml')

    def get_data_dir(self) -> Path:
        return project_root.joinpath(f'data/{self.name}')

    def get_result_dir(self) -> Path:
        return project_root.joinpath(f'result/{self.name}')

    def __eq__(self, another):
        if isinstance(another, Dataset):
            return self.name == another.name
        else:
            return False

    def __hash__(self):
        return hash(self.name)


dataset_dict: Dict[str, Dataset] = {
    'clef': Dataset(
        name='clef',
        converter=CLEFConverter(),
        es_index='clef'),
}
