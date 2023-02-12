#!/bin/bash
#set -euo pipefail

. "$HOME"/repos/.venvs/lokas-bot-scripts/bin/activate

export PYWIKIBOT_DIR="$HOME/repos"

python3  "$HOME"/repos/app/tasks/maintenance/read.py "$1"

# Exit the script after running all the Python files
exit 0
