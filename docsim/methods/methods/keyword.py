"""
extract keywords -> do search
"""
from collections import Counter
import re
from typing import List, Pattern, Set, TypedDict  # type: ignore

from nltk.corpus import stopwords as nltk_sw
from nltk.tokenize import RegexpTokenizer


stopwords: Set[str] = set(nltk_sw.words('english'))
tokenizer: RegexpTokenizer = RegexpTokenizer(r'\w+|\$[\d\.]+|\S+')
not_a_word_pat: Pattern = re.compile(r'^[^a-z0-9]*$')


class KeywordParam(TypedDict):
    n_words: int
    n_docs: int


def extract_keywords_from_text(text: str,
                               param: KeywordParam) -> List[str]:
    # lower and tokenize
    tokens: List[str] = tokenizer.tokenize(text.lower())
    # remove stopwords
    tokens: List[str] = [w for w in tokens if w not in stopwords]  # type: ignore
    tokens: List[str] = [w for w in tokens  # type: ignore
                         if not_a_word_pat.match(w) is None]
    counter: Counter = Counter(tokens)
    keywords: List[str] = [w for w, _ in counter.most_common(param['n_words'])]
    return keywords
