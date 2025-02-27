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
from typing import List, Optional
import shlex

class AlternativeImageProcessor:
    """
    Alternative Image Processor class that provides methods for vectorizing images
    using various libraries and tools.
    """
    
    def __init__(self):
        """Initialize the image processor."""
        self.ALLOWED_TOOLS = ['inkscape', 'autotrace', 'opencv']
        self._validate_tools()
    
    def _validate_tools(self) -> None:
        """Validate and initialize available tools safely."""
        self.has_inkscape = self._check_tool_exists('inkscape')
        self.has_autotrace = self._check_tool_exists('autotrace')
        self.has_opencv = True  # OpenCV is installed via pip
    
    def _check_tool_exists(self, tool_name: str) -> bool:
        """Safely check if a command-line tool exists."""
        if tool_name not in self.ALLOWED_TOOLS:
            return False
        return shutil.which(tool_name) is not None

    def check_tool_exists(self, tool_name: str) -> bool:
        """
        Check if a required external tool exists in the system PATH
        
        Args:
            tool_name: Name of the tool to check (e.g., 'inkscape')
            
        Returns:
            bool: True if tool exists, False otherwise
        """
        return shutil.which(tool_name) is not None

    def _validate_path(self, path: str) -> Path:
        """
        Validate and resolve path safely.
        
        Args:
            path: Path to validate
            
        Returns:
            Path: Resolved path object
            
        Raises:
            ValueError: If path is invalid or doesn't exist
        """
        resolved_path = Path(path).resolve()
        if not resolved_path.exists():
            raise ValueError(f"Path does not exist: {resolved_path}")
        return resolved_path

    def _run_subprocess(self, cmd: List[str], timeout: int = 30) -> subprocess.CompletedProcess:
        """
        Safely run a subprocess command.
        
        Args:
            cmd: List of command arguments
            timeout: Maximum execution time in seconds
            
        Returns:
            CompletedProcess instance
            
        Raises:
            subprocess.SubprocessError: If the command fails
        """
        if not all(isinstance(arg, str) for arg in cmd):
            raise ValueError("All command arguments must be strings")
            
        try:
            return subprocess.run(
                cmd,
                check=True,
                timeout=timeout,
                capture_output=True,
                text=True,
                shell=False  # Explicitly set shell=False for security
            )
        except subprocess.SubprocessError as e:
            raise RuntimeError(f"Command execution failed: {e}")
    
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
    
    def convert_to_svg(self, input_path: str, output_path: str, timeout: int = 30) -> str:
        """Convert image to SVG safely."""
        # Validate paths
        input_path = self._validate_path(input_path)
        output_path = self._validate_path(output_path)
        
        if not input_path.is_file():
            raise ValueError(f"Input image not found: {input_path}")
            
        output_dir = output_path.parent
        if not output_dir.exists():
            raise ValueError(f"Output directory does not exist: {output_dir}")
            
        inkscape_path = shutil.which('inkscape')
        if not inkscape_path:
            raise RuntimeError("Inkscape not found")
            
        cmd = [
            inkscape_path,
            '--export-filename', str(output_path),
            str(input_path)
        ]
        
        self._run_subprocess(cmd, timeout)
        return str(output_path)
    
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
    
    def _vectorize_with_inkscape(self, image_path: str) -> str:
        """Safely vectorize using Inkscape."""
        image_path = self._validate_path(image_path)
        output_path = image_path.with_suffix('.svg')
        
        inkscape_path = shutil.which('inkscape')
        if not inkscape_path:
            raise RuntimeError("Inkscape not found")
            
        cmd = [
            inkscape_path,
            '--export-filename', str(output_path),
            '--export-plain-svg',
            str(image_path)
        ]
        
        self._run_subprocess(cmd)
        
        if not output_path.exists():
            raise ValueError(f"Inkscape failed to create output file: {output_path}")
        return str(output_path)
    
    def _vectorize_with_autotrace(self, image_path: str) -> str:
        """Safely vectorize using AutoTrace."""
        image_path = self._validate_path(image_path)
        output_path = image_path.with_suffix('.svg')
        
        autotrace_path = shutil.which('autotrace')
        if not autotrace_path:
            raise RuntimeError("AutoTrace not found")
            
        cmd = [
            autotrace_path,
            '--output-file', str(output_path),
            '--output-format', 'svg',
            str(image_path)
        ]
        
        self._run_subprocess(cmd)
        
        if not output_path.exists():
            raise ValueError(f"AutoTrace failed to create output file: {output_path}")
        return str(output_path)
    
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
