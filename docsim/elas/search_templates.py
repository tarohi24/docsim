from typing import Dict, List


def initialize(q_words: List[str],
               field: str = 'text') -> Dict:
    return {
        'query': {
            'bool': {
                'should': [
                    {'match': {field: q}}
                    for q in q_words
                ]
            }
        }
    }

def add_size(data: Dict,
             size: int) -> Dict:
    newdata: Dict = data.copy()
    newdata['size'] = size
    return newdata

def add_source_fields(data: Dict,
                      source_fields: List[str]) -> Dict:
    newdata: Dict = data.copy()
    newdata['_source'] = source_fields
    return newdata

def add_keywords(keywords: List[str],
                 field: str = 'tags') -> Dict:
    newdata: Dict = data.copy()
    try:
        newdata['query']['bool']['must'] = [
            {'match': {field: k}} for k in keywords]
    except KeyError:
        raise AssertionError('data have not been initialized properly.')
    return newdata
