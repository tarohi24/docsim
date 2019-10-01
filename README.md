docsim
=========

docsim is a package for estimating ways of document retrieval.
If you have both a set of documents and citations (ground truth) among them,
you can easily evaluate your retrieval method.

NOTE: This is used mainly for conducting experiments (not for producions).

## How to use

### Requirements

- Docker (18.09~), Docker Compose(12.04~)
- Python (3.7~)

### Installation

1. Clone this repository. `git clone https://github.com/tarohi24/docsim`
2. Install this using pip. `pip install .`


## Modules

### Elasticsearch wrapper
You can create/execute Elasticsearch query by chaining methods like:

```python
from docsim.elas.search import EsResult, EsSearcher

candidates: EsResult = searcher\
    # initialize
    .initialize_query()\
    # add search query
    .add_query(terms=q_words, field='text')\
    # specify the number of docs returned
    .add_size(size)\
    # filtering
    .add_filter(terms=query_doc.tags, field='tags')\
    # specify field name where terms exist
    .add_source_fields(['text'])\
    # execute search
    .search()
```

For more defailed information, see [implementation](https://github.com/tarohi24/docsim/blob/master/docsim/elas/search.py).


## Advanced usage

### IR evaluation

- `./run.bash ir dataset method_name paramfile` to execute the method.
- `./run.bash trec dataset method_name` to evaluate the result.
