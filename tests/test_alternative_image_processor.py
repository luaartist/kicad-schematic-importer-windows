import os
import pytest
import cv2
import numpy as np
import shutil
from pathlib import Path
from src.utils.alternative_image_processor import AlternativeImageProcessor

@pytest.fixture
def test_dir():
    dir_path = Path("tests/test_files")
    dir_path.mkdir(parents=True, exist_ok=True)
    yield dir_path
    # Clean up properly
    if dir_path.exists():
        shutil.rmtree(dir_path)

def test_image_processor_debug_output(test_dir):
    """Test that image processor generates debug images"""
    # Create a test image with some components and connections
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    
    # Draw some components
    cv2.rectangle(image, (20, 20), (40, 40), (255, 255, 255), 2)  # Component 1
    cv2.rectangle(image, (120, 120), (140, 140), (255, 255, 255), 2)  # Component 2
    
    # Draw a connection
    cv2.line(image, (40, 30), (120, 130), (255, 255, 255), 2)
    
    # Save test image
    test_image_path = test_dir / "test_schematic.png"
    cv2.imwrite(str(test_image_path), image)
    
    try:
        # Process the image
        processor = AlternativeImageProcessor()
        svg_path = processor.vectorize_image(str(test_image_path))
        
        # Check that debug images were created
        debug_binary = test_dir / "debug_binary.png"
        debug_contours = test_dir / "debug_contours.png"
        debug_lines = test_dir / "debug_lines.png"
        
        assert debug_binary.exists(), "Binary debug image not created"
        assert debug_contours.exists(), "Contours debug image not created"
        assert debug_lines.exists(), "Lines debug image not created"
        
        # Check that SVG was created
        svg_file = test_image_path.with_suffix('.svg')
        assert svg_file.exists(), "SVG file not created"
        
        # Verify SVG content
        with open(svg_file) as f:
            svg_content = f.read()
            assert '<?xml version="1.0"' in svg_content
            assert '<svg' in svg_content
            assert '<path' in svg_content
            assert 'stroke="black"' in svg_content
            assert 'fill="none"' in svg_content
        
    finally:
        # Clean up test files
        for file in [test_image_path, debug_binary, debug_contours, debug_lines]:
            if file.exists():
                file.unlink()
        
        svg_file = test_image_path.with_suffix('.svg')
        if svg_file.exists():
            svg_file.unlink()
            
        if test_dir.exists():
            test_dir.rmdir()

def test_image_processor_error_handling():
    """Test that image processor handles errors gracefully"""
    processor = AlternativeImageProcessor()
    
    # Test with non-existent file
    result = processor.vectorize_image("nonexistent.png")
    assert result is None
    
    # Test with invalid image data
    test_dir = Path(__file__).parent / "test_files"
    test_dir.mkdir(exist_ok=True)
    invalid_image = test_dir / "invalid.png"
    
    try:
        # Create an invalid image file
        with open(invalid_image, 'w') as f:
            f.write("Not a PNG file")
        
        result = processor.vectorize_image(str(invalid_image))
        assert result is None
        
    finally:
        # Clean up
        if invalid_image.exists():
            invalid_image.unlink()
        if test_dir.exists():
            test_dir.rmdir()

def test_image_processor_different_formats():
    """Test that image processor handles different image formats"""
    processor = AlternativeImageProcessor()
    
    # Create test images in different formats
    test_dir = Path(__file__).parent / "test_files"
    test_dir.mkdir(exist_ok=True)
    
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.rectangle(image, (20, 20), (40, 40), (255, 255, 255), 2)
    
    formats = [
        ('png', cv2.IMWRITE_PNG_COMPRESSION, 9),
        ('jpg', cv2.IMWRITE_JPEG_QUALITY, 90),
        ('bmp', None, None)
    ]
    
    try:
        for fmt, param, value in formats:
            test_image = test_dir / f"test.{fmt}"
            if param is not None:
                cv2.imwrite(str(test_image), image, [param, value])
            else:
                cv2.imwrite(str(test_image), image)
            
            # Process each format
            svg_path = processor.vectorize_image(str(test_image))
            assert svg_path is not None
            assert Path(svg_path).exists()
            
            # Clean up SVG
            Path(svg_path).unlink()
            test_image.unlink()
            
            # Clean up debug images
            debug_files = [
                test_dir / "debug_binary.png",
                test_dir / "debug_contours.png",
                test_dir / "debug_lines.png"
            ]
            for debug_file in debug_files:
                if debug_file.exists():
                    debug_file.unlink()
    
    finally:
        if test_dir.exists():
            test_dir.rmdir()
