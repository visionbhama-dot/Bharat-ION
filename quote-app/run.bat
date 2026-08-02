@echo off
setlocal
cd /d "%~dp0"
title Bharat iON Systems - Quotation Generator

echo ============================================================
echo    Bharat iON Systems - Quotation Generator
echo ============================================================
echo.

REM --- check Python ---
where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python was not found.
  echo Install Python 3.11+ from https://www.python.org/downloads/
  echo IMPORTANT: tick "Add python.exe to PATH" during installation, then re-run this file.
  echo.
  pause
  exit /b 1
)

echo Installing / updating dependencies (first run only, please wait)...
python -m pip install --quiet --disable-pip-version-check -r requirements.txt
echo.
echo NOTE: WeasyPrint needs the GTK3 runtime on Windows.
echo If the app fails with a "cannot load library" / pango / cairo error,
echo install the GTK3 runtime from:
echo    https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
echo then run this file again.
echo.

echo Starting the editor at  http://localhost:5000
echo (Keep this window open. Close it to stop the app.)
echo.

REM open the editor in the default browser after a short delay
start "" cmd /c "timeout /t 3 >nul & start http://localhost:5000"

python app.py

echo.
echo Server stopped.
pause
