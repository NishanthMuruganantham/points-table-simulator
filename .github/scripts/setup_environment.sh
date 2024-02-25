#!/bin/bash

# Create virtual environment
bash create_venv.sh

# Install dependencies based on check type
source venv/bin/activate
if [ "$1" == 'pylint_check' ]; then
    pip install pylint
else
    pip install isort
fi
