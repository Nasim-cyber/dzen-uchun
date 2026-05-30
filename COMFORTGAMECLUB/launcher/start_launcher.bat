@echo off
title COMFORTGAMECLUB - Launcher
color 0B
cls
echo.
echo  ============================================================
echo   >>>  COMFORTGAMECLUB  GAMING  LAUNCHER  <<<
echo  ============================================================
echo.

REM Python tekshirish
python --version >nul 2>&1
if errorlevel 1 (
    echo  [XATO] Python topilmadi!
    echo  https://python.org dan Python 3.10+ yuklab ornatib,
    echo  ornatishda "Add Python to PATH" ni belgilang!
    echo.
    pause
    exit /b 1
)

REM PyQt5 tekshirish, yo'q bo'lsa o'rnatish
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo  [INFO] PyQt5 topilmadi, o'rnatilmoqda...
    pip install PyQt5 --quiet
    echo  [OK] PyQt5 o'rnatildi!
    echo.
)

echo  [OK] Ishga tushirilmoqda...
echo.

cd /d "%~dp0"
python launcher_ui.py

if errorlevel 1 (
    echo.
    echo  [XATO] Launcher ishga tushmadi!
    echo  Quyidagi buyruqni ishga tushiring:
    echo     pip install PyQt5
    echo.
    pause
)
