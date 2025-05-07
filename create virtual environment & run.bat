@echo off
cd /d "%~dp0"

:: Check for Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo ❌ Python is not installed or not added to PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo and make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b
)

python -m venv venv
call venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt

python the_turt_tool_0.8.2.2.py

deactivate

pause