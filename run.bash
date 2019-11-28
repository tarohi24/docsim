#!/bin/bash

COMPOSE_FILE="docker-compose.yaml"

case $1 in
    "exp" )
        SCRIPT="scripts/exp.py"
        docker-compose -f ${COMPOSE_FILE} run --rm -e IS_TEST=0 python python "/workplace/${SCRIPT}" ${@:2}
        ;;
    "trec" )
        PREC_FILE=$2
        DATASET=(${PREC_FILE//\// })
        DATASET=${DATASET[1]}
        docker-compose -f compose/trec/docker-compose.yaml run --rm trec trec_eval -m recall -q results/${DATASET}/gt.qrel $PREC_FILE
        ;;
    "test" )
        if [ "${#@}" -eq 1 ]
        then
            options="/workplace/docsim/tests"
        else
            options=${@:2}
        fi
        docker-compose -f ${COMPOSE_FILE} run --workdir="/workplace" -e IS_TEST=1 --rm python pytest ${options}
        ;;
    "python" )
        docker-compose run --workdir="/workplace" -e IS_TEST=0 --rm python python ${@:2}
        ;;
    "lint" )
        docker-compose run -e IS_TEST=0 --rm python make lint
        ;;
    "bash" )
        docker-compose -f ${COMPOSE_FILE} run --rm python bash
        ;;
    "jnote" )
        docker-compose up jnote
        ;;
    "spm" )
        docker-compose -f ${COMPOSE_FILE} run --rm spm bash
        ;;
    * )
        echo "Invalid option ${1}" ;;
esac
