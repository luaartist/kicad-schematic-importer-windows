import os
import shutil
import sys

def install_console():
    # Get KiCad plugins directory
    home = os.path.expanduser('~')
    plugins_dir = os.path.join(home, 'Documents', 'KiCad', '9.0', 'plugins')
    
    # Create plugins directory if it doesn't exist
    os.makedirs(plugins_dir, exist_ok=True)
    
    # Copy the console plugin
    src_file = 'custom_python_console.py'
    dst_file = os.path.join(plugins_dir, src_file)
    
    try:
        shutil.copy2(src_file, dst_file)
        print(f"Successfully installed Python Console plugin to: {dst_file}")
        print("\nTo use the console:")
        print("1. Restart KiCad")
        print("2. Open PCB Editor")
        print("3. Look for 'Python Console' under Tools → External Plugins")
    except Exception as e:
        print(f"Error installing plugin: {e}")

if __name__ == '__main__':
    install_console()