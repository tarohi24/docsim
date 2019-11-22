from enum import Enum


class Strategy(Enum):
    """
    Strategies

    NAIVE
        Fuzzy is used only for extracting keywords from a document

    RERANK
        After prefiltering by normal keywords, rerank by FuzzyBoW similaity
    """
    NAIVE = 1
    RERANK = 2
