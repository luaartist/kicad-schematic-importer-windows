import os
import pytest
import platform
from pathlib import Path
from install_advanced_plugin_fixed_v2 import find_kicad_plugin_dir, install_dependencies

def test_find_kicad_plugin_dir():
    """Test finding KiCad plugin directory"""
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
    """Test finding KiCad plugin directory with different version"""
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

def test_install_dependencies_mock(monkeypatch, tmp_path):
    """Test installing dependencies with mocked subprocess"""
    # Create a temporary requirements.txt
    requirements_path = tmp_path / "requirements.txt"
    requirements_path.write_text("pytest>=7.0.0\n")
    
    # Mock subprocess.check_call
    def mock_check_call(args, **kwargs):
        return 0
    
    monkeypatch.setattr("subprocess.check_call", mock_check_call)
    monkeypatch.setattr("os.path.dirname", lambda x: str(tmp_path))
    monkeypatch.setattr("os.path.join", lambda *args: str(requirements_path))
    monkeypatch.setattr("os.path.exists", lambda x: True)
    
    # Test installing dependencies
    result = install_dependencies()
    assert result == True
