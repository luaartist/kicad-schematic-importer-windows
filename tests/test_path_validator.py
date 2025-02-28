import pytest
from pathlib import Path
import platform
import os
import tempfile
from unittest.mock import patch
from src.utils.path_validator import PathValidator

class TestPathValidator:
    @pytest.fixture
    def validator(self):
        return PathValidator()

    @pytest.fixture
    def platform_paths(self):
        """Platform-specific test paths."""
        if platform.system() == "Windows":
            return {
                'safe_exec': 'C:\\Program Files\\Test\\test.exe',
                'unsafe_exec': 'D:\\Unsafe\\test.exe',
                'safe_output': os.path.join(tempfile.gettempdir(), 'test.txt'),
                'unsafe_output': 'C:\\Unsafe\\test.txt'
            }
        return {
            'safe_exec': '/usr/bin/test',
            'unsafe_exec': '/tmp/unsafe/test',
            'safe_output': '/tmp/test.txt',
            'unsafe_output': '/var/unsafe/test.txt'
        }

    @pytest.mark.parametrize("os_name,path,expected", [
        ("Windows", "C:\\Program Files\\Test\\test.exe", True),
        ("Windows", "D:\\Unsafe\\test.exe", False),
    ])
    def test_is_safe_executable_windows(self, validator, os_name, path, expected):
        """Test executable validation on Windows."""
        # Skip if not on Windows
        if platform.system() != "Windows":
            pytest.skip("Test only runs on Windows")
            
        with patch.object(Path, 'exists', return_value=True):
            assert validator.is_safe_executable(path) == expected
            
    @pytest.mark.parametrize("path,expected", [
        ("/usr/bin/test", True),
        ("/tmp/unsafe/test", False),
    ])
    def test_is_safe_executable_linux(self, validator, path, expected):
        """Test executable validation on Linux."""
        # Skip if not on Linux
        if platform.system() != "Linux":
            pytest.skip("Test only runs on Linux")
            
        with patch.object(Path, 'exists', return_value=True):
            assert validator.is_safe_executable(path) == expected

    def test_path_normalization(self, validator):
        """Test path normalization."""
        test_path = "test/path"
        normalized = validator.normalize_path(test_path)
        assert isinstance(normalized, str)
        assert Path(normalized).is_absolute()

    def test_unsafe_path_different_drive(self, validator):
        """Test path validation with different drives on Windows."""
        if platform.system() == "Windows":
            with patch.object(Path, 'exists', return_value=True):
                assert not validator.is_safe_executable("D:\\Different\\Drive\\test.exe")

    def test_is_safe_output_path(self, validator, tmp_path):
        """Test output path validation."""
        # Test temp directory path
        temp_file = tmp_path / "test.txt"
        assert validator.is_safe_output_path(temp_file)

        # Test current working directory path
        cwd_file = Path.cwd() / "test.txt"
        assert validator.is_safe_output_path(cwd_file)

        # Test unsafe path
        unsafe_path = Path("/unsafe/path/test.txt")
        assert not validator.is_safe_output_path(unsafe_path)
