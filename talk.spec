# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
import sys
import os

a = Analysis(
    ['talk.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('models', 'models'),
        ('talk.ico', '.'),
        ('talk.manifest', '.'),
        # Incluir os dados do espeak-ng do piper
        ('.venv/Lib/site-packages/piper/espeak-ng-data', 'piper/espeak-ng-data'),
    ],
    hiddenimports=[
        'sounddevice',
        'pygame',
        'piper',
        'piper.voice',
    ],
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
    [],
    exclude_binaries=True,
    name='Talk',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=True,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='talk.ico',
    manifest='talk.manifest'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Talk'
)
