import os
import sys

def check_plugin_installation():
    """Check KiCad plugin directories and console installation"""
    
    # Common KiCad plugin paths
    possible_paths = [
        os.path.join(os.path.expanduser('~'), 'Documents', 'KiCad', '9.0', 'plugins'),
        os.path.join(os.path.expanduser('~'), '.kicad', 'scripting', 'plugins'),
        os.path.join(os.path.expanduser('~'), 'KiCad', 'plugins'),
        r'C:\Program Files\KiCad\9.0\share\kicad\scripting\plugins'
    ]
    
    print("Checking KiCad plugin directories...")
    print("-" * 50)
    
    found = False
    for path in possible_paths:
        if os.path.exists(path):
            print(f"\nFound plugin directory: {path}")
            console_path = os.path.join(path, 'custom_python_console.py')
            
            if os.path.exists(console_path):
                print("✓ Python Console plugin found!")
                print(f"  Location: {console_path}")
                found = True
            else:
                print("✗ Python Console plugin not found in this directory")
                
            # List other plugins
            plugins = [f for f in os.listdir(path) if f.endswith('.py')]
            if plugins:
                print("\nOther plugins in directory:")
                for plugin in plugins:
                    print(f"  - {plugin}")
        else:
            print(f"\nDirectory not found: {path}")
    
    if not found:
        print("\nRECOMMENDED ACTION:")
        print("1. Copy custom_python_console.py to one of these directories:")
        for path in possible_paths:
            print(f"   - {path}")
        print("2. Restart KiCad")
        print("3. Look for 'Python Console' under Tools → External Plugins")

if __name__ == '__main__':
    check_plugin_installation()