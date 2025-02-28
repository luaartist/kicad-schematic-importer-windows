import os
import sys
import platform
import subprocess

if platform.system() != "Windows":
    print("Error: Tests can only be run on Windows")
    sys.exit(1)

# Run Windows-specific tests using PowerShell with execution policy bypass
print("Running Windows tests...")
subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", ".\\run_windows_tests.ps1"], check=True)
