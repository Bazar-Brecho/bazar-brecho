#!/bin/sh
set -o errexit

# Change directory to the project root directory.
cd $(git rev-parse --show-toplevel)

# run mypy only in src/
mypy --config-file mypy.ini src/
