#!/bin/bash

echo "========================================"
echo "UNICH-REF Automation Setup"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "ERROR: Python version $python_version is too old. Required: $required_version or higher"
    exit 1
fi

echo "Python $python_version found. Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

echo
echo "========================================"
echo "Installation completed successfully!"
echo "========================================"
echo
echo "To run the automation:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run the script: python main.py"
echo 