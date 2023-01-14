#!/bin/bash
# shellcheck disable=SC1090
set -euo pipefail

mkdir -p "$HOME/repos/.venvs"

function setup-venv {
    echo "Setting up"
    rm -fdr "$HOME/repos/.venvs/"
    python3 -m venv "$HOME/repos/.venvs/"
    . "$HOME/repos/.venvs/bin/activate"
    python3 -m pip install -U pip setuptools wheel
    # shellcheck disable=SC2086
    #python3 -m pip install $2
    deactivate
}

setup-venv lokas-bot-scripts "-U -r $HOME/repos/requirements.txt"

setup-venv pwb "-e $HOME/repos/pywikibot[mwoauth,mwparserfromhell,mysql]"
