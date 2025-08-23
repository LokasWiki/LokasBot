"""
Legacy entry point for medal distribution.

This file is maintained for backward compatibility.
The new clean architecture implementation is in presentation/cli/main.py
"""

import sys
from tasks.distribute_medals.presentation.cli.main import main

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
