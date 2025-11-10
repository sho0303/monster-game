# New Monsters Implementation Guide

## Overview
This document describes the 14 new monsters added to PyQuest Monster Game, organized by biome to fill progression gaps and add variety to encounters.

## Monster Summary

### 🌾 Grassland Monsters (3)
**Angry Bee Swarm** (Level 2)
- HP: 10 | Attack: 3 | Defense: 2 | Gold: 15
- Low HP but decent attack for early game threat

**Goblin Thief** (Level 3)  
- HP: 18 | Attack: 4 | Defense: 3 | Gold: 25
- Slightly higher reward, balanced mid-early enemy

**Wild Boar** (Level 2)
- HP: 15 | Attack: 3 | Defense: 4 | Gold: 20
- Tankier early enemy with higher defense

### 🏜️ Desert Monsters (3)
**Scorpion King** (Level 6)
- HP: 50 | Attack: 9 | Defense: 8 | Gold: 55
- Strong desert enemy between Cyclops tier

**Sand Serpent** (Level 5)
- HP: 45 | Attack: 8 | Defense: 6 | Gold: 45
- Mid-tier desert threat

**Mummy Guardian** (Level 6)
- HP: 60 | Attack: 7 | Defense: 12 | Gold: 60
- High defense tank variant

### 🏰 Dungeon Monsters (3)
**Shadow Wraith** (Level 7)
- HP: 70 | Attack: 18 | Defense: 10 | Gold: 70
- Fast glass cannon enemy

**Stone Golem** (Level 8)
- HP: 100 | Attack: 15 | Defense: 20 | Gold: 75
- Very high defense, moderate attack

**Dark Sorcerer** (Level 7)
- HP: 65 | Attack: 20 | Defense: 8 | Gold: 75
- Powerful magic attacker, low defense

### 🌊 Ocean Monsters (4)
**Jellyfish Swarm** (Level 3)
- HP: 20 | Attack: 5 | Defense: 3 | Gold: 25
- Early ocean encounter

**Shark Patrol** (Level 4)
- HP: 35 | Attack: 6 | Defense: 5 | Gold: 35
- Mid-level ocean threat

**Pirate Ghost** (Level 6)
- HP: 55 | Attack: 11 | Defense: 9 | Gold: 65
- Spooky ocean undead

**Sea Serpent** (Level 7)
- HP: 80 | Attack: 16 | Defense: 12 | Gold: 70
- High-level ocean creature

### 🏘️ Town Monster (1)
**Bandit Leader** (Level 5)
- HP: 50 | Attack: 10 | Defense: 8 | Gold: 100
- Special town encounter with bonus gold

## Files Created

### Monster YAML Files (in `monsters/`)
- `BeeSwarm.yaml`
- `Goblin.yaml`
- `WildBoar.yaml`
- `ScorpionKing.yaml`
- `SandSerpent.yaml`
- `Mummy.yaml`
- `Wraith.yaml`
- `Golem.yaml`
- `Sorcerer.yaml`
- `Jellyfish.yaml`
- `Shark.yaml`
- `PirateGhost.yaml`
- `SeaSerpent.yaml`
- `BanditLeader.yaml`

### Art Generation Scripts (in `art_generation/`)
- `create_bee_swarm.py` ✅
- `create_goblin_art.py` ✅
- `create_boar_art.py` ✅
- `create_scorpion_art.py` ✅
- `generate_all_new_monsters.py` - Batch generator

## Next Steps

### 1. Generate Monster Artwork
Run the art generation scripts:
```powershell
cd art_generation
python create_bee_swarm.py
python create_goblin_art.py
python create_boar_art.py
python create_scorpion_art.py
```

Or generate all at once:
```powershell
python generate_all_new_monsters.py
```

### 2. Add Sound Files
See `NEW_MONSTER_SOUNDS.md` for required sound files and sourcing suggestions.

Temporary workaround - create placeholders:
```powershell
cd sounds
copy punch.mp3 bee-attack.mp3
copy punch.mp3 goblin-attack.mp3
copy punch.mp3 boar-attack.mp3
# ... etc for all sounds
```

### 3. Create Remaining Art Scripts
The following monsters still need art generation scripts:
- Sand Serpent
- Mummy Guardian  
- Shadow Wraith
- Stone Golem
- Dark Sorcerer
- Shark Patrol
- Jellyfish Swarm
- Sea Serpent
- Pirate Ghost
- Bandit Leader

Copy the pattern from existing scripts in `art_generation/`.

### 4. Test in Game
```powershell
python .\monster-game-gui.py
```

Test each biome:
- Press `B` to cycle through biomes
- Look for new encounters in each biome
- Verify stats and difficulty feel balanced

### 5. Balance Adjustments
If monsters feel too hard/easy, adjust in their YAML files:
- Increase/decrease HP for survivability
- Adjust attack for damage output
- Modify defense for tankiness
- Change gold rewards for incentive

## Design Rationale

### Progression Curve
The new monsters fill gaps in the level progression:
- **Levels 1-3**: Grassland now has more variety
- **Levels 4-6**: Desert and ocean have better mid-tier options
- **Levels 7-8**: Dungeon has encounters before Dragon
- **Special**: Bandit Leader provides town-specific content

### Biome Distribution
- Grassland: 3 new (was sparse)
- Desert: 3 new (needed mid-tier)
- Dungeon: 3 new (variety before boss)
- Ocean: 4 new (most needed variety)
- Town: 1 new (special encounter)

### Balance Philosophy
- **Glass cannons**: High attack, low defense (Wraith, Sorcerer)
- **Tanks**: High defense, moderate attack (Mummy, Golem)
- **Balanced**: Even stats (most others)
- **Swarms**: Multiple enemies concept (Bees, Jellyfish)

## Art Style Notes
Pixel art follows existing conventions:
- 32x32 base canvas
- Scaled 8x to 256x256 for game
- Transparent backgrounds (PNG with alpha)
- Similar color palettes to existing monsters
- Attack animations show motion/effects

## Contributing More Monsters

To add your own monsters:

1. **Create YAML file** in `monsters/`:
```yaml
YourMonster:
  name: Your Monster Name
  hp: 50
  maxhp: 50
  attack: 10
  defense: 8
  gold: 50
  level: 5
  xp: 5
  art: art/your_monster.png
  attack_sound: your-attack.mp3
  biome: grassland  # or desert, dungeon, ocean, town
```

2. **Create art generation script** in `art_generation/`:
See existing scripts as templates.

3. **Generate artwork**:
```powershell
python your_art_script.py
```

4. **Add sound file** to `sounds/`

5. **Test in game!**

## Questions?
See `.github/copilot-instructions.md` for more details on codebase structure and conventions.
