#!/bin/bash
cd "$(dirname "$0")"

# Check for python3
if ! command -v python3 &> /dev/null; then
    echo
    echo "❌ Python 3 is not installed or not in PATH."
    echo "Please install Python 3 from https://www.python.org/downloads/"
    echo
    exit 1
fi

# Create virtual environment if not present
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run the main script
python3 the_turt_tool_0.8.2.2.py

# Deactivate the environment
deactivate

# Keep terminal open after completion
read -p "Press enter to exit..."