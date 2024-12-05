# build.spec
import sys
import os
from PyInstaller.utils.hooks import collect_submodules, collect_data_files
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT

# Use os.getcwd() instead of __file__
PROJECT_DIR = os.getcwd()

# Collect all necessary imports and data files
hidden_imports = collect_submodules('flet') + collect_submodules('sqlalchemy')
datas = collect_data_files('flet') + collect_data_files('sqlalchemy')

# Add project directories
additional_datas = [
    (os.path.join(PROJECT_DIR, 'database'), 'database'),
    (os.path.join(PROJECT_DIR, 'data'), 'data'),
    (os.path.join(PROJECT_DIR, 'views'), 'views'),
    (os.path.join(PROJECT_DIR, 'routes'), 'routes'),
    (os.path.join(PROJECT_DIR, 'controllers'), 'controllers'),
    (os.path.join(PROJECT_DIR, 'components'), 'components'),
    (os.path.join(PROJECT_DIR, 'assets'), 'assets'),
]

datas += additional_datas

a = Analysis(
    ['main.py'],
    pathex=[PROJECT_DIR],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Inventario',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='Inventario',
)