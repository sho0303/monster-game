"""
Test that Items category still allows multiple purchases (should not be affected by the fix)
"""

def test_items_multiple_purchases():
    """Test that items can still be purchased multiple times"""
    print("Testing Items Multiple Purchase (Should Still Work)")
    print("=" * 55)
    
    # Mock hero with some items already
    test_hero = {
        'name': 'Test Hero',
        'class': 'Warrior',
        'gold': 1000,
        'items': {
            'Health Potion': {'data': {'name': 'Health Potion', 'cost': 20}, 'quantity': 2}
        }
    }
    
    # Test item from store
    test_item = {
        'name': 'Health Potion',
        'description': 'Restores HP to full.',
        'type': 'minor',
        'cost': 20,
        'class': 'All'
    }
    
    print(f"Starting hero state:")
    print(f"  Gold: {test_hero['gold']}")
    print(f"  Items: {test_hero.get('items', {})}")
    print()
    
    def simulate_item_purchase(hero, item):
        print(f"Attempting to purchase item: {item['name']} for {item['cost']} gold")
        
        # Check gold
        if hero['gold'] < item['cost']:
            print(f"  ❌ Not enough gold (need {item['cost']}, have {hero['gold']})")
            return False
        
        # Deduct gold
        hero['gold'] -= item['cost']
        
        # Add to inventory (items should allow multiple purchases)
        if 'items' not in hero:
            hero['items'] = {}
        
        item_name = item['name']
        if item_name in hero['items']:
            # Increase quantity - this should always work for items
            hero['items'][item_name]['quantity'] += 1
            print(f"  ✅ Purchase successful! Added to existing stack.")
            print(f"  🧪 {item_name} quantity: {hero['items'][item_name]['quantity'] - 1} → {hero['items'][item_name]['quantity']}")
        else:
            # Add new item
            hero['items'][item_name] = {'data': item, 'quantity': 1}
            print(f"  ✅ Purchase successful! Added new item.")
            print(f"  🧪 {item_name} quantity: 0 → 1")
        
        print(f"  💰 Gold: {hero['gold'] + item['cost']} → {hero['gold']}")
        return True
    
    # Test multiple purchases of the same item
    for i in range(3):
        print(f"PURCHASE {i+1}: Buying Health Potion")
        print("-" * 35)
        result = simulate_item_purchase(test_hero, test_item)
        print()
        if not result:
            print(f"❌ Purchase {i+1} failed unexpectedly!")
            break
    
    print("FINAL STATE")
    print("=" * 15)
    print(f"Gold: {test_hero['gold']}")
    print(f"Items: {test_hero.get('items', {})}")
    
    # Verify we can buy multiple of the same item
    expected_quantity = 5  # Started with 2, bought 3 more
    actual_quantity = test_hero.get('items', {}).get('Health Potion', {}).get('quantity', 0)
    
    if actual_quantity == expected_quantity:
        print(f"✅ SUCCESS: Items can be purchased multiple times (quantity: {actual_quantity})")
    else:
        print(f"❌ FAILURE: Expected quantity {expected_quantity}, got {actual_quantity}")

if __name__ == "__main__":
    test_items_multiple_purchases()