@echo off
REM This script provides a convenient way to run the Car RPG on Windows.

echo Starting Car RPG...
@echo off
IF NOT EXIST .installed (
    echo "Dependencies not installed. Please run install.bat first."
    pause
    exit /b
)
python -m car
