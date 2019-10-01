docsim
=========

docsim is a package for estimating methods of document retrieval.
If you have both a set of documents and citations (ground truth) among them,
you can easily evaluate your retrieval method.

NOTE: This is used mainly for conducting experiments (not for producions).

## How to use

### Requirements

- Docker (18.09~)
- Docker Compose(12.04~)
- Python (3.7~)

### Installation and execution
At first, clone this repository. `git clone https://github.com/tarohi24/docsim`

Next, Modify environment variables in `compose/python/env` to tell your environment.

- `ES_URL` is the url of Elasticsearch (for most cases `ES_URL=localhost` works).
- `PROJECT_ROOT` is the root directory path of this project in the docker container. Basically you don't have to change this value.

Assume you cloned this package in your ${HOME} directory,  you can use your python program.

```bash
$ ELAS_MEM="4g" # Set maximum memory capacity allocated to Elasticsearch
$ ELAS_MEM=ELAS_MEM docker-compose -f compose/elas/docker-compose.yaml up -d # launch Elasticsearch (if you don't have launched any ES servers)
$ bash run.bash python path/to/script.py  # run python script
```


## Modules

### Elasticsearch wrapper
You can create/execute an Elasticsearch query by chaining methods like:

```python
from docsim.elas.search import EsResult, EsSearcher

searcher = EsSearcher(es_index='index_name')
candidates = searcher\
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
