## Quick purpose
PyQuest Monster Game — a turn-based RPG with both GUI (primary) and legacy terminal versions. GUI uses tkinter, PIL, and pygame for visuals/audio. YAML-backed data for heroes, monsters, and shops. Modular architecture with separate GUI components for combat, town, quests, inventory, and blacksmith.

## High-level architecture (two versions)
### GUI Version (Primary: `monster-game-gui.py`)
- **Entry point**: `monster-game-gui.py` — launcher with dependency checks, logging setup, error handling
- **Main GUI**: `gui_main.py` (`GameGUI` class) — 800x1050 tkinter window, keyboard shortcuts (1-9 for buttons, B for biome cycling, T for teleport)
- **Modular GUI components**: Each feature is a separate class injected into `GameGUI`:
  - `gui_combat.py` (`CombatGUI`) — turn-based combat with animations, async round execution
  - `gui_town.py` (`TownGUI`) — town hub with shop, blacksmith, tavern (placeholder), fountain (heal 3 HP)
  - `gui_shop.py` (`ShopGUI`) — class-filtered item purchases, duplicate prevention
  - `gui_blacksmith.py` (`BlacksmithGUI`) — permanent stat upgrades (+1 attack/defense for 100 gold)
  - `gui_inventory.py` (`InventoryGUI`) — equip/unequip items, stat display
  - `gui_quests.py` (`QuestManager`) — biome-aware monster kill quests, dynamic rewards
  - `gui_monster_encounter.py` (`MonsterEncounterGUI`) — random encounters, biome-filtered spawns
  - `gui_save_load.py` (`SaveLoadManager`) — JSON save/load with metadata
  - `gui_image_manager.py` (`ImageManager`) — image display, layout (single/multi), canvas management
  - `gui_background_manager.py` (`BackgroundManager`) — biome switching, backgrounds, teleportation
  - `gui_audio.py` (`Audio`) — pygame.mixer wrapper for sounds/music
- **Game state**: `game_state.py` (`GameState` class) — holds `hero`, `monsters`, `heros` dicts; `initialize_game_state()` loads YAML
- **Game logic**: `game_logic.py` — `damage_calculator()` (level-aware, 80-120% randomness, percentage-based defense), `fight_round()`, `level_up()`

### Legacy Terminal Version
- `monster-game.py` (not actively maintained) — single-file procedural script with global state, colorama output, ASCII art

## Data schema (YAML files)
### Heroes (`heros/*.yaml`)
```yaml
Shadow Billy Bob:  # Top-level key is hero name
    age: 16
    weapon: Ninja Stars
    armour: Students Robe
    attack: 5
    hp: 15
    maxhp: 15
    defense: 10
    level: 1
    class: 'Ninja'  # Must be Warrior, Ninja, or Magician
```

### Monsters (`monsters/*.yaml`)
```yaml
Cyclops:
  name: Cyclops
  hp: 55
  maxhp: 55
  attack: 7
  defense: 10
  gold: 50
  level: 5
  xp: 5
  art: art/cyclops_monster.png  # PNG image path
  attack_sound: cyclops-attack.mp3  # Sound file in sounds/
  biome: desert  # grassland, desert, dungeon, ocean (town excluded from spawns)
  finalboss: True  # Optional, only for Dragon
```

### Store (`store.yaml`)
```yaml
Weapons:  # Category name
  - name: Excalibur
    attack: 40
    cost: 500
    class: Warrior  # Or 'All' for all classes
    ascii_art: art/strong_sword.png  # PNG (not ASCII despite name)
```

## Biome system (critical for spawns/quests)
- **Biomes**: `grassland`, `desert`, `dungeon`, `ocean`, `town`
- **Monster spawns**: Filtered by `monster.get('biome', 'grassland')` — town monsters don't spawn randomly
- **Backgrounds**: Each biome has `art/{biome}_background.png` (800x600 or larger)
- **Switching**: B key cycles biomes, T key teleports (excludes town unless explicitly navigating)
- **Quest integration**: `QuestManager.generate_kill_quest()` filters by `current_biome` to avoid impossible quests

## Runtime & developer workflow
### Running the GUI (primary method)
```powershell
# From repo root (critical — relative paths required)
python .\monster-game-gui.py
```
**Dependencies**: `pip install pyyaml pygame pillow` (tkinter is built-in on most Python installs)

### Testing
- **Test directory**: `tests/` contains 40+ integration tests (no unit test framework — tests are manual GUI scripts)
- **Test pattern**: Create `tk.Tk()` root, instantiate `GameGUI`, manipulate `game_state.hero`, call GUI methods, observe
- **Example**: `tests/test_town_system.py` — sets up hero, calls `gui.town.show_town_menu()`
- **Run tests**: `python .\tests\test_town_system.py` (opens GUI window, manual verification)

### Logging
- Auto-created in `logs/game_YYYYMMDD_HHMMSS.log` by `monster-game-gui.py`
- Use `logging.info()` for new features (already configured)

## Critical conventions and gotchas
### 1. Canvas vs Frame image display
- **Background images**: Use `ImageManager.show_background()` → renders to canvas
- **Foreground images** (monsters, heroes): Use `ImageManager.show_image()` or `show_images()` → renders to canvas with transparency support
- **Why**: Canvas allows layering (background + multiple foreground images), Frame widgets don't stack properly

### 2. Async combat pattern (avoid blocking UI)
```python
# CombatGUI uses root.after() for timing between rounds
def _start_combat_round(self):
    self._show_hero_attack_animation(hero)
    self.gui.root.after(1500, lambda: self._complete_hero_attack(...))  # 1.5s delay
```
**Reason**: Tkinter is single-threaded — blocking sleep() freezes UI. Use `root.after()` for delays.

