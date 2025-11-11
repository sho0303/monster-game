# New Monster Sound Files Needed

## 🌾 Grassland Monsters
- **bee-attack.mp3** - Buzzing/swarming sound effect
- **goblin-attack.mp3** - Goblin cackle or weapon swoosh
- **boar-attack.mp3** - Boar snort/charge sound

## 🏜️ Desert Monsters
- **scorpion-attack.mp3** - Clicking/chittering scorpion sound
- **serpent-attack.mp3** - Hissing snake sound (can be reused for Sand Serpent and Sea Serpent)
- **mummy-attack.mp3** - Creepy mummy groan/wrapping sounds

## 🏰 Dungeon Monsters
- **wraith-attack.mp3** - Ghostly wail or ethereal swoosh
- **golem-attack.mp3** - Heavy stone grinding/rumbling
- **sorcerer-attack.mp3** - Magic spell casting sound

## 🌊 Ocean Monsters
- **shark-attack.mp3** - Water splashing with aggressive sounds
- **jellyfish-attack.mp3** - Electric zapping or water pulse
- **serpent-attack.mp3** - (Already listed above - can be reused)
- **ghost-attack.mp3** - Spooky phantom sound

## 🏘️ Town Monsters
- **sword-clash.mp3** - Metal sword clashing sound

## Sound Sourcing Suggestions
1. **Free sound libraries:**
   - Freesound.org
   - OpenGameArt.org
   - ZapSplat.com (free tier)

2. **Search terms for each:**
   - Bee: "bee swarm", "angry bees", "buzzing attack"
   - Goblin: "goblin laugh", "creature cackle", "dagger swoosh"
   - Boar: "pig grunt", "boar charge", "animal attack"
   - Scorpion: "scorpion click", "insect attack"
   - Snake/Serpent: "snake hiss", "serpent attack"
   - Mummy: "mummy groan", "zombie moan", "wrapping cloth"
   - Wraith: "ghost wail", "ethereal swoosh", "spirit attack"
   - Golem: "rock slide", "stone rumble", "heavy footstep"
   - Sorcerer: "magic spell", "dark magic", "energy blast"
   - Shark: "shark attack", "water thrash"
   - Jellyfish: "electric shock", "static zap"
   - Ghost: "phantom sound", "ghostly moan"
   - Bandit: "sword fight", "blade clash"

## File Format Requirements
- **Format**: MP3 preferred (smaller file size)
- **Duration**: 0.5-2 seconds ideal
- **Volume**: Normalized to match existing sound files
- **Channels**: Mono or Stereo

## Temporary Solution
Until sound files are added, you can:
1. Reuse existing similar sounds:
   - Use `punch.mp3` for physical attacks
   - Use `buzzer.mp3` for any "miss" or "alert" sounds
   - Use existing monster sounds as placeholders

2. Or create placeholder files:
```bash
# In sounds/ directory
copy punch.mp3 bee-attack.mp3
copy punch.mp3 goblin-attack.mp3
copy snake-attack.mp3 serpent-attack.mp3
# etc.
```

## Testing Sound Files
Run the game and encounter each monster to test:
```powershell
python .\monster-game-gui.py
```

Then navigate to the appropriate biome and trigger encounters to verify sounds play correctly.
