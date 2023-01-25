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
    python -m pip install "requests>=2.20.1"
    python -m pip install "mwparserfromhell>=0.5.0"
    python -m pip install "wikitextparser>=0.47.5"
    python -m pip install pywikibot
    # shellcheck disable=SC2086
    python3 -m pip install $2
    deactivate
}

setup-venv lokas-bot-scripts "-U -r $HOME/repos/requirements.txt"

setup-venv lokas-bot-web "-U -r $HOME/repos/LokasBot-web/requirements.txt"

setup-venv pwb "-e $HOME/repos/pywikibot[mwoauth,mwparserfromhell,mysql]"

