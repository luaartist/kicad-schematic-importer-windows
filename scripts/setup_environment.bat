@echo off
NET SESSION >nul 2>&1
if %errorLevel% == 0 (
    echo Running with administrator privileges...
) else (
    echo Please run this script as administrator
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

echo Creating virtual environment...
if exist .venv (
    echo Removing existing virtual environment...
    rmdir /s /q .venv
)

python -m venv .venv

if exist .venv\Scripts\python.exe (
    echo Virtual environment created successfully!
    echo Installing requirements...
    .venv\Scripts\python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install requirements
        pause
        exit /b 1
    )
    echo Setup completed successfully!
) else (
    echo Failed to create virtual environment
    pause
    exit /b 1
)

pause