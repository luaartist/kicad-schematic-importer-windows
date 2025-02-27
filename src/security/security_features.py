import os
import json
import hashlib
import base64
import secrets
import time

class SecurityFeatures:
    """Security features for the KiCad Schematic Importer Plugin"""
    
    def __init__(self, config_path=None):
        self.config = self._load_config(config_path)
        self.security_config = self.config.get('security', {})
    
    def _load_config(self, config_path):
        """Load configuration from file"""
        if config_path is None:
            # Try to find config in standard locations
            possible_paths = [
                'config.json',
                os.path.join(os.path.dirname(__file__), '..', 'config.json'),
                os.path.join(os.path.expanduser('~'), '.kicad_schematic_importer', 'config.json')
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    config_path = path
                    break
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
        
        return {}
    
    def is_feature_enabled(self, feature_name):
        """Check if a security feature is enabled"""
        if feature_name in self.security_config:
            return self.security_config[feature_name].get('enabled', False)
        return False
    
    def get_secure_hash(self, data):
        """Generate a secure hash of data"""
        if isinstance(data, str):
            data = data