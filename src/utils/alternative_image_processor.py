import cv2
import numpy as np
from PIL import Image
import os
import logging
import hashlib
import time

class AlternativeImageProcessor:
    """Class for processing and vectorizing schematic images"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        
        # Add console handler if none exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(handler)
    
    def vectorize_image(self, image_path):
        """Convert raster image to vector format"""
        self.logger.info("\n========== STARTING NEW CONVERSION ==========")
        self.logger.info(f"Processing image: {image_path}")
        
        # Check if file exists
        if not os.path.exists(image_path):
            self.logger.error(f"Image file not found: {image_path}")
            return None
        
        # Generate file hash for uniqueness verification
        try:
            with open(image_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            self.logger.info(f"Input file hash: {file_hash}")
        except Exception as e:
            self.logger.error(f"Error hashing file: {e}")
            return None
        
        # Create debug directory
        debug_dir = os.path.join(os.path.dirname(image_path), "debug")
        os.makedirs(debug_dir, exist_ok=True)
        
        # Load and analyze image
        try:
            with Image.open(image_path) as img:
                self.logger.info(f"Image size: {img.size}, format: {img.format}, mode: {img.mode}")
                
                # Save thumbnail for verification
                thumb_path = os.path.join(debug_dir, f"thumb_{int(time.time())}.png")
                img_copy = img.copy()
                img_copy.thumbnail((100, 100))
                img_copy.save(thumb_path)
                self.logger.info(f"Thumbnail saved to {thumb_path}")
                
                # Convert to RGB if needed
                if img.mode != 'RGB':
                    self.logger.info(f"Converting image from {img.mode} to RGB")
                    img = img.convert('RGB')
                
                # Convert to numpy array for OpenCV processing
                image = np.array(img)
        except Exception as e:
            self.logger.error(f"Error opening image: {e}")
            return None
        
        # Convert to grayscale
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            self.logger.info(f"Converted to grayscale. Shape: {gray.shape}")
            
            # Save grayscale debug image
            debug_path = os.path.join(debug_dir, f"gray_{int(time.time())}.png")
            cv2.imwrite(debug_path, gray)
            self.logger.info(f"Saved grayscale debug image to: {debug_path}")
        except Exception as e:
            self.logger.error(f"Error converting to grayscale: {e}")
            return None
        
        # Apply adaptive thresholding
        try:
            binary = cv2.adaptiveThreshold(
                gray,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY_INV,
                11,
                2
            )
            self.logger.info("Applied adaptive thresholding")
            
            # Save binary debug image
            debug_path = os.path.join(debug_dir, f"binary_{int(time.time())}.png")
            cv2.imwrite(debug_path, binary)
            self.logger.info(f"Saved binary debug image to: {debug_path}")
            
            # Calculate and log binary image statistics
            white_pixels = np.sum(binary == 255)
            total_pixels = binary.size
            white_percentage = (white_pixels / total_pixels) * 100
            self.logger.info(f"Binary image statistics: {white_percentage:.2f}% white pixels")
        except Exception as e:
            self.logger.error(f"Error during thresholding: {e}")
            return None
        
        # Find contours
        try:
            contours, hierarchy = cv2.findContours(
                binary,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )
            self.logger.info(f"Found {len(contours)} contours")
            
            # Draw and save contours debug image
            debug_contours = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
            cv2.drawContours(debug_contours, contours, -1, (0,255,0), 2)
            debug_path = os.path.join(debug_dir, f"contours_{int(time.time())}.png")
            cv2.imwrite(debug_path, debug_contours)
            self.logger.info(f"Saved contours debug image to: {debug_path}")
            
            # Log contour statistics
            areas = [cv2.contourArea(c) for c in contours]
            if areas:
                self.logger.info(f"Contour areas - Min: {min(areas):.2f}, Max: {max(areas):.2f}, Mean: {np.mean(areas):.2f}")
        except Exception as e:
            self.logger.error(f"Error finding contours: {e}")
            return None
        
        # Detect lines
        try:
            lines = cv2.HoughLinesP(
                binary,
                rho=1,
                theta=np.pi/180,
                threshold=50,
                minLineLength=20,
                maxLineGap=10
            )
            
            if lines is not None:
                self.logger.info(f"Found {len(lines)} lines")
                
                # Draw and save lines debug image
                debug_lines = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    cv2.line(debug_lines, (x1,y1), (x2,y2), (0,0,255), 2)
                debug_path = os.path.join(debug_dir, f"lines_{int(time.time())}.png")
                cv2.imwrite(debug_path, debug_lines)
                self.logger.info(f"Saved lines debug image to: {debug_path}")
                
                # Log line statistics
                lengths = [np.sqrt((x2-x1)**2 + (y2-y1)**2) for line in lines for x1,y1,x2,y2 in [line[0]]]
                self.logger.info(f"Line lengths - Min: {min(lengths):.2f}, Max: {max(lengths):.2f}, Mean: {np.mean(lengths):.2f}")
            else:
                self.logger.warning("No lines detected")
        except Exception as e:
            self.logger.error(f"Error detecting lines: {e}")
            return None
        
        # Generate unique output path
        timestamp = int(time.time())
        base_name = os.path.basename(image_path)
        name, ext = os.path.splitext(base_name)
        output_dir = os.path.dirname(image_path)
        svg_path = os.path.join(output_dir, f"{name}_{timestamp}_{file_hash[:8]}.svg")
        self.logger.info(f"Generated output path: {svg_path}")
        
        # Create SVG path
        try:
            # Convert contours to SVG paths
            svg_paths = []
            for contour in contours:
                path = "M"
                for i, point in enumerate(contour):
                    x, y = point[0]
                    if i == 0:
                        path += f" {x},{y}"
                    else:
                        path += f" L {x},{y}"
                path += " Z"
                svg_paths.append(path)
            
            # Add lines to SVG
            if lines is not None:
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    path = f"M {x1},{y1} L {x2},{y2}"
                    svg_paths.append(path)
            
            # Create SVG file
            width, height = image.shape[1], image.shape[0]
            
            with open(svg_path, 'w') as f:
                f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n')
                f.write(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">\n')
                f.write(f'<!-- Source image: {os.path.basename(image_path)} -->\n')
                f.write(f'<!-- Hash: {file_hash} -->\n')
                f.write(f'<!-- Timestamp: {timestamp} -->\n')
                f.write(f'<!-- Statistics: {len(contours)} contours, {len(lines) if lines is not None else 0} lines -->\n')
                for path in svg_paths:
                    f.write(f'  <path d="{path}" stroke="black" fill="none"/>\n')
                f.write('</svg>\n')
            
            self.logger.info(f"Created SVG file: {svg_path}")
            return svg_path
            
        except Exception as e:
            self.logger.error(f"Error creating SVG: {e}")
            return None
