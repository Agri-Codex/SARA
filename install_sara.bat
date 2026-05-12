@echo off
setlocal
title SARA Assistant Installer

echo ========================================
echo        SARA Assistant Installer
echo ========================================
echo.

where py >nul 2>nul
if errorlevel 1 (
    echo Python launcher not found.
    echo Please install Python 3.10 or 3.11 first from python.org.
    pause
    exit /b 1
)

echo Checking Python 3.10...
py -3.10 --version >nul 2>nul
if errorlevel 1 (
    echo Python 3.10 not found. Trying Python 3.11...
    py -3.11 --version >nul 2>nul
    if errorlevel 1 (
        echo Python 3.10 or 3.11 is required.
        echo Install Python 3.10, then run this installer again.
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=py -3.11
    )
) else (
    set PYTHON_CMD=py -3.10
)

echo Creating virtual environment...
%PYTHON_CMD% -m venv venv
if errorlevel 1 (
    echo Failed to create virtual environment.
    pause
    exit /b 1
)

echo Activating environment...
call venv\Scripts\activate.bat

echo Updating pip...
python -m pip install --upgrade pip

echo Installing SARA requirements...
pip install -r requirements-phase1.txt
if errorlevel 1 (
    echo Dependency installation failed.
    echo Check internet connection and Python version.
    pause
    exit /b 1
)

echo Creating folders...
if not exist models mkdir models
if not exist data mkdir data

if not exist .env (
    copy .env.example .env >nul 2>nul
)

echo Creating desktop launcher...
powershell -ExecutionPolicy Bypass -File scripts\create_shortcut.ps1

echo.
echo ========================================
echo Installation complete.
echo.
echo IMPORTANT:
echo 1. Download Vosk model manually.
echo 2. Extract it into: models\vosk-model-small-en-us-0.15
echo 3. Add your OpenAI key in .env if you want AI brain.
echo.
echo Start SARA by double-clicking SARA Assistant on desktop
echo or run: start_sara_gui.bat
echo ========================================
pause
