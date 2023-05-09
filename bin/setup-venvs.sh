#!/bin/bash
# shellcheck disable=SC1090
set -euo pipefail

mkdir -p "$HOME/repos/.venvs"

function setup-venv {
    echo "Setting up $1"
    rm -fdr "$HOME/repos/.venvs/$1"
    python3 -m venv "$HOME/repos/.venvs/$1"
    . "$HOME/repos/.venvs/$1/bin/activate"
    python3 -m pip install -U pip setuptools wheel
    python -m pip install pywikibot
    # shellcheck disable=SC2086
    python3 -m pip install $2
    deactivate
    echo "=========================\end setup $1\n========================="
}

setup-venv lokas-bot-scripts "-U -r $HOME/repos/requirements.txt"

#setup-venv pwb "-e $HOME/repos/pywikibot[mwoauth,mwparserfromhell,mysql]"

