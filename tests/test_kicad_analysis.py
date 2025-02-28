import pytest

@pytest.fixture
def sample_yaml_content():
    return """
    version: 1.0
    settings:
        debug: true
    """

def test_analyze_yaml_files(sample_yaml_content):  # Fix: Use fixture as parameter
    # Test implementation
    pass

def test_fix_yaml_files(sample_yaml_content):  # Fix: Use fixture as parameter
    # Test implementation
    pass
