# This file makes the directory a Python package
# It allows the plugin to be imported by KiCad

# Import statements for the package
import os
import sys

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# For pytest compatibility, use absolute imports
if __name__ != "__main__" and __package__ is None:
    __package__ = os.path.basename(current_dir)

# Import the SchematicImporter class from action_plugin.py
try:
    # Use absolute import for pytest compatibility
    import action_plugin
    SchematicImporter = action_plugin.SchematicImporter
except Exception as e:
    import traceback
    traceback.print_exc()
