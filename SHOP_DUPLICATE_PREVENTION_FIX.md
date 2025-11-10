# Shop Duplicate Purchase Prevention Fix

## Problem Description
The shop system previously allowed players to purchase the same weapon or armor multiple times, which would infinitely stack their stats by repeatedly buying the same equipment. For example, a player could buy "Titanium Sword" multiple times and get +20 attack each time, making them infinitely powerful.

## Solution Implemented
Added duplicate purchase prevention for **Weapons** and **Armour** categories only, while preserving the ability to buy multiple **Items** (as intended).

## Changes Made

### Modified `gui_shop.py` - `_purchase_item()` method:

#### 1. Weapon Purchase Prevention
```python
# Check if player already owns this specific weapon
current_weapon = hero.get('weapon', 'None')
if current_weapon == item['name']:
    self.gui.clear_text()
    self.gui.print_text(f"\n❌ You already own {item['name']}!")
    self.gui.print_text("   You cannot purchase the same weapon again.")
    # Refund the gold since we already deducted it
    hero['gold'] += item_cost
    # Unlock interface and return to shop after delay
    self.gui.unlock_interface()
    self.gui.root.after(2500, self._show_items)
    return
```

#### 2. Armor Purchase Prevention  
```python
# Check if player already owns this specific armor
current_armour = hero.get('armour', 'None')
if current_armour == item['name']:
    self.gui.clear_text()
    self.gui.print_text(f"\n❌ You already own {item['name']}!")
    self.gui.print_text("   You cannot purchase the same armor again.")
    # Refund the gold since we already deducted it
    hero['gold'] += item_cost
    # Unlock interface and return to shop after delay
    self.gui.unlock_interface()
    self.gui.root.after(2500, self._show_items)
    return
```

## Key Features of the Fix

### ✅ **What is Protected:**
- **Weapons**: Cannot buy the same weapon twice
- **Armour**: Cannot buy the same armor twice  
- **Automatic Gold Refund**: Gold is refunded if duplicate purchase is attempted
- **Clear User Feedback**: Players see exactly why the purchase was blocked
- **Interface Management**: Properly unlocks interface and returns to shop

### ✅ **What Still Works:**
- **Items**: Can still be purchased multiple times (Health Potions, etc.)
- **Equipment Upgrades**: Can still buy different/better weapons and armor
- **Normal Purchases**: First-time purchases work exactly as before

### ✅ **Error Handling:**
- Gold is automatically refunded on blocked purchases
- Clear error messages explain why purchase was blocked
- Interface is properly unlocked and user is returned to shop menu
- No side effects or broken states

## Behavior Examples

### Before Fix (Broken):
1. Buy "Titanium Sword" → Attack becomes 25 (5 base + 20)
2. Buy "Titanium Sword" again → Attack becomes 45 (5 base + 20 + 20) ❌
3. Buy "Titanium Sword" again → Attack becomes 65 (5 base + 20 + 20 + 20) ❌

### After Fix (Correct):
1. Buy "Titanium Sword" → Attack becomes 25 (5 base + 20) ✅
2. Try to buy "Titanium Sword" again → **BLOCKED** + Gold Refunded ✅
3. Buy "Excalibur" instead → Attack becomes 45 (5 base + 40) ✅

### Items Still Work (Unchanged):
1. Buy "Health Potion" → Inventory: 1 Health Potion ✅
2. Buy "Health Potion" again → Inventory: 2 Health Potions ✅
3. Buy "Health Potion" again → Inventory: 3 Health Potions ✅

## Testing Results

Created comprehensive tests that verify:
- ✅ Duplicate weapon purchases are blocked
- ✅ Duplicate armor purchases are blocked  
- ✅ Gold is properly refunded on blocked purchases
- ✅ Item purchases still allow multiple quantities
- ✅ Equipment upgrades (buying different items) still work
- ✅ Interface properly unlocks after blocked purchases
- ✅ All purchase logic remains intact for valid scenarios

## Technical Implementation Notes

- **Detection Method**: Compares `item['name']` with `hero.get('weapon')` or `hero.get('armour')`
- **Timing**: Check happens after gold deduction but before stat application
- **Gold Handling**: Automatic refund ensures no gold is lost on blocked purchases
- **Interface**: Properly unlocks interface and provides user feedback
- **Categories**: Only affects 'Weapons' and 'Armour' categories, 'Items' unchanged