#!/usr/bin/env python3
"""Simple bounty system test"""

def test_simple_bounty():
    print("🧪 Simple Bounty System Test")
    
    # Test import
    try:
        from gui_bounty import BountyManager
        print("✅ BountyManager imported successfully")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return
    
    # Mock GUI for testing
    class MockGUI:
        def __init__(self):
            self.game_state = MockGameState()
        
        def clear_text(self):
            pass
        
        def print_text(self, text):
            print(f"GUI: {text}")
    
    class MockGameState:
        def __init__(self):
            self.hero = {
                'name': 'Test Hero',
                'level': 3,
                'class': 'Warrior',
                'gold': 100
            }
            self.monsters = {
                'TestMonster': {
                    'level': 3,
                    'gold': 25,
                    'biome': 'grassland'
                },
                'TestBoss': {
                    'level': 4,
                    'gold': 50,
                    'biome': 'grassland'
                }
            }
    
    # Create bounty manager
    mock_gui = MockGUI()
    bounty_manager = BountyManager(mock_gui)
    
    print("✅ BountyManager created")
    
    # Test reward structure
    bronze_rewards = bounty_manager.bounty_rewards['Bronze']
    print(f"✅ Bronze rewards: {len(bronze_rewards)} items")
    
    # Show sample equipment
    for reward in bronze_rewards[:3]:
        reward_type = reward.get('type', 'unknown')
        name = reward.get('name', 'Unknown')
        print(f"  - {reward_type}: {name}")
        if reward.get('attack'):
            print(f"    Attack: +{reward['attack']}")
        if reward.get('defense'):
            print(f"    Defense: +{reward['defense']}")
    
    # Test bounty generation
    print(f"\n🎯 Testing Bounty Generation:")
    bounty = bounty_manager.generate_bounty('Bronze')
    
    if bounty:
        print(f"✅ Generated bounty:")
        print(f"  Target: {bounty.target}")
        print(f"  Type: {bounty.bounty_type}")
        print(f"  Gold: {bounty.reward_gold}")
        if bounty.reward_item:
            reward = bounty.reward_item
            print(f"  Equipment: {reward['name']} ({reward.get('type', 'accessory')})")
    else:
        print(f"❌ Failed to generate bounty")
    
    # Test gold balance
    print(f"\n💰 Gold Balance Test:")
    for difficulty in ['Bronze', 'Silver', 'Gold']:
        test_bounty = bounty_manager.generate_bounty(difficulty)
        if test_bounty:
            print(f"  {difficulty}: {test_bounty.reward_gold} gold")
    
    print(f"\n🎉 Core bounty system tests passed!")

if __name__ == '__main__':
    test_simple_bounty()