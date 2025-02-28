
import pytest
import platform
import sys
import os
from pathlib import Path
from unittest.mock import MagicMock

# Add mock module path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
try:
    import mock_pcbnew
    sys.modules['pcbnew'] = mock_pcbnew
except ImportError:
    sys.modules['pcbnew'] = MagicMock()

# Define a fixture to check if we're on Windows
@pytest.fixture
def windows_only():
    """Skip test if not on Windows."""
    if platform.system() != 'Windows':
        pytest.skip("This test only runs on Windows")
    return True

# Make platform info available to all tests
@pytest.fixture(scope="session", autouse=True)
def platform_info():
    """Add platform information to the pytest configuration."""
    return {
        "system": platform.system(),
        "python_version": sys.version,
        "is_windows": platform.system() == "Windows"
    }

@pytest.fixture
def normalize_path():
    """Normalize paths for comparison."""
    def _normalize(path):
        return str(Path(path).resolve())
    return _normalize

@pytest.fixture
def test_image_path():
    """Provide test image path."""
    return str(Path(__file__).parent / 'test_files' / 'test_image.png')
