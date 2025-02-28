"""
Installation instructions for the Schematic Importer Debug functionality.

This script provides instructions for installing the debug plugin in KiCad.
The actual installation must be done from within KiCad's Python console
since it requires KiCad's Python environment.
"""

import os
import shutil

def print_instructions():
    print("\nSchematic Importer Debug Installation")
    print("====================================")
    print("\nTo install the debug functionality:")
    print("\n1. Copy these files to KiCad's plugin directory:")
    
    # Get source files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    files_to_copy = ['debug_plugin.py', 'test_debug.py']
    
    # Get KiCad v9.0 plugin directory
    kicad_plugin_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'KiCad', '9.0', '3rdparty', 'plugins', 'enhanced_importer_v2')
    if not os.path.exists(kicad_plugin_dir):
        print(f"Error: Plugin directory not found: {kicad_plugin_dir}")
        print("Please ensure KiCad v9.0 is installed and the enhanced_importer_v2 plugin is present")
        return
    
    # Copy files
    for file in files_to_copy:
        src = os.path.join(current_dir, file)
        dst = os.path.join(kicad_plugin_dir, file)
        try:
            shutil.copy2(src, dst)
            print(f"   ✓ Copied {file} to {dst}")
        except Exception as e:
            print(f"   × Error copying {file}: {e}")
    
    print("\n2. Open KiCad v9.0 PCB Editor")
    print("\n3. Open Python Console (View → Python Console)")
    print("\n4. Run these commands in the Python Console:")
    print("   >>> import sys")
    print(f"   >>> sys.path.append(r'{kicad_plugin_dir}')")
    print("   >>> import debug_plugin")
    print("   >>> debug_plugin.register_debug_plugin()")
    
    print("\nAfter installation:")
    print("1. The debug window will be available in:")
    print("   Tools → External Plugins → Schematic Importer Debug")
    print("2. Or use the keyboard shortcut: Alt+S then D")
    
    print("\nDebug files will be saved to:")
    print(f"- Log: {os.path.join(kicad_plugin_dir, 'debug', 'schematic_importer_debug.log')}")
    print(f"- Images: {os.path.join(kicad_plugin_dir, 'debug', 'images')}")
    
    # Create debug directories
    debug_dir = os.path.join(kicad_plugin_dir, 'debug')
    images_dir = os.path.join(debug_dir, 'images')
    os.makedirs(debug_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    
    print("\nTo test the installation:")
    print("1. Open KiCad PCB Editor")
    print("2. Open Python Console")
    print("3. Run:")
    print("   >>> import test_debug")
    print("   >>> test_debug.test_schematic_import()")

def setup_debug_structure():
    """Setup debug plugin structure based on working enhanced importer"""
    kicad_plugin_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'KiCad', '9.0', '3rdparty', 'plugins')
    debug_dir = os.path.join(kicad_plugin_dir, 'enhanced_importer_v2_debug')
    
    # Create directory structure
    dirs = [
        os.path.join(debug_dir, 'src'),
        os.path.join(debug_dir, 'src', 'utils'),
        os.path.join(debug_dir, 'resources'),
        os.path.join(debug_dir, 'resources', 'icons'),
        os.path.join(debug_dir, 'debug')
    ]
    
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, '__init__.py'), 'w') as f:
            f.write('# Debug plugin package\n')
    
    # Copy necessary files from enhanced importer
    enhanced_dir = os.path.join(kicad_plugin_dir, 'enhanced_importer_v2')
    if os.path.exists(enhanced_dir):
        for root, _, files in os.walk(enhanced_dir):
            for file in files:
                if file.endswith(('.py', '.png', '.json')):
                    src = os.path.join(root, file)
                    rel_path = os.path.relpath(src, enhanced_dir)
                    dst = os.path.join(debug_dir, rel_path)
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    shutil.copy2(src, dst)
    
    print(f"Debug plugin structure created at: {debug_dir}")
    return debug_dir

def main():
    print_instructions()
    
    print("\nSetup Complete!")
    print("===============")
    print("\nTo use the debug window:")
    print("1. Open KiCad PCB Editor")
    print("2. Access the debug window via:")
    print("   - Tools → External Plugins → Schematic Importer Debug")
    print("   - Or use shortcut: Alt+S then D")
    
    print("\nDebug files are saved to:")
    print(f"- Log file: {os.path.abspath('schematic_importer_debug.log')}")
    print(f"- Debug images: {os.path.abspath('debug')}")
    
    print("\nTroubleshooting:")
    print("1. If the plugin doesn't appear in KiCad:")
    print("   - Restart KiCad")
    print("   - Check the plugin directory in KiCad's preferences")
    print("2. If the debug window doesn't show:")
    print("   - Check the log file for errors")
    print("   - Try running the test_debug.py script directly")
    print("\nFor more help, check the documentation or report issues on GitHub")

if __name__ == '__main__':
    main()
