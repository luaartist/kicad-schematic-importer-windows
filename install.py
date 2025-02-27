#!/usr/bin/env python3
import os
import sys
import shutil
import platform
import argparse
import subprocess
import stat

def find_kicad_plugin_dir(kicad_version="7.0"):
    """Find KiCad plugin directory based on platform"""
    system = platform.system()
    home = os.path.expanduser("~")
    
    if system == "Windows":
        # Windows: %APPDATA%\kicad\7.0\scripting\plugins
        return os.path.join(os.getenv("APPDATA"), "kicad", kicad_version, "scripting", "plugins")
    elif system == "Darwin":
        # macOS: ~/Library/Preferences/kicad/7.0/scripting/plugins
        return os.path.join(home, "Library", "Preferences", "kicad", kicad_version, "scripting", "plugins")
    else:
        # Linux: ~/.kicad/7.0/scripting/plugins
        return os.path.join(home, ".kicad", kicad_version, "scripting", "plugins")

def install_plugin(plugin_dir=None, kicad_plugin_dir=None, kicad_version="7.0", create_shortcut=False):
    """Install the plugin to KiCad plugins directory"""
    # Use current directory if no plugin directory specified
    if plugin_dir is None:
        plugin_dir = os.path.abspath(os.path.dirname(__file__))
    
    # Find KiCad plugins directory if not specified
    if kicad_plugin_dir is None:
        kicad_plugin_dir = find_kicad_plugin_dir(kicad_version)
    
    # Create target directory
    target_dir = os.path.join(kicad_plugin_dir, "schematic_importer")
    os.makedirs(target_dir, exist_ok=True)
    
    # Copy plugin files
    files_copied = 0
    for item in os.listdir(plugin_dir):
        # Skip some files/directories
        if item in [".git", ".github", "venv", "env", "__pycache__", "install.py", ".gitignore", ".clineignore"]:
            continue
        
        source = os.path.join(plugin_dir, item)
        destination = os.path.join(target_dir, item)
        
        if os.path.isdir(source):
            shutil.copytree(source, destination, dirs_exist_ok=True)
            files_copied += len([f for _, _, files in os.walk(source) for f in files])
        else:
            shutil.copy2(source, destination)
            files_copied += 1
    
    print(f"Plugin installed to: {target_dir}")
    print(f"Copied {files_copied} files")
    
    # Create desktop shortcut if requested
    if create_shortcut:
        create_desktop_shortcut(target_dir)
    
    print("\nTo use the plugin:")
    print("1. Start KiCad")
    print("2. Open PCB Editor")
    print("3. Look for 'Import Schematic from Image' in the Tools menu or toolbar")
    print("\nIf KiCad is already running, please restart it to load the plugin.")
    
    return target_dir

def create_desktop_shortcut(plugin_dir):
    """Create a desktop shortcut to launch KiCad with the plugin"""
    system = platform.system()
    desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
    
    if system == "Windows":
        # Windows shortcut
        try:
            import winshell
            from win32com.client import Dispatch
            
            kicad_path = find_kicad_executable()
            if not kicad_path:
                print("Could not find KiCad executable. Skipping shortcut creation.")
                return
                
            shortcut_path = os.path.join(desktop_dir, "KiCad with Schematic Importer.lnk")
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = kicad_path
            shortcut.WorkingDirectory = os.path.dirname(kicad_path)
            shortcut.IconLocation = kicad_path
            shortcut.save()
            
            print(f"Created desktop shortcut: {shortcut_path}")
        except ImportError:
            print("Could not create Windows shortcut. Please install winshell and pywin32 packages.")
            print("pip install winshell pywin32")
    
    elif system == "Linux":
        # Linux .desktop file
        desktop_file = os.path.join(desktop_dir, "kicad-schematic-importer.desktop")
        kicad_path = find_kicad_executable()
        
        if not kicad_path:
            print("Could not find KiCad executable. Skipping shortcut creation.")
            return
            
        with open(desktop_file, 'w') as f:
            f.write(f"""[Desktop Entry]
Type=Application
Name=KiCad with Schematic Importer
Comment=Open KiCad with Schematic Importer plugin
Exec={kicad_path}
Icon=kicad
Terminal=false
Categories=Development;Electronics;
""")
        # Make executable
        os.chmod(desktop_file, os.stat(desktop_file).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        print(f"Created desktop shortcut: {desktop_file}")
    
    elif system == "Darwin":
        # macOS shortcut/alias
        print("Desktop shortcut creation not implemented for macOS.")
        print("You can create an alias manually by right-clicking KiCad in Applications and selecting 'Make Alias'.")

def find_kicad_executable():
    """Find the KiCad executable path"""
    system = platform.system()
    
    if system == "Windows":
        # Common installation paths on Windows
        possible_paths = [
            os.path.join(os.environ.get('ProgramFiles', 'C:\\Program Files'), "KiCad", "bin", "kicad.exe"),
            os.path.join(os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)'), "KiCad", "bin", "kicad.exe")
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
                
    elif system == "Linux":
        # Try to find using 'which'
        try:
            return subprocess.check_output(["which", "kicad"]).decode().strip()
        except:
            pass
            
    elif system == "Darwin":
        # Common installation path on macOS
        path = "/Applications/KiCad/KiCad.app/Contents/MacOS/KiCad"
        if os.path.exists(path):
            return path
    
    return None

def create_executable():
    """Create an executable version of the installer"""
    try:
        import PyInstaller.__main__
        
        print("Creating executable installer...")
        PyInstaller.__main__.run([
            'install.py',
            '--onefile',
            '--name=schematic_importer_installer',
            '--console'
        ])
        
        print("\nExecutable created successfully!")
        print("Look for 'schematic_importer_installer' in the 'dist' folder")
        
    except ImportError:
        print("PyInstaller not found. Please install it with:")
        print("pip install pyinstaller")
        print("\nThen run this script again with the --create-exe option")

def main():
    parser = argparse.ArgumentParser(description='Install KiCad Schematic Importer Plugin')
    parser.add_argument('--plugin-dir', type=str, help='Plugin source directory')
    parser.add_argument('--kicad-dir', type=str, help='KiCad plugins directory')
    parser.add_argument('--kicad-version', type=str, default="7.0", help='KiCad version (default: 7.0)')
    parser.add_argument('--shortcut', action='store_true', help='Create desktop shortcut')
    parser.add_argument('--create-exe', action='store_true', help='Create executable installer')
    
    args = parser.parse_args()
    
    if args.create_exe:
        create_executable()
    else:
        install_plugin(args.plugin_dir, args.kicad_dir, args.kicad_version, args.shortcut)

if __name__ == "__main__":
    # Make the script executable on Unix-like systems
    if platform.system() != "Windows":
        script_path = os.path.abspath(__file__)
        current_mode = os.stat(script_path).st_mode
        os.chmod(script_path, current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    
    main()
