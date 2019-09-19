#!/bin/bash

case $1 in
    "ir" )
        IR_SCRIPT="scripts/experiments/ir.py"
        docker-compose -f compose/python/docker-compose.yaml run python python "/workplace/${IR_SCRIPT}" ${@:2}
        ;;
    "trec" )
        DATASET=$2
        METHOD=$3
        RESULT_FILE="/workplace/results/ir/${DATASET}/${METHOD}.prel"
        GT="/workplace/results/ir/${DATASET}/gt.qrel"
        docker-compose -f compose/trec/docker-compose.yaml run trec trec_eval -q -m "recall"  $GT $RESULT_FILE
        ;;
    * )
        echo "Invalid option ${1}" ;;
esac
