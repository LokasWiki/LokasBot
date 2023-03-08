#!/bin/bash
#set -euo pipefail

. "$HOME"/repos/.venvs/lokas-bot-scripts/bin/activate

export PYWIKIBOT_DIR="$HOME/repos"

export PYTHONPATH="${PYTHONPATH}:$HOME/repos"

# maintenance tasks
python3  "$HOME"/repos/tasks/maintenance/read.py "$1"
python3  "$HOME"/repos/tasks/maintenance/task/add/orphan_remove.py "$1"
# web cite tasks
python3  "$HOME"/repos/tasks/webcite/read.py "$1"

# Exit the script after running all the Python files
exit 0
