import os
import sys
import pytest

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def test_import_project_manager():
    """Test that we can import the HomeAutomationProjectManager class"""
    from src.core.project_manager import HomeAutomationProjectManager
    assert HomeAutomationProjectManager is not None
    
def test_create_project_manager_instance():
    """Test that we can create an instance of HomeAutomationProjectManager"""
    from src.core.project_manager import HomeAutomationProjectManager
    pm = HomeAutomationProjectManager(None)
    assert pm is not None
