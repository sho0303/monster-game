# Quick Start: Building the Executable

## Step 1: Install PyInstaller
```powershell
pip install pyinstaller
```

## Step 2: Run the Build Script

### Option A: Folder with EXE (Recommended)
```powershell
python build_exe.py
```
Creates: `dist/PyQuest-Monster-Game/` folder with exe + files

### Option B: Single Standalone EXE
```powershell
python build_exe.py --onefile
```
Creates: `dist/PyQuest-Monster-Game.exe` (single file)

## Step 3: Find Your Executable

### Folder Mode:
```
dist/PyQuest-Monster-Game/PyQuest-Monster-Game.exe
```

### Single File Mode:
```
dist/PyQuest-Monster-Game.exe
```

## Step 4: Test It

### Folder Mode:
```powershell
.\dist\PyQuest-Monster-Game\PyQuest-Monster-Game.exe
```

### Single File Mode:
```powershell
.\dist\PyQuest-Monster-Game.exe
```

## To Distribute:

### Folder Mode (Recommended):
1. Zip the entire `dist/PyQuest-Monster-Game` folder
2. Share the zip file
3. Users extract and double-click `PyQuest-Monster-Game.exe`
4. Save files created in same folder ✓

### Single File Mode:
1. Share `dist/PyQuest-Monster-Game.exe` directly
2. Users run it (no extraction needed)
3. Save files may go to temp folder ⚠️

---

## Which Mode Should I Use?

**Use Folder Mode (default) if:**
- You want faster startup times
- You want save files in an accessible location
- File size isn't critical (~200MB folder → ~100MB zipped)

**Use Single File Mode (--onefile) if:**
- You want easiest distribution (single file)
- You don't mind slower first launch
- You're okay with saves in temp folder

---

For detailed options and troubleshooting, see [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)
