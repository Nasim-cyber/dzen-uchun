@echo off
title COMFORTGAMECLUB - Admin Panel
color 0B
echo.
echo  ==========================================
echo   COMFORTGAMECLUB - Admin Panel
echo  ==========================================
echo.

REM Python borligini tekshirish
python --version >nul 2>&1
if errorlevel 1 (
    echo  [XATO] Python topilmadi!
    echo  https://python.org dan Python 3.10+ yuklab o'rnating
    echo  O'rnatishda "Add Python to PATH" ni belgilang!
    pause
    exit /b 1
)

echo  Ishga tushirilmoqda...
echo.

cd /d "%~dp0"
python admin\admin_ui.py

if errorlevel 1 (
    echo.
    echo  [XATO] Quyidagi buyruqni ishga tushiring:
    echo  pip install PyQt5
    pause
)
