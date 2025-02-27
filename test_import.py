import os
import sys

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Try to import the module
try:
    from project_manager import HomeAutomationProjectManager
    print("Successfully imported HomeAutomationProjectManager")
    
    # Try to create an instance
    pm = HomeAutomationProjectManager(None)
    print("Successfully created HomeAutomationProjectManager instance")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("Python path:", sys.path)
print("Current directory:", os.getcwd())
print("Files in current directory:", os.listdir("."))
