@echo off
echo ===============================================================================
echo                          IMPORT ISSUE FIX TOOLS
echo ===============================================================================
echo.
echo This batch file will run the Python diagnostic script to identify and fix
echo import issues with Pillow, NumPy, and pytest test collection.
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause > nul

echo.
echo ===============================================================================
echo                          RUNNING DIAGNOSTICS
echo ===============================================================================
echo.
python fix_package_imports.py

echo.
echo ===============================================================================
echo                          FIX OPTIONS
echo ===============================================================================
echo.
echo Based on the diagnostics, would you like to:
echo 1. Reinstall Pillow to fix C extension issues
echo 2. Reinstall NumPy to fix import issues
echo 3. Fix both Pillow and NumPy
echo 4. Exit without making changes
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo ===============================================================================
    echo                          FIXING PILLOW
    echo ===============================================================================
    echo.
    echo Uninstalling Pillow...
    pip uninstall -y pillow
    echo.
    echo Reinstalling Pillow with C extensions...
    pip install --no-cache-dir pillow>=8.0.0
) else if "%choice%"=="2" (
    echo.
    echo ===============================================================================
    echo                          FIXING NUMPY
    echo ===============================================================================
    echo.
    echo Uninstalling NumPy...
    pip uninstall -y numpy
    echo.
    echo Reinstalling NumPy...
    pip install --no-cache-dir numpy>=1.20.0
) else if "%choice%"=="3" (
    echo.
    echo ===============================================================================
    echo                          FIXING BOTH PACKAGES
    echo ===============================================================================
    echo.
    echo Uninstalling Pillow and NumPy...
    pip uninstall -y pillow numpy
    echo.
    echo Reinstalling both packages...
    pip install --no-cache-dir pillow>=8.0.0 numpy>=1.20.0
) else if "%choice%"=="4" (
    echo Exiting without making changes
    goto end
) else (
    echo Invalid choice. Exiting without making changes
    goto end
)

echo.
echo ===============================================================================
echo                          VERIFYING TEST COLLECTION
echo ===============================================================================
echo.
echo Running pytest in collect-only mode to verify test collection...
python -m pytest --collect-only -v

echo.
echo ===============================================================================
echo                          COMPLETION
echo ===============================================================================
echo.
echo Package fixes have been applied.
echo To verify that all issues are resolved, run the diagnostic script again:
echo python fix_package_imports.py
echo.
echo If you still encounter issues, you may need to:
echo 1. Check your PYTHONPATH environment variable for conflicting paths
echo 2. Ensure you're not running Python from a directory containing source versions of packages
echo 3. Consider creating a fresh virtual environment for this project
echo.

:end
echo.
echo Press any key to exit...
pause > nul
