#!/bin/bash

IR_SCRIPT="scripts/experiments/ir.py"

case $1 in
    "ir" )
        docker-compose -f compose/python/docker-compose.yaml run python python "/workplace/${IR_SCRIPT}" ${@:1} ;;
    * )
        echo "Invalid option ${1}" ;;
esac
