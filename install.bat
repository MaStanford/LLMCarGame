@echo off
echo "Installing base requirements..."
pip install -r requirements.txt

echo "Installing Windows-specific requirements..."
pip install -r requirements-windows.txt

echo "Installation complete."
echo. > .installed
pause
