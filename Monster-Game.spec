# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('heros', 'heros'), ('monsters', 'monsters'), ('sounds', 'sounds'), ('art', 'art'), ('store.yaml', '.')]
binaries = []
hiddenimports = ['yaml', 'PIL', 'PIL._tkinter_finder', 'pygame', 'pygame.mixer', 'gui_main', 'gui_audio', 'gui_background_manager', 'gui_blacksmith', 'gui_combat', 'gui_image_manager', 'gui_inventory', 'gui_monster_encounter', 'gui_quests', 'gui_save_load', 'gui_shop', 'gui_town', 'gui_bounty']
tmp_ret = collect_all('gui_main')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('game_state')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('game_logic')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['monster-game-gui.py'],
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
    name='Monster-Game',
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
