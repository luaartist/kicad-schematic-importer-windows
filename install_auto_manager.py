import os
import sys
from pathlib import Path

def install_auto_manager():
    """Install the automatic plugin manager"""
    # Determine KiCad plugin directory
    if os.name == 'nt':  # Windows
        plugin_dir = Path.home() / "Documents" / "KiCad" / "9.0" / "scripting" / "plugins"
    else:
        plugin_dir = Path.home() / ".local" / "share" / "kicad" / "9.0" / "scripting" / "plugins"

    # Create startup script
    startup_script = plugin_dir.parent / "startup" / "plugin_manager_startup.py"
    startup_script.parent.mkdir(parents=True, exist_ok=True)

    with open(startup_script, 'w') as f:
        f.write("""
import sys
from pathlib import Path

# Add plugin manager to path
plugin_manager_path = Path(__file__).parent.parent / "plugin_manager"
sys.path.append(str(plugin_manager_path))

# Initialize automatic startup
from integration.auto_startup import AutoStartupManager
manager = AutoStartupManager()
manager.initialize()
""")

if __name__ == "__main__":
    install_auto_manager()