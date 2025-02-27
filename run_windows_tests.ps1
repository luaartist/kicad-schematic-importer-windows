# Run basic import test
Write-Host "Running import tests..."
python -m pytest test_import.py -v

# Run pytest suite
Write-Host "`nRunning pytest suite..."
python -m pytest tests/ -v

# Run specific Windows tests
Write-Host "`nChecking Windows-specific functionality..."
# Test shortcut creation
python install.py --shortcut

# Test file paths
python -c "import os; print('Path separators working:', os.path.join('foo', 'bar') == 'foo\\bar')"
