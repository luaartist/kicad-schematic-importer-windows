# Requires -RunAsAdministrator

# Function to test path writability
function Test-PathWritable {
    param([string]$Path)
    try {
        $testFile = Join-Path $Path "test.tmp"
        [IO.File]::OpenWrite($testFile).Close()
        Remove-Item $testFile
        return $true
    }
    catch {
        return $false
    }
}

# Function to create venv with proper permissions
function Create-VirtualEnv {
    param([string]$VenvPath)
    
    Write-Host "Creating virtual environment at $VenvPath..." -ForegroundColor Yellow
    
    # Remove existing venv if present
    if (Test-Path $VenvPath) {
        Write-Host "Removing existing virtual environment..." -ForegroundColor Yellow
        Remove-Item -Path $VenvPath -Recurse -Force
    }
    
    # Create new venv with explicit permissions
    try {
        # Create base directory with explicit permissions
        New-Item -ItemType Directory -Path $VenvPath -Force | Out-Null
        $acl = Get-Acl $VenvPath
        $currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
        $permission = $currentUser, "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow"
        $accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule $permission
        $acl.SetAccessRule($accessRule)
        Set-Acl $VenvPath $acl
        
        # Create virtual environment
        python -m venv $VenvPath
        
        # Verify creation
        if (Test-Path (Join-Path $VenvPath "Scripts\python.exe")) {
            Write-Host "Virtual environment created successfully!" -ForegroundColor Green
            return $true
        }
        else {
            Write-Host "Virtual environment creation failed!" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "Error creating virtual environment: $_" -ForegroundColor Red
        return $false
    }
}

# Function to install requirements
function Install-Requirements {
    param([string]$VenvPath)
    
    $pipPath = Join-Path $VenvPath "Scripts\pip.exe"
    $requirementsPath = "requirements.txt"
    
    if (-not (Test-Path $requirementsPath)) {
        Write-Host "requirements.txt not found!" -ForegroundColor Red
        return $false
    }
    
    Write-Host "Installing requirements..." -ForegroundColor Yellow
    try {
        & $pipPath install -r $requirementsPath
        Write-Host "Requirements installed successfully!" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "Error installing requirements: $_" -ForegroundColor Red
        return $false
    }
}

# Main execution
$venvPath = ".venv"
$projectRoot = $PSScriptRoot

# Check if running as administrator
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "Please run this script as Administrator" -ForegroundColor Red
    exit 1
}

# Create virtual environment
if (Create-VirtualEnv $venvPath) {
    # Install requirements
    Install-Requirements $venvPath
}