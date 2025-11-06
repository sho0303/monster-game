## Quick purpose
This repository is a single-file, terminal-based Python game (`monster-game.py`) that loads YAML-backed data for heroes, monsters and the in-game store. The guidance below helps an AI agent make safe, useful edits and add small features without breaking runtime assumptions.

## High-level architecture (big picture)
- One main program: `monster-game.py` — procedural script that wires data, audio, and I/O together.
- Data sources: YAML files under `heros/`, `monsters/`, and `store.yaml` are merged into Python dicts at startup.
- Assets: `ascii_art/` (printed directly), `sounds/` (played via `pygame.mixer`).
- Runtime expectations: run from repository root so relative paths like `monsters/` and `ascii_art/` resolve.

## Key files and patterns to reference
- `monster-game.py` — entrypoint. Many helper functions (e.g. `fight_calculator`, `shop`, `use_item`) assume global variables `monsters`, `heros`, and a runtime `hero` object.
- `heros/*.yaml` — hero templates. Example (`heros/Billy.yaml`):
  - keys: `attack`, `hp`, `maxhp`, `defense`, `class`, `weapon`, `armour`.
- `monsters/*.yaml` — monster definitions. Example (`monsters/Cyclops.yaml`):
  - keys: `name`, `hp`, `maxhp`, `attack`, `defense`, `gold`, `level`, optional `finalboss`.
- `store.yaml` — store categories used by `shop()`; items have `class`, `cost`, and optional `ascii_art` and equipment fields like `attack` or `defense`.

## Runtime & developer workflow
- Dependencies (discoverable from imports): `PyYAML`, `pygame`, `colorama`.
  - Install with pip before running: `pip install pyyaml pygame colorama` (run from virtualenv).
- Run locally from repo root (paths are relative):
  - Windows PowerShell: `python .\monster-game.py`
- Audio: `play_sound(name)` loads files from `./sounds/{name}`. If audio device isn't present, `pygame.mixer` calls may raise—wrap or mock when testing.

## Project-specific conventions and gotchas
- Global state: many functions reference globals (notably `hero`, `monsters`, `heros`). When refactoring, either preserve the global usage or update all call sites.
- YAML merging: `yaml_file_to_dictionary` reads each file and calls `dict.update(...)`. Each hero/monster file typically contains a mapping where top-level key is the entity name.
- Item filtering: `shop()` uses the item's `class` field (string) to filter gear for hero classes (e.g. `class: 'Ninja'` or `class: 'All'`).
- ASCII art: `print_ascii(path, color)` expects plain text files under `ascii_art/` and ANSI color codes or `colorama` usage.
- Minimal error handling: code assumes files exist and keys are present. Add validation checks before changing behavior.

## Safe edit rules for an AI agent
1. Preserve existing function signatures unless updating all call sites (many functions rely on globals).
2. When adding new YAML fields, ensure defaulting logic is added where values are read (e.g., `hero.get('item')`).
3. Prefer non-breaking changes: add new helper functions rather than changing global state semantics.
4. For audio/IO changes, keep relative paths and verify files exist under `sounds/` or `ascii_art/`.

## Examples (use when making edits)
- Adding a monster: create `monsters/MyBeast.yaml` with structure similar to `Cyclops.yaml` (include `level`, `hp`, `maxhp`, `attack`, `defense`, `gold`).
- Adding an item to store: update `store.yaml` with an item that has `name`, `cost`, `class` and optional `ascii_art` path used by `shop()`.
- Debugging run: if screen clearing or colors look wrong on Windows, run from PowerShell and ensure `colorama` is installed; call `colorama.init()` if adding prints in other modules.

## Integration points and places to check when changing behavior
- `pygame.mixer` usage (calls to `mixer.init()` and `mixer.music.load()` in `play_sound`) — audio issues can crash runs.
- File I/O: `os.listdir('monsters/')` and `open('store.yaml')` — ensure working directory is the repo root in tests or runtime.
- Global modifications: `hero` is populated interactively after reading `heros/` files. Modifying hero shape requires edits to selection logic and `hero_status()`.

## Where tests/builds/live checks are (or are not)
- There are no discovered tests or build scripts. Introduce tests carefully and mock audio and terminal I/O.

If any section is unclear or you'd like examples turned into small automated checks (e.g., a schema validator for YAML files), tell me which part to expand and I'll iterate.
