#!/usr/bin/env python3
import os
import sys
import shutil
import platform
import argparse
import subprocess
import stat
from pathlib import Path

def check_build_dependencies():
    """Check if required build tools are installed and provide installation instructions"""
    dependencies = {
        'cmake': 'cmake --version',
        'git': 'git --version',
        'python': 'python --version',
        'msbuild': 'msbuild -version' if platform.system() == "Windows" else None
    }
    
    missing = []
    for tool, command in dependencies.items():
        if command:
            try:
                subprocess.run(command.split(), capture_output=True, check=True)
            except (subprocess.SubprocessError, FileNotFoundError):
                missing.append(tool)
    
    if missing:
        print("\nMissing required build tools. Please install the following:")
        
        if 'cmake' in missing:
            print("\nCMake:")
            print("1. Download from https://cmake.org/download/")
            print("2. During installation, select 'Add CMake to system PATH'")
        
        if 'msbuild' in missing:
            print("\nMSBuild (Visual Studio Build Tools):")
            print("1. Download Visual Studio Build Tools from:")
            print("   https://visualstudio.microsoft.com/visual-cpp-build-tools/")
            print("2. In the installer, select:")
            print("   - Desktop development with C++")
            print("   - C++ CMake tools for Windows")
            print("3. After installation, run this from Developer Command Prompt:")
            print("   setx PATH \"%PATH%;C:\\Program Files (x86)\\Microsoft Visual Studio\\2022\\BuildTools\\MSBuild\\Current\\Bin\"")
        
        if 'git' in missing:
            print("\nGit:")
            print("1. Download from https://git-scm.com/download/win")
            print("2. During installation, select 'Git from the command line'")
        
        print("\nAfter installing, you may need to:")
        print("1. Close and reopen your terminal")
        print("2. Run this script again")
        
    return missing

def setup_build_environment():
    """Setup and verify build environment"""
    print("Checking build environment...")
    
    # Check Visual Studio installation
    vs_path = os.environ.get('VS2022INSTALLDIR') or os.environ.get('VS2019INSTALLDIR')
    if not vs_path:
        print("\nVisual Studio not found. Please install Visual Studio 2022 or 2019:")
        print("1. Download Visual Studio Community or Build Tools:")
        print("   https://visualstudio.microsoft.com/downloads/")
        print("2. In the installer, select:")
        print("   - Desktop development with C++")
        print("   - C++ CMake tools for Windows")
        return False
    
    # Check Python development files
    try:
        import distutils.sysconfig
        python_include = distutils.sysconfig.get_python_inc()
        if not os.path.exists(os.path.join(python_include, "Python.h")):
            print("\nPython development files not found. Please install:")
            print("pip install python-dev-tools")
            return False
    except ImportError:
        print("\nCould not verify Python development files.")
        return False
    
    # Check environment variables
    required_vars = ['PATH', 'TEMP', 'SystemRoot']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    if missing_vars:
        print(f"\nMissing required environment variables: {', '.join(missing_vars)}")
        return False
    
    return True

def build_kicad_from_source(python_version, build_dir=None, branch="master"):
    """Build KiCad from source with specified Python version"""
    if platform.system() != "Windows":
        raise RuntimeError("Custom builds currently only supported on Windows")
    
    # Verify build environment
    if not setup_build_environment():
        raise RuntimeError("Build environment setup failed")
    
    # Check build dependencies
    missing_deps = check_build_dependencies()
    if missing_deps:
        raise RuntimeError("Please install required build tools before continuing")
    
    build_dir = build_dir or os.path.join(os.path.expanduser("~"), "kicad-build")
    source_dir = os.path.join(build_dir, "kicad-source")
    install_dir = os.path.join(build_dir, "kicad-install")
    
    print(f"\nBuild configuration:")
    print(f"Build directory: {build_dir}")
    print(f"Source directory: {source_dir}")
    print(f"Install directory: {install_dir}")
    print(f"Python version: {python_version}")
    print(f"Branch: {branch}")
    
    # Clone KiCad repository
    if not os.path.exists(source_dir):
        subprocess.run([
            "git", "clone", 
            "--depth", "1", 
            "--branch", branch,
            "https://gitlab.com/kicad/code/kicad.git",
            source_dir
        ], check=True)
    
    # Configure CMake
    cmake_args = [
        "cmake",
        "-G", "Visual Studio 17 2022",
        "-A", "x64",
        "-DKICAD_SCRIPTING=ON",
        "-DKICAD_SCRIPTING_PYTHON3=ON",
        f"-DPYTHON_EXECUTABLE={sys.executable}",
        "-DKICAD_BUILD_QA_TESTS=OFF",
        f"-DCMAKE_INSTALL_PREFIX={install_dir}",
        source_dir
    ]
    
    os.makedirs(os.path.join(build_dir, "build"), exist_ok=True)
    subprocess.run(cmake_args, cwd=os.path.join(build_dir, "build"), check=True)
    
    # Build KiCad
    subprocess.run([
        "cmake", "--build", ".", 
        "--config", "Release",
        "--target", "install"
    ], cwd=os.path.join(build_dir, "build"), check=True)
    
    return install_dir

def find_kicad_plugin_dir(kicad_version="7.0", custom_build_dir=None):
    """Find KiCad plugin directory for Windows"""
    if custom_build_dir:
        # For custom builds, use the build directory
        return os.path.join(custom_build_dir, "share", "kicad", "scripting", "plugins")
    elif kicad_version == "9.0":
        return os.path.join(os.path.expanduser("~"), "Documents", "KiCad", "9.0", "3rdparty", "plugins")
    else:
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
    parser.add_argument('--build-kicad', action='store_true', help='Build KiCad from source')
    parser.add_argument('--python-version', type=str, help='Python version for custom build')
    parser.add_argument('--build-dir', type=str, help='Directory for custom build')
    
    args = parser.parse_args()
    
    if args.build_kicad:
        try:
            install_dir = build_kicad_from_source(
                args.python_version,
                args.build_dir
            )
            args.kicad_dir = find_kicad_plugin_dir(custom_build_dir=install_dir)
            print(f"Custom KiCad build completed. Installing plugin...")
        except Exception as e:
            print(f"Error building KiCad: {e}")
            sys.exit(1)
    
    if args.create_exe:
        create_executable()
    else:
        install_plugin(args.plugin_dir, args.kicad_dir, args.kicad_version, args.shortcut)

if __name__ == "__main__":
    main()
