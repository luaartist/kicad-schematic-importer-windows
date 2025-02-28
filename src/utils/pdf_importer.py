#!/usr/bin/env python3
"""
PDF Importer module for extracting images from PDF files.
This module provides functionality to extract pages from PDF files
and convert them to images for further processing.
"""

import os
import tempfile
from pathlib import Path
import fitz  # PyMuPDF
import cv2
import numpy as np
from typing import List, Tuple, Optional, Union, Dict, Any

class PDFImporter:
    """
    PDF Importer class that provides methods for extracting images from PDF files
    and converting them to formats suitable for schematic recognition.
    """
    
    def __init__(self, dpi: int = 300):
        """
        Initialize the PDF importer.
        
        Args:
            dpi: Resolution in dots per inch for rendering PDF pages.
        """
        self.dpi = dpi
        self.zoom = dpi / 72  # PDF uses 72 dpi as default
    
    def get_pdf_info(self, pdf_path: str) -> Dict[str, Any]:
        """
        Get information about a PDF file.
        
        Args:
            pdf_path: Path to the PDF file.
            
        Returns:
            Dictionary containing PDF information.
        """
        try:
            # Open the PDF file
            doc = fitz.open(pdf_path)
            
            # Get basic information
            info = {
                "path": pdf_path,
                "filename": os.path.basename(pdf_path),
                "page_count": len(doc),
                "metadata": doc.metadata,
                "pages": []
            }
            
            # Get information about each page
            for i, page in enumerate(doc):
                page_info = {
                    "page_number": i + 1,
                    "width": page.rect.width,
                    "height": page.rect.height,
                    "rotation": page.rotation,
                    "image_count": len(page.get_images())
                }
                info["pages"].append(page_info)
            
            doc.close()
            return info
        except Exception as e:
            print(f"Error getting PDF info: {e}")
            return {"error": str(e)}
    
    def extract_page_as_image(self, pdf_path: str, page_number: int = 0) -> Optional[np.ndarray]:
        """
        Extract a specific page from a PDF file as an image.
        
        Args:
            pdf_path: Path to the PDF file.
            page_number: Page number to extract (0-based index).
            
        Returns:
            Extracted page as a numpy array (image) or None if extraction fails.
        """
        try:
            # Open the PDF file
            doc = fitz.open(pdf_path)
            
            # Check if page number is valid
            if page_number < 0 or page_number >= len(doc):
                print(f"Invalid page number: {page_number}")
                doc.close()
                return None
            
            # Get the specified page
            page = doc[page_number]
            
            # Render page to an image
            pix = page.get_pixmap(matrix=fitz.Matrix(self.zoom, self.zoom))
            
            # Convert to numpy array
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
            
            # Convert to RGB if needed
            if pix.n == 4:  # RGBA
                img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
            
            doc.close()
            return img
        except Exception as e:
            print(f"Error extracting page: {e}")
            return None
    
    def extract_all_pages(self, pdf_path: str) -> List[np.ndarray]:
        """
        Extract all pages from a PDF file as images.
        
        Args:
            pdf_path: Path to the PDF file.
            
        Returns:
            List of extracted pages as numpy arrays (images).
        """
        try:
            # Open the PDF file
            doc = fitz.open(pdf_path)
            
            # Extract all pages
            images = []
            for page_number in range(len(doc)):
                img = self.extract_page_as_image(pdf_path, page_number)
                if img is not None:
                    images.append(img)
            
            doc.close()
            return images
        except Exception as e:
            print(f"Error extracting all pages: {e}")
            return []
    
    def extract_region(self, image: np.ndarray, region: Tuple[int, int, int, int]) -> np.ndarray:
        """
        Extract a region from an image.
        
        Args:
            image: Input image.
            region: Region to extract as (x, y, width, height).
            
        Returns:
            Extracted region as a numpy array (image).
        """
        x, y, width, height = region
        return image[y:y+height, x:x+width]
    
    def save_as_image(self, pdf_path: str, output_path: str, page_number: int = 0, dpi: Optional[int] = None) -> bool:
        """
        Save a PDF page as an image file.
        
        Args:
            pdf_path: Path to the PDF file.
            output_path: Path to save the image.
            page_number: Page number to extract (0-based index).
            dpi: Resolution in dots per inch. If None, use the default DPI.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            # Use specified DPI or default
            zoom = (dpi / 72) if dpi else self.zoom
            
            # Open the PDF file
            doc = fitz.open(pdf_path)
            
            # Check if page number is valid
            if page_number < 0 or page_number >= len(doc):
                print(f"Invalid page number: {page_number}")
                doc.close()
                return False
            
            # Get the specified page
            page = doc[page_number]
            
            # Render page to an image
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
            
            # Save the image
            pix.save(output_path)
            
            doc.close()
            return True
        except Exception as e:
            print(f"Error saving as image: {e}")
            return False
    
    def extract_embedded_images(self, pdf_path: str, min_size: int = 100) -> List[np.ndarray]:
        """
        Extract embedded images from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file.
            min_size: Minimum size (width or height) for extracted images.
            
        Returns:
            List of extracted images as numpy arrays.
        """
        try:
            # Open the PDF file
            doc = fitz.open(pdf_path)
            
            # Extract images
            images = []
            for page_number in range(len(doc)):
                page = doc[page_number]
                
                # Get image list
                img_list = page.get_images(full=True)
                
                # Process each image
                for img_index, img_info in enumerate(img_list):
                    xref = img_info[0]
                    
                    # Extract image
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    
                    # Convert to numpy array
                    try:
                        img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
                        
                        # Check image size
                        if img.shape[0] >= min_size and img.shape[1] >= min_size:
                            images.append(img)
                    except Exception as e:
                        print(f"Error decoding image: {e}")
            
            doc.close()
            return images
        except Exception as e:
            print(f"Error extracting embedded images: {e}")
            return []
    
    def preprocess_for_schematic(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess an image for schematic recognition.
        
        Args:
            image: Input image.
            
        Returns:
            Preprocessed image.
        """
        # Convert to grayscale if it's a color image
        if image.ndim == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Apply adaptive thresholding
        binary = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11,
            2
        )
        
        # Apply morphological operations to remove noise
        kernel = np.ones((2, 2), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        
        return binary
    
    def pdf_to_svg(self, pdf_path: str, output_path: str, page_number: int = 0) -> bool:
        """
        Convert a PDF page to SVG format.
        
        Args:
            pdf_path: Path to the PDF file.
            output_path: Path to save the SVG file.
            page_number: Page number to convert (0-based index).
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            # Open the PDF file
            doc = fitz.open(pdf_path)
            
            # Check if page number is valid
            if page_number < 0 or page_number >= len(doc):
                print(f"Invalid page number: {page_number}")
                doc.close()
                return False
            
            # Get the specified page
            page = doc[page_number]
            
            # Convert to SVG
            svg_data = page.get_svg_image()
            
            # Save SVG data to file
            with open(output_path, "w") as f:
                f.write(svg_data)
            
            doc.close()
            return True
        except Exception as e:
            print(f"Error converting to SVG: {e}")
            return False

# Example usage
if __name__ == "__main__":
    # Create a PDF importer
    importer = PDFImporter(dpi=300)
    
    # Example PDF file
    pdf_path = "example.pdf"
    if os.path.exists(pdf_path):
        # Get PDF info
        info = importer.get_pdf_info(pdf_path)
        print(f"PDF Info: {info}")
        
        # Extract first page as image
        img = importer.extract_page_as_image(pdf_path, 0)
        if img is not None:
            # Save the image
            cv2.imwrite("page_0.png", img)
            
            # Preprocess for schematic recognition
            preprocessed = importer.preprocess_for_schematic(img)
            cv2.imwrite("page_0_preprocessed.png", preprocessed)
            
            # Convert to SVG
            importer.pdf_to_svg(pdf_path, "page_0.svg", 0)
            
            print("PDF processing completed successfully.")
        else:
            print("Failed to extract page.")
    else:
        print(f"PDF file not found: {pdf_path}")
