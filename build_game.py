"""
PyQuest Monster Game - Build Script
Automated build process for creating distributable Windows .exe

This script:
1. Checks dependencies
2. Collects all game resources
3. Generates PyInstaller spec file
4. Builds one-file executable
5. Creates distribution package

Usage:
    python build_game.py
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime


class GameBuilder:
    """Handles the game build process"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.dist_dir = self.project_root / "dist"
        self.build_dir = self.project_root / "build"
        self.spec_file = self.project_root / "PyQuest-Monster-Game.spec"
        
        # Build configuration
        self.game_name = "PyQuest-Monster-Game"
        self.entry_point = "monster-game-gui.py"
        self.icon_file = None  # Add icon path if you have one
        
        # Resources to include
        self.data_files = []
        self.collect_resources()
    
    def print_header(self, text):
        """Print formatted header"""
        print("\n" + "=" * 70)
        print(f"  {text}")
        print("=" * 70)
    
    def print_step(self, text):
        """Print step indicator"""
        print(f"\n> {text}")
    
    def print_success(self, text):
        """Print success message"""
        print(f"[OK] {text}")
    
    def print_error(self, text):
        """Print error message"""
        print(f"[ERROR] {text}")
    
    def collect_resources(self):
        """Collect all game resources to bundle"""
        self.print_step("Collecting game resources...")
        
        resources = {
            'heros': '*.yaml',
            'monsters': '*.yaml',
            'art': '*.png',
            'sounds': '*.mp3'
        }
        
        for directory, pattern in resources.items():
            dir_path = self.project_root / directory
            if dir_path.exists():
                # Add directory with all matching files
                self.data_files.append((str(dir_path), directory))
                file_count = len(list(dir_path.glob(pattern)))
                self.print_success(f"Found {file_count} files in {directory}/")
            else:
                self.print_error(f"Directory not found: {directory}/")
        
        # Add individual YAML files in root
        yaml_files = ['store.yaml', 'tavern.yaml', 'story.yaml']
        for yaml_file in yaml_files:
            yaml_path = self.project_root / yaml_file
            if yaml_path.exists():
                self.data_files.append((str(yaml_path), '.'))
                self.print_success(f"Found {yaml_file}")
            else:
                print(f"  Warning: {yaml_file} not found (may not be required)")
    
    def check_dependencies(self):
        """Check if all required tools and packages are installed"""
        self.print_step("Checking dependencies...")
        
        # Check Python version
        py_version = sys.version_info
        if py_version < (3, 7):
            self.print_error(f"Python 3.7+ required, found {py_version.major}.{py_version.minor}")
            return False
        self.print_success(f"Python {py_version.major}.{py_version.minor}.{py_version.micro}")
        
        # Check required packages
        required_packages = {
            'PyInstaller': 'pyinstaller',
            'tkinter': 'tkinter',
            'PIL': 'Pillow',
            'pygame': 'pygame',
            'yaml': 'PyYAML'
        }
        
        missing_packages = []
        for module_name, package_name in required_packages.items():
            try:
                __import__(module_name)
                self.print_success(f"{package_name} installed")
            except ImportError:
                missing_packages.append(package_name)
                self.print_error(f"{package_name} not installed")
        
        if missing_packages:
            print("\n[INSTALL] Install missing packages with:")
            print(f"   pip install {' '.join(missing_packages)}")
            return False
        
        return True
    
    def clean_build_artifacts(self):
        """Clean previous build artifacts"""
        self.print_step("Cleaning previous build artifacts...")
        
        # Remove build directory
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
            self.print_success("Removed build/ directory")
        
        # Remove dist directory
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
            self.print_success("Removed dist/ directory")
        
        # Remove spec file (will be regenerated)
        if self.spec_file.exists():
            self.spec_file.unlink()
            self.print_success("Removed old .spec file")
    
    def generate_spec_file(self):
        """Generate PyInstaller spec file"""
        self.print_step("Generating PyInstaller spec file...")
        
        # Prepare data files list for spec (use forward slashes or raw strings)
        datas_str = ",\n        ".join([f"(r'{src}', '{dst}')" for src, dst in self.data_files])
        
        # Icon parameter
        icon_param = f"icon='{self.icon_file}'," if self.icon_file and os.path.exists(self.icon_file) else "icon=None,"
        
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-
"""
PyQuest Monster Game - PyInstaller Spec File
Auto-generated by build_game.py on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

block_cipher = None

a = Analysis(
    ['{self.entry_point}'],
    pathex=[],
    binaries=[],
    datas=[
        {datas_str}
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.scrolledtext',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'pygame',
        'pygame.mixer',
        'yaml',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'tests',
        'art_generation',
        'matplotlib',
        'numpy',
        'scipy',
    ],
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
    name='{self.game_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    {icon_param}
)
'''
        
        # Write spec file
        with open(self.spec_file, 'w', encoding='utf-8') as f:
            f.write(spec_content)
        
        self.print_success(f"Created {self.spec_file.name}")
    
    def run_pyinstaller(self):
        """Run PyInstaller to build the executable"""
        self.print_step("Building executable with PyInstaller...")
        print("  This may take 5-10 minutes...\n")
        
        # Run PyInstaller
        cmd = [sys.executable, '-m', 'PyInstaller', '--clean', str(self.spec_file)]
        
        try:
            result = subprocess.run(
                cmd,
                cwd=str(self.project_root),
                check=True,
                capture_output=False,
                text=True
            )
            
            self.print_success("Build completed successfully!")
            return True
            
        except subprocess.CalledProcessError as e:
            self.print_error("PyInstaller build failed!")
            print(f"  Error code: {e.returncode}")
            return False
        except Exception as e:
            self.print_error(f"Unexpected error during build: {e}")
            return False
    
    def verify_build(self):
        """Verify the build output"""
        self.print_step("Verifying build output...")
        
        exe_path = self.dist_dir / f"{self.game_name}.exe"
        
        if not exe_path.exists():
            self.print_error(f"Executable not found: {exe_path}")
            return False
        
        exe_size_mb = exe_path.stat().st_size / (1024 * 1024)
        self.print_success(f"Executable created: {exe_path.name}")
        self.print_success(f"File size: {exe_size_mb:.1f} MB")
        
        return True
    
    def create_distribution_package(self):
        """Create a distributable package with README"""
        self.print_step("Creating distribution package...")
        
        # Create README for users
        readme_content = f"""PyQuest Monster Game
