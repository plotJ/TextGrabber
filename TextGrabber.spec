# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['text_grabber.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['PIL._tkinter_finder'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Add Tesseract executable and data files
import os
tesseract_path = r'C:\Program Files\Tesseract-OCR'
if os.path.exists(tesseract_path):
    a.datas += [(f'tessdata/{f}', os.path.join(tesseract_path, 'tessdata', f), 'DATA')
                for f in os.listdir(os.path.join(tesseract_path, 'tessdata'))
                if f.endswith('.traineddata')]
    a.binaries += [(f'tesseract/{os.path.basename(f)}', f, 'BINARY')
                   for f in [os.path.join(tesseract_path, 'tesseract.exe')]]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TextGrabber_v2',
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
    icon='NONE',
    uac_admin=True,
)
