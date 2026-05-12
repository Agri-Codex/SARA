@echo off
setlocal
title Build SARA EXE

echo ========================================
echo        Building SARA Assistant EXE
echo ========================================

if not exist venv (
    echo Virtual environment not found. Running installer first...
    call install_sara.bat
)

call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements-phase1.txt
pip install pyinstaller

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

pyinstaller packaging\sara_gui.spec --clean --noconfirm

if errorlevel 1 (
    echo EXE build failed.
    pause
    exit /b 1
)

echo.
echo EXE created at:
echo dist\SARA Assistant\SARA Assistant.exe
echo.
pause
