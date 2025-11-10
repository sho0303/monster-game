# Quick Start: Building the Executable

## Step 1: Install PyInstaller
```powershell
pip install pyinstaller
```

## Step 2: Run the Build Script
```powershell
python build_exe.py
```

## Step 3: Find Your Executable
```
dist/PyQuest-Monster-Game/PyQuest-Monster-Game.exe
```

## Step 4: Test It
```powershell
.\dist\PyQuest-Monster-Game\PyQuest-Monster-Game.exe
```

## To Distribute:
1. Zip the entire `dist/PyQuest-Monster-Game` folder
2. Share the zip file
3. Users extract and double-click `PyQuest-Monster-Game.exe`

**Note**: The .exe needs all the files in the folder - it's not standalone!

---

For detailed options and troubleshooting, see [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)
