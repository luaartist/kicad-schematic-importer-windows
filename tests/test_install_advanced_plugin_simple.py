import os
import platform
import pytest
from pathlib import Path
from install_advanced_plugin_simple import find_kicad_plugin_dir, install_dependencies

def test_find_kicad_plugin_dir():
    """Test the plugin directory finder function"""
    test_version = "9.0"
    plugin_dir = find_kicad_plugin_dir(test_version)
    
    if platform.system() == "Windows":
        expected_path = os.path.join(os.path.expanduser("~"), "Documents", "KiCad", "9.0", "3rdparty", "plugins")
        assert plugin_dir == expected_path
    elif platform.system() == "Darwin":
        expected_path = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "kicad", "9.0", "scripting", "plugins")
        assert plugin_dir == expected_path
    else:
        expected_path = os.path.join(os.path.expanduser("~"), ".local", "share", "kicad", "9.0", "scripting", "plugins")
        assert plugin_dir == expected_path

def test_find_kicad_plugin_dir_different_version():
    """Test the plugin directory finder function with a different KiCad version"""
    test_version = "7.0"
    plugin_dir = find_kicad_plugin_dir(test_version)
    
    if platform.system() == "Windows":
        expected_path = os.path.join(os.getenv("APPDATA"), "kicad", "7.0", "scripting", "plugins")
        assert plugin_dir == expected_path
    elif platform.system() == "Darwin":
        expected_path = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "kicad", "7.0", "scripting", "plugins")
        assert plugin_dir == expected_path
    else:
        expected_path = os.path.join(os.path.expanduser("~"), ".local", "share", "kicad", "7.0", "scripting", "plugins")
        assert plugin_dir == expected_path

@pytest.mark.parametrize(
    "kicad_version, platform_system, expected_path",
    [
        ("9.0", "Windows", os.path.join(os.path.expanduser("~"), "Documents", "KiCad", "9.0", "3rdparty", "plugins")),  # windows_kicad_9
        ("7.0", "Windows", os.path.join(os.getenv("APPDATA"), "kicad", "7.0", "scripting", "plugins")),  # windows_kicad_7
        ("9.0", "Darwin", os.path.join(os.path.expanduser("~"), "Library", "Application Support", "kicad", "9.0", "scripting", "plugins")),  # macos_kicad_9
        ("7.0", "Darwin", os.path.join(os.path.expanduser("~"), "Library", "Application Support", "kicad", "7.0", "scripting", "plugins")),  # macos_kicad_7
        ("9.0", "Linux", os.path.join(os.path.expanduser("~"), ".local", "share", "kicad", "9.0", "scripting", "plugins")),  # linux_kicad_9
        ("7.0", "Linux", os.path.join(os.path.expanduser("~"), ".local", "share", "kicad", "7.0", "scripting", "plugins")),  # linux_kicad_7
    ],
    ids=["windows_kicad_9", "windows_kicad_7", "macos_kicad_9", "macos_kicad_7", "linux_kicad_9", "linux_kicad_7"]
)
def test_find_kicad_plugin_dir_parametrized(kicad_version, platform_system, expected_path, monkeypatch):
    """Test find_kicad_plugin_dir with various inputs using parametrization"""
    # Skip if not testing on the current platform
    if platform_system != platform.system():
        pytest.skip(f"This test is for {platform_system} only")
    
    # Test with the current platform
    result = find_kicad_plugin_dir(kicad_version)
    assert result == expected_path

def test_install_dependencies_mock(monkeypatch, tmp_path):
    """Test the dependency installation function with mocks"""
    # Create a temporary requirements.txt
    requirements_path = tmp_path / "requirements.txt"
    requirements_path.write_text("pytest>=7.0.0\n")
    
    # Mock subprocess.check_call to avoid actually installing packages
    def mock_check_call(args, **kwargs):
        return 0
    
    monkeypatch.setattr("subprocess.check_call", mock_check_call)
    monkeypatch.setattr("os.path.dirname", lambda x: str(tmp_path))
    monkeypatch.setattr("os.path.join", lambda *args: str(requirements_path))
    monkeypatch.setattr("os.path.exists", lambda x: True)
    
    # Call the function
    result = install_dependencies()
    
    # Check the result
    assert result == True
