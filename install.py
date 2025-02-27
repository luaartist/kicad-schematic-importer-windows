#!/usr/bin/env python3
import os
import sys
import shutil
import platform
import argparse
import subprocess
import stat

def find_kicad_plugin_dir(kicad_version="7.0"):
    """Find KiCad plugin directory for Windows"""
    # Windows: %APPDATA%\kicad\7.0\scripting\plugins
    return os.path.join(os.getenv("APPDATA"), "kicad", kicad_version, "scripting", "plugins")

def install_plugin(plugin_dir=None, kicad_plugin_dir=None, kicad_version="7.0", create_shortcut=False):
    """Install the plugin to KiCad plugins directory"""
    if platform.system() != "Windows":
        print("Error: This plugin only supports Windows")
        sys.exit(1)

    if not plugin_dir:
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
    
    if not kicad_plugin_dir:
        kicad_plugin_dir = find_kicad_plugin_dir(kicad_version)
    
    target_dir = os.path.join(kicad_plugin_dir, "schematic_importer")
    
    # Create plugin directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    
    # Copy plugin files
    files_copied = 0
    for source in os.listdir(plugin_dir):
        if source.startswith((".", "__")) or source == "install.py":
            continue
            
        source_path = os.path.join(plugin_dir, source)
        destination = os.path.join(target_dir, source)
        
        if os.path.isdir(source_path):
            shutil.copytree(source_path, destination, dirs_exist_ok=True)
            files_copied += len([f for _, _, files in os.walk(source_path) for f in files])
        else:
            shutil.copy2(source_path, destination)
            files_copied += 1
    
    print(f"Plugin installed to: {target_dir}")
    print(f"Copied {files_copied} files")
    
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
    try:
        import winshell
        from win32com.client import Dispatch
        
        kicad_path = find_kicad_executable()
        if not kicad_path:
            print("Could not find KiCad executable. Skipping shortcut creation.")
            return
            
        desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
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

def find_kicad_executable():
    """Find the KiCad executable path on Windows"""
    possible_paths = [
        os.path.join(os.environ.get('ProgramFiles', 'C:\\Program Files'), "KiCad", "bin", "kicad.exe"),
        os.path.join(os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)'), "KiCad", "bin", "kicad.exe")
    ]
    
    for path in possible_paths:
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
    if platform.system() != "Windows":
        print("Error: This plugin only supports Windows")
        sys.exit(1)

    parser = argparse.ArgumentParser(description='Install KiCad Schematic Importer Plugin (Windows Only)')
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
    main()
