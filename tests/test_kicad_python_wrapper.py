import pytest
from unittest.mock import Mock, patch
from src.kicad_python_wrapper import KicadPythonWrapper

class TestKicadPythonWrapper:
    @pytest.fixture
    def wrapper(self):
        return KicadPythonWrapper()

    @patch('pcbnew.GetBuildVersion')
    def test_kicad_initialization(self, mock_version, wrapper):
        mock_version.return_value = "7.0.0"
        assert wrapper.initialize()
        
    def test_path_handling(self, wrapper):
        test_path = "test/path/file.kicad_pcb"
        assert wrapper.normalize_path(test_path)
        
    def test_reinitialize(self, wrapper):
        assert wrapper.reinitialize()
        
    def test_sync_project(self, wrapper):
        assert wrapper.sync_project("test_project")