====================

Version: 1.0
Built: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

HOW TO PLAY
-----------
1. Double-click PyQuest-Monster-Game.exe to start
2. Use mouse or keyboard shortcuts (1-9 for buttons)
3. Your saves will be stored in the "saves" folder
4. Game logs are stored in the "logs" folder

KEYBOARD SHORTCUTS
------------------
1-9, 0    : Select menu buttons
ESC       : Back/Main Menu
SPACE     : Continue/First Option
F1        : Show help
M         : Mute/Unmute
+/-       : Volume control
B         : Cycle biomes (testing)
T         : Teleport (testing)

SYSTEM REQUIREMENTS
-------------------
- Windows 7 or later
- 500 MB disk space
- Screen resolution: 1024x768 or higher

TROUBLESHOOTING
---------------
- If antivirus blocks the game, add it to exceptions
- If the game doesn't start, check the logs folder
- Ensure you have administrator privileges if needed

CONTACT
-------
For support or feedback, please contact the developer.

Enjoy the game!
"""
        
        readme_path = self.dist_dir / "README.txt"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        self.print_success("Created README.txt")
    
    def print_final_summary(self):
        """Print final build summary"""
        self.print_header("BUILD COMPLETE!")
        
        exe_path = self.dist_dir / f"{self.game_name}.exe"
        
        print(f"""
[PACKAGE] Distribution Package Location:
   {self.dist_dir.absolute()}

[CONTENTS] Contents:
   * {self.game_name}.exe  (Main executable)
   * README.txt            (User instructions)

[NEXT] Next Steps:
   1. Test the executable by running it
   2. Game will create 'logs' and 'saves' folders on first run
   3. Compress the dist folder to .zip for sharing
   4. Share with friends and family!

[IMPORTANT] Important Notes:
   * First launch may be slower (Windows security scan)
   * Some antivirus programs may flag it (false positive)
   * Users don't need Python installed
   * Save files are stored alongside the .exe

[TIP] Distribution Tips:
   * Zip the entire dist folder for easy sharing
   * Upload to Google Drive, Dropbox, or your website
   * Expected download size: ~50-70 MB (zipped)
   * Uncompressed size: ~150-200 MB
""")
    
    def build(self):
        """Main build process"""
        self.print_header("PyQuest Monster Game - Build Process")
        
        print(f"Project: {self.project_root}")
        print(f"Entry:   {self.entry_point}")
        print(f"Output:  {self.game_name}.exe")
        
        # Step 1: Check dependencies
        if not self.check_dependencies():
            print("\n[FAIL] Build aborted: Missing dependencies")
            return False
        
        # Step 2: Clean previous builds
        self.clean_build_artifacts()
        
        # Step 3: Generate spec file
        self.generate_spec_file()
        
        # Step 4: Run PyInstaller
        if not self.run_pyinstaller():
            print("\n[FAIL] Build failed")
            return False
        
        # Step 5: Verify build
        if not self.verify_build():
            print("\n[FAIL] Build verification failed")
            return False
        
        # Step 6: Create distribution package
        self.create_distribution_package()
        
        # Step 7: Print summary
        self.print_final_summary()
        
        return True


def main():
    """Main entry point"""
    try:
        builder = GameBuilder()
        success = builder.build()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n[CANCEL] Build cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
