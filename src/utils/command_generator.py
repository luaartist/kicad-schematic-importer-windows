from pathlib import Path
from typing import List, Dict, Optional
import shutil

class ConversionCommandGenerator:
    """Generates commands for external conversion tools without executing them"""
    
    def __init__(self):
        self.available_tools = self._check_available_tools()
    
    def _check_available_tools(self) -> Dict[str, bool]:
        """Check which tools are available without running them"""
        return {
            'inkscape': bool(shutil.which('inkscape')),
            'potrace': bool(shutil.which('potrace'))
        }
    
    def get_inkscape_command(self, input_path: str, output_path: str) -> List[str]:
        """Generate Inkscape conversion command"""
        return [
            'inkscape',
            '--export-filename', str(output_path),
            '--export-type=svg',
            '--export-plain-svg',
            str(input_path)
        ]
    
    def get_potrace_command(self, input_path: str, output_path: str) -> List[str]:
        """Generate Potrace conversion command"""
        return [
            'potrace',
            '--svg',
            '--output', str(output_path),
            str(input_path)
        ]
    
    def get_available_commands(self, input_path: str, output_path: str) -> Dict[str, List[str]]:
        """Get all available conversion commands"""
        commands = {}
        if self.available_tools['inkscape']:
            commands['inkscape'] = self.get_inkscape_command(input_path, output_path)
        if self.available_tools['potrace']:
            commands['potrace'] = self.get_potrace_command(input_path, output_path)
        return commands