@echo off
REM This script provides a convenient way to run The Genesis Module on Windows.

echo Starting The Genesis Module...
@echo off
IF NOT EXIST .installed (
    echo "Dependencies not installed. Please run install.bat first."
    pause
    exit /b
)

REM Activate venv if present
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

python3 -m car %*
