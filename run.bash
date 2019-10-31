#!/bin/bash

# load dotenv
eval "$(cat .env/main.env <(echo) <(declare -x))"

COMPOSE_FILE="docker-compose.yaml"

case $1 in
    "exp" )
        SCRIPT="scripts/exp.py"
        docker-compose -f ${COMPOSE_FILE} run --rm -e IS_TEST=0 python python "/workplace/${SCRIPT}" ${@:2}
        ;;
    "trec" )
        DATASET=$2
        METHOD=$3
        RESULT_FILE="/workplace/results/ir/${DATASET}/${METHOD}.prel"
        GT="/workplace/results/ir/${DATASET}/gt.qrel"
        docker-compose -f compose/trec/docker-compose.yaml run --rm trec trec_eval -q  $GT $RESULT_FILE
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
        docker-compose -f ${COMPOSE_FILE} run --workdir="/workplace" -e IS_TEST=0 --rm python python ${@:2}
        ;;
    "lint" )
        docker-compose -f ${COMPOSE_FILE} run --workdir=${PROJECT_ROOT} -e IS_TEST=0 --rm lsp make lint
        ;;
    "bash" )
        docker-compose -f ${COMPOSE_FILE} run --rm python bash
        ;;
    "jnote" )
        docker-compose -f ${COMPOSE_FILE} up -d jnote
        ;;
    "spm" )
        docker-compose -f ${COMPOSE_FILE} run --rm spm bash
        ;;
    * )
        echo "Invalid option ${1}" ;;
esac
