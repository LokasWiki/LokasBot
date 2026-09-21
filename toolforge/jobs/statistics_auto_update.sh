#!/bin/bash
#set -euo pipefail

# On-demand statistics update.
#
# Reads the {{حدث الصفحة بالبوت}} flag (|حدث الصفحة = نعم) on the statistics
# pages and, only when it is set, refreshes them (e.g. cite_q). Kept in its own
# job so a stuck request pipeline (requests-raed) can never block it again.
# See tasks/statistics/auto_update/.

. "$HOME"/repos/.venvs/lokas-bot-scripts/bin/activate

export PYWIKIBOT_DIR="$HOME/repos"

export PYTHONPATH="${PYTHONPATH}:$HOME/repos"

python3  "$HOME"/repos/tasks/statistics/auto_update/cite_q.py

# Exit the script after running all the Python files
exit 0
