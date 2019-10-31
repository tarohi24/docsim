from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Dict, List, Pattern, Set

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import sentencepiece as spm

from docsim.settings import data_dir


clef_spm_models: Dict = {
    al: spm.SentencePieceProcessor()
    for al in 'ABCDEFG'
}
for al, model in clef_spm_models.items():
    model.Load(str(data_dir.joinpath(f'spm/clef/{al}.model').resolve()))


class Filter:

    def apply(self, tokens: List[str]) -> List[str]:
        raise NotImplementedError('This is an abstract class')

    def __call__(self, tokens: List[str]) -> List[str]:
        return self.apply(tokens)


class LowerFilter(Filter):

    def apply(self, tokens: List[str]) -> List[str]:
        return [w.lower() for w in tokens]


@dataclass
class StopWordRemover(Filter):
    stop_words: Set[str] = field(default_factory=lambda: set(stopwords.words('english')))

    def apply(self, tokens: List[str]) -> List[str]:
        return [w for w in tokens if w not in self.stop_words]


@dataclass
class RegexRemover(Filter):
    regex: Pattern = field(default_factory=lambda: re.compile('^[^a-zA-Z0-9]+$'))

    def apply(self, tokens: List[str]) -> List[str]:
        return [w for w in [re.sub(self.regex, '', w) for w in tokens] if w != '']


@dataclass
class TFFilter(Filter):
    """
    extract top n words
    """
    n_words: int

    def apply(self, tokens: List[str]) -> List[str]:
        return [token for token, _ in Counter(tokens).most_common(self.n_words)]


class SPMFilter(Filter):
    """
    sentencepiece filter
    """
    def __init__(self,
                 al: str):
        self.model = clef_spm_models[al]

    def apply(self, tokens: List[str]) -> List[str]:
        s: str = ' '.join(tokens)
        res: List[str] = self.model.EncodeAsPieces(s)
        return res


@dataclass
class TextProcessor:
    filters: List[Filter]

    def apply(self, text: str) -> List[str]:

        def apply_filter(tokens: List[str],
                         filters: List[Filter]) -> List[str]:
            if len(filters) == 0:
                return tokens
            else:
                head, *tail = filters
                head_applied: List[str] = head.apply(tokens)
                return apply_filter(head_applied, tail)

        tokenized: List[str] = word_tokenize(text)
        return apply_filter(tokenized, self.filters)
