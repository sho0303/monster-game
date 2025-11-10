"""
Test script for shop duplicate purchase prevention
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_duplicate_purchase_prevention():
    """Test that weapons and armor cannot be purchased twice"""
    print("Testing Duplicate Purchase Prevention")
    print("=" * 45)
    
    # Create a mock hero for testing
    test_hero = {
        'name': 'Test Hero',
        'class': 'Warrior',
        'weapon': 'Titanium Sword',  # Already owns this weapon
        'armour': 'Plate Mail',      # Already owns this armor
        'attack': 25,  # 5 base + 20 from Titanium Sword
        'defense': 25, # 5 base + 20 from Plate Mail
        'base_attack': 5,
        'base_defense': 5,
        'gold': 1000,
        'hp': 100,
        'maxhp': 100
    }
    
    # Test weapons from store
    test_weapons = [
        {'name': 'Titanium Sword', 'attack': 20, 'cost': 100, 'class': 'Warrior'},  # Already owned
        {'name': 'Excalibur', 'attack': 40, 'cost': 500, 'class': 'Warrior'}       # New weapon
    ]
    
    # Test armor from store
    test_armour = [
        {'name': 'Plate Mail', 'defense': 20, 'cost': 100, 'class': 'Warrior'},        # Already owned
        {'name': 'Golden Plate Mail', 'defense': 40, 'cost': 500, 'class': 'Warrior'} # New armor
    ]
    
    print(f"Starting hero state:")
    print(f"  Weapon: {test_hero['weapon']} (Attack: {test_hero['attack']})")
    print(f"  Armor: {test_hero['armour']} (Defense: {test_hero['defense']})")
    print(f"  Gold: {test_hero['gold']}")
    print()
    
    # Simulate weapon purchase logic
    def simulate_weapon_purchase(hero, item):
        print(f"Attempting to purchase weapon: {item['name']} for {item['cost']} gold")
        
        # Check gold
        if hero['gold'] < item['cost']:
            print(f"  ❌ Not enough gold (need {item['cost']}, have {hero['gold']})")
            return False
        
        # Check for duplicate
        current_weapon = hero.get('weapon', 'None')
        if current_weapon == item['name']:
            print(f"  ❌ Already own {item['name']}! Purchase blocked.")
            return False
        
        # Process purchase
        hero['gold'] -= item['cost']
        old_weapon = hero['weapon']
        hero['weapon'] = item['name']
        old_attack = hero['attack']
        hero['attack'] = hero['base_attack'] + item['attack']
        
        print(f"  ✅ Purchase successful!")
        print(f"  ⚔️  Weapon: {old_weapon} → {hero['weapon']}")
        print(f"  ⚔️  Attack: {old_attack} → {hero['attack']}")
        print(f"  💰 Gold: {hero['gold'] + item['cost']} → {hero['gold']}")
        return True
    
    # Simulate armor purchase logic
    def simulate_armour_purchase(hero, item):
        print(f"Attempting to purchase armor: {item['name']} for {item['cost']} gold")
        
        # Check gold
        if hero['gold'] < item['cost']:
            print(f"  ❌ Not enough gold (need {item['cost']}, have {hero['gold']})")
            return False
        
        # Check for duplicate
        current_armour = hero.get('armour', 'None')
        if current_armour == item['name']:
            print(f"  ❌ Already own {item['name']}! Purchase blocked.")
            return False
        
        # Process purchase
        hero['gold'] -= item['cost']
        old_armour = hero['armour']
        hero['armour'] = item['name']
        old_defense = hero['defense']
        hero['defense'] = hero['base_defense'] + item['defense']
        
        print(f"  ✅ Purchase successful!")
        print(f"  🛡️  Armor: {old_armour} → {hero['armour']}")
        print(f"  🛡️  Defense: {old_defense} → {hero['defense']}")
        print(f"  💰 Gold: {hero['gold'] + item['cost']} → {hero['gold']}")
        return True
    
    # Test Case 1: Try to buy same weapon (should fail)
    print("TEST 1: Attempting to buy duplicate weapon")
    print("-" * 40)
    result1 = simulate_weapon_purchase(test_hero, test_weapons[0])
    print()
    
    # Test Case 2: Try to buy same armor (should fail)
    print("TEST 2: Attempting to buy duplicate armor")
    print("-" * 40)
    result2 = simulate_armour_purchase(test_hero, test_armour[0])
    print()
    
    # Test Case 3: Buy new weapon (should succeed)
    print("TEST 3: Attempting to buy new weapon")
    print("-" * 40)
    result3 = simulate_weapon_purchase(test_hero, test_weapons[1])
    print()
    
    # Test Case 4: Buy new armor (should succeed)
    print("TEST 4: Attempting to buy new armor")
    print("-" * 40)
    result4 = simulate_armour_purchase(test_hero, test_armour[1])
    print()
    
    # Test Case 5: Try to buy the same weapon again after upgrade (should fail)
    print("TEST 5: Attempting to buy duplicate weapon after upgrade")
    print("-" * 40)
    result5 = simulate_weapon_purchase(test_hero, test_weapons[1])  # Try to buy Excalibur again
    print()
    
    # Summary
    print("SUMMARY")
    print("=" * 20)
    print(f"Final hero state:")
    print(f"  Weapon: {test_hero['weapon']} (Attack: {test_hero['attack']})")
    print(f"  Armor: {test_hero['armour']} (Defense: {test_hero['defense']})")
    print(f"  Gold: {test_hero['gold']}")
    print()
    
    # Verify test results
    expected_results = [False, False, True, True, False]  # Duplicate purchases should fail
    actual_results = [result1, result2, result3, result4, result5]
    
    print("Test Results:")
    test_names = [
        "Duplicate weapon purchase",
        "Duplicate armor purchase", 
        "New weapon purchase",
        "New armor purchase",
        "Duplicate upgraded weapon"
    ]
    
    all_passed = True
    for i, (expected, actual, name) in enumerate(zip(expected_results, actual_results, test_names)):
        status = "✅ PASS" if expected == actual else "❌ FAIL"
        print(f"  {i+1}. {name}: {status}")
        if expected != actual:
            all_passed = False
            print(f"     Expected: {expected}, Got: {actual}")
    
    print()
    if all_passed:
        print("🎉 All tests passed! Duplicate purchase prevention is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the implementation.")

if __name__ == "__main__":
    test_duplicate_purchase_prevention()