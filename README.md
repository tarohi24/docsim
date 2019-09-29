docsim
=========

docsim is the tool to estimate document simiarity for document ranking.
If you have both a set of documents and citations (ground truth) among them,
you can easily use our advanced method.

## How to use

### Requirements

- Docker (18.09~), Docker Compose(12.04~)
- Python (3.7~)

### IR evaluation

- `./run.bash ir dataset method_name paramfile` to execute the method.
- `./run.bash trec dataset method_name` to evaluate the result.
