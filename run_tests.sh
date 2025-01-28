#!/bin/bash

# Change to the code directory
cd "$(dirname "$0")"

# Run all sandbox tests
echo "Running all sandbox tests..."
python3 -m unittest tests/tasks/sandbox/test_*.py -v

# Run specific test file if provided
if [ "$1" ]; then
    echo "Running specific test file: $1"
    python3 -m unittest "$1" -v
fi 