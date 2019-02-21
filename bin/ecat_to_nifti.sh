#!/usr/bin/env bash

BIN_PATH="$( cd "$(dirname "$0")" ; pwd -P )"
PACKAGE_PATH="$BIN_PATH/.."

source "$PACKAGE_PATH"/.venv/bin/activate

PIPENV_VENV_IN_PROJECT=1 PYTHONPATH=$PACKAGE_PATH "$BIN_PATH"/ecat_to_nifti.py $*
