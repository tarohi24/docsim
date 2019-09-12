from collections import Counter
import re
from typing import Callable, List

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


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
    stop_words: Set[str] = set(stopwords.words('english'))

    def apply(self, tokens: List[str]) -> List[str]:
        return [w for w in tokens if w not in self.stop_words]


@dataclass
class RegexRemover(Filter):
    regex: re.Pattern = re.compile('[!@#$]')

    def apply(self, tokens: List[str]) -> List[str]:
        return [w for w in [re.sub(regex, '', w) for w in tokens] if w != '']


@dataclass
class TFFilter(Filter):
    """
    extract top n words
    """
    n_words: int

    def apply(self, tokens: List[str]) -> List[str]:
        return [token for token, _ in Counter(tokens).most_common(self.n_words)]


class TextProcessor:
    text: str
    filters: List[Filter] = [LowerFilter, StopWordRemover, RegexRemover]

    def apply(self) -> List[str]:

        def apply_filter(tokens: List[str],
                         filters: List[FilterType]) -> List[str]:
            if len(filters) == 0:
                return tokens
            else:
                head, *tail = filters
                head_applied: List[str] = head(tokens)
                return apply_filter(head_applied, tail)

        tokenized: List[str] = word_tokenize(self.text)
        return apply_filter(tokenized, self.filters)
