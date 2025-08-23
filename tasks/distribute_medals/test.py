"""
Legacy test entry point for medal distribution.

This file is maintained for backward compatibility.
The new clean architecture test mode is available by running:
    python -m tasks.distribute_medals.presentation.cli.main --test
"""

import sys
from tasks.distribute_medals.presentation.cli.main import main

if __name__ == "__main__":
    # Force test mode
    sys.exit(main("--test"))
