#!/bin/bash
#set -euo pipefail

. "$HOME"/repos/.venvs/lokas-bot-scripts/bin/activate

export PYWIKIBOT_DIR="$HOME/repos"
export PYTHONPATH="${PYTHONPATH}:$HOME/repos"


python3  "$HOME"/repos/tasks/requests/link_replacement/load.py
python3  "$HOME"/repos/tasks/requests/template_distribution/load.py
python3  "$HOME"/repos/tasks/requests/add_category/load.py
python3  "$HOME"/repos/tasks/requests/portal_distribution/load.py
python3  "$HOME"/repos/tasks/requests/replace_template/load.py
python3  "$HOME"/repos/tasks/requests/cite/load.py


# Exit the script after running all the Python files
exit 0
