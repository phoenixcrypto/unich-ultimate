#!/bin/bash

echo "========================================"
echo "UNICH-REF Automation Runner"
echo "========================================"
echo

# Check if virtual environment exists
if [ ! -f "venv/bin/activate" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run install.sh first"
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Starting UNICH-REF Automation..."
python main.py 