
import pytest
import platform
import sys
import os

# Mock pcbnew module for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
try:
    import mock_pcbnew
    sys.modules['pcbnew'] = mock_pcbnew
except ImportError:
    sys.modules['pcbnew'] = MagicMock()

@pytest.fixture
def windows_only():
    """Skip test if not on Windows."""
    if platform.system() != 'Windows':
        pytest.skip("This test only runs on Windows")
    return True

@pytest.fixture(scope="session", autouse=True)
def platform_info():
    return {"system": platform.system()}
