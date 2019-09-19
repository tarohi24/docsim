#!/bin/bash

case $1 in
    "ir" )
        IR_SCRIPT="scripts/experiments/ir.py"
        docker-compose -f compose/python/docker-compose.yaml run --rm python python "/workplace/${IR_SCRIPT}" ${@:2}
        ;;
    "trec" )
        DATASET=$2
        METHOD=$3
        RESULT_FILE="/workplace/results/ir/${DATASET}/${METHOD}.prel"
        GT="/workplace/results/ir/${DATASET}/en.valid.qrel"
        docker-compose -f compose/trec/docker-compose.yaml run --rm trec trec_eval -q -m "recall"  $GT $RESULT_FILE
        ;;
    "test" )
        docker-compose -f compose/python/docker-compose.yaml run --workdir="/workplace" --rm python make test
        ;;
    * )
        echo "Invalid option ${1}" ;;
esac
