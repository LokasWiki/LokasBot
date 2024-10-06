#!/bin/bash
#set -euo pipefail

. "$HOME"/repos/.venvs/lokas-bot-scripts/bin/activate

export PYWIKIBOT_DIR="$HOME/repos"
export PYTHONPATH="${PYTHONPATH}:$HOME/repos"


# python3  "$HOME"/repos/tasks/requests/link_replacement/read.py
# python3  "$HOME"/repos/tasks/requests/template_distribution/read.py
# python3  "$HOME"/repos/tasks/requests/add_category/read.py
# python3  "$HOME"/repos/tasks/requests/portal_distribution/read.py
# python3  "$HOME"/repos/tasks/requests/replace_template/read.py
# python3  "$HOME"/repos/tasks/requests/cite/read.py
# python3  "$HOME"/repos/tasks/requests/remove/read.py
#python3  "$HOME"/repos/tasks/check_usernames/check/check.py
python3  "$HOME"/repos/tasks/statistics/auto_update/cite_q.py

# Exit the script after running all the Python files
exit 0
