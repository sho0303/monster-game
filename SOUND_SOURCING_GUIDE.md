# Sound File Sourcing Guide for New Monsters

## 🎵 Quick Reference - Needed Sound Files

You need **14 sound files** total (some can be reused):
- bee-attack.mp3
- goblin-attack.mp3
- boar-attack.mp3
- scorpion-attack.mp3
- serpent-attack.mp3 (can reuse for both Sand Serpent and Sea Serpent)
- mummy-attack.mp3
- wraith-attack.mp3
- golem-attack.mp3
- sorcerer-attack.mp3
- shark-attack.mp3
- jellyfish-attack.mp3
- ghost-attack.mp3 (for Pirate Ghost)
- sword-clash.mp3 (for Bandit Leader)

## 🌐 Best Free Sound Libraries

### 1. **Freesound.org** (RECOMMENDED - Largest Library)
**URL**: https://freesound.org
- ✅ Largest free sound library (500,000+ sounds)
- ✅ All sounds are Creative Commons licensed
- ✅ Download in MP3/WAV formats
- ⚠️ Requires free account (quick signup)

**How to use:**
1. Go to https://freesound.org
2. Create free account
3. Search for sound (e.g., "bee swarm attack")
4. Filter by license: Choose "Creative Commons 0" for no attribution required
5. Download MP3 format
6. Rename to match your needs (e.g., `bee-attack.mp3`)

**Search terms for each monster:**
```
Bee Swarm: "angry bees", "bee swarm", "buzzing attack", "wasp swarm"
Goblin: "goblin laugh", "creature cackle", "imp", "evil laugh"
Boar: "pig grunt", "boar charge", "wild boar", "pig squeal"
Scorpion: "scorpion click", "insect chittering", "spider click"
Sand/Sea Serpent: "snake hiss", "serpent hiss", "cobra hiss"
Mummy: "zombie moan", "mummy groan", "undead", "creepy groan"
Wraith: "ghost wail", "spectral", "phantom", "ethereal whoosh"
Golem: "rock slide", "stone rumble", "heavy stomp", "boulder"
Sorcerer: "magic spell", "dark magic", "energy blast", "wizard"
Shark: "shark", "water splash aggressive", "bite"
Jellyfish: "electric zap", "static shock", "taser"
Pirate Ghost: "ghost moan", "phantom", "spooky"
Bandit: "sword clash", "sword fight", "blade"
```

### 2. **ZapSplat.com** (High Quality)
**URL**: https://www.zapsplat.com
- ✅ Professional quality sounds
- ✅ Free tier available (20 downloads/day)
- ✅ Great for creature sounds
- ⚠️ Requires free account

**How to use:**
1. Go to https://www.zapsplat.com
2. Create free account
3. Search for sounds
4. Download (up to 20/day on free plan)

### 3. **OpenGameArt.org** (Game-Focused)
**URL**: https://opengameart.org
- ✅ Specifically for game development
- ✅ Public domain and CC licensed
- ✅ No account required for some downloads

**How to use:**
1. Go to https://opengameart.org
2. Click "Art" → "Music & Sounds"
3. Search for needed sound
4. Check license (prefer CC0 or Public Domain)

### 4. **YouTube Audio Library** (Google)
**URL**: https://www.youtube.com/audiolibrary
- ✅ All sounds free to use
- ✅ No attribution required
- ✅ High quality
- ⚠️ Requires YouTube/Google account

**How to use:**
1. Go to YouTube Studio → Audio Library
2. Filter by "Sound effects"
3. Search and download

### 5. **Mixkit.co** (Modern, Clean)
**URL**: https://mixkit.co/free-sound-effects/
- ✅ No account needed
- ✅ All free to use
- ✅ Modern sound effects

## 🎯 Step-by-Step: Complete Workflow

### Option A: Quick Method (Use Freesound)

```powershell
# 1. Create account at freesound.org

# 2. Search and download each sound (search terms above)
#    Save downloads to your Downloads folder

# 3. Move and rename files
cd D:\monster-game\sounds

# Rename your downloaded files
move $env:USERPROFILE\Downloads\bee-swarm-sound.mp3 bee-attack.mp3
move $env:USERPROFILE\Downloads\goblin-laugh.mp3 goblin-attack.mp3
# ... etc for each file
```

### Option B: Automated Search Script

I can create a Python script to help you find sounds:

```python
# sound_finder.py - Opens browser tabs with search results
import webbrowser

searches = {
    "bee-attack.mp3": "https://freesound.org/search/?q=angry+bees",
    "goblin-attack.mp3": "https://freesound.org/search/?q=goblin+laugh",
    "boar-attack.mp3": "https://freesound.org/search/?q=wild+boar",
    # ... etc
}

for filename, url in searches.items():
    print(f"Opening search for {filename}...")
    webbrowser.open(url)
```

