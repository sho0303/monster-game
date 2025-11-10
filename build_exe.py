"""
Build script for creating PyQuest Monster Game executable
Run: python build_exe.py          (builds folder with exe)
Run: python build_exe.py --onefile (builds single exe)
"""
import PyInstaller.__main__
import os
import shutil
import sys
from pathlib import Path

def clean_previous_builds():
    """Remove old build artifacts"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name}/...")
            shutil.rmtree(dir_name)
    
    spec_file = 'monster-game-gui.spec'
    if os.path.exists(spec_file):
        print(f"Removing old {spec_file}...")
        os.remove(spec_file)

def build_executable():
    """Build the executable with PyInstaller"""
    # Check for --onefile argument
    use_onefile = '--onefile' in sys.argv
    
    print("\n" + "="*60)
    print("Building PyQuest Monster Game Executable")
    if use_onefile:
        print("Mode: Single File (--onefile)")
    else:
        print("Mode: Folder (--onedir)")
    print("="*60 + "\n")
    
    clean_previous_builds()
    
    # PyInstaller arguments
    args = [
        'monster-game-gui.py',  # Main script
        '--name=PyQuest-Monster-Game',  # Executable name
        '--onefile' if use_onefile else '--onedir',  # Single file or folder
        '--windowed',  # No console window (GUI only)
        
        # Add data files and directories
        '--add-data=heros;heros',
        '--add-data=monsters;monsters',
        '--add-data=sounds;sounds',
        '--add-data=art;art',
        '--add-data=store.yaml;.',
        
        # Collect all Python modules (not as data, as code)
        '--collect-all=gui_main',
        '--collect-all=game_state',
        '--collect-all=game_logic',
        
        # Hidden imports (modules loaded dynamically)
        '--hidden-import=yaml',
        '--hidden-import=PIL',
        '--hidden-import=PIL._tkinter_finder',
        '--hidden-import=pygame',
        '--hidden-import=pygame.mixer',
        
        # Collect all GUI modules
        '--hidden-import=gui_main',
        '--hidden-import=gui_audio',
        '--hidden-import=gui_background_manager',
        '--hidden-import=gui_blacksmith',
        '--hidden-import=gui_combat',
        '--hidden-import=gui_image_manager',
        '--hidden-import=gui_inventory',
        '--hidden-import=gui_monster_encounter',
        '--hidden-import=gui_quests',
        '--hidden-import=gui_save_load',
        '--hidden-import=gui_shop',
        '--hidden-import=gui_town',
        '--hidden-import=gui_bounty',
        
        # Optimization
        '--noconfirm',  # Replace output directory without asking
    ]
    
    # Add icon if it exists
    icon_path = 'art/logo.png'
    if os.path.exists(icon_path):
        args.append(f'--icon={icon_path}')
        print(f"Using icon: {icon_path}")
    else:
        print("Note: No icon file found, building without custom icon")
    
    print("Running PyInstaller with the following configuration:")
    if use_onefile:
        print("  - Output: Single executable file")
        print("  - Mode: Windowed (no console)")
        print("  - Including: YAML data, images, sounds (embedded)")
    else:
        print("  - Output: dist/PyQuest-Monster-Game/ folder")
        print("  - Mode: Windowed (no console)")
        print("  - Including: YAML data, images, sounds")
    print("\nThis may take a few minutes...\n")
    
    PyInstaller.__main__.run(args)
    
    print("\n" + "="*60)
    print("Build Complete!")
    print("="*60)
    
    if use_onefile:
        print("\nExecutable location: dist/PyQuest-Monster-Game.exe")
        print("Run: dist\\PyQuest-Monster-Game.exe")
        print("\nTo distribute:")
        print("  1. Share the single PyQuest-Monster-Game.exe file")
        print("  2. Users run it directly (no extraction needed)")
        print("  3. Save files created in user's temp folder or exe directory")
        print("\nNote: First launch may be slower (extracts files to temp)")
    else:
        print("\nExecutable location: dist/PyQuest-Monster-Game/")
        print("Run: dist\\PyQuest-Monster-Game\\PyQuest-Monster-Game.exe")
        print("\nTo distribute:")
        print("  1. Zip the entire 'dist/PyQuest-Monster-Game' folder")
        print("  2. Users extract and run PyQuest-Monster-Game.exe")
        print("  3. All save files will be created in the same folder")
    print("="*60 + "\n")

if __name__ == '__main__':
    try:
        build_executable()
    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        print("\nMake sure PyInstaller is installed:")
        print("  pip install pyinstaller")
        input("\nPress Enter to exit...")
