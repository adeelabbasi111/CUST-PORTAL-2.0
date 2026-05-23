# Student Portal - Executable Build Guide

## Overview
This guide will help you build a standalone .exe executable for the Student Portal project.

## Prerequisites
- Python 3.7+ installed and added to PATH
- Windows operating system

## Build Methods

### Method 1: Using Batch Script (Recommended for Windows)
The simplest method - just double-click the batch file.

1. Open Command Prompt (cmd.exe) or File Explorer
2. Navigate to: `c:\Users\adeel\PycharmProjects\Student-Portal`
3. Double-click `build.bat` or run:
   ```
   build.bat
   ```
4. Wait for the build to complete. You should see "BUILD SUCCESSFUL! ✅"

### Method 2: Using PowerShell Script
If you prefer PowerShell:

1. Open PowerShell as Administrator
2. Navigate to: `c:\Users\adeel\PycharmProjects\Student-Portal`
3. Allow script execution (one-time):
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
4. Run the build script:
   ```powershell
   .\build.ps1
   ```

### Method 3: Using Python Script
For manual control:

1. Open Command Prompt
2. Navigate to: `c:\Users\adeel\PycharmProjects\Student-Portal`
3. Run:
   ```
   python build_exe.py
   ```

### Method 4: Manual Command Line
For experienced users:

1. Open Command Prompt
2. Navigate to: `c:\Users\adeel\PycharmProjects\Student-Portal`
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Build with PyInstaller:
   ```
   pyinstaller main.py --name=StudentPortal --onedir --windowed ^
     --add-data="Codes/templates:Codes/templates" ^
     --add-data="Codes/static:Codes/static" ^
     --add-data="StudentData:StudentData" ^
     --add-data="drivers:drivers" ^
     --collect-all=flask ^
     --collect-all=werkzeug ^
     --hidden-import=utils.browser_manager ^
     --hidden-import=utils.web_routes ^
     --hidden-import=utils.grade_calculator ^
     --hidden-import=utils.file_manager ^
     --hidden-import=utils.feedback ^
     --hidden-import=utils.login_handler ^
     --hidden-import=models.student_data ^
     --hidden-import=models.config ^
     --hidden-import=Codes.WebHandler ^
     --hidden-import=Codes.course_scraper ^
     --hidden-import=Codes.dashboard_scraper
   ```

## After Build Completion

Once the build completes successfully, your executable will be located at:
```
c:\Users\adeel\PycharmProjects\Student-Portal\dist\StudentPortal\StudentPortal.exe
```

### Running the Executable

You can run the application in two ways:

1. **Double-click the executable:**
   - Navigate to `dist\StudentPortal\StudentPortal.exe` and double-click it

2. **Run from Command Line:**
   ```
   cd dist\StudentPortal
   StudentPortal.exe
   ```

## What's Included

The executable includes:
- ✅ All Python modules (utils, models, Codes)
- ✅ Flask web server and dependencies
- ✅ Selenium and WebDriver support
- ✅ HTML templates (from Codes/templates)
- ✅ CSS and static assets (from Codes/static)
- ✅ Data folder (StudentData)
- ✅ Edge WebDriver (msedgedriver.exe)

## Expected Behavior

When you run `StudentPortal.exe`:
1. A warning message will display about closing Microsoft Edge tabs
2. You'll be prompted to press Enter to start
3. The application will launch Edge browser
4. A Flask web server will start at `http://127.0.0.1:5000`
5. The Student Portal UI will open in the browser
6. You can then use the "Scrape" button to begin data collection

## Troubleshooting

### "Build Failed" Error
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that you have write permissions in the project directory
- Try cleaning previous builds manually:
  - Delete the `dist` folder
  - Delete the `build` folder
  - Delete the `StudentPortal.spec` file (if it exists)

### "Missing drivers" or "drivers not found"
- Verify that `drivers\msedgedriver.exe` exists
- Check that the driver is compatible with your Windows version
- Update the driver if needed

### Executable won't run
- Try running from Command Prompt to see error messages:
  ```
  dist\StudentPortal\StudentPortal.exe
  ```
- Ensure Microsoft Edge is installed on your system
- Check Windows Defender or antivirus for blocked files

### Large executable size
- This is normal. PyInstaller packages all dependencies and Python runtime.
- Typical size: 150-300 MB
- To reduce size, consider using UPX compression with PyInstaller

## Build Details

### PyInstaller Configuration
- **Format:** One-file directory (onedir) - easier to distribute
- **Window:** Windowed mode - no console window
- **Data Paths:**
  - Templates: `Codes/templates`
  - Static assets: `Codes/static`
  - Student data: `StudentData`
  - Drivers: `drivers`
- **Hidden Imports:** All internal modules explicitly listed for complete packaging

### Project Structure
```
Student-Portal/
├── main.py                 # Entry point
├── Codes/
│   ├── WebHandler.py      # Flask app
│   ├── course_scraper.py
│   ├── dashboard_scraper.py
│   ├── templates/         # Flask HTML templates
│   └── static/            # CSS, JS, images
├── utils/                 # Utility modules
├── models/                # Data models
├── drivers/               # WebDriver executables
├── StudentData/           # Data storage folder
├── requirements.txt       # Dependencies
├── build.bat             # Build script (Batch)
├── build.ps1             # Build script (PowerShell)
└── build_exe.py          # Build script (Python)
```

## Next Steps

After building successfully:

1. **Test the executable:**
   - Run it and ensure all features work
   - Test the web UI in the browser
   - Verify data scraping functionality

2. **Distribute the executable:**
   - The entire `dist\StudentPortal` folder is needed
   - You can ZIP it for distribution
   - Include this README with the executable

3. **Keep the source:**
   - Keep the original source code for future updates
   - If you update the code, rebuild the executable

## Additional Notes

- The executable requires Windows 7 or later
- Internet connection is required for web scraping features
- Microsoft Edge must be installed on the target system
- Total size of dist folder will be 150-300 MB depending on dependencies

## Support

If you encounter issues:
1. Run the build script again
2. Delete previous build artifacts (dist/, build/, .spec files)
3. Reinstall dependencies: `pip install -r requirements.txt --upgrade`
4. Try again

For more information about PyInstaller: https://pyinstaller.org/
