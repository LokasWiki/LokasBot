#!/bin/bash
#set -euo pipefail

. "$HOME"/repos/.venvs/lokas-bot-scripts/bin/activate

export PYWIKIBOT_DIR="$HOME/repos"

export PYTHONPATH="${PYTHONPATH}:$HOME/repos"


python3  "$HOME"/repos/tasks/ci_cd_log_task/main.py

# Exit the script after running all the Python files
exit 0
