@echo off
title COMFORTGAMECLUB - O'rnatish
color 0A
echo.
echo  ==========================================
echo   COMFORTGAMECLUB - Barcha paketlar o'rnatilmoqda
echo  ==========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo  [XATO] Python topilmadi!
    echo  https://python.org dan Python 3.10+ yuklab o'rnating
    pause
    exit /b 1
)

echo  PyQt5 o'rnatilmoqda...
pip install PyQt5

echo.
echo  pynput o'rnatilmoqda (keyboard bloklash uchun)...
pip install pynput

echo.
echo  ==========================================
echo   O'rnatish tugadi! Endi ishga tushirishingiz mumkin:
echo   - Admin PC da: start_admin.bat
echo   - Client PC da: start_client.bat
echo  ==========================================
echo.
pause
