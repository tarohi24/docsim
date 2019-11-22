import re
from typing import List, Pattern, Set

from nltk.corpus import stopwords as nltk_sw
from nltk.tokenize import RegexpTokenizer

from docsim.models import ColDocument


stopwords: Set[str] = set(nltk_sw.words('english'))
not_a_word_pat: Pattern = re.compile(r'^[^a-z0-9]*$')
tokenizer: RegexpTokenizer = RegexpTokenizer(r'\w+|\$[\d\.]+|\S+')


def get_all_tokens(doc: ColDocument) -> List[str]:
    tokens: List[str] = tokenizer.tokenize(doc.text.lower())
    # remove stopwords
    tokens: List[str] = [w for w in tokens if w not in stopwords]  # type: ignore
    tokens: List[str] = [w for w in tokens  # type: ignore
                         if not_a_word_pat.match(w) is None
                         and not w.isdigit()]
    return tokens
