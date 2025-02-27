import os
import sys
import pytest
import tempfile
import shutil
import cv2
import numpy as np
import subprocess
from unittest.mock import MagicMock, patch
from pathlib import Path

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.image_processor import ImageProcessor, HAS_POTRACE

class TestImageProcessor:
    """Test suite for ImageProcessor"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def test_image_path(self, temp_dir):
        """Create a test image for testing"""
        # Create a simple test image
        img_path = os.path.join(temp_dir, 'test_image.png')
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        # Draw a rectangle to simulate a component
        cv2.rectangle(img, (20, 20), (80, 80), (255, 255, 255), 2)
        cv2.imwrite(img_path, img)
        return img_path
    
    @pytest.fixture
    def image_processor(self):
        """Create an ImageProcessor instance"""
        with patch('builtins.print'):  # Suppress print statements during initialization
            processor = ImageProcessor()
            # Mock the tools availability
            processor.has_inkscape = False
            processor.has_potrace = False
            return processor
    
    def test_initialization(self, image_processor):
        """Test that the ImageProcessor initializes correctly"""
        assert hasattr(image_processor, 'ALLOWED_TOOLS')
        assert 'inkscape' in image_processor.ALLOWED_TOOLS
        assert 'potrace' in image_processor.ALLOWED_TOOLS
        assert hasattr(image_processor, 'has_inkscape')
        assert hasattr(image_processor, 'has_potrace')
    
    def test_check_tool_exists(self, image_processor):
        """Test checking if a tool exists"""
        # Test with allowed tools
        result = image_processor.check_tool_exists('inkscape')
        assert isinstance(result, bool)
        
        result = image_processor.check_tool_exists('potrace')
        assert isinstance(result, bool)
        
        # Test with disallowed tool
        result = image_processor.check_tool_exists('not_allowed_tool')
        assert result is False
    
    @patch('PIL.Image.open')
    def test_get_image_dpi(self, mock_open, image_processor, test_image_path):
        """Test getting image DPI"""
        # Mock the Image.open method
        mock_img = MagicMock()
        mock_img.info = {'dpi': (300, 300)}
        mock_open.return_value.__enter__.return_value = mock_img
        
        dpi = image_processor.get_image_dpi(test_image_path)
        assert dpi == 300.0
        mock_open.assert_called_once_with(test_image_path)
        
        # Test with no DPI info
        mock_img.info = {}
        dpi = image_processor.get_image_dpi(test_image_path)
        assert dpi == 96.0  # Default DPI
        
        # Test with exception
        mock_open.side_effect = Exception("Error opening image")
        dpi = image_processor.get_image_dpi(test_image_path)
        assert dpi is None
    
    @patch('shutil.which')
    @patch('subprocess.run')
    def test_convert_to_svg(self, mock_run, mock_which, image_processor, test_image_path, temp_dir):
        """Test converting an image to SVG"""
        # Mock the path validator to allow the Inkscape path
        with patch.object(image_processor.path_validator, 'is_safe_executable', return_value=True), \
             patch.object(image_processor.path_validator, 'is_safe_output_path', return_value=True), \
             patch('pathlib.Path.exists', return_value=True):
            
            # Mock the shutil.which method to return a path
            mock_which.return_value = 'C:\\Program Files\\Inkscape\\bin\\inkscape.exe'
            
            # Mock the subprocess.run method
            mock_run.return_value = MagicMock(returncode=0)
            
            output_path = os.path.join(temp_dir, 'output.svg')
            result = image_processor.convert_to_svg(test_image_path, output_path)
            
            assert result == output_path
            mock_which.assert_called_with('inkscape')
            mock_run.assert_called_once()

        # Test with Inkscape not found
        mock_which.return_value = None
        with pytest.raises(RuntimeError) as excinfo:
            image_processor.convert_to_svg(test_image_path, output_path)
        assert "No suitable conversion tool found" in str(excinfo.value)

        # Test with timeout
        mock_which.return_value = '/usr/bin/inkscape'
        mock_run.side_effect = subprocess.TimeoutExpired(cmd='inkscape', timeout=30)
        with pytest.raises(TimeoutError) as excinfo:
            image_processor.convert_to_svg(test_image_path, output_path)
        assert "SVG conversion timed out" in str(excinfo.value)
    
    @patch.object(ImageProcessor, '_vectorize_with_inkscape')
    @patch.object(ImageProcessor, '_vectorize_with_potrace')
    @patch.object(ImageProcessor, '_vectorize_builtin')
    def test_vectorize_image(self, mock_builtin, mock_potrace, mock_inkscape, image_processor, test_image_path):
        """Test vectorizing an image"""
        # Set up the mocks
        vector_path = test_image_path.replace('.png', '.svg')
        
        # Test with Inkscape available
        image_processor.has_inkscape = True
        mock_inkscape.return_value = vector_path
        
        result = image_processor.vectorize_image(test_image_path)
        assert result == vector_path
        mock_inkscape.assert_called_once_with(test_image_path)
        mock_potrace.assert_not_called()
        mock_builtin.assert_not_called()
        
        # Reset mocks
        mock_inkscape.reset_mock()
        mock_potrace.reset_mock()
        mock_builtin.reset_mock()
        
        # Test with Inkscape failing, Potrace available
        image_processor.has_inkscape = True
        image_processor.has_potrace = True
        mock_inkscape.side_effect = Exception("Inkscape failed")
        mock_potrace.return_value = vector_path
        
        result = image_processor.vectorize_image(test_image_path)
        assert result == vector_path
        mock_inkscape.assert_called_once_with(test_image_path)
        mock_potrace.assert_called_once_with(test_image_path)
        mock_builtin.assert_not_called()
        
        # Reset mocks
        mock_inkscape.reset_mock()
        mock_potrace.reset_mock()
        mock_builtin.reset_mock()
        
        # Test with all methods failing
        mock_inkscape.side_effect = Exception("Inkscape failed")
        mock_potrace.side_effect = Exception("Potrace failed")
        mock_builtin.side_effect = Exception("Builtin failed")
        
        with pytest.raises(ValueError) as excinfo:
            image_processor.vectorize_image(test_image_path)
        assert "All vectorization methods failed" in str(excinfo.value)
    
    @patch('shutil.which')
    @patch('subprocess.run')
    @patch('pathlib.Path.exists')
    def test_vectorize_with_inkscape(self, mock_exists, mock_run, mock_which, image_processor, test_image_path):
        """Test vectorizing with Inkscape"""
        # Mock the methods
        mock_which.return_value = '/usr/bin/inkscape'
        mock_run.return_value = MagicMock(returncode=0)
        mock_exists.return_value = True
        
        vector_path = test_image_path.replace('.png', '.svg')
        result = image_processor._vectorize_with_inkscape(test_image_path)
        
        assert result == vector_path
        mock_which.assert_called_once_with('inkscape')
        mock_run.assert_called_once()
        
        # Test with output file not created
        mock_exists.return_value = False
        with pytest.raises(ValueError) as excinfo:
            image_processor._vectorize_with_inkscape(test_image_path)
        assert "Inkscape failed to create output file" in str(excinfo.value)
    
    @patch('shutil.which')
    @patch('subprocess.run')
    @patch('pathlib.Path.exists')
    def test_vectorize_with_potrace(self, mock_exists, mock_run, mock_which, image_processor, test_image_path):
        """Test vectorizing with Potrace"""
        with patch.object(image_processor.path_validator, 'is_safe_executable', return_value=True), \
             patch('os.path.exists', return_value=True):  # Mock os.path.exists too
        
            # Mock the methods
            mock_which.return_value = 'C:\\Program Files\\Potrace\\potrace.exe'
            mock_run.return_value = MagicMock(returncode=0)
            mock_exists.return_value = True
        
            vector_path = test_image_path.replace('.png', '.svg')
            result = image_processor._vectorize_with_potrace(test_image_path)
        
            assert os.path.normcase(result) == os.path.normcase(vector_path)
            mock_which.assert_called_once_with('potrace')
            mock_run.assert_called_once()
        
            # Reset mocks
            mock_exists.reset_mock()
            mock_run.reset_mock()
        
            # Test with output file not created
            mock_exists.return_value = False
            with pytest.raises(ValueError) as excinfo:
                image_processor._vectorize_with_potrace(test_image_path)
            assert "Potrace failed to create output file" in str(excinfo.value)
    
    @pytest.mark.skipif(not HAS_POTRACE, reason="Potrace library not available")
    def test_vectorize_builtin(self, image_processor, test_image_path):
        """Test built-in vectorization"""
        # This test only runs if potrace is available
        vector_path = test_image_path.replace('.png', '.svg')
        
        # Test with valid image
        result = image_processor._vectorize_builtin(test_image_path)
        assert result == vector_path
        assert os.path.exists(vector_path)
        
        # Test with invalid image
        with pytest.raises(ValueError) as excinfo:
            image_processor._vectorize_builtin('nonexistent.png')
        assert "Failed to load image" in str(excinfo.value)
    
    def test_generate_svg(self, image_processor):
        """Test generating SVG from potrace path"""
        # Create a mock path
        mock_path = MagicMock()
        
        # Create a mock curve
        mock_curve = MagicMock()
        
        # Create mock segments
        mock_segment1 = MagicMock()
        mock_segment1.start_point = (10, 10)
        mock_segment1.end_point = (20, 20)
        mock_segment1.is_corner = True
        
        mock_segment2 = MagicMock()
        mock_segment2.start_point = (20, 20)
        mock_segment2.end_point = (30, 10)
        mock_segment2.is_corner = False
        mock_segment2.c1 = (22, 22)
        mock_segment2.c2 = (28, 12)
        
        # Add segments to curve
        mock_curve.__iter__.return_value = [mock_segment1, mock_segment2]
        
        # Add curve to path
        mock_path.__iter__.return_value = [mock_curve]
        
        # Call the method
        svg = image_processor._generate_svg(mock_path)
        
        # Check that the SVG contains the expected elements
        assert '<?xml version="1.0" encoding="UTF-8"?>' in svg
        assert '<svg xmlns="http://www.w3.org/2000/svg" version="1.1">' in svg
        assert '<path d=' in svg
        assert 'M 10,10 L 20,20' in svg
        assert 'C 22,22 28,12 30,10' in svg
