
import pytest
import sys
from pathlib import Path

def pytest_configure(config):
    """Configure pytest for Windows-only testing."""
    if sys.platform != 'win32':
        raise pytest.UsageError("These tests can only be run on Windows")

@pytest.fixture
def normalize_path():
    """Normalize paths for Windows comparison."""
    def _normalize(path):
        return str(Path(path).resolve())
    return _normalize

@pytest.fixture
def test_image_path():
    """Provide test image path in Windows format."""
    return str(Path(__file__).parent / 'test_files' / 'test_image.png')
