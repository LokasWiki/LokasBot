#!/bin/bash
set -euo pipefail

. "$HOME"/repos/.venvs/lokas-bot-scripts/bin/activate

export PYWIKIBOT_DIR="$HOME/repos"

python3 "$HOME"/repos/tasks/users_this_week/week.py