### Option C: Use Existing Game Sounds as Placeholders

**Quick temporary solution** while you source proper sounds:

```powershell
cd D:\monster-game\sounds

# Use punch.mp3 for physical attacks
copy punch.mp3 bee-attack.mp3
copy punch.mp3 goblin-attack.mp3
copy punch.mp3 boar-attack.mp3
copy punch.mp3 scorpion-attack.mp3

# Use existing monster sounds
copy snake-attack.mp3 serpent-attack.mp3
copy demon-attack.mp3 wraith-attack.mp3
copy cyclops-attack.mp3 golem-attack.mp3

# Use buzzer for special effects
copy buzzer.mp3 jellyfish-attack.mp3

# Copy for remaining
copy punch.mp3 mummy-attack.mp3
copy punch.mp3 sorcerer-attack.mp3
copy punch.mp3 shark-attack.mp3
copy vampire-attack.mp3 ghost-attack.mp3
copy punch.mp3 sword-clash.mp3
```

## 🔧 Converting and Preparing Sound Files

### If you download WAV files:

**Install ffmpeg** (if not already):
```powershell
# Using Chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

**Convert WAV to MP3:**
```powershell
cd D:\monster-game\sounds

# Convert single file
ffmpeg -i your-sound.wav -codec:a libmp3lame -b:a 192k bee-attack.mp3

# Convert all WAV files in folder
Get-ChildItem *.wav | ForEach-Object {
    $output = $_.BaseName + ".mp3"
    ffmpeg -i $_.Name -codec:a libmp3lame -b:a 192k $output
}
```

### Audio Requirements
- **Format**: MP3 (preferred) or WAV
- **Duration**: 0.5 - 2 seconds ideal
- **Sample Rate**: 44100 Hz standard
- **Bitrate**: 128-192 kbps is fine
- **Volume**: Normalize to match existing sounds

**Normalize volume with ffmpeg:**
```powershell
ffmpeg -i input.mp3 -af "volume=1.5" output.mp3
```

## 📝 My Recommendation: Freesound.org Walkthrough

### Best approach for quality + free:

1. **Create account** at https://freesound.org (1 minute)

2. **Search for each sound** using these specific searches:
   - "bee swarm" → Download best result
   - "goblin cackle" → Download
   - "boar grunt" → Download
   - etc.

3. **Download tips:**
   - Choose MP3 format when available
   - Look for sounds 0.5-2 seconds long
   - Preview before downloading
   - Prefer CC0 license (no attribution needed)

4. **Batch rename** in PowerShell:
   ```powershell
   cd $env:USERPROFILE\Downloads
   # Rename each file to match the required names
   ren "123456__user__bee-swarm.mp3" "bee-attack.mp3"
   # Then move all to sounds folder
   move *-attack.mp3 D:\monster-game\sounds\
   ```

5. **Test in game:**
   ```powershell
   cd D:\monster-game
   python monster-game-gui.py
   ```

## 🎨 Alternative: AI Sound Generation (Advanced)

If you want custom sounds:

1. **ElevenLabs** (AI sound effects) - https://elevenlabs.io
2. **AudioGen** by Meta - https://audiocraft.metademolab.com/
3. **Riffusion** - https://www.riffusion.com/

## ✅ Verification Checklist

After sourcing sounds:
- [ ] All 14 MP3 files in `sounds/` folder
- [ ] Files named exactly as listed in YAML files
- [ ] Duration under 3 seconds each
- [ ] Volume normalized
- [ ] Tested at least one monster in game

## 🆘 If You Get Stuck

**Quick solution - Just use placeholders:**
```powershell
cd D:\monster-game\sounds
copy punch.mp3 bee-attack.mp3
copy punch.mp3 goblin-attack.mp3
copy punch.mp3 boar-attack.mp3
copy punch.mp3 scorpion-attack.mp3
copy snake-attack.mp3 serpent-attack.mp3
copy demon-attack.mp3 mummy-attack.mp3
copy vampire-attack.mp3 wraith-attack.mp3
copy cyclops-attack.mp3 golem-attack.mp3
copy demon-attack.mp3 sorcerer-attack.mp3
copy slime-attack.mp3 shark-attack.mp3
copy buzzer.mp3 jellyfish-attack.mp3
copy vampire-attack.mp3 ghost-attack.mp3
copy punch.mp3 sword-clash.mp3
```

The game will work perfectly - you can always swap in better sounds later!

## 📞 Need Help?

If you run into issues:
1. Try the placeholder solution above first
2. Check file names match exactly (case-sensitive on some systems)
3. Ensure files are in `D:\monster-game\sounds\` directory
4. Test with: `ls D:\monster-game\sounds\*-attack.mp3`
