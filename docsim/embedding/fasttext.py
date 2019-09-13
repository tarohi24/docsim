from docsim.embedding.base import Model, return_vector
from docsim.settings import project_root


@dataclass
class Fasttext(Model):
    model = fasttext.load_model(
        str(project_root.joinpath('models/fasttext/wiki.en.bin').resolve()))
