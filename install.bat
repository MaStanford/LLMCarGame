@echo off
echo "Installing base requirements..."
pip install -r requirements.txt

echo "Installing Windows-specific requirements..."
pip install -r requirements-windows.txt

echo "Installation complete."
echo. > .installed

set /P "DOWNLOAD_MODEL=Do you want to download the AI model now? (~2GB) [y/N] "
if /I "%DOWNLOAD_MODEL%"=="y" (
    echo Downloading model...
    python download_model.py
) else (
    echo Skipping model download. You can run 'python download_model.py' later.
)

pause
