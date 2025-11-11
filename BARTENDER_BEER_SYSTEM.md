# Bartender Beer System Implementation

## Overview
Added a humorous bartender named "Bob" to the tavern who only sells beer - but offers it under 4 different "fancy" names that are all just beer.

## Features

### 1. Bartender Bob's Beer Emporium
- **Location**: Town → Tavern → Talk to Bartender
- **Character**: Jovial bartender Bob who admits all his drinks are just beer
- **Menu**: 4 "different" beers that are all identical in function

### 2. Beer Options (All identical functionality)
1. **Beer** - "Classic brew, recommended by Bob" 
2. **Ale** - "It's beer, but fancier name"
3. **Lager** - "Still beer, Bob assures you" 
4. **Stout** - "Dark beer, but definitely beer"

**All beers:**
- Cost: 5 gold each
- Healing: 5 HP restoration
- Effect: Same regardless of "type" chosen

### 3. Humorous Dialogue
Bob provides different flavor text for each "beer type" while admitting they're all the same:
- Serves "ale" from the same tap as beer
- Claims lager is "lighter" than regular beer
- Proudly declares stout is "the darkest beer I've got!"

### 4. Secret Beer Quest (Easter Egg)
- **Trigger**: 10% random chance when buying any beer
- **Objective**: Drink 10 beers total (across multiple visits)
- **Reward**: "Tavern Regular" badge + 100 bonus gold
- **Tracking**: Uses `hero['beers_consumed']` counter
- **Reset**: Counter resets to 0 after achievement

## Implementation Details

### Files Modified
- **`gui_town.py`** - Added bartender functionality to tavern

### New Methods Added
```python
def _talk_to_bartender(self):
    """Display Bob's beer menu with 4 options"""

def _buy_beer(self, beer_type):
    """Purchase and consume one of the 4 beer types"""
```

### Integration Points
1. **Tavern Menu**: Added "🍻 Talk to Bartender" button
2. **Gold Economy**: Beers cost 5 gold (affordable healing option)  
3. **Health System**: 5 HP healing per beer (modest but useful)
4. **Save System**: Beer counter persists in hero data

## User Flow
1. Enter Town → Visit Tavern
2. Click "🍻 Talk to Bartender" 
3. See Bob's enthusiastic beer menu
4. Choose any of the 4 "different" beers
5. Pay 5 gold, restore 5 HP
6. Enjoy Bob's humorous admission they're all just beer
7. Potentially trigger secret achievement

## Balancing
- **Cost vs Healing**: 5 gold for 5 HP (1:1 ratio - reasonable but not overpowered)
- **Fountain Alternative**: Fountain heals 3 HP for free, beer heals 5 HP for cost
- **Shop Integration**: Cheaper than most potions, but heals less

## Testing
- Created `tests/test_bartender.py` for automated testing
- All functionality verified: dialogue, purchases, healing, gold deduction
- Secret achievement system tested and working

## Future Enhancements (Optional)
- Add beer-specific temporary buffs (courage, luck, etc.)
- Drunk status effect after multiple beers
- Daily beer specials with different effects
- Beer brewing mini-game

## Credits
Inspired by user's brother's idea: "have a bartender that only sells beer and all the options it has is beer"

## Code Location
- Main implementation: `gui_town.py` (lines ~95-220)
- Test file: `tests/test_bartender.py`