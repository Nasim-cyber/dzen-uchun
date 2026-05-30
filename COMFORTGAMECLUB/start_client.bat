@echo off
title COMFORTGAMECLUB - Client
color 0B
echo.
echo  ==========================================
echo   COMFORTGAMECLUB - Client ishga tushmoqda...
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
echo  [1/3] Kerakli paketlar o'rnatilmoqda...
pip install PyQt5 pynput --quiet

echo  [2/3] Admin server IP manzilini kiriting:
echo.
set /p SERVER_IP="  Admin PC IP manzili (masalan: 192.168.1.100): "

if "%SERVER_IP%"=="" set SERVER_IP=127.0.0.1

echo.
echo  [3/3] Client ishga tushirilmoqda... Server: %SERVER_IP%
echo.

cd /d "%~dp0"
python client\client_ui.py --server %SERVER_IP%

if errorlevel 1 (
    echo.
    echo  [XATO] Client ishga tushmadi!
    pause
)
