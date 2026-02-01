import sys
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.py', '.'),
        ('data', 'data'),
        ('examples', 'examples'),
        ('output', 'output'),
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
        'docx',
        'docx.opcconstants',
        'docx.oxml',
        'docx.oxml.table',
        'docx.oxml.ns',
        'docx.oxml.xmlchar',
        'fitz',
        'pytesseract',
        'PIL',
        'PIL.Image',
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

# For macOS .app, use COLLECT + BUNDLE (not EXE)
coll = COLLECT(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MedicalSupplementAdvisor',
)

app = BUNDLE(
    coll,
    name='MedicalSupplementAdvisor.app',
    icon=None,
    bundle_identifier='com.medicalsupplementadvisor.app',
    info_plist={
        'CFBundleName': 'Medical Supplement Advisor',
        'CFBundleDisplayName': 'Medical Supplement Advisor',
        'CFBundleIdentifier': 'com.medicalsupplementadvisor.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': 'True',
        'LSMinimumSystemVersion': '10.13.0',
        'NSPrincipalClass': 'NSApplication',
        'NSRequiresAquaSystemAppearance': 'False',
    },
)
