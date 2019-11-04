from collections import Counter
import re
from typing import List, Pattern, Set

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


pat_token_non_alphabet: Pattern = re.compile('^[^a-z]+$')
stop_words: Set[str] = set(stopwords.words('english'))


def tokenize(text: str) -> List[str]:
    return word_tokenize(text)


def remove_stopwords(tokens: List[str]) -> List[str]:
    return [w for w in tokens if w not in stop_words]


def remove_nonalphabet_tokens(tokens: List[str]) -> List[str]:
    """
    it requires `lower` in advance
    """
    return [w for w in tokens if pat_token_non_alphabet.match(w) is None]


def extract_toptf_tokens(tokens: List[str],
                         n_words: int) -> List[str]:
    return [token for token, _ in Counter(tokens).most_common(n_words)]
