# Import Issue Fix Tools

This directory contains tools to diagnose and fix common import issues with Pillow, NumPy, and pytest test collection in the KiCad Schematic Importer project.

## Issues Addressed

1. **Pillow (PIL) Import Issues**
   - Missing C extensions causing performance issues or import errors
   - Incorrect installation or build configuration

2. **NumPy Import Issues**
   - Source tree version conflicts
   - Missing C extensions
   - Path conflicts

3. **Test Collection Issues**
   - Pytest collecting tests from unwanted directories (e.g., kicad_reference/bin/Lib)
   - Excessive test collection slowing down test runs

## Files Included

- **fix_package_imports.py**: Python diagnostic script that checks for common issues with Pillow and NumPy imports and provides recommendations.
- **fix_imports.ps1**: PowerShell script that runs the diagnostic script and provides options to fix the identified issues.
- **fix_imports.bat**: Batch file alternative for users who prefer batch files over PowerShell.
- **pytest.ini**: Updated configuration file that excludes unwanted directories from test collection.

## How to Use

### Option 1: Run the PowerShell Script (Recommended)

1. Open PowerShell in the project directory
2. Run the script:
   ```powershell
   .\fix_imports.ps1
   ```
3. Follow the on-screen prompts to diagnose and fix issues

### Option 2: Run the Batch File

1. Open a command prompt in the project directory
2. Run the batch file:
   ```
   fix_imports.bat
   ```
3. Follow the on-screen prompts to diagnose and fix issues

### Option 3: Run the Python Script Directly

1. Open a command prompt or PowerShell in the project directory
2. Run the script:
   ```
   python fix_package_imports.py
   ```
3. Review the diagnostic output and manually apply the recommended fixes

## Fixes Applied

### Pillow Fix

The script reinstalls Pillow to ensure its C extensions are built properly:

```
pip uninstall -y pillow
pip install --no-cache-dir pillow>=8.0.0
```

### NumPy Fix

The script ensures your interpreter is not inadvertently using a source tree version of NumPy and reinstalls NumPy if needed:

```
pip uninstall -y numpy
pip install --no-cache-dir numpy>=1.20.0
```

### Test Collection Fix

The pytest.ini file has been updated to exclude directories that should not be included in test collection:

```
norecursedirs = 
    */kicad_reference/* 
    */kicad_reference/bin/Lib/*
    */kicad_ref/*
    */kicad_ref/bin/Lib/*
    */venv/*
    */env/*
    */.venv/*
    */build/*
    */dist/*
    */.git/*
    */.github/*
    */docs/*
```

## Additional Troubleshooting

If you continue to experience issues after running these scripts:

1. **Check your PYTHONPATH environment variable** for paths that might contain conflicting versions of packages.

2. **Ensure you're not running Python from a directory** that contains source versions of packages (e.g., a directory with a 'numpy' folder).

3. **Consider creating a fresh virtual environment** for this project:
   ```
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Check for stale .pyc files** that might be causing import conflicts:
   ```
   powershell -Command "Get-ChildItem -Path . -Include *.pyc -Recurse | Remove-Item"
   ```

5. **Verify your Python installation** is not corrupted by running:
   ```
   python -m pip check
