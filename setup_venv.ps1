# Ensure we're in the correct directory
$projectRoot = $PSScriptRoot
Set-Location $projectRoot

# Remove existing venv if it exists
Write-Host "Removing existing virtual environment..." -ForegroundColor Yellow
Remove-Item -Path ".venv" -Recurse -Force -ErrorAction SilentlyContinue

# Create new virtual environment
Write-Host "Creating new virtual environment..." -ForegroundColor Yellow
& "C:\Program Files\Python312\python.exe" -m venv .venv

# Ensure pip is installed and updated
Write-Host "Installing and updating pip..." -ForegroundColor Yellow
& ".\.venv\Scripts\python.exe" -m ensurepip --default-pip
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip

# Add KiCad Python path
$KiCadPath = "C:\Program Files\KiCad\7.0\bin"  # Adjust version as needed
if (Test-Path $KiCadPath) {
    $env:PYTHONPATH = "$KiCadPath;$env:PYTHONPATH"
    Write-Host "Added KiCad Python path to PYTHONPATH"
}
else {
    Write-Host "Warning: KiCad installation not found at $KiCadPath"
    Write-Host "Please install KiCad and ensure pcbnew module is available"
}

# Install packages one by one to better handle errors
Write-Host "Installing packages..." -ForegroundColor Yellow
$packages = @(
    "opencv-python>=4.5.0",
    "numpy>=1.24.0",
    "pillow>=8.0.0",
    "skidl>=1.0.0",
    "svgpathtools>=1.5.0",
    "svgwrite>=1.4.0",
    "networkx>=2.6.0",
    "pymupdf>=1.19.0",
    "scikit-image>=0.18.0",
    "pytesseract>=0.3.8",
    "matplotlib>=3.4.0",
    "shapely>=1.8.0",
    "pytest>=7.0.0",
    "black>=22.0.0",
    "pylint>=2.17.0",
    "wxPython>=4.2.0"
)

foreach ($package in $packages) {
    Write-Host "Installing $package..." -ForegroundColor Cyan
    & ".\.venv\Scripts\python.exe" -m pip install $package
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Warning: Failed to install $package" -ForegroundColor Red
    }
}

Write-Host "Setup complete!" -ForegroundColor Green
