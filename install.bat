@echo off
setlocal

echo === The Genesis Module — Installer ===
echo.

REM --- Check for python3 ---
where python3 >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    REM Try 'python' as fallback on Windows (py launcher or store install)
    where python >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Python is not installed or not in PATH.
        echo.
        echo   Option 1: Download from https://www.python.org/downloads/
        echo             Be sure to check "Add Python to PATH" during install.
        echo.
        echo   Option 2: Install via Windows Store: "python3" in Start Menu
        echo.
        echo   Option 3: winget install Python.Python.3.12
        echo.
        pause
        exit /b 1
    )
    set PYTHON=python
) else (
    set PYTHON=python3
)

echo Found Python:
%PYTHON% --version

REM --- Check for pip ---
%PYTHON% -m pip -V >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: pip is not available.
    echo.
    echo   Try: %PYTHON% -m ensurepip --upgrade
    echo   Or reinstall Python with "pip" checked in the installer.
    echo.
    pause
    exit /b 1
)

echo Found pip.
echo.

REM --- Create virtual environment ---
if not exist "venv" (
    echo Creating virtual environment...
    %PYTHON% -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to create virtual environment.
        echo   Try: %PYTHON% -m pip install virtualenv
        pause
        exit /b 1
    )
)
echo Virtual environment ready.

REM Activate venv
call venv\Scripts\activate.bat

REM --- Install base requirements ---
echo.
echo Installing base requirements...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

REM --- llama-cpp-python ---
echo.
echo Installing llama-cpp-python...
REM Check for NVIDIA GPU via nvidia-smi
where nvidia-smi >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Detected NVIDIA GPU — building with CUDA support...
    echo   This requires the CUDA toolkit. Download from:
    echo   https://developer.nvidia.com/cuda-downloads
    set CMAKE_ARGS=-DGGML_CUDA=on
    python -m pip install llama-cpp-python --force-reinstall --no-cache-dir
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo WARNING: CUDA build failed. Falling back to CPU-only build.
        set CMAKE_ARGS=
        python -m pip install llama-cpp-python --force-reinstall --no-cache-dir
    )
) else (
    echo No NVIDIA GPU detected — installing CPU-only build.
    python -m pip install llama-cpp-python --force-reinstall --no-cache-dir
)

REM Install Windows-specific extras if file is non-empty
for %%A in (requirements-windows.txt) do if %%~zA GTR 2 (
    python -m pip install -r requirements-windows.txt
)

echo.
echo Installation complete.
echo. > .installed

REM --- Offer model download ---
echo.
set /P "DOWNLOAD_MODEL=Download an AI model now? (Required for local mode) [y/N] "
if /I "%DOWNLOAD_MODEL%"=="y" (
    python download_model.py
) else (
    echo Skipping model download. Run 'python download_model.py' later.
)

echo.
echo === Setup complete! ===
echo Run the game with: run_game.bat
echo.
pause
