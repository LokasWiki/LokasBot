#!/bin/bash
#set -euo pipefail


. "$HOME"/repos/.venvs/lokas-bot-scripts/bin/activate

export PYWIKIBOT_DIR="$HOME/repos"
export PYTHONPATH="${PYTHONPATH}:$HOME/repos"


python3 "$HOME"/repos/tasks/distribute_medals/run.py


# Reusable dictionaries count (عدد المعاجم): loops over the قائمة list page,
# sums ↑ per subject page (redirects skipped) and saves the total on the
# .../إحصائيات/عدد المعاجم page so any wiki page can transclude it.
# Also refreshed at the start of every cite_q.py update (see its main).
myArrayFiles=( "$HOME"/repos/tasks/statistics/dictionaries_count.py )
# myArrayFiles+=( "$HOME"/repos/tasks/statistics/cite_q.py )

run_file() {
    python3 "$1"  || (echo "Error running file $1" && false)
}

for file in "${myArrayFiles[@]}"; do
    run_file "$file"
done

# Exit the script after running all the Python files
exit 0
