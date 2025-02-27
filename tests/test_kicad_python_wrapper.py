from src.integration.kicad_python_wrapper import KicadPythonWrapper
import pytest
import platform
import sys

class TestKicadPythonWrapper:
    def test_kicad_initialization(self, windows_only):
        """Test KiCad wrapper initialization"""
        wrapper = KicadPythonWrapper()
        assert wrapper.initialized == False
        assert wrapper.kicad_version is not None

    def test_path_handling(self, windows_only):
        """Test Windows-specific path handling"""
        wrapper = KicadPythonWrapper()
        test_path = wrapper._normalize_path("C:\\Program Files\\KiCad\\")
        assert '\\' in test_path

    def test_reinitialize(self, windows_only):
        """Test reinitialization of KiCad integration"""
        wrapper = KicadPythonWrapper()
        assert wrapper.reinitialize() == True
        assert wrapper.initialized == True

    def test_sync_project(self, windows_only, tmp_path):
        """Test project synchronization"""
        wrapper = KicadPythonWrapper()
        project_path = tmp_path / "test_project"
        project_path.mkdir()
        
        # Create a dummy .kicad_pcb file
        board_file = project_path / "test_project.kicad_pcb"
        board_file.write_text("(kicad_pcb (version 20221018))")
        
        assert wrapper.sync_project(str(project_path)) == True
        assert wrapper.project_path == str(project_path)
