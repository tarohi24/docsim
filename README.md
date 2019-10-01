docsim
=========

docsim is the tool to estimate document simiarity for document ranking.
If you have both a set of documents and citations (ground truth) among them,
you can easily use our advanced method.

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
    .initialize_query()\  # initialize
    .add_query(terms=q_words, field='text')\  # term query
    .add_size(size)\  # specify the number of docs returned
    .add_filter(terms=query_doc.tags, field='tags')\  # filtering
    .add_source_fields(['text'])\  # specify field name where terms exist
    .search()  # execute search
```

For more defailed information, see [implementation](https://github.com/tarohi24/docsim/blob/master/docsim/elas/search.py).


## Advanced usage

### IR evaluation

- `./run.bash ir dataset method_name paramfile` to execute the method.
- `./run.bash trec dataset method_name` to evaluate the result.
