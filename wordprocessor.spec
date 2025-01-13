# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['wordprocessor.py'],
    pathex=[r'C:\Users\intro\miniconda3\envs\word_processor_new\libs',
             r'C:\Users\intro\miniconda3\envs\word_processor_new\Lib\site-packages'],
    binaries=[],
    datas=[('fonts', 'fonts'),('C:\\Users\\intro\\OneDrive\\Documents\\CAI-FLAME\\indic-word-processor\\images\\logo.ico', '.')],
    hiddenimports=['aksharamukha'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='wordprocessor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="C:\\Users\\intro\\OneDrive\\Documents\\CAI-FLAME\\indic-word-processor\\images\\logo.ico",
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='wordprocessor',
)
