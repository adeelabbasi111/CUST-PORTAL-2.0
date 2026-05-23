"""
PyInstaller build script for Student Portal
This script builds the Student Portal as a standalone executable.

Usage:
    python build_exe.py
    
Or use the batch file:
    build.bat
"""

import os
import sys
import shutil
import subprocess

def main():
    # Get the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("\n" + "="*70)
    print("  Student Portal .exe Build Script")
    print("="*70 + "\n")
    
    # Step 1: Install dependencies
    print("[STEP 1/3] Installing dependencies from requirements.txt...")
    print("-" * 70)
    result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                          cwd=project_dir)
    if result.returncode != 0:
        print("\n❌ ERROR: Failed to install dependencies")
        return 1
    
    # Clean previous builds
    dist_dir = os.path.join(project_dir, 'dist')
    build_dir = os.path.join(project_dir, 'build')
    spec_file = os.path.join(project_dir, 'StudentPortal.spec')
    
    print("\nCleaning previous builds...")
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    if os.path.exists(spec_file):
        os.remove(spec_file)
    
    # Step 2: Run PyInstaller
    print("\n[STEP 2/3] Building executable with PyInstaller...")
    print("-" * 70)
    
    pyinstaller_args = [
        'main.py',
        '--name=StudentPortal',
        '--onedir',
        '--windowed',
        '--add-data=Codes/templates:Codes/templates',
        '--add-data=Codes/static:Codes/static',
        '--add-data=StudentData:StudentData',
        '--add-data=drivers:drivers',
        '--collect-all=flask',
        '--collect-all=werkzeug',
        '--hidden-import=utils.browser_manager',
        '--hidden-import=utils.web_routes',
        '--hidden-import=utils.grade_calculator',
        '--hidden-import=utils.file_manager',
        '--hidden-import=utils.feedback',
        '--hidden-import=utils.login_handler',
        '--hidden-import=models.student_data',
        '--hidden-import=models.config',
        '--hidden-import=Codes.WebHandler',
        '--hidden-import=Codes.course_scraper',
        '--hidden-import=Codes.dashboard_scraper',
    ]
    
    result = subprocess.run([sys.executable, "-m", "PyInstaller"] + pyinstaller_args,
                          cwd=project_dir)
    if result.returncode != 0:
        print("\n❌ ERROR: PyInstaller build failed")
        return 1
    
    # Step 3: Verify executable
    print("\n[STEP 3/3] Verifying executable...")
    print("-" * 70)
    
    exe_path = os.path.join(dist_dir, 'StudentPortal', 'StudentPortal.exe')
    if os.path.exists(exe_path):
        exe_size = os.path.getsize(exe_path) / (1024 * 1024)  # Convert to MB
        print(f"\n✅ Executable created successfully!")
        print(f"   Size: {exe_size:.2f} MB")
        print(f"   Location: {exe_path}")
        
        print("\n" + "="*70)
        print("  BUILD SUCCESSFUL! ✅")
        print("="*70)
        print(f"\nExecutable Path:")
        print(f"  {exe_path}\n")
        print("To run the application:")
        print(f"  1. Double-click the executable, or")
        print(f"  2. Run: {exe_path}\n")
        print("="*70 + "\n")
        return 0
    else:
        print(f"\n❌ ERROR: Executable not found at {exe_path}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
