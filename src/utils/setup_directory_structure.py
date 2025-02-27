#!/usr/bin/env python3
"""
Script to set up the directory structure for the KiCad Schematic Importer project.
Run this from the root of your repository.
"""

import os
import shutil

def setup_test_repository():
    """Set up the complete repository structure for testing"""
    
    # Core directories
    directories = [
        "src",
        "src/core",
        "src/ui",
        "src/utils",
        "src/ai",
        "src/integration",
        "src/plugin",
        "tests",
        "tests/unit",
        "tests/integration",
        "tests/data",
        "tests/ref_layouts",
        "resources",
        "resources/icons",
        "resources/templates",
        "docs",
        ".github/workflows",
        ".github/ISSUE_TEMPLATE"
    ]

    # Create directories
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        if directory.startswith(("src", "tests")):
            with open(os.path.join(directory, "__init__.py"), "w") as f:
                pass

    # Essential files
    essential_files = {
        "requirements.txt": "",
        "requirements-dev.txt": "",
        ".gitignore": """
*.pyc
__pycache__/
.pytest_cache/
.coverage
htmlcov/
dist/
build/
*.egg-info/
.env
.venv/
""",
        ".github/workflows/ci.yml": """
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt
      - name: Run tests
        run: pytest
""",
        "tests/conftest.py": """
import pytest
import os
import sys

# Add src to path for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
""",
        "setup.py": """
from setuptools import setup, find_packages

setup(
    name="kicad-schematic-importer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Add your dependencies
    ],
)
"""
    }

    # Create essential files
    for file_path, content in essential_files.items():
        dir_path = os.path.dirname(file_path)
        if dir_path:  # Only create directory if path is not empty
            os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "w") as f:
            f.write(content)

    # Move reference layouts
    ref_layouts_sources = [
        "kicad-python/tests/geometry/7.0/ref_layouts",
        "kicad-python/tests/geometry/8.0/ref_layouts",
        "kicad-python/tests/geometry/9.0/ref_layouts"
    ]
    
    for source in ref_layouts_sources:
        if os.path.exists(source):
            version = source.split("/")[3]
            dest = f"tests/ref_layouts/{version}"
            shutil.copytree(source, dest, dirs_exist_ok=True)

    print("Repository structure set up successfully!")
    print("\nNext steps:")
    print("1. Initialize git repository: git init")
    print("2. Make initial commit: git add . && git commit -m 'Initial commit'")
    print("3. Add remote repository and push")

if __name__ == "__main__":
    setup_test_repository()  # Call the main function
