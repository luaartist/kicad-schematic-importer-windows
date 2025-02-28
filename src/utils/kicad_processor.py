import os
import subprocess
import logging
import json
from pathlib import Path

class KicadProcessor:
    """Class for handling KiCad CLI operations and netlist generation"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        
        # Add console handler if none exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(handler)
        
        # Find kicad-cli executable
        self.kicad_cli = self._find_kicad_cli()
    
    def _find_kicad_cli(self):
        """Find kicad-cli executable"""
        if os.name == 'nt':  # Windows
            paths = [
                r"C:\Program Files\KiCad\7.0\bin\kicad-cli.exe",
                r"C:\Program Files\KiCad\8.0\bin\kicad-cli.exe",
                r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"
            ]
            for path in paths:
                if os.path.exists(path):
                    return path
        else:  # Linux/macOS
            # Try to find in PATH
            try:
                result = subprocess.run(['which', 'kicad-cli'], capture_output=True, text=True)
                if result.returncode == 0:
                    return result.stdout.strip()
            except Exception:
                pass
            
            # Check common locations
            paths = [
                "/usr/bin/kicad-cli",
                "/usr/local/bin/kicad-cli",
                "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"
            ]
            for path in paths:
                if os.path.exists(path):
                    return path
        
        self.logger.error("Could not find kicad-cli executable")
        return None
    
    def import_svg(self, svg_path, output_dir=None):
        """Import SVG file into KiCad"""
        if not self.kicad_cli:
            self.logger.error("kicad-cli not found")
            return None
        
        if not os.path.exists(svg_path):
            self.logger.error(f"SVG file not found: {svg_path}")
            return None
        
        if output_dir is None:
            output_dir = os.path.dirname(svg_path)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Base name for output files
        base_name = os.path.splitext(os.path.basename(svg_path))[0]
        
        try:
            # Convert SVG to PCB
            pcb_path = os.path.join(output_dir, f"{base_name}.kicad_pcb")
            self.logger.info(f"Converting SVG to PCB: {pcb_path}")
            
            cmd = [
                self.kicad_cli,
                "pcb",
                "import",
                "--input", svg_path,
                "--output", pcb_path,
                "--dpi", "3000",  # High DPI for better accuracy
                "--format", "svg"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                self.logger.error(f"Error converting SVG to PCB: {result.stderr}")
                return None
            
            # Generate netlist
            netlist_path = os.path.join(output_dir, f"{base_name}.net")
            self.logger.info(f"Generating netlist: {netlist_path}")
            
            cmd = [
                self.kicad_cli,
                "pcb",
                "export",
                "netlist",
                "--input", pcb_path,
                "--output", netlist_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                self.logger.error(f"Error generating netlist: {result.stderr}")
                return None
            
            # Generate debug info
            debug_info = {
                "svg_path": svg_path,
                "pcb_path": pcb_path,
                "netlist_path": netlist_path,
                "dpi": 3000,
                "kicad_cli_version": self._get_kicad_cli_version(),
                "timestamp": str(Path(svg_path).stat().st_mtime)
            }
            
            debug_path = os.path.join(output_dir, f"{base_name}_debug.json")
            with open(debug_path, 'w') as f:
                json.dump(debug_info, f, indent=2)
            
            self.logger.info(f"Debug info saved to: {debug_path}")
            return pcb_path
            
        except Exception as e:
            self.logger.error(f"Error during KiCad processing: {e}")
            return None
    
    def _get_kicad_cli_version(self):
        """Get kicad-cli version"""
        if not self.kicad_cli:
            return None
        
        try:
            result = subprocess.run([self.kicad_cli, "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception as e:
            self.logger.error(f"Error getting kicad-cli version: {e}")
        
        return None
