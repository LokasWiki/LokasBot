#!/bin/bash
#set -euo pipefail


. "$HOME"/repos/.venvs/lokas-bot-scripts/bin/activate

export PYWIKIBOT_DIR="$HOME/repos"
export PYTHONPATH="${PYTHONPATH}:$HOME/repos"


python3 "$HOME"/repos/tasks/missingtopics/update.py
python3 "$HOME"/repos/tasks/distribute_medals/run.py



myArrayFiles=( "$HOME"/repos/tasks/statistics/cite_q.py )

run_file() {
    python3 "$1"  || (echo "Error running file $1" && false)
}

for file in "${myArrayFiles[@]}"; do
    run_file "$file"
done

# Exit the script after running all the Python files
exit 0
