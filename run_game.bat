@echo off
REM This script provides a convenient way to run The Genesis Module on Windows.

echo Starting The Genesis Module...
@echo off
IF NOT EXIST .installed (
    echo "Dependencies not installed. Please run install.bat first."
    pause
    exit /b
)
python -m car
