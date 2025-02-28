# Ensure running as admin
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "Please run as Administrator" -ForegroundColor Red
    exit 1
}

$projectPath = $PSScriptRoot
$venvPath = Join-Path $projectPath ".venv"

# Remove existing venv
if (Test-Path $venvPath) {
    Write-Host "Removing existing venv..." -ForegroundColor Yellow
    Remove-Item -Path $venvPath -Recurse -Force
}

# Create venv directory with explicit permissions
Write-Host "Creating venv directory..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path $venvPath -Force | Out-Null

# Set explicit permissions
$acl = Get-Acl $venvPath
$currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule($currentUser, "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow")
$acl.SetAccessRule($rule)
Set-Acl $venvPath $acl

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
$pythonPath = (Get-Command python).Path
$process = Start-Process -FilePath $pythonPath -ArgumentList "-m", "venv", $venvPath -NoNewWindow -Wait -PassThru

if ($process.ExitCode -eq 0) {
    Write-Host "Virtual environment created successfully" -ForegroundColor Green
    
    # Install requirements
    Write-Host "Installing requirements..." -ForegroundColor Yellow
    $pipPath = Join-Path $venvPath "Scripts\pip.exe"
    $process = Start-Process -FilePath $pipPath -ArgumentList "install", "-r", "requirements.txt" -NoNewWindow -Wait -PassThru
    
    if ($process.ExitCode -eq 0) {
        Write-Host "Requirements installed successfully" -ForegroundColor Green
    } else {
        Write-Host "Failed to install requirements" -ForegroundColor Red
    }
} else {
    Write-Host "Failed to create virtual environment" -ForegroundColor Red
}