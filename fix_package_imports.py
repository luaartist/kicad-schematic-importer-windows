#!/usr/bin/env python3
"""
Script to diagnose and fix Pillow and NumPy import issues.
This script checks for common issues with these packages and provides
recommendations for fixing them.
"""

import os
import sys
import importlib
import subprocess
import platform
from pathlib import Path

def print_section(title):
    """Print a section title with formatting."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)

def check_pillow():
    """Check Pillow installation and configuration."""
    print_section("PILLOW (PIL) DIAGNOSTICS")
    
    try:
        # Try to import PIL
        import PIL
        print(f"✓ PIL is installed (version: {PIL.__version__})")
        
        # Check if PIL has the C extensions
        try:
            from PIL import _imaging
            print("✓ PIL C extensions are available")
        except ImportError:
            print("✗ PIL C extensions are NOT available - this will cause performance issues")
            print("  This usually happens when Pillow is installed without proper build dependencies")
            print("  Recommendation: Reinstall Pillow with pip")
        
        # Try to open an image to test functionality
        try:
            from PIL import Image
            # Create a small test image
            img = Image.new('RGB', (10, 10), color='red')
            print("✓ PIL can create images")
        except Exception as e:
            print(f"✗ Error testing PIL image creation: {e}")
        
        # Check installation location
        print(f"  Installation path: {os.path.dirname(PIL.__file__)}")
        
    except ImportError as e:
        print(f"✗ Error importing PIL: {e}")
        print("  Pillow is not installed or not in the Python path")
    except Exception as e:
        print(f"✗ Unexpected error with PIL: {e}")

def check_numpy():
    """Check NumPy installation and configuration."""
    print_section("NUMPY DIAGNOSTICS")
    
    try:
        # Try to import numpy
        import numpy as np
        print(f"✓ NumPy is installed (version: {np.__version__})")
        
        # Check if numpy has the C extensions by testing a basic operation
        try:
            # Create a small array and perform an operation that requires C extensions
            arr = np.array([1, 2, 3])
            result = np.sum(arr)
            print("✓ NumPy C extensions appear to be working")
        except Exception as e:
            print(f"✗ Error testing NumPy operations: {e}")
            print("  This may indicate issues with NumPy C extensions")
        
        # Check installation location
        numpy_path = os.path.dirname(np.__file__)
        print(f"  Installation path: {numpy_path}")
        
        # Check if numpy is from a source tree
        if 'site-packages' not in numpy_path and 'dist-packages' not in numpy_path:
            print("✗ NumPy appears to be imported from a source tree, not an installed package")
            print("  This can cause import issues, especially with C extensions")
            print("  Recommendation: Check your PYTHONPATH and current working directory")
        else:
            print("✓ NumPy is installed in site-packages (normal installation)")
        
    except ImportError as e:
        print(f"✗ Error importing NumPy: {e}")
        print("  NumPy is not installed or not in the Python path")
    except Exception as e:
        print(f"✗ Unexpected error with NumPy: {e}")

def check_python_path():
    """Check the Python path for potential issues."""
    print_section("PYTHON PATH DIAGNOSTICS")
    
    print("Current Python path (sys.path):")
    for i, path in enumerate(sys.path):
        print(f"  {i+1}. {path}")
    
    # Check for potential issues in the path
    issues = []
    for path in sys.path:
        # Check for source directories that might contain uninstalled packages
        if os.path.exists(os.path.join(path, 'numpy')) and 'site-packages' not in path and 'dist-packages' not in path:
            issues.append(f"Found NumPy in non-standard location: {path}")
        if os.path.exists(os.path.join(path, 'PIL')) and 'site-packages' not in path and 'dist-packages' not in path:
            issues.append(f"Found PIL in non-standard location: {path}")
    
    if issues:
        print("\nPotential issues found in Python path:")
        for issue in issues:
            print(f"  ! {issue}")
    else:
        print("\n✓ No obvious issues found in Python path")

def check_pytest_collection():
    """Check pytest collection to identify issues."""
    print_section("PYTEST COLLECTION DIAGNOSTICS")
    
    try:
        # Run pytest in collect-only mode
        print("Running pytest in collect-only mode to check test discovery...")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only", "-v"],
            capture_output=True,
            text=True,
            check=False
        )
        
        # Check for collection errors
        if "ImportError" in result.stderr or "ImportError" in result.stdout:
            print("✗ Import errors detected during test collection:")
            for line in (result.stderr + result.stdout).split('\n'):
                if "ImportError" in line or "Error" in line:
                    print(f"  {line.strip()}")
        
        # Check for excessive test collection
        test_count = result.stdout.count("collected ")
        if test_count > 100:  # Arbitrary threshold
            print(f"✗ Collected a large number of tests ({test_count})")
            print("  This may indicate pytest is collecting tests from unwanted directories")
            print("  Check your pytest.ini norecursedirs setting")
        
        print("\nTest collection summary:")
        for line in result.stdout.split('\n'):
            if "collected " in line:
                print(f"  {line.strip()}")
        
    except Exception as e:
        print(f"✗ Error running pytest collection: {e}")

def provide_recommendations():
    """Provide recommendations for fixing common issues."""
    print_section("RECOMMENDATIONS")
    
    print("Based on common issues with Pillow and NumPy in this project:")
    
    print("\n1. For Pillow (PIL) issues:")
    print("   - Reinstall Pillow with pip to ensure C extensions are built properly:")
    print("     pip uninstall -y pillow")
    print("     pip install --no-cache-dir pillow>=8.0.0")
    
    print("\n2. For NumPy issues:")
    print("   - Ensure your interpreter is not using a source tree version of NumPy:")
    print("     - Check your working directory and PYTHONPATH")
    print("     - If needed, reinstall NumPy:")
    print("       pip uninstall -y numpy")
    print("       pip install --no-cache-dir numpy>=1.20.0")
    
    print("\n3. For test collection issues:")
    print("   - Exclude directories with the norecursedirs setting in pytest.ini")
    print("   - The pytest.ini file has been updated to exclude:")
    print("     - */kicad_reference/*")
    print("     - */kicad_reference/bin/Lib/*")
    print("     - */kicad_ref/*")
    print("     - */kicad_ref/bin/Lib/*")
    
    print("\nTo run this diagnostic script again after making changes:")
    print(f"  {sys.executable} {__file__}")

def main():
    """Main function to run all diagnostics."""
    print_section("PACKAGE IMPORT DIAGNOSTICS")
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Current working directory: {os.getcwd()}")
    
    check_pillow()
    check_numpy()
    check_python_path()
    check_pytest_collection()
    provide_recommendations()

if __name__ == "__main__":
    main()
