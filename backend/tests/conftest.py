import sys
from pathlib import Path

# Ensure project root is on sys.path so 'backend' package can be imported
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
