# Run basic import test
Write-Host "Running import tests..."
python test_import.py

# Run pytest suite
Write-Host "`nRunning pytest suite..."
python -m pytest tests/test_basic.py -v

# Run specific Windows tests
Write-Host "`nChecking Windows-specific functionality..."
# Test shortcut creation
python install.py --shortcut

# Test file paths
python -c "import os; print('Path separators working:', os.path.join('foo', 'bar') == 'foo\\bar')"