from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Generator

from docsim.converters.aan import AANConverter
from docsim.initialize.base import Dataset
from docsim.settings import data_dir


@dataclass
class AANDataset(Dataset):
    converter: AANConverter = field(default_factory=AANConverter)

    @property
    def mapping_fpath(self) -> Path:
        """dummy"""
        raise FileNotFoundError()

    def iter_orig_files(self) -> Generator[Path, None, None]:
        return data_dir.joinpath(f'aan/orig/collection').glob(f'*.txt')

    def iter_query_files(self) -> Generator[Path, None, None]:
        return self.iter_orig_files()

    def create_name_mapping(self) -> Dict[str, str]:
        return dict()
