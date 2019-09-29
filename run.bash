#!/bin/bash


COMPOSE_FILE="compose/python/docker-compose.yaml"

case $1 in
    "ir" )
        IR_SCRIPT="scripts/experiments/ir.py"
        docker-compose -f ${COMPOSE_FILE} run --rm python python "/workplace/${IR_SCRIPT}" ${@:2}
        ;;
    "trec" )
        DATASET=$2
        METHOD=$3
        RESULT_FILE="/workplace/results/ir/${DATASET}/${METHOD}.prel"
        GT="/workplace/results/ir/${DATASET}/en.valid.qrel"
        docker-compose -f compose/trec/docker-compose.yaml run --rm trec trec_eval -q -m "recall"  $GT $RESULT_FILE
        ;;
    "test" )
        if [ "${#@}" -eq 1 ]
        then
            options="/workplace/docsim/tests"
        else
            options=${@:2}
        fi
        docker-compose -f ${COMPOSE_FILE} run --workdir="/workplace" --rm python pytest ${options}
        ;;
    "python" )
        docker-compose -f ${COMPOSE_FILE} run --workdir="/workplace" --rm python python ${@:2}
        ;;
    "bash" )
        docker-compose -f ${COMPOSE_FILE} run --rm python bash
        ;;
    "jnote" )
        docker-compose -f ${COMPOSE_FILE} up -d jnote
        ;;
    * )
        echo "Invalid option ${1}" ;;
esac
