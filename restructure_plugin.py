#!/usr/bin/env python3
import os
import shutil
import re
import sys

def create_directory_structure(base_dir):
    """Create the directory structure for the plugin"""
    print(f"Creating directory structure in {base_dir}...")
    
    # Create directories
    directories = [
        "resources",
        "src/core",
        "src/ui",
        "src/utils",
        "tests"
    ]
    
    for directory in directories:
        dir_path = os.path.join(base_dir, directory)
        os.makedirs(dir_path, exist_ok=True)
        print(f"Created directory: {dir_path}")
    
    # Create __init__.py files
    init_files = [
        "__init__.py",
        "resources/__init__.py",
        "src/__init__.py",
        "src/core/__init__.py",
        "src/ui/__init__.py",
        "src/utils/__init__.py",
        "tests/__init__.py"
    ]
    
    for init_file in init_files:
        file_path = os.path.join(base_dir, init_file)
        with open(file_path, "w") as f:
            f.write("# This file makes the directory a Python package\n")
        print(f"Created file: {file_path}")
    
    # Create placeholder files
    placeholder_files = [
        "README.md",
        "LICENSE"
    ]
    
    for placeholder_file in placeholder_files:
        file_path = os.path.join(base_dir, placeholder_file)
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write(f"# {os.path.splitext(placeholder_file)[0]}\n")
            print(f"Created placeholder file: {file_path}")

def copy_files(source_dir, target_dir):
    """Copy the necessary files to the new structure"""
    print(f"Copying files from {source_dir} to {target_dir}...")
    
    # Files to copy
    files_to_copy = [
        ("action_plugin.py", "action_plugin.py"),
        ("minimal_plugin.py", "minimal_plugin.py"),  # For reference
        ("metadata.json", "metadata.json"),
        ("src/utils/path_validator.py", "src/utils/path_validator.py"),
        ("src/utils/image_processor.py", "src/utils/image_processor.py"),
        ("src/utils/alternative_image_processor.py", "src/utils/alternative_image_processor.py"),
        ("src/core/schematic_importer.py", "src/core/schematic_importer.py"),
        ("src/ui/import_dialog.py", "src/ui/import_dialog.py"),
        ("tests/test_path_validator.py", "tests/test_path_validator.py"),
        ("tests/test_image_processor.py", "tests/test_image_processor.py"),
        ("tests/test_schematic_importer.py", "tests/test_schematic_importer.py"),
        ("resources/icon.png", "resources/icon.png")
    ]
    
    for source_file, target_file in files_to_copy:
        source_path = os.path.join(source_dir, source_file)
        target_path = os.path.join(target_dir, target_file)
        
        # Create target directory if it doesn't exist
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        # Copy file if it exists
        if os.path.exists(source_path):
            shutil.copy2(source_path, target_path)
            print(f"Copied file: {source_path} -> {target_path}")
        else:
            print(f"Warning: Source file not found: {source_path}")

def generalize_code(base_dir):
    """Generalize the code to remove personal information"""
    print(f"Generalizing code in {base_dir}...")
    
    # Files to process
    files_to_process = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith((".py", ".json", ".md")):
                files_to_process.append(os.path.join(root, file))
    
    # Patterns to replace
    patterns = [
        (r"C:\\Users\\walla\\", ""),  # Remove personal paths
        (r"C:/Users/walla/", ""),     # Remove personal paths
        (r"walla", "user"),           # Replace username
        (r"\\", "/"),                 # Normalize path separators
    ]
    
    for file_path in files_to_process:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Apply replacements
            for pattern, replacement in patterns:
                content = re.sub(pattern, replacement, content)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            print(f"Generalized file: {file_path}")
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

def create_install_script(base_dir):
    """Create an install script for the plugin"""
    print(f"Creating install script in {base_dir}...")
    
    install_script = """#!/usr/bin/env python3
import os
import sys
import shutil
import platform
import argparse

def find_kicad_plugin_dir(kicad_version="7.0"):
    """Find KiCad plugin directory"""
    if platform.system() == "Windows":
        if kicad_version == "9.0":
            # KiCad 9.0 uses a different location on Windows
            return os.path.join(os.path.expanduser("~"), "Documents", "KiCad", "9.0", "3rdparty", "plugins")
        else:
            # Windows: %APPDATA%\\kicad\\7.0\\scripting\\plugins
            return os.path.join(os.getenv("APPDATA"), "kicad", kicad_version, "scripting", "plugins")
    elif platform.system() == "Darwin":  # macOS
        # macOS: ~/Library/Application Support/kicad/scripting/plugins
        return os.path.join(os.path.expanduser("~"), "Library", "Application Support", "kicad", kicad_version, "scripting", "plugins")
    else:  # Linux
        # Linux: ~/.local/share/kicad/scripting/plugins
        return os.path.join(os.path.expanduser("~"), ".local", "share", "kicad", kicad_version, "scripting", "plugins")

def install_plugin(plugin_dir=None, kicad_plugin_dir=None, kicad_version="7.0"):
    """Install the plugin to KiCad plugins directory"""
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
    
    print("\\nTo use the plugin:")
    print("1. Start KiCad")
    print("2. Open PCB Editor")
    print("3. Look for 'Schematic Importer' in the Tools menu or toolbar")
    print("\\nIf KiCad is already running, please restart it to load the plugin.")
    
    return target_dir

def main():
    parser = argparse.ArgumentParser(description='Install KiCad Schematic Importer Plugin')
    parser.add_argument('--plugin-dir', type=str, help='Plugin source directory')
    parser.add_argument('--kicad-dir', type=str, help='KiCad plugins directory')
    parser.add_argument('--kicad-version', type=str, default="7.0", help='KiCad version (default: 7.0)')
    
    args = parser.parse_args()
    
    install_plugin(args.plugin_dir, args.kicad_dir, args.kicad_version)

if __name__ == "__main__":
    main()
"""
    
    install_path = os.path.join(base_dir, "install.py")
    with open(install_path, "w") as f:
        f.write(install_script)
    
    print(f"Created install script: {install_path}")

def main():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create a new directory for the restructured plugin
    target_dir = os.path.join(current_dir, "schematic_importer")
    
    # Create the directory structure
    create_directory_structure(target_dir)
    
    # Copy files
    copy_files(current_dir, target_dir)
    
    # Generalize code
    generalize_code(target_dir)
    
    # Create install script
    create_install_script(target_dir)
    
    print("\nPlugin restructuring complete!")
    print(f"The restructured plugin is located at: {target_dir}")
    print("\nTo install the plugin, run:")
    print(f"cd {target_dir}")
    print("python install.py --kicad-version 9.0")

if __name__ == "__main__":
    main()
