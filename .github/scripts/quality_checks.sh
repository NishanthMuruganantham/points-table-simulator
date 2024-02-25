#!/bin/bash

if [ "$1" == 'pylint_check' ]; then
    venv/bin/python -m pylint $(git ls-files 'src/*.py')
else
    venv/bin/python -m isort --check $(git ls-files 'src/*.py')
fi
