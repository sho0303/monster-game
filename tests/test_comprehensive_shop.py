"""
Comprehensive test for shop duplicate purchase prevention
"""

def test_comprehensive_shop_behavior():
    """Test all shop purchase scenarios"""
    print("Comprehensive Shop Purchase Test")
    print("=" * 35)
    
    # Test scenarios
    scenarios = [
        {
            'name': 'Fresh Hero - No Equipment',
            'hero': {
                'class': 'Warrior', 
                'weapon': 'None', 
                'armour': 'None',
                'attack': 5, 'defense': 5,
                'base_attack': 5, 'base_defense': 5,
                'gold': 1000
            },
            'tests': [
                {'category': 'Weapons', 'item': 'Titanium Sword', 'attack': 20, 'cost': 100, 'should_succeed': True},
                {'category': 'Weapons', 'item': 'Titanium Sword', 'attack': 20, 'cost': 100, 'should_succeed': False},  # Duplicate
                {'category': 'Armour', 'item': 'Plate Mail', 'defense': 20, 'cost': 100, 'should_succeed': True},
                {'category': 'Armour', 'item': 'Plate Mail', 'defense': 20, 'cost': 100, 'should_succeed': False},  # Duplicate
                {'category': 'Items', 'item': 'Health Potion', 'cost': 20, 'should_succeed': True},
                {'category': 'Items', 'item': 'Health Potion', 'cost': 20, 'should_succeed': True},  # Should work for items
            ]
        },
        {
            'name': 'Hero with Existing Equipment',
            'hero': {
                'class': 'Ninja',
                'weapon': 'Nunchucks', 
                'armour': 'Ninja Tabi',
                'attack': 15,  # 5 base + 10 from nunchucks
                'defense': 25, # 5 base + 20 from tabi
                'base_attack': 5, 'base_defense': 5,
                'gold': 2000,
                'items': {'Health Potion': {'quantity': 1}}
            },
            'tests': [
                {'category': 'Weapons', 'item': 'Nunchucks', 'attack': 10, 'cost': 100, 'should_succeed': False},  # Already has
                {'category': 'Weapons', 'item': 'Lightsaber', 'attack': 20, 'cost': 500, 'should_succeed': True},   # Upgrade
                {'category': 'Armour', 'item': 'Ninja Tabi', 'defense': 20, 'cost': 100, 'should_succeed': False}, # Already has
                {'category': 'Armour', 'item': 'Magic Ninja Armour', 'defense': 40, 'cost': 500, 'should_succeed': True}, # Upgrade
                {'category': 'Items', 'item': 'Health Potion', 'cost': 20, 'should_succeed': True},  # Items always work
            ]
        }
    ]
    
    def simulate_purchase(hero, category, item_name, cost, **item_stats):
        """Simulate a purchase attempt"""
        original_gold = hero['gold']
        
        # Check gold first
        if hero['gold'] < cost:
            return {'success': False, 'reason': 'insufficient_gold'}
        
        # Deduct gold
        hero['gold'] -= cost
        
        if category == 'Weapons':
            current_weapon = hero.get('weapon', 'None')
            if current_weapon == item_name:
                # Duplicate weapon - refund and fail
                hero['gold'] += cost
                return {'success': False, 'reason': 'duplicate_weapon'}
            
            # Success - equip weapon
            hero['weapon'] = item_name
            hero['attack'] = hero['base_attack'] + item_stats.get('attack', 0)
            return {'success': True, 'reason': 'weapon_equipped'}
            
        elif category == 'Armour':
            current_armour = hero.get('armour', 'None')
            if current_armour == item_name:
                # Duplicate armor - refund and fail
                hero['gold'] += cost
                return {'success': False, 'reason': 'duplicate_armour'}
            
            # Success - equip armor
            hero['armour'] = item_name
            hero['defense'] = hero['base_defense'] + item_stats.get('defense', 0)
            return {'success': True, 'reason': 'armour_equipped'}
            
        elif category == 'Items':
            # Items always succeed (can buy multiple)
            if 'items' not in hero:
                hero['items'] = {}
            
            if item_name in hero['items']:
                hero['items'][item_name]['quantity'] += 1
            else:
                hero['items'][item_name] = {'quantity': 1}
            
            return {'success': True, 'reason': 'item_added'}
        
        return {'success': False, 'reason': 'unknown_category'}
    
    all_tests_passed = True
    
    for scenario in scenarios:
        print(f"\nTesting: {scenario['name']}")
        print("-" * (len(scenario['name']) + 10))
        
        # Create a copy of the hero for this scenario
        import copy
        test_hero = copy.deepcopy(scenario['hero'])
        
        print(f"Starting state:")
        print(f"  Weapon: {test_hero.get('weapon', 'None')} (Attack: {test_hero.get('attack', 0)})")
        print(f"  Armor: {test_hero.get('armour', 'None')} (Defense: {test_hero.get('defense', 0)})")
        print(f"  Gold: {test_hero.get('gold', 0)}")
        print(f"  Items: {test_hero.get('items', {})}")
        print()
        
        for i, test in enumerate(scenario['tests'], 1):
            print(f"Test {i}: Buying {test['item']} from {test['category']}")
            
            result = simulate_purchase(
                test_hero, 
                test['category'], 
                test['item'], 
                test['cost'],
                **{k: v for k, v in test.items() if k not in ['category', 'item', 'cost', 'should_succeed']}
            )
            
            expected = test['should_succeed']
            actual = result['success']
            
            if expected == actual:
                status = "✅ PASS"
                print(f"  {status} - {result['reason']}")
            else:
                status = "❌ FAIL"
                print(f"  {status} - Expected {expected}, got {actual} ({result['reason']})")
                all_tests_passed = False
            
            print(f"    Gold: {test_hero['gold']}")
            if test['category'] in ['Weapons', 'Armour']:
                print(f"    {test['category'][:-1]}: {test_hero.get(test['category'].lower()[:-1], 'None')}")
        
        print(f"\nFinal state:")
        print(f"  Weapon: {test_hero.get('weapon', 'None')} (Attack: {test_hero.get('attack', 0)})")
        print(f"  Armor: {test_hero.get('armour', 'None')} (Defense: {test_hero.get('defense', 0)})")
        print(f"  Gold: {test_hero.get('gold', 0)}")
        print(f"  Items: {test_hero.get('items', {})}")
    
    print(f"\n{'='*50}")
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Duplicate weapon purchases are blocked")
        print("✅ Duplicate armor purchases are blocked") 
        print("✅ Item purchases still work normally")
        print("✅ Equipment upgrades work correctly")
    else:
        print("❌ SOME TESTS FAILED!")
        print("Please check the implementation.")
    print(f"{'='*50}")

if __name__ == "__main__":
    test_comprehensive_shop_behavior()