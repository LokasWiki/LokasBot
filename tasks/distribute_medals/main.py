"""
Main entry point for the medal distribution system.

This module provides a clean interface to the medal distribution
application using Clean Architecture principles.

Usage:
    # Production mode
    python -m tasks.distribute_medals.main

    # Test mode
    python -m tasks.distribute_medals.main --test
"""

import sys
from tasks.distribute_medals.presentation.cli.main import main

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))