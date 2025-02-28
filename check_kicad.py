import os
import sys

def check_kicad_install():
    print("\nKiCad Installation Check")
    print("=======================")
    
    # Check common KiCad installation paths
    kicad_paths = [
        r"C:\Program Files\KiCad\9.0",
        r"C:\Program Files (x86)\KiCad\9.0",
        r"C:\KiCad\9.0"
    ]
    
    for path in kicad_paths:
        if os.path.exists(path):
            print(f"Found KiCad at: {path}")
            # Check for key files
            bin_dir = os.path.join(path, "bin")
            if os.path.exists(bin_dir):
                print("  Checking key files:")
                for file in ["kicad.exe", "pcbnew.exe", "python.exe"]:
                    full_path = os.path.join(bin_dir, file)
                    if os.path.exists(full_path):
                        print(f"    ✓ {file} found")
                    else:
                        print(f"    ✗ {file} missing")
            break
    else:
        print("KiCad installation not found in common locations")
    
    # Check Python environment
    print("\nPython Environment:")
    print(f"Python Version: {sys.version}")
    print(f"Python Path: {sys.executable}")

if __name__ == "__main__":
    check_kicad_install()