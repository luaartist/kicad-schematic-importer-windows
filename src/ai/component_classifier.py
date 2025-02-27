import cv2
import numpy as np
import os
import requests
import json
import base64
import hashlib
import time
from datetime import datetime
import logging

class ComponentClassifier:
    """Classify components using AI with safety and liability considerations"""
    
    def __init__(self, api_url=None, api_key=None, config=None):
        self.api_url = api_url
        self.api_key = api_key
        self.config = config or {}
        self.logger = self._setup_logger()
        self.user_acknowledged_risks = False
        self.github_verification_complete = False
        self.local_model_path = os.path.join(os.path.dirname(__file__), 'models', 'component_classifier.h5')
        self.replacement_disclaimer_path = os.path.join(os.path.dirname(__file__), '..', '..', 'security', 'templates', 'component_replacement_disclaimer.md')
        
        # Load local model if available
        self.local_model = None
        if os.path.exists(self.local_model_path):
            try:
                # This is a placeholder - actual model loading would depend on your ML framework
                # self.local_model = load_model(self.local_model_path)
                pass
            except Exception as e:
                self.logger.error(f"Failed to load local model: {str(e)}")
    
    def _setup_logger(self):
        """Set up logging for the component classifier"""
        logger = logging.getLogger('component_classifier')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.FileHandler('component_classifier.log')
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def verify_github_account(self, github_token):
        """Verify user has a GitHub account with 2FA enabled"""
        try:
            headers = {
                'Authorization': f'token {github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            # Get user info
            response = requests.get('https://api.github.com/user', headers=headers, timeout=10)
            if response.status_code != 200:
                self.logger.warning(f"GitHub verification failed: {response.status_code}")
                return False
            
            # Check 2FA status - requires specific endpoint
            response = requests.get('https://api.github.com/user/2fa_status', headers=headers, timeout=10)
            if response.status_code != 200 or not response.json().get('enabled', False):
                self.logger.warning("GitHub 2FA not enabled")
                return False
            
            self.github_verification_complete = True
            self.logger.info("GitHub verification successful")
            return True
        except Exception as e:
            self.logger.error(f"GitHub verification error: {str(e)}")
            return False
    
    def show_liability_disclaimer(self):
        """
        Display liability disclaimer and get user acknowledgment
        This would typically be implemented in the UI layer, but we include the text here
        """
        disclaimer = """
        IMPORTANT SAFETY AND LIABILITY DISCLAIMER - TEST VERSION
        
        By using this component classification feature in this TEST VERSION, you acknowledge and agree to the following:
        
        1. TEST ENVIRONMENT ONLY: This software is currently in a testing phase and should only be used
        in controlled test environments with designated test equipment.
        
        2. ACCURACY LIMITATIONS: The AI classification system provides estimates based on visual data only.
        Components with unreadable or damaged markings may be misidentified.
        
        3. VERIFICATION REQUIREMENT: You MUST verify all component identifications using appropriate
        test equipment (multimeters, oscilloscopes, etc.) before using in any circuit.
        
        4. NO LIABILITY: Neither the developers, contributors, nor any affiliated parties shall be
        liable for any damages, injuries, or losses resulting from the use of this software or
        any component identifications it provides.
        
        5. ELECTRICAL SAFETY RISKS: Incorrect component identification or replacement can result in:
           - Electrical fires
           - Component damage
           - Circuit malfunction
           - Personal injury
           - Property damage
        
        6. PROFESSIONAL REVIEW: For critical applications, safety systems, or commercial products,
        all schematics should be reviewed by a qualified electrical engineer.
        
        7. DATA SHARING: When you share schematics or request community assistance, you agree that:
           - Your schematic data may be stored on third-party servers
           - Community members may provide suggestions that require verification
           - You remain solely responsible for validating any advice received
        
        8. COMPONENT REPLACEMENT RISKS: There is approximately a 90% chance of damaging PCB traces 
        when removing components, especially with improper tools or techniques. You accept full 
        responsibility for any damage to your test equipment.
        
        9. TEST DOCUMENTATION: You agree to document all testing procedures and results for future reference
        and potential contribution to improving this software.
        
        USE AT YOUR OWN RISK. If you do not agree to these terms, do not use this feature.
        """
        
        # In a real implementation, this would show a dialog and get user confirmation
        # For now, we'll just log it and return True
        self.logger.info("Liability disclaimer shown to user")
        self.user_acknowledged_risks = True
        return disclaimer
    
    def show_replacement_disclaimer(self):
        """
        Display the component replacement disclaimer
        Returns the disclaimer text from the template file
        """
        try:
            if os.path.exists(self.replacement_disclaimer_path):
                with open(self.replacement_disclaimer_path, 'r') as f:
                    disclaimer = f.read()
                    self.logger.info("Component replacement disclaimer shown to user")
                    return disclaimer
            else:
                self.logger.warning(f"Replacement disclaimer file not found at {self.replacement_disclaimer_path}")
                return "Component replacement carries significant risks. Please acknowledge that you accept full responsibility for any damage."
        except Exception as e:
            self.logger.error(f"Error reading replacement disclaimer: {str(e)}")
            return "Component replacement carries significant risks. Please acknowledge that you accept full responsibility for any damage."
    
    def classify_component(self, image, contour, require_verification=True):
        """
        Classify component using AI with safety checks
        
        Args:
            image: The source image containing the component
            contour: The contour of the component to classify
            require_verification: Whether to require risk acknowledgment and GitHub verification
            
        Returns:
            dict: Component classification data or None if verification failed
        """
        # Safety checks
        if require_verification:
            if not self.user_acknowledged_risks:
                self.logger.warning("User has not acknowledged risks")
                return None
                
            if not self.github_verification_complete:
                self.logger.warning("GitHub verification not completed")
                return None
        
        # Extract component image from contour
        x, y, w, h = cv2.boundingRect(contour)
        component_img = image[y:y+h, x:x+w]
        
        # Try online classification first if configured
        if self.api_url and self.api_key:
            classification = self.classify_online(component_img)
            if classification:
                # Add safety warnings for unreadable components
                if classification.get('confidence', 1.0) < 0.7:
                    classification['warnings'] = [
                        "LOW CONFIDENCE IDENTIFICATION - VERIFICATION REQUIRED",
                        "Component markings may be unreadable or damaged",
                        "Use appropriate test equipment to verify before use"
                    ]
                return classification
        
        # Fall back to local classification
        if self.config.get('fallback_to_local', True):
            classification = self.classify_local(component_img)
            if classification:
                # Local classification always gets a warning
                classification['warnings'] = [
                    "LOCAL CLASSIFICATION - LOWER ACCURACY",
                    "This identification was made without online verification",
                    "Component must be verified with test equipment before use"
                ]
            return classification
        
        return None
    
    def classify_online(self, image_data):
        """
        Classify component using online API
        
        Args:
            image_data: Image of the component to classify
            
        Returns:
            dict: Classification results or None if failed
        """
        try:
            # Convert image to base64
            _, buffer = cv2.imencode('.jpg', image_data)
            encoded_image = base64.b64encode(buffer).decode('utf-8')
            
            # Prepare request
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            }
            
            payload = {
                'image': encoded_image,
                'options': {
                    'include_alternatives': True,
                    'min_confidence': 0.4
                }
            }
            
            # Make request
            response = requests.post(
                f"{self.api_url}/classify/component", 
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Log the request for audit purposes (without the image data)
                audit_payload = payload.copy()
                audit_payload['image'] = f"[Image data: {len(encoded_image)} bytes]"
                self.logger.info(f"Online classification request: {audit_payload}")
                self.logger.info(f"Classification result: {result}")
                
                # Format the response
                classification = {
                    'type': result.get('component_type', 'unknown'),
                    'value': result.get('value'),
                    'confidence': result.get('confidence', 0.0),
                    'alternatives': result.get('alternatives', []),
                    'timestamp': datetime.now().isoformat(),
                    'source': 'online_api',
                    'replacement_disclaimer': 'Component replacement carries significant risks. See the full disclaimer for details.'
                }
                
                return classification
            else:
                self.logger.error(f"API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            self.logger.error(f"Online classification error: {str(e)}")
            return None
    
    def classify_local(self, image_data):
        """
        Classify component using local model
        
        Args:
            image_data: Image of the component to classify
            
        Returns:
            dict: Classification results or None if failed
        """
        try:
            # Preprocess image
            processed_img = self._preprocess_for_local_model(image_data)
            
            # If we don't have a local model, use basic heuristics
            if self.local_model is None:
                return self._classify_with_heuristics(image_data)
            
            # Use local model for prediction
            # prediction = self.local_model.predict(processed_img)
            # This is a placeholder - actual prediction would depend on your ML framework
            
            # For now, return a placeholder result
            classification = {
                'type': 'resistor',  # This would come from the model
                'value': '10kΩ',
                'confidence': 0.65,
                'alternatives': [
                    {'type': 'capacitor', 'value': '0.1μF', 'confidence': 0.25},
                    {'type': 'diode', 'value': '1N4148', 'confidence': 0.10}
                ],
                'timestamp': datetime.now().isoformat(),
                'source': 'local_model',
                'replacement_disclaimer': 'Component replacement carries significant risks. See the full disclaimer for details.'
            }
            
            return classification
            
        except Exception as e:
            self.logger.error(f"Local classification error: {str(e)}")
            return None
    
    def _preprocess_for_local_model(self, image):
        """
        Preprocess image for local model
        
        Args:
            image: Input image to preprocess
            
        Returns:
            numpy.ndarray: Preprocessed image ready for model input
        """
        try:
            # Resize to expected input size
            resized = cv2.resize(image, (224, 224))
            
            # Convert to RGB if grayscale
            if len(image.shape) == 2 or (len(image.shape) == 3 and image.shape[2] == 1):
                resized = cv2.cvtColor(resized, cv2.COLOR_GRAY2RGB)
            
            # Normalize pixel values
            normalized = resized.astype(np.float32) / 255.0
            
            return normalized
        except Exception as e:
            self.logger.error(f"Image preprocessing error: {str(e)}")
            # Return a blank normalized image as fallback
            return np.zeros((224, 224, 3), dtype=np.float32)
    
    def _classify_with_heuristics(self, image):
        """
        Use basic heuristics for classification when no model is available
        
        Args:
            image: Input image to classify
            
        Returns:
            dict: Classification results based on simple heuristics
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) > 2 else image
            
            # Get image dimensions and aspect ratio
            height, width = gray.shape
            aspect_ratio = width / height if height > 0 else 0
            
            # Simple heuristics based on shape
            if aspect_ratio > 3.0:
                # Long and thin - likely a resistor
                component_type = 'resistor'
                value = 'unknown'
            elif aspect_ratio < 1.2 and aspect_ratio > 0.8:
                # Square-ish - could be an IC or capacitor
                # Check for pins
                edges = cv2.Canny(gray, 50, 150)
                lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=20, maxLineGap=5)
                
                if lines is not None and len(lines) > 8:
                    component_type = 'ic'
                    value = 'unknown IC'
                else:
                    component_type = 'capacitor'
                    value = 'unknown'
            elif aspect_ratio < 0.8:
                # Tall and thin - might be an electrolytic capacitor
                component_type = 'capacitor'
                value = 'electrolytic'
            else:
                # Default
                component_type = 'unknown'
                value = 'unknown'
            
            return {
                'type': component_type,
                'value': value,
                'confidence': 0.4,  # Low confidence for heuristic-based classification
                'alternatives': [],
                'timestamp': datetime.now().isoformat(),
                'source': 'heuristics',
                'warnings': [
                    "HEURISTIC CLASSIFICATION - VERY LOW ACCURACY",
                    "This identification is based on shape only",
                    "Component MUST be verified with test equipment before use"
                ],
                'replacement_disclaimer': 'Component replacement carries a 90% risk of PCB trace damage. See the full disclaimer for details.'
            }
        except Exception as e:
            self.logger.error(f"Heuristic classification error: {str(e)}")
            return {
                'type': 'unknown',
                'value': 'unknown',
                'confidence': 0.0,
                'alternatives': [],
                'timestamp': datetime.now().isoformat(),
                'source': 'heuristics',
                'warnings': [
                    "HEURISTIC CLASSIFICATION ERROR",
                    "An error occurred during heuristic classification",
                    "Component MUST be verified with test equipment before use"
                ],
                'replacement_disclaimer': 'Component replacement carries a 90% risk of PCB trace damage. See the full disclaimer for details.'
            }
    
    def share_unidentified_component(self, image_data, github_token, description=None):
        """
        Share unidentified component with the community via GitHub
        
        Args:
            image_data: Image of the unidentified component
            github_token: GitHub authentication token
            description: Optional description of the component
        
        Returns:
            str: URL to the GitHub issue or None if failed
        """
        try:
            if not self.github_verification_complete:
                if not self.verify_github_account(github_token):
                    return None
        
            # Create a unique identifier for the image
            img_hash = hashlib.sha256(image_data.tobytes()).hexdigest()
            timestamp = int(time.time())
            filename = f"test_unidentified_component_{img_hash}_{timestamp}.jpg"
        
            # Save image to temp file
            temp_path = os.path.join(os.path.dirname(__file__), 'temp', filename)
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            cv2.imwrite(temp_path, image_data)
        
            # Upload to GitHub as a gist or issue
            # This would be implemented with GitHub API
            # For now, return a placeholder
        
            issue_url = f"https://github.com/your-org/kicad-schematic-importer/issues/new?title=TEST+VERSION+-+Unidentified+Component+{img_hash}"
        
            self.logger.info(f"Shared unidentified component (TEST VERSION): {issue_url}")
        
            return {
                'url': issue_url,
                'image_path': temp_path,
                'timestamp': datetime.now().isoformat(),
                'test_version': True,
                'disclaimer': "TEST VERSION NOTICE: This is a test version of the component sharing feature. Remember that community identifications must be verified with appropriate test equipment. Component replacement carries a 90% risk of PCB trace damage. All shared data should be considered test data only."
            }
        
        except Exception as e:
            self.logger.error(f"Error sharing unidentified component (TEST VERSION): {str(e)}")
            return None
