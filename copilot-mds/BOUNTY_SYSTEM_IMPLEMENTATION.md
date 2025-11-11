# Bounty Board System Implementation

## Overview
Complete bounty board system for the tavern with three bounty types, unique rewards, and elite monster encounters.

## Features

### 1. Three Bounty Types
- **Hunt Bounties**: Kill 1 specific monster (2-4x gold reward)
- **Collector Bounties**: Kill multiple (3-7) of the same monster type
- **Elite Boss Bounties**: Face enhanced version with 1.5x HP/Attack

### 2. Difficulty Tiers
- **Bronze**: Low-level monsters, basic rewards
- **Silver**: Mid-level monsters, enhanced rewards
- **Gold**: High-level monsters, legendary rewards

### 3. Unique Bounty Rewards
Items that can ONLY be obtained from bounties (not in shop):

**Bronze Tier:**
- Hunter's Trophy (+5 attack)
- Bounty Medal (+3 defense)
- Lucky Charm (+3 attack, +2 defense)

**Silver Tier:**
- Elite Hunter Badge (+10 attack)
- Champion's Ring (+8 defense)
- Slayer's Pendant (+7 attack, +5 defense)

**Gold Tier:**
- Legendary Bounty Crown (+15 attack, +10 defense)
- Master Hunter Amulet (+20 attack)
- Titan's Bracer (+15 defense)

### 4. Elite Monster System
When an elite boss bounty is active:
- 10% chance to spawn elite variant during random encounters
- Elite monsters have:
  - 1.5x HP
  - 1.5x Attack
  - 2x Gold reward
  - 2x XP reward
  - +1 Level
  - Special "⚡ ELITE ENCOUNTER! ⚡" visual indicator

### 5. Level-Aware Bounty Generation
Bounties are filtered based on hero level:
- Bronze: Hero level 1-10
- Silver: Hero level 6-20
- Gold: Hero level 15+

Monsters are filtered to be within hero level range (±3 levels).

## Integration Points

### Files Modified
1. **`gui_bounty.py`** (NEW) - Complete bounty system
   - `Bounty` class with serialization
   - `BountyManager` class with all logic
   - Bounty generation, tracking, completion
   - Elite monster creation

2. **`gui_town.py`** - Tavern integration
   - Added "🎯 Bounty Board" button to tavern
   - Removed "under construction" message

3. **`gui_main.py`** - System initialization
   - Import BountyManager
   - Create `self.bounty_manager` instance

4. **`gui_monster_encounter.py`** - Combat integration
   - Check bounty progress after each kill
   - Display bounty completion notifications
   - 10% elite spawn chance when bounty active
   - Elite encounter visual indicators

5. **`gui_save_load.py`** - Persistence
   - Save active and available bounties
   - Load bounties with save game
   - Serialize/deserialize bounty data

## Save/Load Support

### What's Saved
- All available bounties (not yet accepted)
- All active bounties (accepted, in progress)
- Bounty progress (kill counts)
- Bounty completion status

### Save Format (YAML)
```yaml
bounties:
  available:
    - bounty_type: hunt
      target: Cyclops
      target_count: 1
      current_count: 0
      reward_gold: 200
      reward_item: Hunter's Trophy
      description: Hunt down a Cyclops
      difficulty: Bronze
      completed: false
      status: available
  active:
    - bounty_type: collector
      target: Goblin
      target_count: 5
      current_count: 3
      reward_gold: 300
      reward_item: Elite Hunter Badge
      description: Eliminate 5 Goblins
      difficulty: Silver
      completed: false
      status: active
```

## Usage Flow

### For Players
1. Visit Town → Tavern → Bounty Board
2. View available bounties (up to 3 at a time)
3. Accept bounty (moved to active list)
4. Hunt monsters to complete bounty
5. Return to bounty board to claim rewards
6. Refresh board for new bounties (costs 25 gold)

### For Developers
```python
# Check if monster kill contributes to bounty
bounty_manager.update_bounty_progress(hero, monster_name)

# Check for elite encounter before spawning monster
elite_monster = bounty_manager.check_for_elite_encounter(hero, monster_type)
if elite_monster and random.random() < 0.10:
    monster = elite_monster
    # Display elite warning

# Generate new bounties
bounty_manager.generate_bounty(hero, difficulty='Silver')

# Complete bounty and give rewards
bounty_manager.complete_bounty(bounty, hero)
```

## Balancing

### Gold Rewards
- Hunt (1 kill): 2-4x monster base gold
- Collector (3-7 kills): 1.5-2x total gold from kills
- Elite Boss: 3-5x base gold + elite monster 2x gold bonus

### Difficulty Progression
- Bronze unlocks at level 1
- Silver unlocks at level 6
- Gold unlocks at level 15

### Elite Spawn Rate
- 10% chance when bounty active
- Only spawns for matching monster type
- Prevents farming by requiring active bounty

## Testing Checklist

### Manual Testing
- [x] Bounty board accessible from tavern
- [x] Bounties generate at different difficulty levels
- [ ] Hunt bounties complete after 1 kill
- [ ] Collector bounties track multiple kills
- [ ] Elite monsters spawn with active elite bounty
- [ ] Elite visual indicator displays correctly
- [ ] Rewards distributed (gold + items)
- [ ] Bounties persist through save/load
- [ ] Can accept multiple bounties
- [ ] Can refresh bounty board (25 gold cost)

### Edge Cases to Test
- [ ] Save/load with no bounties
- [ ] Save/load with active bounties in progress
- [ ] Complete bounty, don't claim, save/load
- [ ] Multiple elite bounties active
- [ ] Bounty completion with full inventory
- [ ] Level up mid-bounty

## Known Limitations
1. No bounty expiration system
2. Maximum 3 available bounties at once
3. Elite spawn is random (10%) - may take multiple encounters
4. Refresh cost is fixed (25 gold)
5. Cannot abandon/cancel bounties once accepted

## Future Enhancements (Optional)
- Daily/weekly bounties
- Reputation system (bounty hunter rank)
- Bounty chains (complete X to unlock special bounty)
- Time-limited bounties with bonus rewards
- Bounty leaderboard
- Town crier announces available bounties
- Rare "legendary" bounties with unique mechanics

## Performance Notes
- Bounty checks run after each combat (minimal overhead)
- Elite spawn check only when bounty active
- Save file size increase: ~500 bytes per bounty
- No performance impact on game startup

## Credits
Implemented as part of tavern functionality expansion.
Follows existing quest system architecture for consistency.
