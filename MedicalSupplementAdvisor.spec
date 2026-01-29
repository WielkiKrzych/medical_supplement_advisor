import sys
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

a = Analysis(
    ['src/gui/app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.py', '.'),
        ('data', 'data'),
    ],
    hiddenimports=[
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'reportlab',
        'pydantic',
        'pandas',
        'pdfplumber',
        'python-docx',
    ],
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
    name='MedicalSupplementAdvisor',
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
)
app = BUNDLE(
    exe,
    name='MedicalSupplementAdvisor.app',
    icon=None,
    bundle_identifier='com.medicalsupplementadvisor.app',
    info_plist={
        'CFBundleName': 'Medical Supplement Advisor',
        'CFBundleDisplayName': 'Medical Supplement Advisor',
        'CFBundleExecutable': 'MedicalSupplementAdvisor',
        'CFBundleIdentifier': 'com.medicalsupplementadvisor.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': 'True',
        'LSMinimumSystemVersion': '10.13.0',
    },
)