### 3. Class filtering in shop
```python
hero_class = hero.get('class', 'Warrior')
filtered = [item for item in items if item.get('class') == hero_class or item.get('class') == 'All']
```
**Critical**: All items must have `class` field. Missing `class` = item never shows.

### 4. Monster biome filtering
```python
# MonsterEncounterGUI.get_random_encounter()
valid = [m for m in monsters.values() if m.get('biome', 'grassland') == current_biome]
```
**Gotcha**: Monsters without `biome` default to `grassland`. Town monsters (if any) should have `biome: town` and won't spawn via random encounter.

### 5. Image paths (PNG, not ASCII despite legacy names)
- **Art directory**: `art/` contains PNG images (e.g., `art/cyclops_monster.png`, `art/grassy_background.png`)
- **Sounds directory**: `sounds/` contains MP3/WAV files
- **Legacy**: Some YAML fields say `ascii_art` but expect PNG paths (historical artifact from terminal version)

### 6. Keyboard shortcuts (gui_main.py)
```python
# _handle_keypress() method
'1'-'9': Click numbered buttons
'b': Cycle biomes (grassland → desert → dungeon → ocean → town)
't': Random teleport (excludes town)
```
**Implementation**: Each button is tagged with `button_1`, `button_2`, etc. Keypress invokes button callback.

## Safe edit rules
1. **When adding GUI features**: Create new `gui_*.py` module, instantiate in `gui_main.py.__init__()`, pass `self` as `gui` parameter
2. **New YAML fields**: Add `.get('field', default)` everywhere the field is read (YAML files lack validation)
3. **New monsters**: Require `biome` field (or they spawn in grassland by default)
4. **New items**: Require `class` field (or they won't appear in shop for any class)
5. **Images/sounds**: Verify file exists before referencing (no asset validation at runtime)
6. **Combat changes**: Update `game_logic.damage_calculator()` (shared by all combat) — don't duplicate logic in `gui_combat.py`

## Implementation patterns (copy these)
### Adding a new monster
1. Create `monsters/MyMonster.yaml`:
```yaml
MyMonster:
  name: My Fearsome Beast
  hp: 80
  maxhp: 80
  attack: 15
  defense: 12
  gold: 60
  level: 6
  xp: 6
  art: art/my_monster.png
  attack_sound: my-attack.mp3
  biome: desert  # Don't forget this!
```
2. Add `art/my_monster.png` (512x256 recommended)
3. Add `sounds/my-attack.mp3`
4. Add `art/my_monster_attack.png` (for attack animation, optional)

### Adding a new GUI feature (e.g., tavern)
1. Create `gui_tavern.py`:
```python
class TavernGUI:
    def __init__(self, gui):
        self.gui = gui  # Access to GameGUI instance
    
    def show_tavern(self):
        self.gui.clear_text()
        self.gui.show_background('art/tavern_background.png')
        self.gui.print_text("🍺 Welcome to the Tavern!")
        # ... implementation
```
2. In `gui_main.py.__init__()`:
```python
from gui_tavern import TavernGUI
self.tavern = TavernGUI(self)
```
3. Wire up button callback:
```python
self.show_buttons([("🍺 Tavern", self.tavern.show_tavern)])
```

### Adding a test
```python
# tests/test_my_feature.py
import tkinter as tk
from gui_main import GameGUI

def test_my_feature():
    root = tk.Tk()
    gui = GameGUI(root)
    root.update()  # Process pending events
    
    # Setup test hero
    gui.game_state.hero = {'name': 'Tester', 'hp': 100, ...}
    
    # Test the feature
    gui.my_feature.do_something()
    
    # Manual verification
    print("✓ Feature works!")
    root.mainloop()

if __name__ == '__main__':
    test_my_feature()
```

## Where implementation details live
- **Damage formula**: `game_logic.py:damage_calculator()` — level differential (±15%/level), 80-120% randomness, capped defense (max 85% reduction)
- **Save format**: `gui_save_load.py` — JSON with `{'hero': {...}, 'current_biome': '...', 'quests': [...], 'timestamp': ...}`
- **Button rendering**: `gui_main.py:show_buttons()` — creates labeled buttons with keyboard shortcuts (1-9)
- **Quest generation**: `gui_quests.py:generate_kill_quest()` — filters by biome, prevents duplicates
- **Animation timing**: `gui_combat.py` — all delays use `root.after(milliseconds, callback)` pattern

## Documentation markdown files (*.md in repo root)
Feature implementation histories (useful for understanding design decisions):
- `TOWN_SYSTEM_IMPLEMENTATION.md` — Town hub design, fountain mechanics
- `BLACKSMITH_IMPLEMENTATION.md` — Permanent stat upgrades, 100 gold cost rationale
- `IMPROVED_DAMAGE_CALCULATOR.md` — Damage formula evolution, level scaling
- `DROP_QUEST_IMPLEMENTATION.md` — Quest reward system, biome filtering
- `LAST_BIOME_TRACKING.md` — Teleport exclusion logic

## Known limitations
- No automated tests (all tests are manual GUI scripts in `tests/`)
- No YAML schema validation (rely on `.get()` with defaults)
- Single-threaded (tkinter limitation) — use `root.after()` for delays, not `time.sleep()`
- Hardcoded window size (800x1050) — responsive layouts not implemented
- Legacy `monster-game.py` unmaintained — focus on GUI version
