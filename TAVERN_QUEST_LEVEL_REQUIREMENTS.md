# Tavern Quest Level Requirements Implementation

## Problem Identified
User reported that at level 2, they were being offered tavern quests for biomes they couldn't access, causing confusion about why they couldn't complete the quests.

## Root Cause Analysis
The tavern quest system had hardcoded NPC encounters that could offer quests for any biome regardless of the player's level:
- Desert quests require level 3+ but were offered to level 2 players
- Ocean quests require level 5+ but were offered to low-level players  
- Dungeon quests require level 7+ but were offered to beginners

The biome unlock system existed in the quest manager but wasn't integrated with the tavern NPC system.

## Solution Implemented

### 1. Added Level Requirement Checking
```python
def _can_access_biome(self, biome):
    """Check if hero can access a specific biome based on level"""
    hero_level = hero.get('level', 1)
    required_level = self.gui.quest_manager.BIOME_UNLOCK_LEVELS.get(biome, 1)
    return hero_level >= required_level
```

### 2. Enhanced Quest Offering Logic
- Before showing quest choice, check if player can access the target biome
- If level too low, show informative message with level requirement
- Display current player level vs required level
- Provide "Return to Tavern" option instead of broken quest acceptance

### 3. Improved Quest Descriptions
Updated all tavern quest descriptions to show level requirements upfront:
- `"Location: Desert biome (Level 3+ required)"`
- `"Location: Ocean biome (Level 5+ required)"`
- `"Location: Dungeon biome (Level 7+ required)"`
- `"Location: Grassland biome (Level 1+)"`

### 4. Enhanced Quest Details
When players ask for "More Details" about quests:
- Shows biome name and required level
- Displays player's current level
- Clear indication if requirements are met: ✅ or ⚠️
- Explains location and level requirements before quest acceptance

### 5. Fixed Missing Achievement Methods
Discovered and fixed multiple missing achievement tracking methods that were causing runtime errors:
- `track_combat_win()`
- `track_monster_kill()`
- `track_combat_loss()`
- `track_death()`
- `track_blacksmith_visit()`
- `track_side_quest_completion()`
- `track_gold_earned()`
- `track_bounty_completion()`

## Biome Access Levels

| Biome | Required Level | Example Quests |
|-------|---------------|----------------|
| Grassland | Level 1+ | Boar elimination, crop protection |
| Desert | Level 3+ | Bandit gems, desert wyrm |
| Ocean | Level 5+ | Pirate lute recovery |
| Dungeons | Level 7+ | Ancient tome, missing child rescue |

## User Experience Improvements

### Before Fix:
- ❌ Level 2 players offered desert/ocean/dungeon quests
- ❌ Confusing when players couldn't find quest targets
- ❌ No indication of level requirements
- ❌ Runtime errors from missing achievement methods

### After Fix:
- ✅ Only appropriate quests offered based on player level
- ✅ Clear level requirements shown in quest descriptions
- ✅ Informative error messages when level too low
- ✅ Enhanced quest details with biome/level info
- ✅ All achievement tracking methods working properly

## Files Modified

1. **gui_town.py**:
   - Added `_can_access_biome()` method
   - Enhanced `_show_side_quest_choice()` with level checking
   - Improved `_ask_side_quest_details()` with requirement display
   - Updated all quest descriptions with level requirements

2. **gui_achievements.py**:
   - Added 8 missing achievement tracking methods
   - Enhanced player stats initialization
   - Fixed compatibility with combat/quest/bounty systems

## Testing

### Manual Testing Steps:
1. Create level 2 character
2. Visit tavern and encounter NPCs
3. Verify only grassland quests are offered
4. Verify desert/ocean/dungeon quests show level requirements
5. Verify quest details show biome access information
6. Test combat system without achievement errors

### Expected Behavior:
- Level 2 players should only see grassland quests (level 1+)
- Higher biome quests should display: "You need to be level X to access the [Biome]"
- All quest descriptions should show "(Level X+ required)"
- Combat victories should track achievements without errors

## Prevention Strategy

1. **Always check level requirements** before offering location-based content
2. **Display requirements upfront** in quest descriptions and menus  
3. **Provide clear feedback** when requirements aren't met
4. **Implement all required methods** before referencing them in code
5. **Test with various player levels** to ensure appropriate content gating

This ensures players have a clear progression path and understand why certain content isn't available yet, improving the overall game experience and reducing confusion.