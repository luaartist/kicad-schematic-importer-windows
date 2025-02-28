# PowerShell script to diagnose and fix Pillow and NumPy import issues
# This script runs the Python diagnostic script and provides options to fix issues

# Set error action preference
$ErrorActionPreference = "Stop"

# Function to print section headers
function Print-Section {
    param (
        [string]$Title
    )
    
    Write-Host "`n" -NoNewline
    Write-Host ("=" * 80)
    Write-Host (" $Title ".PadLeft(40 + $Title.Length/2).PadRight(80, "="))
    Write-Host ("=" * 80)
}

# Function to run a command and display its output
function Run-Command {
    param (
        [string]$Command,
        [string]$Description
    )
    
    Write-Host "`n$Description" -ForegroundColor Cyan
    Write-Host "Running: $Command" -ForegroundColor Gray
    
    try {
        Invoke-Expression $Command
        Write-Host "Command completed successfully" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "Error executing command: $_" -ForegroundColor Red
        return $false
    }
}

# Check if Python is available
Print-Section "CHECKING PYTHON"
try {
    $pythonVersion = python --version
    Write-Host "Python is available: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "Error: Python is not available in the PATH" -ForegroundColor Red
    Write-Host "Please install Python or add it to your PATH and try again"
    exit 1
}

# Run the diagnostic script
Print-Section "RUNNING DIAGNOSTICS"
Write-Host "Running the diagnostic script to identify issues..."
python fix_package_imports.py

# Ask user if they want to fix the issues
Print-Section "FIX OPTIONS"
Write-Host "Based on the diagnostics, would you like to:" -ForegroundColor Yellow
Write-Host "1. Reinstall Pillow to fix C extension issues"
Write-Host "2. Reinstall NumPy to fix import issues"
Write-Host "3. Fix both Pillow and NumPy"
Write-Host "4. Exit without making changes"

$choice = Read-Host "Enter your choice (1-4)"

switch ($choice) {
    "1" {
        Print-Section "FIXING PILLOW"
        Run-Command "pip uninstall -y pillow" "Uninstalling Pillow..."
        Run-Command "pip install --no-cache-dir pillow>=8.0.0" "Reinstalling Pillow with C extensions..."
    }
    "2" {
        Print-Section "FIXING NUMPY"
        Run-Command "pip uninstall -y numpy" "Uninstalling NumPy..."
        Run-Command "pip install --no-cache-dir numpy>=1.20.0" "Reinstalling NumPy..."
    }
    "3" {
        Print-Section "FIXING BOTH PACKAGES"
        Run-Command "pip uninstall -y pillow numpy" "Uninstalling Pillow and NumPy..."
        Run-Command "pip install --no-cache-dir pillow>=8.0.0 numpy>=1.20.0" "Reinstalling both packages..."
    }
    "4" {
        Write-Host "Exiting without making changes" -ForegroundColor Yellow
        exit 0
    }
    default {
        Write-Host "Invalid choice. Exiting without making changes" -ForegroundColor Red
        exit 1
    }
}

# Run pytest to verify test collection
Print-Section "VERIFYING TEST COLLECTION"
Write-Host "Running pytest in collect-only mode to verify test collection..."
python -m pytest --collect-only -v

# Final message
Print-Section "COMPLETION"
Write-Host "Package fixes have been applied." -ForegroundColor Green
Write-Host "To verify that all issues are resolved, run the diagnostic script again:"
Write-Host "python fix_package_imports.py" -ForegroundColor Cyan
Write-Host "`nIf you still encounter issues, you may need to:"
Write-Host "1. Check your PYTHONPATH environment variable for conflicting paths"
Write-Host "2. Ensure you're not running Python from a directory containing source versions of packages"
Write-Host "3. Consider creating a fresh virtual environment for this project"
