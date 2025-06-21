@echo off
echo ========================================
echo UNICH-REF Automation Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo Python found. Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing requirements...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo Installation completed successfully!
echo ========================================
echo.
echo To run the automation:
echo 1. Activate virtual environment: venv\Scripts\activate.bat
echo 2. Run the script: python main.py
echo.
pause 