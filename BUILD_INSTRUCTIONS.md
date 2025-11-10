# Building PyQuest Monster Game Executable

This guide explains how to compile PyQuest Monster Game into a standalone Windows executable (.exe).

## Prerequisites

1. **Python 3.7+** installed
2. **All dependencies** installed:
   ```powershell
   pip install -r requirements.txt
   ```

3. **PyInstaller** installed:
   ```powershell
   pip install pyinstaller
   ```

## Build Process

### Option 1: Using the Build Script (Recommended)

Simply run the provided build script:

```powershell
python build_exe.py
```

This will:
- Clean previous builds
- Bundle all game files (YAML, images, sounds)
- Create a windowed executable (no console)
- Output to `dist/PyQuest-Monster-Game/`

### Option 2: Manual PyInstaller Command

If you prefer manual control:

```powershell
pyinstaller --name=PyQuest-Monster-Game --onedir --windowed --icon=art/logo.png --add-data=heros;heros --add-data=monsters;monsters --add-data=sounds;sounds --add-data=art;art --add-data=store.yaml;. --hidden-import=yaml --hidden-import=PIL --hidden-import=pygame monster-game-gui.py
```

## Output Structure

After building, you'll have:

```
dist/
└── PyQuest-Monster-Game/
    ├── PyQuest-Monster-Game.exe  ← Main executable
    ├── heros/                     ← Hero YAML files
    ├── monsters/                  ← Monster YAML files
    ├── sounds/                    ← Sound effects & music
    ├── art/                       ← Images & backgrounds
    ├── store.yaml                 ← Shop inventory
    ├── _internal/                 ← Python runtime & dependencies
    └── (various DLL files)
```

## Running the Executable

### From Build Directory
```powershell
.\dist\PyQuest-Monster-Game\PyQuest-Monster-Game.exe
```

### For Distribution
1. Zip the entire `dist/PyQuest-Monster-Game` folder
2. Share the zip file
3. Users extract and run `PyQuest-Monster-Game.exe`

**Important**: All files in the folder are required - the .exe alone won't work!

## Build Options Explained

### `--onedir` vs `--onefile`
- **`--onedir`** (default): Creates a folder with exe + dependencies
  - ✅ Faster startup time
  - ✅ Easier to debug
  - ✅ Save files created in accessible location
  - ❌ Multiple files to distribute

- **`--onefile`**: Creates a single .exe file
  - ✅ Single file distribution
  - ❌ Slower startup (extracts to temp folder)
  - ❌ Harder to debug
  - ❌ Save files may go to temp directory

For this game, `--onedir` is recommended because:
1. Players need to access save files (`saves/` folder)
2. Faster loading of images/sounds
3. Easier troubleshooting

### `--windowed` vs `--console`
- **`--windowed`** (default): No console window, pure GUI
- **`--console`**: Shows terminal window for debugging

Change to `--console` if you need to see error messages during development.

## Troubleshooting

### Build Fails: "Module not found"
**Solution**: Add missing module to `--hidden-import` in `build_exe.py`:
```python
'--hidden-import=missing_module_name',
```

### Images/Sounds Not Loading
**Solution**: Verify `--add-data` paths in `build_exe.py`. Format is:
```
'--add-data=source_folder;destination_folder',
```
(Semicolon `;` on Windows, colon `:` on Linux/Mac)

### "PyInstaller is not installed"
**Solution**:
```powershell
pip install pyinstaller
```

### Executable Too Large
**Typical size**: 150-300 MB (includes Python runtime, pygame, PIL, sounds, images)

To reduce size:
1. Remove unused sound files
2. Compress images (use smaller PNGs)
3. Use `--onefile` mode (slightly smaller but slower)
4. Exclude debug files: `--exclude-module=matplotlib` (if accidentally included)

### Antivirus Flags Executable
**Why**: PyInstaller executables sometimes trigger false positives

**Solutions**:
1. Add exception in antivirus for the .exe
2. Sign the executable with a code signing certificate (for distribution)
3. Build on the target machine instead of downloading

## Advanced: Creating an Installer

For professional distribution, create an installer using:

### Inno Setup (Windows)
1. Download Inno Setup: https://jrsoftware.org/isdl.php
2. Create installer script:

```inno
[Setup]
AppName=PyQuest Monster Game
AppVersion=1.0
DefaultDirName={pf}\PyQuest Monster Game
DefaultGroupName=PyQuest Monster Game
OutputDir=installer_output
OutputBaseFilename=PyQuest_Installer

[Files]
Source: "dist\PyQuest-Monster-Game\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\PyQuest Monster Game"; Filename: "{app}\PyQuest-Monster-Game.exe"
Name: "{commondesktop}\PyQuest Monster Game"; Filename: "{app}\PyQuest-Monster-Game.exe"
```

### NSIS (Alternative)
Use NSIS for more control over installation process.

## Testing the Build

Before distributing:

1. **Test on clean machine** (no Python installed)
2. **Verify all features work**:
   - Game launches
   - Images load correctly
   - Sounds play
   - Save/Load functions
   - All battles, shops, quests work
3. **Check file paths**: Logs and saves go to correct location
4. **Test different Windows versions** (10, 11)

## File Size Optimization

Current build size breakdown:
- Python runtime: ~50 MB
- pygame/PIL dependencies: ~30 MB
- Game assets (art/sounds): ~50-100 MB
- Game code: <1 MB

To minimize:
```powershell
# Use UPX compression (optional)
pip install pyinstaller[encryption]
pyinstaller --onedir --upx-dir=C:\path\to\upx monster-game-gui.py
```

## Distribution Checklist

- [ ] Build executable with `python build_exe.py`
- [ ] Test exe on your machine
- [ ] Test exe on machine without Python
- [ ] Verify saves folder creates properly
- [ ] Check all sounds/images load
- [ ] Zip the `dist/PyQuest-Monster-Game` folder
- [ ] Create README.txt for users
- [ ] Include LICENSE file
- [ ] Test extracted zip on clean machine
- [ ] Upload to distribution platform

## Support

If users encounter issues:
1. Ask them to run in `--console` mode to see errors
2. Check logs folder for error messages
3. Verify they extracted ALL files (not just .exe)
4. Ensure Windows Defender isn't blocking

---

**Build tested on**: Windows 10/11, Python 3.12
**Typical build time**: 2-5 minutes
**Output size**: ~200 MB (compressed zip: ~100 MB)
