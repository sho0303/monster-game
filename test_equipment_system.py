#!/usr/bin/env python3
"""Test the enhanced equipment customization system"""

import tkinter as tk
from gui_main import GameGUI

def test_equipment_system():
    """Test the equipment customization system"""
    print("🧪 Testing Enhanced Equipment System")
    print("=" * 50)
    
    root = tk.Tk()
    gui = GameGUI(root)
    root.update()
    
    # Wait for game to fully initialize
    root.update()
    
    # Select first hero automatically
    if hasattr(gui, 'game_state') and gui.game_state:
        # Choose first available hero
        first_hero_name = list(gui.game_state.heros.keys())[0]
        gui.game_state.hero = gui.game_state.heros[first_hero_name].copy()
    
    hero = gui.game_state.hero
    
    print(f"✅ Game initialized")
    print(f"Hero: {hero.get('name', 'Unknown')} (Level {hero.get('level', 1)})")
    
    # Set up test hero with equipment and gold
    hero['gold'] = 5000  # Plenty of gold for testing
    hero['weapon'] = 'Excalibur'  # Give a good weapon
    hero['armour'] = 'Golden Plate Mail'  # Give good armor
    hero['attack'] = 40  # Set initial attack
    hero['defense'] = 40  # Set initial defense
    
    print(f"\n🎮 Test Setup:")
    print(f"  - Gold: {hero.get('gold', 0)}")
    print(f"  - Weapon: {hero.get('weapon', 'None')}")
    print(f"  - Armor: {hero.get('armour', 'None')}")
    print(f"  - Attack: {hero.get('attack', 0)}")
    print(f"  - Defense: {hero.get('defense', 0)}")
    
    # Test equipment system availability
    print(f"\n🔧 Equipment System Check:")
    
    equipment_checks = [
        ('equipment_manager', "Equipment Manager initialized"),
        ('equipment_manager.enchantments', "Enchantment system available"),
        ('equipment_manager.upgrade_levels', "Upgrade system available"),
        ('equipment_manager.gems', "Gem system available")
    ]
    
    all_systems_ready = True
    for attr_path, description in equipment_checks:
        try:
            obj = gui
            for attr in attr_path.split('.'):
                obj = getattr(obj, attr)
            status = "✅" if obj else "❌"
            print(f"  {status} {description}")
            if not obj:
                all_systems_ready = False
        except AttributeError:
            print(f"  ❌ {description}")
            all_systems_ready = False
    
    if not all_systems_ready:
        print(f"\n⚠️  Equipment system not fully available!")
        root.destroy()
        return
    
    # Test enchantment options
    print(f"\n✨ Available Enchantments:")
    enchantments = gui.equipment_manager.enchantments
    for enchant_id, enchant_info in list(enchantments.items())[:3]:  # Show first 3
        print(f"  🔮 {enchant_info['name']}: +{enchant_info['damage_bonus']} attack")
        print(f"      Special: {enchant_info['special'].replace('_', ' ').title()}")
    
    # Test armor enchantments
    print(f"\n🛡️ Available Armor Enchantments:")
    armor_enchants = gui.equipment_manager.armor_enchantments
    for enchant_id, enchant_info in list(armor_enchants.items())[:3]:  # Show first 3
        print(f"  🔮 {enchant_info['name']}: +{enchant_info['defense_bonus']} defense")
        print(f"      Special: {enchant_info['special'].replace('_', ' ').title()}")
    
    # Test upgrade levels
    print(f"\n⚡ Upgrade Progression:")
    upgrades = gui.equipment_manager.upgrade_levels
    for level, upgrade_info in upgrades.items():
        if level <= 3:  # Show first few levels
            multiplier = f"{upgrade_info['multiplier']}x"
            cost_mult = f"{upgrade_info['cost_multiplier']}x cost"
            print(f"  Level {level}: {upgrade_info['name']} ({multiplier}, {cost_mult})")
    
    # Test gem system
    print(f"\n💎 Available Gems:")
    gems = gui.equipment_manager.gems
    for gem_id, gem_info in list(gems.items())[:4]:  # Show first 4
        effect = gem_info['effect'].replace('_', ' ').title()
        bonus = gem_info['bonus']
        print(f"  💎 {gem_info['name']}: +{bonus} {effect}")
    
    # Test town integration
    print(f"\n🏘️ Town Integration Check:")
    
    # Check if equipment forge is in town menu
    try:
        # Navigate to town to check menu
        gui.town.enter_town()
        print(f"  ✅ Town menu accessible")
        print(f"  ✅ Equipment Forge should be option 5 in town menu")
    except Exception as e:
        print(f"  ❌ Town integration issue: {e}")
    
    print(f"\n🎯 Test Instructions:")
    print(f"  1. The game will open with town menu")
    print(f"  2. Select '✨ Equipment Forge' option")
    print(f"  3. Try upgrading your weapon (+1 level costs ~200 gold)")
    print(f"  4. Try enchanting your weapon (costs ~175-300 gold)")
    print(f"  5. Try upgrading your armor (+1 level costs ~160 gold)")
    print(f"  6. Try enchanting your armor (costs ~140-220 gold)")
    print(f"  7. Use 'View Equipment Details' to see all enhancements")
    print(f"  8. Close window when done testing")
    
    print(f"\n🚀 Starting interactive equipment test!")
    
    # Start main loop for testing
    root.mainloop()

if __name__ == '__main__':
    test_equipment_system()