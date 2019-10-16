from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Generator, Iterable, List, Type

from docsim.converters.clef import CLEFConverter
from docsim.initialize.base import Dataset
from docsim.settings import data_dir


@dataclass
class CLEFDataset(Dataset):
    converter: CLEFConverter = field(default_factory=CLEFConverter)

    def iter_orig_files(self) -> Generator[Path, None, None]:
        return data_dir.joinpath(f'clef/orig/collection').glob(f'**/*.xml')

    def iter_query_files(self) -> Generator[Path, None, None]:
        return data_dir.joinpath(f'clef/orig/query').glob(f'**/*.xml')
