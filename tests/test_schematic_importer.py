import os
import sys
import pytest
import tempfile
import shutil
import cv2
import numpy as np
from unittest.mock import MagicMock, patch

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.schematic_importer import SchematicImporter
from src.utils.image_processor import ImageProcessor

class TestSchematicImporter:
    """Test suite for SchematicImporter"""
    
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
    def test_vector_path(self, temp_dir):
        """Create a test vector file for testing"""
        # Create a simple SVG file
        svg_path = os.path.join(temp_dir, 'test_vector.svg')
        with open(svg_path, 'w') as f:
            f.write('<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"></svg>')
        return svg_path
    
    @pytest.fixture
    def schematic_importer(self):
        """Create a SchematicImporter instance"""
        return SchematicImporter()
    
    def test_initialization(self, schematic_importer):
        """Test that the SchematicImporter initializes correctly"""
        assert schematic_importer.config is not None
        assert isinstance(schematic_importer.image_processor, ImageProcessor)
        assert 'vector' in schematic_importer.supported_formats
        assert 'raster' in schematic_importer.supported_formats
    
    def test_validate_image_valid_png(self, schematic_importer, test_image_path):
        """Test validating a valid PNG image"""
        result = schematic_importer.validate_image(test_image_path)
        assert result is not None
        assert result['type'] == 'raster'
        assert result['needs_conversion'] is True
    
    def test_validate_image_valid_vector(self, schematic_importer, test_vector_path):
        """Test validating a valid vector image"""
        result = schematic_importer.validate_image(test_vector_path)
        assert result is not None
        assert result['type'] == 'vector'
        assert result['needs_conversion'] is False
    
    def test_validate_image_invalid_format(self, schematic_importer, temp_dir):
        """Test validating an image with invalid format"""
        # Create a file with unsupported extension
        invalid_path = os.path.join(temp_dir, 'invalid.txt')
        with open(invalid_path, 'w') as f:
            f.write('This is not an image')
        
        with pytest.raises(ValueError) as excinfo:
            schematic_importer.validate_image(invalid_path)
        assert "Unsupported file format" in str(excinfo.value)
    
    def test_validate_image_nonexistent(self, schematic_importer):
        """Test validating a non-existent image"""
        with pytest.raises(ValueError) as excinfo:
            schematic_importer.validate_image('nonexistent.png')
        assert "Could not load image" in str(excinfo.value)
    
    @patch('src.utils.image_processor.ImageProcessor.vectorize_image')
    def test_preprocess_image(self, mock_vectorize, schematic_importer, test_image_path):
        """Test preprocessing an image"""
        # Mock the vectorize_image method to return a path
        vector_path = test_image_path.replace('.png', '.svg')
        mock_vectorize.return_value = vector_path
        
        result = schematic_importer.preprocess_image(test_image_path)
        assert result == vector_path
        mock_vectorize.assert_called_once_with(test_image_path)
    
    @patch('src.utils.image_processor.ImageProcessor.vectorize_image')
    def test_preprocess_image_vectorization_failure(self, mock_vectorize, schematic_importer, test_image_path):
        """Test preprocessing an image when vectorization fails"""
        # Mock the vectorize_image method to raise an exception
        mock_vectorize.side_effect = Exception("Vectorization failed")
        
        with pytest.raises(ValueError) as excinfo:
            schematic_importer.preprocess_image(test_image_path)
        assert "Failed to vectorize image" in str(excinfo.value)
    
    @patch('pcbnew.Board')
    def test_import_from_image(self, mock_board, schematic_importer, test_image_path):
        """Test importing from an image"""
        # Mock the board
        board = MagicMock()
        
        # Call the method
        schematic_importer.import_from_image(test_image_path, board)
        
        # No assertions needed as the method is a placeholder
    
    def test_detect_components(self, schematic_importer):
        """Test detecting components in an image"""
        # Create a mock image
        image = np.zeros((100, 100, 3), dtype=np.uint8)
        
        # Call the method
        components = schematic_importer.detect_components(image)
        
        # Assert that it returns an empty list (placeholder implementation)
        assert components == []
    
    def test_detect_connections(self, schematic_importer):
        """Test detecting connections in an image"""
        # Create a mock image
        image = np.zeros((100, 100, 3), dtype=np.uint8)
        
        # Call the method
        connections = schematic_importer.detect_connections(image)
        
        # Assert that it returns an empty list (placeholder implementation)
        assert connections == []
