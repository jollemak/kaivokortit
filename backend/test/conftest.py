import sys
from pathlib import Path

# Make the backend root importable from inside the test/ subdirectory
sys.path.insert(0, str(Path(__file__).parent.parent))
