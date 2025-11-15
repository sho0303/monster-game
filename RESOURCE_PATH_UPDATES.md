# Resource Path Updates for PyInstaller Bundle

## Overview
Updated the game to support PyInstaller bundled execution (single .exe file) by implementing resource path handling that works in both development and bundled modes.

## Changes Made

### 1. New Module: `resource_utils.py`
Created a new utility module with the following functions:

- **`get_resource_path(relative_path)`** - Resolves paths for resources (images, sounds, YAML files)
  - Dev mode: Uses current directory
  - Bundle mode: Uses `sys._MEIPASS` (PyInstaller's temp extraction folder)

- **`get_resource_dir(relative_dir)`** - Gets absolute path to resource directories

- **`list_resource_files(relative_dir, extension)`** - Lists files in resource directories

- **`resource_exists(relative_path)`** - Checks if resource exists

- **`ensure_writable_dir(dir_name)`** - Creates writable directories outside the bundle
  - Used for: `saves/` and `logs/` directories
  - Bundle mode: Creates alongside executable
  - Dev mode: Uses current directory

- **`is_bundled()`** - Checks if running as PyInstaller bundle

### 2. Updated Files

#### Core Game Files
- **`game_state.py`**
  - Added `from resource_utils import get_resource_path, list_resource_files`
  - Updated `_get_project_path()` to use `get_resource_path()`
  - Updated `initialize_game_state()` to use `list_resource_files()` for YAML loading

#### GUI Image & Audio Files
- **`gui_image_manager.py`**
  - Added `from resource_utils import get_resource_path`
  - Updated `show_image()` to resolve paths with `get_resource_path()`
  - Updated `add_canvas_image()` to resolve paths with `get_resource_path()`

- **`gui_background_manager.py`**
  - Added `from resource_utils import get_resource_path`
  - Updated `set_background_image()` to resolve paths with `get_resource_path()`
  - Updated `initialize_default_background()` to resolve paths with `get_resource_path()`

- **`gui_audio.py`**
  - Added `from resource_utils import get_resource_path`
  - Updated `play_background_music()` to resolve paths with `get_resource_path()`
  - Updated `play_sound_effect()` to resolve paths with `get_resource_path()`

#### Writable Directory Files
- **`logger_utils.py`**
  - Added `from resource_utils import ensure_writable_dir`
  - Updated `setup_logging()` to use `ensure_writable_dir('logs')`
  - Ensures logs directory is created alongside executable in bundle mode

- **`gui_save_load.py`**
  - Added `from resource_utils import ensure_writable_dir`
  - Updated `__init__()` to use `ensure_writable_dir('saves')`
  - Ensures saves directory is created alongside executable in bundle mode

## How It Works

### Development Mode (Running from source)
```python
get_resource_path('art/ninja.png')
# Returns: C:\Users\...\monster-game\art\ninja.png
```

### Bundled Mode (Running as .exe)
```python
get_resource_path('art/ninja.png')
# Returns: C:\Users\...\AppData\Local\Temp\_MEI12345\art\ninja.png
# (PyInstaller extracts resources to temporary folder)
```

### Writable Directories (logs, saves)
```python
ensure_writable_dir('saves')
# Dev: C:\Users\...\monster-game\saves
# Bundle: C:\Users\...\PyQuest-Monster-Game\saves (alongside .exe)
```

## Resources Handled

### Read-Only Resources (bundled with .exe)
- ✅ `heros/*.yaml` (3 hero files)
- ✅ `monsters/*.yaml` (38 monster files)
- ✅ `store.yaml`, `tavern.yaml`, `story.yaml`
- ✅ `art/*.png` (all game graphics)
- ✅ `sounds/*.mp3` (all audio files)

### Writable Directories (created alongside .exe)
- ✅ `logs/` - Game logs with timestamps
- ✅ `saves/` - Player save files

## Testing Checklist

Before building final .exe, verify:
- [ ] Game launches in dev mode
- [ ] All images display correctly
- [ ] All sounds play correctly
- [ ] Monsters load from YAML
- [ ] Heroes load from YAML
- [ ] Save/Load creates saves folder
- [ ] Logs are created properly
- [ ] All biomes display correctly
- [ ] Combat works with attack animations
- [ ] Town, shop, blacksmith functional

## Next Steps

Now ready for Phase 2: Creating the PyInstaller build script and .spec file.

The build script will:
1. Collect all resources (art, sounds, YAML files)
2. Configure PyInstaller for one-file mode
3. Set proper executable name and icon
4. Exclude unnecessary files (tests, saves, art_generation, etc.)
5. Create distributable .exe

## Technical Notes

### Why `sys._MEIPASS`?
PyInstaller extracts bundled resources to a temporary folder at runtime. The path to this folder is stored in `sys._MEIPASS`. All resource loading must check for this attribute to locate files correctly.

### Why Separate Writable Directories?
The `sys._MEIPASS` temp folder is read-only and gets deleted when the app closes. User-generated content (saves, logs) must be stored in a persistent writable location, which we place alongside the executable.

### Path Handling Strategy
All resource paths in YAML files remain as-is (e.g., `art/ninja.png`). The `resource_utils` module transparently resolves them to the correct absolute path based on execution mode.
