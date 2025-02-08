import os
import sys
from pathlib import Path

# Add the project root to Python path for imports
project_root = str(Path(__file__).parent.parent.parent.parent)
sys.path.insert(0, project_root) 