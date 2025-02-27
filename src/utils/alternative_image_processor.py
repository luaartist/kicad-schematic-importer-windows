#!/usr/bin/env python3
"""
Alternative Image Processor module for vectorizing images.
This module provides alternatives to the potrace library for vectorization.
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
import cv2
import numpy as np
from svgpathtools import Path as SvgPath, Line, CubicBezier, QuadraticBezier
import svgwrite

class AlternativeImageProcessor:
    """
    Alternative Image Processor class that provides methods for vectorizing images
    using various libraries and tools.
    """
    
    def __init__(self):
        """Initialize the image processor."""
        self.ALLOWED_TOOLS = ['inkscape', 'autotrace', 'opencv']
        
        # Check which tools are available
        self.has_inkscape = self.check_tool_exists('inkscape')
        self.has_autotrace = self.check_tool_exists('autotrace')
        self.has_opencv = True  # OpenCV is installed via pip
        
        print(f"Available vectorization tools: " +
              f"Inkscape: {self.has_inkscape}, " +
              f"AutoTrace: {self.has_autotrace}, " +
              f"OpenCV: {self.has_opencv}")
    
    def check_tool_exists(self, tool_name):
        """
        Check if a command-line tool exists.
        
        Args:
            tool_name (str): The name of the tool to check.
            
        Returns:
            bool: True if the tool exists, False otherwise.
        """
        if tool_name not in self.ALLOWED_TOOLS:
            return False
        
        try:
            # Use shutil.which to check if the tool is in the PATH
            return shutil.which(tool_name) is not None
        except Exception:
            return False
    
    def get_image_dpi(self, image_path):
        """
        Get the DPI of an image.
        
        Args:
            image_path (str): Path to the image.
            
        Returns:
            float or None: The DPI of the image, or None if not available.
        """
        try:
            # Use OpenCV to get image dimensions
            img = cv2.imread(image_path)
            if img is None:
                return None
            
            # Default to 96 DPI if not specified
            return 96.0
        except Exception as e:
            print(f"Error getting image DPI: {e}")
            return None
    
    def convert_to_svg(self, input_path, output_path, timeout=30):
        """
        Convert an image to SVG using Inkscape.
        
        Args:
            input_path (str): Path to the input image.
            output_path (str): Path to save the output SVG.
            timeout (int, optional): Timeout in seconds. Defaults to 30.
            
        Returns:
            str: Path to the output SVG.
            
        Raises:
            ValueError: If the input image does not exist or the output directory does not exist.
            RuntimeError: If Inkscape is not found.
            TimeoutError: If the conversion times out.
        """
        # Check if input file exists
        if not os.path.isfile(input_path):
            raise ValueError(f"Input image not found: {input_path}")
        
        # Check if output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.isdir(output_dir):
            raise ValueError(f"Output directory does not exist: {output_dir}")
        
        # Check if Inkscape is available
        inkscape_path = shutil.which('inkscape')
        if not inkscape_path:
            raise RuntimeError("Inkscape not found. Please install Inkscape.")
        
        try:
            # Run Inkscape to convert the image to SVG
            cmd = [
                inkscape_path,
                '--export-filename=' + output_path,
                input_path
            ]
            
            subprocess.run(cmd, check=True, timeout=timeout)
            return output_path
        except subprocess.TimeoutExpired:
            raise TimeoutError(f"SVG conversion timed out after {timeout} seconds")
        except Exception as e:
            raise RuntimeError(f"Error converting to SVG: {e}")
    
    def vectorize_image(self, image_path):
        """
        Vectorize an image using available tools.
        
        Args:
            image_path (str): Path to the image to vectorize.
            
        Returns:
            str: Path to the vectorized SVG.
            
        Raises:
            ValueError: If all vectorization methods fail.
        """
        errors = []
        
        # Try Inkscape first if available
        if self.has_inkscape:
            try:
                return self._vectorize_with_inkscape(image_path)
            except Exception as e:
                errors.append(f"Inkscape vectorization failed: {e}")
        
        # Try AutoTrace if available
        if self.has_autotrace:
            try:
                return self._vectorize_with_autotrace(image_path)
            except Exception as e:
                errors.append(f"AutoTrace vectorization failed: {e}")
        
        # Try OpenCV as a fallback
        try:
            return self._vectorize_with_opencv(image_path)
        except Exception as e:
            errors.append(f"OpenCV vectorization failed: {e}")
        
        # If all methods fail, raise an error
        raise ValueError(f"All vectorization methods failed: {', '.join(errors)}")
    
    def _vectorize_with_inkscape(self, image_path):
        """
        Vectorize an image using Inkscape.
        
        Args:
            image_path (str): Path to the image to vectorize.
            
        Returns:
            str: Path to the vectorized SVG.
            
        Raises:
            ValueError: If Inkscape fails to create the output file.
        """
        # Check if Inkscape is available
        inkscape_path = shutil.which('inkscape')
        if not inkscape_path:
            raise RuntimeError("Inkscape not found. Please install Inkscape.")
        
        # Create output path
        output_path = image_path.replace('.png', '.svg')
        output_path = output_path.replace('.jpg', '.svg')
        output_path = output_path.replace('.jpeg', '.svg')
        
        # Run Inkscape to vectorize the image
        cmd = [
            inkscape_path,
            '--export-filename=' + output_path,
            '--export-plain-svg',
            image_path
        ]
        
        subprocess.run(cmd, check=True)
        
        # Check if the output file was created
        if not Path(output_path).exists():
            raise ValueError(f"Inkscape failed to create output file: {output_path}")
        
        return output_path
    
    def _vectorize_with_autotrace(self, image_path):
        """
        Vectorize an image using AutoTrace.
        
        Args:
            image_path (str): Path to the image to vectorize.
            
        Returns:
            str: Path to the vectorized SVG.
            
        Raises:
            ValueError: If AutoTrace fails to create the output file.
        """
        # Check if AutoTrace is available
        autotrace_path = shutil.which('autotrace')
        if not autotrace_path:
            raise RuntimeError("AutoTrace not found. Please install AutoTrace.")
        
        # Create output path
        output_path = image_path.replace('.png', '.svg')
        output_path = output_path.replace('.jpg', '.svg')
        output_path = output_path.replace('.jpeg', '.svg')
        
        # Run AutoTrace to vectorize the image
        cmd = [
            autotrace_path,
            '--output-file=' + output_path,
            '--output-format=svg',
            image_path
        ]
        
        subprocess.run(cmd, check=True)
        
        # Check if the output file was created
        if not Path(output_path).exists():
            raise ValueError(f"AutoTrace failed to create output file: {output_path}")
        
        return output_path
    
    def _vectorize_with_opencv(self, image_path):
        """
        Vectorize an image using OpenCV.
        
        Args:
            image_path (str): Path to the image to vectorize.
            
        Returns:
            str: Path to the vectorized SVG.
            
        Raises:
            ValueError: If the image cannot be loaded or processed.
        """
        # Load the image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Failed to load image: {image_path}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold to get binary image
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Create output path
        output_path = image_path.replace('.png', '.svg')
        output_path = output_path.replace('.jpg', '.svg')
        output_path = output_path.replace('.jpeg', '.svg')
        
        # Create SVG drawing
        dwg = svgwrite.Drawing(output_path, profile='tiny')
        
        # Add contours to SVG
        for contour in contours:
            # Simplify contour
            epsilon = 0.01 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # Convert contour to SVG path
            points = [f"{pt[0][0]},{pt[0][1]}" for pt in approx]
            if points:
                path_data = "M " + " L ".join(points) + " Z"
                dwg.add(dwg.path(d=path_data, fill='none', stroke='black'))
        
        # Save SVG
        dwg.save()
        
        return output_path
    
    def trace_bitmap(self, image_path):
        """
        Trace a bitmap image to create a vector representation.
        This is a wrapper around vectorize_image for compatibility.
        
        Args:
            image_path (str): Path to the image to trace.
            
        Returns:
            str: Path to the traced SVG.
        """
        return self.vectorize_image(image_path)
