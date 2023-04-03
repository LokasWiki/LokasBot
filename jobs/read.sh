#!/bin/bash
#set -euo pipefail

. "$HOME"/repos/.venvs/lokas-bot-scripts/bin/activate

export PYWIKIBOT_DIR="$HOME/repos"

export PYTHONPATH="${PYTHONPATH}:$HOME/repos"

python3  "$HOME"/repos/tasks/maintenance/read.py
python3  "$HOME"/repos/tasks/webcite/read.py
python3  "$HOME"/repos/tasks/maintenance/data/orphan/remove.py
python3  "$HOME"/repos/tasks/maintenance/data/orphan/add.py
python3  "$HOME"/repos/tasks/maintenance/data/unreviewed_article/remove.py
python3  "$HOME"/repos/tasks/maintenance/data/unreviewed_article/add.py

# Exit the script after running all the Python files
exit 0
