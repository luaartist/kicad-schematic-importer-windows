import json
import yaml
from pathlib import Path
from typing import Dict, Any

class AutoConfig:
    DEFAULT_CONFIG = {
        "python_versions": {
            "development": "3.12",
            "fallback": "3.11.5"
        },
        "auto_setup": True,
        "plugins": {
            "schematic_importer": {
                "auto_load": True,
                "preferred_version": "3.12",
                "dependencies": ["opencv-python", "numpy"]
            }
        },
        "monitoring": {
            "enable_logging": True,
            "performance_tracking": True
        }
    }

    def __init__(self):
        self.config_path = Path.home() / ".kicad" / "plugin_manager.yaml"
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        return self.DEFAULT_CONFIG

    def save_config(self):
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f)