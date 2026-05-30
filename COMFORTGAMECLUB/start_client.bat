@echo off
title COMFORTGAMECLUB - Client
color 0B
echo.
echo  ==========================================
echo   COMFORTGAMECLUB - Client
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

echo  Admin server IP manzilini kiriting:
echo.
set /p SERVER_IP="  Admin PC IP (masalan: 192.168.1.100): "
if "%SERVER_IP%"=="" set SERVER_IP=127.0.0.1

echo.
echo  Ishga tushirilmoqda... Server: %SERVER_IP%
echo.

cd /d "%~dp0"
python client\client_ui.py --server %SERVER_IP%

if errorlevel 1 (
    echo.
    echo  [XATO] Quyidagi buyruqni ishga tushiring:
    echo  pip install PyQt5 pynput
    pause
)
