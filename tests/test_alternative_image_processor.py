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

def normalize_path(path: str) -> str:
    """Normalize path for comparison in tests."""
    return os.path.normcase(os.path.normpath(str(Path(path).resolve())))

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.alternative_image_processor import AlternativeImageProcessor

class TestAlternativeImageProcessor:
    """Test suite for AlternativeImageProcessor"""
    
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
            return AlternativeImageProcessor()
    
    def test_initialization(self, image_processor):
        """Test that the ImageProcessor initializes correctly"""
        assert hasattr(image_processor, 'ALLOWED_TOOLS')
        assert 'inkscape' in image_processor.ALLOWED_TOOLS
        assert 'autotrace' in image_processor.ALLOWED_TOOLS
        assert 'opencv' in image_processor.ALLOWED_TOOLS
        assert hasattr(image_processor, 'has_inkscape')
        assert hasattr(image_processor, 'has_autotrace')
        assert hasattr(image_processor, 'has_opencv')
        assert image_processor.has_opencv is True
    
    def test_check_tool_exists(self, image_processor):
        """Test checking if a tool exists"""
        # Test with allowed tools
        result = image_processor.check_tool_exists('inkscape')
        assert isinstance(result, bool)
        
        result = image_processor.check_tool_exists('autotrace')
        assert isinstance(result, bool)
        
        # Test with disallowed tool
        result = image_processor.check_tool_exists('not_allowed_tool')
        assert result is False
    
    def test_get_image_dpi(self, image_processor, test_image_path):
        """Test getting image DPI"""
        dpi = image_processor.get_image_dpi(test_image_path)
        assert dpi == 96.0
        
        # Test with non-existent image
        with patch('cv2.imread', return_value=None):
            dpi = image_processor.get_image_dpi('nonexistent.png')
            assert dpi is None
        
        # Test with exception
        with patch('cv2.imread', side_effect=Exception("Error opening image")):
            dpi = image_processor.get_image_dpi(test_image_path)
            assert dpi is None
    
    @patch('shutil.which')
    @patch('subprocess.run')
    @patch('pathlib.Path.exists')
    def test_convert_to_svg(self, mock_exists, mock_run, mock_which, image_processor, test_image_path, temp_dir):
        """Test converting an image to SVG"""
        mock_which.return_value = 'C:\\Program Files\\Inkscape\\bin\\inkscape.exe'
        mock_run.return_value = MagicMock(returncode=0)
        
        # Mock Path.exists to return True for all paths
        mock_exists.return_value = True
        
        output_path = os.path.join(temp_dir, 'output.svg')
        result = image_processor.convert_to_svg(test_image_path, output_path)
        
        assert normalize_path(result) == normalize_path(output_path)
        
        # Test with non-existent input file
        # Set up exists() to return False for input file
        def exists_side_effect_no_input(path):
            if test_image_path in str(path):
                return False
            return True
        mock_exists.side_effect = exists_side_effect_no_input
        
        with pytest.raises(ValueError) as excinfo:
            image_processor.convert_to_svg('nonexistent.png', output_path)
        assert "Input file not found" in str(excinfo.value)
        
        # Reset mock
        mock_exists.side_effect = None
        mock_exists.return_value = True
        
        # Test with non-existent output directory
        with pytest.raises(ValueError) as excinfo:
            image_processor.convert_to_svg(test_image_path, '/nonexistent/dir/output.svg')
        assert "Output directory does not exist" in str(excinfo.value)
        
        # Test with Inkscape not found
        mock_which.return_value = None
        with pytest.raises(RuntimeError) as excinfo:
            image_processor.convert_to_svg(test_image_path, output_path)
        assert "Inkscape not found" in str(excinfo.value)
        
        # Test with timeout
        mock_which.return_value = '/usr/bin/inkscape'
        mock_run.side_effect = subprocess.TimeoutExpired(cmd='inkscape', timeout=30)
        with pytest.raises(TimeoutError) as excinfo:
            image_processor.convert_to_svg(test_image_path, output_path)
        assert "SVG conversion timed out" in str(excinfo.value)
    
    @patch.object(AlternativeImageProcessor, '_vectorize_with_inkscape')
    @patch.object(AlternativeImageProcessor, '_vectorize_with_autotrace')
    @patch.object(AlternativeImageProcessor, '_vectorize_with_opencv')
    def test_vectorize_image(self, mock_opencv, mock_autotrace, mock_inkscape, image_processor, test_image_path):
        """Test vectorizing an image"""
        # Set up the mocks
        vector_path = test_image_path.replace('.png', '.svg')
        
        # Test with Inkscape available
        image_processor.has_inkscape = True
        image_processor.has_autotrace = False
        mock_inkscape.return_value = vector_path
        
        result = image_processor.vectorize_image(test_image_path)
        assert result == vector_path
        mock_inkscape.assert_called_once_with(test_image_path)
        mock_autotrace.assert_not_called()
        mock_opencv.assert_not_called()
        
        # Reset mocks
        mock_inkscape.reset_mock()
        mock_autotrace.reset_mock()
        mock_opencv.reset_mock()
        
        # Test with Inkscape failing, AutoTrace available
        image_processor.has_inkscape = True
        image_processor.has_autotrace = True
        mock_inkscape.side_effect = Exception("Inkscape failed")
        mock_autotrace.return_value = vector_path
        
        result = image_processor.vectorize_image(test_image_path)
        assert result == vector_path
        mock_inkscape.assert_called_once_with(test_image_path)
        mock_autotrace.assert_called_once_with(test_image_path)
        mock_opencv.assert_not_called()
        
        # Reset mocks
        mock_inkscape.reset_mock()
        mock_autotrace.reset_mock()
        mock_opencv.reset_mock()
        
        # Test with both Inkscape and AutoTrace failing, OpenCV as fallback
        image_processor.has_inkscape = True
        image_processor.has_autotrace = True
        mock_inkscape.side_effect = Exception("Inkscape failed")
        mock_autotrace.side_effect = Exception("AutoTrace failed")
        mock_opencv.return_value = vector_path
        
        result = image_processor.vectorize_image(test_image_path)
        assert result == vector_path
        mock_inkscape.assert_called_once_with(test_image_path)
        mock_autotrace.assert_called_once_with(test_image_path)
        mock_opencv.assert_called_once_with(test_image_path)
        
        # Reset mocks
        mock_inkscape.reset_mock()
        mock_autotrace.reset_mock()
        mock_opencv.reset_mock()
        
        # Test with all methods failing
        mock_inkscape.side_effect = Exception("Inkscape failed")
        mock_autotrace.side_effect = Exception("AutoTrace failed")
        mock_opencv.side_effect = Exception("OpenCV failed")
        
        with pytest.raises(ValueError) as excinfo:
            image_processor.vectorize_image(test_image_path)
        assert "All vectorization methods failed" in str(excinfo.value)
    
    @patch('shutil.which')
    @patch('subprocess.run')
    @patch('pathlib.Path.exists')
    def test_vectorize_with_inkscape(self, mock_exists, mock_run, mock_which, image_processor, test_image_path):
        """Test vectorizing with Inkscape"""
        # Mock the methods
        mock_which.return_value = 'C:\\Program Files\\Inkscape\\bin\\inkscape.exe'
        mock_run.return_value = MagicMock(returncode=0)
        
        # Set up exists() to return True for all paths initially
        mock_exists.return_value = True
        
        vector_path = test_image_path.replace('.png', '.svg')
        
        # Test successful conversion
        result = image_processor._vectorize_with_inkscape(test_image_path)
        assert normalize_path(result) == normalize_path(vector_path)
        
        # Test output file not created
        # Set up exists() to return True for input, False for output
        def exists_side_effect(path):
            path_str = str(path)
            if '.svg' in path_str:  # Output file
                return False
            return True
        mock_exists.side_effect = exists_side_effect
        
        with pytest.raises(ValueError) as excinfo:
            image_processor._vectorize_with_inkscape(test_image_path)
        assert "Inkscape failed to create output file" in str(excinfo.value)
    
    @patch('shutil.which')
    @patch('subprocess.run')
    @patch('pathlib.Path.exists')
    def test_vectorize_with_autotrace(self, mock_exists, mock_run, mock_which, image_processor, test_image_path):
        """Test vectorizing with AutoTrace"""
        # Mock the methods
        mock_which.return_value = 'C:\\Program Files\\AutoTrace\\autotrace.exe'
        mock_run.return_value = MagicMock(returncode=0)
        
        # Set up exists() to return True for all paths initially
        mock_exists.return_value = True
        
        vector_path = test_image_path.replace('.png', '.svg')
        result = image_processor._vectorize_with_autotrace(test_image_path)
        
        assert normalize_path(result) == normalize_path(vector_path)
        mock_which.assert_called_once_with('autotrace')
        mock_run.assert_called_once()
        
        # Reset mocks
        mock_run.reset_mock()
        
        # Test with output file not created
        # Set up exists() to return True for input, False for output
        def exists_side_effect(path):
            path_str = str(path)
            if '.svg' in path_str:  # Output file
                return False
            return True
        mock_exists.side_effect = exists_side_effect
        
        with pytest.raises(ValueError) as excinfo:
            image_processor._vectorize_with_autotrace(test_image_path)
        assert "AutoTrace failed to create output file" in str(excinfo.value)
    
    @patch('cv2.imread')
    @patch('cv2.cvtColor')
    @patch('cv2.threshold')
    @patch('cv2.findContours')
    @patch('cv2.arcLength')
    @patch('cv2.approxPolyDP')
    @patch('svgwrite.Drawing')
    def test_vectorize_with_opencv(self, mock_drawing, mock_approx, mock_arclen, mock_contours, 
                                  mock_threshold, mock_cvtcolor, mock_imread, 
                                  image_processor, test_image_path):
        """Test vectorizing with OpenCV"""
        # Mock the methods
        mock_img = MagicMock()
        mock_imread.return_value = mock_img
        
        mock_gray = MagicMock()
        mock_cvtcolor.return_value = mock_gray
        
        mock_binary = MagicMock()
        mock_threshold.return_value = (None, mock_binary)
        
        # Create mock contours
        mock_contour = np.array([[[10, 10]], [[20, 20]], [[30, 10]]])
        mock_contours.return_value = ([mock_contour], None)
        
        mock_arclen.return_value = 100.0
        
        mock_approx_contour = np.array([[[10, 10]], [[20, 20]], [[30, 10]]])
        mock_approx.return_value = mock_approx_contour
        
        # Mock the SVG drawing
        mock_dwg = MagicMock()
        mock_drawing.return_value = mock_dwg
        mock_path = MagicMock()
        mock_dwg.path.return_value = mock_path
        mock_dwg.add.return_value = None
        
        vector_path = test_image_path.replace('.png', '.svg')
        result = image_processor._vectorize_with_opencv(test_image_path)
        
        assert result == vector_path
        mock_imread.assert_called_once_with(test_image_path)
        mock_cvtcolor.assert_called_once()
        mock_threshold.assert_called_once()
        mock_contours.assert_called_once()
        mock_drawing.assert_called_once()
        mock_dwg.save.assert_called_once()
        
        # Test with image loading failure
        mock_imread.return_value = None
        with pytest.raises(ValueError) as excinfo:
            image_processor._vectorize_with_opencv(test_image_path)
        assert "Failed to load image" in str(excinfo.value)
    
    def test_trace_bitmap(self, image_processor):
        """Test trace_bitmap method"""
        # Mock the vectorize_image method
        with patch.object(image_processor, 'vectorize_image') as mock_vectorize:
            mock_vectorize.return_value = 'output.svg'
            
            result = image_processor.trace_bitmap('input.png')
            
            assert result == 'output.svg'
            mock_vectorize.assert_called_once_with('input.png')
