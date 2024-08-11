# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files

a = Analysis(
    ['main.py'],
    pathex=['.'],  # Adicione o caminho do seu diretório de trabalho se necessário
    binaries=[],
    datas=[
        ('resources/sprites/background0.png', 'resources/sprites'),
        ('resources/music/Horizonte Digital01.mp3', 'resources/music'),
        ('resources/music/Horizonte Digital02.mp3', 'resources/music'),
        ('resources/music/Sentido de Viver01.mp3', 'resources/music'),
        ('resources/fonts/ComicSansMS.ttf', 'resources/fonts'),
    ],
    hiddenimports=[],
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
    name='StickMan',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
