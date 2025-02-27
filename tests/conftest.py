import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import project modules directly
def pytest_configure(config):
    """
    Configure pytest to add the project root to the Python path
    """
    print("Configuring pytest to add project root to Python path")
    print(f"Current Python path: {sys.path}")
