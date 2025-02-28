# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "Found Python: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "Python not found in PATH. Please install Python 3.9 or later" -ForegroundColor Red
    exit 1
}

# Check Python location
$pythonPath = (Get-Command python).Path
Write-Host "Python path: $pythonPath" -ForegroundColor Green

# Check if venv module is available
Write-Host "`nChecking venv module..." -ForegroundColor Yellow
$venvCheck = python -c "import venv; print('venv module available')" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "venv module is available" -ForegroundColor Green
}
else {
    Write-Host "venv module not available. Please reinstall Python with venv support" -ForegroundColor Red
    exit 1
}

# Create test venv in temp directory
$tempDir = [System.IO.Path]::GetTempPath()
$testVenvPath = Join-Path $tempDir "test_venv"
Write-Host "`nTesting venv creation in temp directory: $testVenvPath" -ForegroundColor Yellow

if (Test-Path $testVenvPath) {
    Remove-Item -Path $testVenvPath -Recurse -Force
}

try {
    python -m venv $testVenvPath
    if (Test-Path (Join-Path $testVenvPath "Scripts\python.exe")) {
        Write-Host "Test venv creation successful" -ForegroundColor Green
    }
    else {
        Write-Host "Test venv creation failed - no python.exe found" -ForegroundColor Red
    }
}
catch {
    Write-Host "Test venv creation failed with error: $_" -ForegroundColor Red
}

# Cleanup
Remove-Item -Path $testVenvPath -Recurse -Force -ErrorAction SilentlyContinue