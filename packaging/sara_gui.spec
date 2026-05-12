# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['sara_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('.env.example', '.'), ('data', 'data')],
    hiddenimports=['customtkinter', 'pyttsx3', 'vosk', 'sounddevice'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SARA Assistant',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)
