"""
Build script for creating PyQuest Monster Game executable
Run: python build_exe.py
"""
import PyInstaller.__main__
import os
import shutil
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
    print("\n" + "="*60)
    print("Building PyQuest Monster Game Executable")
    print("="*60 + "\n")
    
    clean_previous_builds()
    
    # PyInstaller arguments
    args = [
        'monster-game-gui.py',  # Main script
        '--name=PyQuest-Monster-Game',  # Executable name
        '--onedir',  # Create a folder with dependencies (easier to debug)
        '--windowed',  # No console window (GUI only)
        
        # Add data files and directories
        '--add-data=heros;heros',
        '--add-data=monsters;monsters',
        '--add-data=sounds;sounds',
        '--add-data=art;art',
        '--add-data=store.yaml;.',
        '--add-data=game_state.py;.',
        '--add-data=game_logic.py;.',
        
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
    print("  - Output: dist/PyQuest-Monster-Game/")
    print("  - Mode: Windowed (no console)")
    print("  - Including: YAML data, images, sounds")
    print("\nThis may take a few minutes...\n")
    
    PyInstaller.__main__.run(args)
    
    print("\n" + "="*60)
    print("Build Complete!")
    print("="*60)
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
