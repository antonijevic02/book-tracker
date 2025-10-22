# tests/conftest.py
import os
import sys

# Add project root to sys.path so "from app import app" works no matter where pytest is run
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)