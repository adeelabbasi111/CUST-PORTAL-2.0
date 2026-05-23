# Student Portal .exe Build Script (PowerShell)
# This script builds a standalone executable from the Student Portal project
#
# Usage: .\build.ps1

$ProjectDir = "c:\Users\adeel\PycharmProjects\Student-Portal"

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  Student Portal .exe Build Script" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Change to project directory
Set-Location -Path $ProjectDir -ErrorAction Stop

Write-Host "[STEP 1/3] Installing dependencies from requirements.txt..." -ForegroundColor Yellow
Write-Host "----------------------------------------------------------------------"
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Clean previous builds
Write-Host ""
Write-Host "Cleaning previous builds..."
$DistDir = Join-Path $ProjectDir "dist"
$BuildDir = Join-Path $ProjectDir "build"

if (Test-Path $DistDir) {
    Remove-Item -Path $DistDir -Recurse -Force
}
if (Test-Path $BuildDir) {
    Remove-Item -Path $BuildDir -Recurse -Force
}

Write-Host ""
Write-Host "[STEP 2/3] Building executable with PyInstaller..." -ForegroundColor Yellow
Write-Host "----------------------------------------------------------------------"

$PyInstallerArgs = @(
    "main.py"
    "--name=StudentPortal"
    "--onedir"
    "--windowed"
    "--add-data=Codes/templates:Codes/templates"
    "--add-data=Codes/static:Codes/static"
    "--add-data=StudentData:StudentData"
    "--add-data=drivers:drivers"
    "--collect-all=flask"
    "--collect-all=werkzeug"
    "--hidden-import=utils.browser_manager"
    "--hidden-import=utils.web_routes"
    "--hidden-import=utils.grade_calculator"
    "--hidden-import=utils.file_manager"
    "--hidden-import=utils.feedback"
    "--hidden-import=utils.login_handler"
    "--hidden-import=models.student_data"
    "--hidden-import=models.config"
    "--hidden-import=Codes.WebHandler"
    "--hidden-import=Codes.course_scraper"
    "--hidden-import=Codes.dashboard_scraper"
)

& python -m PyInstaller $PyInstallerArgs
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: PyInstaller build failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[STEP 3/3] Verifying executable..." -ForegroundColor Yellow
Write-Host "----------------------------------------------------------------------"

$ExePath = Join-Path $DistDir "StudentPortal\StudentPortal.exe"
if (Test-Path $ExePath) {
    $FileSize = (Get-Item $ExePath).Length / 1MB
    
    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Green
    Write-Host "  BUILD SUCCESSFUL! ✅" -ForegroundColor Green
    Write-Host "======================================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Executable Location:" -ForegroundColor Green
    Write-Host "  $ExePath"
    Write-Host ""
    Write-Host "File Size: $([Math]::Round($FileSize, 2)) MB"
    Write-Host ""
    Write-Host "To run the application, either:" -ForegroundColor Cyan
    Write-Host "  1. Double-click the executable" -ForegroundColor Cyan
    Write-Host "  2. Run from command line: $ExePath" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "ERROR: Executable not found at $ExePath" -ForegroundColor Red
    exit 1
}
