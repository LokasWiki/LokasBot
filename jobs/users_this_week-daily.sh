#!/bin/bash
set -euo pipefail

. "$HOME"/repos/.venvs/bin/activate

python3 "$HOME"/repos/users_this_week/daily.py