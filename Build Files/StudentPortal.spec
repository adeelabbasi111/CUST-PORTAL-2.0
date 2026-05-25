# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('Codes\\templates', 'Codes\\templates'), ('Codes\\static', 'Codes\\static'), ('StudentData', 'StudentData')]
binaries = []
hiddenimports = ['tkinter', '_tkinter', 'logging', 'utils.browser_manager', 'utils.web_routes', 'utils.grade_calculator', 'utils.file_manager', 'utils.feedback', 'utils.login_handler', 'models.student_data', 'models.config', 'Codes.WebHandler', 'Codes.course_scraper', 'Codes.dashboard_scraper']
tmp_ret = collect_all('flask')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('werkzeug')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('selenium')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='StudentPortal',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
