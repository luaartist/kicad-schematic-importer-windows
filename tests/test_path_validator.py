import pytest
from pathlib import Path
from src.utils.path_validator import PathValidator

class TestPathValidator:
    def test_windows_executable_validation(self, windows_only):
        """Test Windows executable path validation"""
        validator = PathValidator()
        assert validator.is_safe_executable('C:\\Program Files\\KiCad\\bin\\kicad.exe')
        assert not validator.is_safe_executable('/usr/bin/kicad')

    def test_windows_path_normalization(self, windows_only):
        """Test Windows path normalization"""
        validator = PathValidator()
        normalized = validator.normalize_path('C:/Program Files/KiCad')
        assert normalized == 'C:\\Program Files\\KiCad'
