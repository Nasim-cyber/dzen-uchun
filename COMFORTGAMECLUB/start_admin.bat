@echo off
title COMFORTGAMECLUB - Admin Panel
color 0B
echo.
echo  ==========================================
echo   COMFORTGAMECLUB - Admin Panel ishga tushmoqda...
echo  ==========================================
echo.

REM Python borligini tekshirish
python --version >nul 2>&1
if errorlevel 1 (
    echo  [XATO] Python topilmadi! Python 3.8+ o'rnating.
    pause
    exit /b 1
)

REM Kerakli paketlarni o'rnatish
echo  [1/3] Kerakli paketlar tekshirilmoqda...
pip install PyQt5 --quiet

echo  [2/3] Admin Panel ishga tushirilmoqda...
echo.

cd /d "%~dp0"
python admin\admin_ui.py

if errorlevel 1 (
    echo.
    echo  [XATO] Admin Panel ishga tushmadi!
    pause
)
