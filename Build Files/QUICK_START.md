# Quick Start - Build Student Portal .exe

## Fastest Way to Build (30 seconds)

### Option A: Double-click build script
```
1. Open: c:\Users\adeel\PycharmProjects\Student-Portal
2. Double-click: build.bat
3. Wait for "BUILD SUCCESSFUL!" message
```

### Option B: Command line
```
cd c:\Users\adeel\PycharmProjects\Student-Portal
build.bat
```

### Option C: Python script
```
cd c:\Users\adeel\PycharmProjects\Student-Portal
python build_exe.py
```

---

## After Build Completes

Your executable is located at:
```
c:\Users\adeel\PycharmProjects\Student-Portal\dist\StudentPortal\StudentPortal.exe
```

To run it:
- **Double-click** the .exe file, OR
- **Run** from Command Prompt: `StudentPortal.exe`

---

## What Gets Built

✅ Executable with all dependencies bundled  
✅ Flask web server included  
✅ Microsoft Edge WebDriver included  
✅ All HTML templates and static files  
✅ Configuration and data folders  
✅ Standalone - ready to distribute  

---

## File Size
Expected: 150-300 MB (includes Python runtime + all dependencies)

---

## Troubleshooting

**Build fails?**
```
1. Delete dist/ and build/ folders
2. Delete StudentPortal.spec file
3. Try building again
```

**EXE won't run?**
```
1. Ensure Microsoft Edge is installed
2. Run from Command Prompt to see error messages
3. Check antivirus/Windows Defender didn't block it
```

---

## Additional Help

See **BUILD_GUIDE.md** for detailed instructions and troubleshooting.
