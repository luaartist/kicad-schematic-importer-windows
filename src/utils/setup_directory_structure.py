#!/usr/bin/env python3
"""
Script to set up the directory structure for the KiCad Schematic Importer project.
Run this from the root of your repository.
"""

import os
import shutil
from pathlib import Path

def create_directory(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def create_empty_file(path):
    """Create an empty file if it doesn't exist"""
    if not os.path.exists(path):
        with open(path, 'w') as f:
            pass
        print(f"Created empty file: {path}")

def create_init_file(path):
    """Create an __init__.py file in the directory"""
    init_path = os.path.join(path, "__init__.py")
    if not os.path.exists(init_path):
        with open(init_path, 'w') as f:
            f.write("# This file is part of the KiCad Schematic Importer plugin\n")
        print(f"Created __init__.py: {init_path}")

# Define the directory structure
directories = [
    "src",
    "src/core",
    "src/ui",
    "src/utils",
    "src/ai",
    "src/integration",
    "resources",
    "resources/icons",
    "resources/templates",
    "security",
    "security/templates",
    "tests",
    "docs",
    ".github",
    ".github/workflows",
    ".github/ISSUE_TEMPLATE",
]

# Create the directory structure
for directory in directories:
    create_directory(directory)
    if directory.startswith("src") or directory == "tests":
        create_init_file(directory)

# Create essential files if they don't exist
essential_files = [
    "requirements.txt",
    ".gitignore",
    "setup.py",
    "install.py",
    ".github/workflows/ci.yml",
    ".github/workflows/release.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/feature_request.md",
]

for file_path in essential_files:
    create_empty_file(file_path)

# Move existing files to their proper locations
file_moves = [
    # Add your file moves here, for example:
    # ("existing_file.py", "new/location/file.py"),
]

for source, destination in file_moves:
    if os.path.exists(source) and not os.path.exists(destination):
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.move(source, destination)
        print(f"Moved {source} to {destination}")

print("\nDirectory structure setup complete!")
print("Next steps:")
print("1. Add content to the empty files")
print("2. Implement core functionality")
print("3. Add documentation")