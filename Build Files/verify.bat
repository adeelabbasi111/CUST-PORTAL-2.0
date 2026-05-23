@echo off
REM Pre-build verification script
REM Checks if all requirements are met before building the executable

setlocal enabledelayedexpansion

echo.
echo ======================================================================
echo  Student Portal - Pre-Build Verification
echo ======================================================================
echo.

cd /d c:\Users\adeel\PycharmProjects\Student-Portal

echo [CHECK 1/5] Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ FAILED: Python not found or not in PATH
    echo    Please install Python 3.7+ and ensure it's in your PATH
    goto :error
) else (
    for /f "tokens=*" %%i in ('python --version') do echo ✅ PASSED: %%i
)

echo.
echo [CHECK 2/5] Required folders...
if not exist "utils" (
    echo ❌ FAILED: utils folder not found
    goto :error
) else (
    echo ✅ PASSED: utils folder found
)

if not exist "models" (
    echo ❌ FAILED: models folder not found
    goto :error
) else (
    echo ✅ PASSED: models folder found
)

if not exist "Codes" (
    echo ❌ FAILED: Codes folder not found
    goto :error
) else (
    echo ✅ PASSED: Codes folder found
)

if not exist "drivers" (
    echo ❌ FAILED: drivers folder not found
    goto :error
) else (
    echo ✅ PASSED: drivers folder found
)

echo.
echo [CHECK 3/5] Required files...
if not exist "main.py" (
    echo ❌ FAILED: main.py not found
    goto :error
) else (
    echo ✅ PASSED: main.py found
)

if not exist "requirements.txt" (
    echo ❌ FAILED: requirements.txt not found
    goto :error
) else (
    echo ✅ PASSED: requirements.txt found
)

echo.
echo [CHECK 4/5] WebDriver...
if not exist "drivers\msedgedriver.exe" (
    echo ❌ FAILED: drivers\msedgedriver.exe not found
    echo    Please ensure msedgedriver.exe is in the drivers folder
    goto :error
) else (
    echo ✅ PASSED: msedgedriver.exe found
)

echo.
echo [CHECK 5/5] Flask templates and static files...
if not exist "Codes\templates" (
    echo ❌ FAILED: Codes\templates folder not found
    goto :error
) else (
    echo ✅ PASSED: Codes\templates folder found
)

if not exist "Codes\static" (
    echo ❌ FAILED: Codes\static folder not found
    goto :error
) else (
    echo ✅ PASSED: Codes\static folder found
)

echo.
echo ======================================================================
echo  ALL CHECKS PASSED! ✅
echo ======================================================================
echo.
echo You are ready to build the executable. Run:
echo   build.bat
echo.
pause
goto :end

:error
echo.
echo ======================================================================
echo  VERIFICATION FAILED! ❌
echo ======================================================================
echo.
echo Please fix the issues above and try again.
echo.
pause
exit /b 1

:end
endlocal
