#!/usr/bin/env python
import argparse
import os
from pathlib import Path
import subprocess
from subprocess import check_output
import sys

from dotenv import load_dotenv

load_dotenv('.env/main.env')

compose_file = os.environ['COMPOSE_YAML']
service_name = os.environ['PYTHON_SERVICE']
type_ = sys.argv[1]

if type_ == 'bash':
    command =  f'docker-compose -f {compose_file} run --rm {service_name} bash'.split()
elif type_ == 'jnote':
    command =  f'docker-compose -f {compose_file} up -d jnote'.split()

subprocess.run(command)
