docsim
=========

docsim is a package for evaluating methods of document retrieval.

NOTE: This is used mainly for conducting experiments (not for producions).

## How to use

### Requirements

- Docker (18.09~)
- Docker Compose(12.04~)
- Python (3.7~)

### Prepare for datasets

We use three datasets for testing methods, AAN, CLEF and NTCIR. To use NTCIR, you need to [contact NTCIR](http://research.nii.ac.jp/ntcir/permission/ntcir-6/perm-en-PATENT.html) to get a license.

**AAN** Download AAN corpus in [this website](http://aan.how/download/).

### Installation and execution
At first, clone this repository. `git clone https://github.com/tarohi24/docsim`

Next, download [fastText English pre-training model.

```sh
$ cd models/fasttext
$ wget https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.en.300.bin.gz
$ gzip -d cc.en.300.bin.gz
```

Next, Modify environment variables in `compose/python/env` to tell your environment.

- `ES_URL` is the url of Elasticsearch (for most cases `ES_URL=localhost` works).
- `PROJECT_ROOT` is the root directory path of this project in the docker container. Basically you don't have to change this value.

Assume you cloned this package in your ${HOME} directory,  you can use your python program.

```bash
$ ELAS_MEM="4g" # Set maximum memory capacity allocated to Elasticsearch
$ ELAS_MEM=ELAS_MEM docker-compose -f compose/elas/docker-compose.yaml up -d # launch Elasticsearch (if you don't have launched any ES servers)
$ bash run.bash python path/to/script.py  # run python script
```



## Advanced usage

### IR evaluation

- `./run.bash ir dataset method_name paramfile` to execute the method.
- `./run.bash trec dataset method_name` to evaluate the result.
