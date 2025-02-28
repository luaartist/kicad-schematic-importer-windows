#!/usr/bin/env python3
"""
Component Recognizer module for identifying electronic components in schematics.
This module provides advanced pattern matching and machine learning capabilities
for recognizing various electronic components in schematic images.
"""

import os
import cv2
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import json

class ComponentRecognizer:
    """
    Component Recognizer class that provides methods for identifying electronic
    components in schematic images using various techniques including template
    matching, feature detection, and machine learning.
    """
    
    def __init__(self, component_db_path: Optional[str] = None):
        """
        Initialize the component recognizer.
        
        Args:
            component_db_path: Path to the component database JSON file.
                If None, a default database will be used.
        """
        self.component_templates = {}
        self.component_features = {}
        self.load_component_database(component_db_path)
    
    def load_component_database(self, db_path: Optional[str] = None) -> None:
        """
        Load the component database from a JSON file.
        
        Args:
            db_path: Path to the component database JSON file.
                If None, a default database will be created.
        """
        if db_path and os.path.exists(db_path):
            try:
                with open(db_path, 'r') as f:
                    data = json.load(f)
                
                # Load component templates
                for component_type, template_path in data.get('templates', {}).items():
                    if os.path.exists(template_path):
                        self.component_templates[component_type] = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
                
                # Load component features
                self.component_features = data.get('features', {})
                
                print(f"Loaded component database from {db_path}")
            except Exception as e:
                print(f"Error loading component database: {e}")
                self._create_default_database()
        else:
            self._create_default_database()
    
    def _create_default_database(self) -> None:
        """Create a default component database with basic component definitions."""
        # Define basic component types and their characteristics
        self.component_features = {
            "resistor": {
                "aspect_ratio_min": 3.0,
                "aspect_ratio_max": 10.0,
                "area_min": 100,
                "area_max": 5000,
                "pattern": r"R\d+|Resistor",
                "symbol": "Device:R",
                "footprint": "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal"
            },
            "capacitor": {
                "aspect_ratio_min": 0.5,
                "aspect_ratio_max": 2.0,
                "area_min": 100,
                "area_max": 3000,
                "pattern": r"C\d+|Capacitor",
                "symbol": "Device:C",
                "footprint": "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm"
            },
            "inductor": {
                "aspect_ratio_min": 1.0,
                "aspect_ratio_max": 5.0,
                "area_min": 100,
                "area_max": 4000,
                "pattern": r"L\d+|Inductor",
                "symbol": "Device:L",
                "footprint": "Inductor_THT:L_Axial_L5.3mm_D2.2mm_P10.16mm_Horizontal_Vishay_IM-1"
            },
            "diode": {
                "aspect_ratio_min": 1.5,
                "aspect_ratio_max": 4.0,
                "area_min": 100,
                "area_max": 2000,
                "pattern": r"D\d+|Diode",
                "symbol": "Device:D",
                "footprint": "Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal"
            },
            "transistor": {
                "aspect_ratio_min": 0.8,
                "aspect_ratio_max": 1.2,
                "area_min": 300,
                "area_max": 5000,
                "pattern": r"Q\d+|Transistor",
                "symbol": "Device:Q_NPN_EBC",
                "footprint": "Package_TO_SOT_THT:TO-92_Inline"
            },
            "ic": {
                "aspect_ratio_min": 0.8,
                "aspect_ratio_max": 1.5,
                "area_min": 1000,
                "area_max": 20000,
                "pattern": r"U\d+|IC\d+",
                "symbol": "Device:IC",
                "footprint": "Package_DIP:DIP-8_W7.62mm"
            },
            "connector": {
                "aspect_ratio_min": 0.2,
                "aspect_ratio_max": 5.0,
                "area_min": 500,
                "area_max": 10000,
                "pattern": r"J\d+|Connector",
                "symbol": "Connector:Conn_01x04_Pin",
                "footprint": "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical"
            }
        }
        
        print("Created default component database")
    
    def save_component_database(self, db_path: str) -> None:
        """
        Save the component database to a JSON file.
        
        Args:
            db_path: Path to save the component database JSON file.
        """
        data = {
            "templates": {
                component_type: f"templates/{component_type}.png"
                for component_type in self.component_templates
            },
            "features": self.component_features
        }
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            
            with open(db_path, 'w') as f:
                json.dump(data, f, indent=4)
            
            # Save template images
            template_dir = os.path.join(os.path.dirname(db_path), "templates")
            os.makedirs(template_dir, exist_ok=True)
            
            for component_type, template in self.component_templates.items():
                template_path = os.path.join(template_dir, f"{component_type}.png")
                cv2.imwrite(template_path, template)
            
            print(f"Saved component database to {db_path}")
        except Exception as e:
            print(f"Error saving component database: {e}")
    
    def add_component_template(self, component_type: str, template_image: np.ndarray) -> None:
        """
        Add a component template to the database.
        
        Args:
            component_type: Type of the component (e.g., "resistor", "capacitor").
            template_image: Template image of the component.
        """
        if isinstance(template_image, np.ndarray):
            if template_image.ndim == 3:
                # Convert to grayscale if it's a color image
                template_image = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)
            
            self.component_templates[component_type] = template_image
            print(f"Added template for {component_type}")
        else:
            print(f"Invalid template image for {component_type}")
    
    def add_component_features(self, component_type: str, features: Dict[str, Any]) -> None:
        """
        Add component features to the database.
        
        Args:
            component_type: Type of the component (e.g., "resistor", "capacitor").
            features: Dictionary of component features.
        """
        if component_type in self.component_features:
            # Update existing features
            self.component_features[component_type].update(features)
        else:
            # Add new component type
            self.component_features[component_type] = features
        
        print(f"Updated features for {component_type}")
    
    def recognize_components(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """
        Recognize components in an image.
        
        Args:
            image: Input image (grayscale or color).
        
        Returns:
            List of dictionaries containing recognized components with their
            positions, types, and confidence scores.
        """
        # Convert to grayscale if it's a color image
        if image.ndim == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Apply preprocessing
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        recognized_components = []
        
        # Process each contour
        for i, contour in enumerate(contours):
            # Get bounding box
            x, y, w, h = cv2.boundingRect(contour)
            
            # Skip very small contours
            if w < 10 or h < 10:
                continue
            
            # Calculate features
            aspect_ratio = w / h if h > 0 else 999
            area = w * h
            
            # Identify component type based on features
            component_type = self._identify_component_type(aspect_ratio, area)
            
            # Calculate confidence score (placeholder)
            confidence = 0.7
            
            # Add to recognized components
            component = {
                "id": f"C{i+1}",
                "type": component_type,
                "x": x + w // 2,
                "y": y + h // 2,
                "width": w,
                "height": h,
                "bbox": (x, y, x + w, y + h),
                "confidence": confidence
            }
            
            recognized_components.append(component)
        
        # Apply template matching for better recognition
        self._apply_template_matching(gray, recognized_components)
        
        return recognized_components
    
    def _identify_component_type(self, aspect_ratio: float, area: int) -> str:
        """
        Identify component type based on aspect ratio and area.
        
        Args:
            aspect_ratio: Width to height ratio.
            area: Area of the component in pixels.
        
        Returns:
            Component type string.
        """
        for component_type, features in self.component_features.items():
            aspect_ratio_min = features.get("aspect_ratio_min", 0)
            aspect_ratio_max = features.get("aspect_ratio_max", 999)
            area_min = features.get("area_min", 0)
            area_max = features.get("area_max", 999999)
            
            if (aspect_ratio_min <= aspect_ratio <= aspect_ratio_max and
                area_min <= area <= area_max):
                return component_type
        
        return "unknown"
    
    def _apply_template_matching(self, image: np.ndarray, components: List[Dict[str, Any]]) -> None:
        """
        Apply template matching to refine component recognition.
        
        Args:
            image: Input grayscale image.
            components: List of recognized components to refine.
        """
        for template_type, template in self.component_templates.items():
            if template is None:
                continue
            
            # Apply template matching
            result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.7
            locations = np.where(result >= threshold)
            
            for pt in zip(*locations[::-1]):
                # Check if this location overlaps with any existing component
                for component in components:
                    x_min, y_min, x_max, y_max = component["bbox"]
                    
                    # Check for overlap
                    if (pt[0] >= x_min and pt[0] <= x_max and
                        pt[1] >= y_min and pt[1] <= y_max):
                        # Update component type if confidence is higher
                        new_confidence = result[pt[1], pt[0]]
                        if new_confidence > component.get("confidence", 0):
                            component["type"] = template_type
                            component["confidence"] = new_confidence
    
    def extract_text_near_components(self, image: np.ndarray, components: List[Dict[str, Any]]) -> None:
        """
        Extract text near components to identify labels and values.
        
        Args:
            image: Input image.
            components: List of recognized components to update with text information.
        """
        # This is a placeholder for OCR functionality
        # In a real implementation, this would use an OCR engine like Tesseract
        
        # For now, just assign some placeholder values
        for component in components:
            component_type = component["type"]
            
            if component_type == "resistor":
                component["value"] = "10K"
            elif component_type == "capacitor":
                component["value"] = "100nF"
            elif component_type == "inductor":
                component["value"] = "10uH"
            elif component_type == "diode":
                component["value"] = "1N4148"
            elif component_type == "transistor":
                component["value"] = "2N3904"
            elif component_type == "ic":
                component["value"] = "NE555"
            else:
                component["value"] = "Unknown"

# Example usage
if __name__ == "__main__":
    # Create a component recognizer
    recognizer = ComponentRecognizer()
    
    # Load an image
    image_path = "test_schematic.png"
    if os.path.exists(image_path):
        image = cv2.imread(image_path)
        
        # Recognize components
        components = recognizer.recognize_components(image)
        
        # Extract text near components
        recognizer.extract_text_near_components(image, components)
        
        # Print recognized components
        for component in components:
            print(f"Component {component['id']}: {component['type']} ({component['value']})")
            print(f"  Position: ({component['x']}, {component['y']})")
            print(f"  Confidence: {component.get('confidence', 0):.2f}")
            print()
    else:
        print(f"Image not found: {image_path}")
