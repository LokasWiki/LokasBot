#!/bin/bash
#set -euo pipefail

. "$HOME"/repos/.venvs/lokas-bot-scripts/bin/activate

export PYWIKIBOT_DIR="$HOME/repos"

export PYTHONPATH="${PYTHONPATH}:$HOME/repos"


python3  "$HOME"/repos/tasks/maintenance/task/portal_aliases.py
python3  "$HOME"/repos/tasks/maintenance/task/awb/template_redirects.py
python3  "$HOME"/repos/tasks/maintenance/task/awb/rename_template_parameters.py
python3  "$HOME"/repos/tasks/maintenance/task/skip/ignore_pages.py
python3  "$HOME"/repos/tasks/maintenance/check.py
python3  "$HOME"/repos/tasks/maintenance/task/portals_merge.py
python3  "$HOME"/repos/tasks/maintenance/task/protection/protection_add.py
python3  "$HOME"/repos/tasks/maintenance/task/protection/protection_remove.py

# Exit the script after running all the Python files
exit 0
