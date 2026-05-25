@echo off
setlocal enabledelayedexpansion

echo.
echo ======================================================================
echo  Student Portal .exe Build Script (OneFile + Hidden Console)
echo ======================================================================
echo.

cd /d "%~dp0"
if not exist "main.py" (
    echo ERROR: main.py not found!
    pause & exit /b 1
)

echo [STEP 1/3] Installing dependencies...
pip install -r requirements.txt >nul 2>&1

echo.
echo [STEP 2/3] Building ONEFILE executable...
echo.

if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist "Portal Scraper.spec" del /q "Portal Scraper.spec"

python -m PyInstaller main.py ^
--name="StudentPortal" ^
--icon="icon.ico" ^
--onefile ^
--noconsole ^
--add-data "Codes\templates;Codes\templates" ^
--add-data "Codes\static;Codes\static" ^
--add-data "StudentData;StudentData" ^
--collect-all flask ^
--collect-all werkzeug ^
--collect-all selenium ^
--hidden-import tkinter ^
--hidden-import _tkinter ^
--hidden-import logging ^
--hidden-import utils.browser_manager ^
--hidden-import utils.web_routes ^
--hidden-import utils.grade_calculator ^
--hidden-import utils.file_manager ^
--hidden-import utils.feedback ^
--hidden-import utils.login_handler ^
--hidden-import models.student_data ^
--hidden-import models.config ^
--hidden-import Codes.WebHandler ^
--hidden-import Codes.course_scraper ^
--hidden-import Codes.dashboard_scraper

if errorlevel 1 (
    echo ERROR: PyInstaller build failed!
    pause & exit /b 1
)

echo.
echo [STEP 3/3] Build Complete!
echo ======================================================================
echo  Executable: dist\StudentPortal.exe
echo  Console hidden. Logs saved to app.log
echo ======================================================================
pause