"""
Quick test of the save/load system
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui_save_load import SaveLoadManager
from game_state import initialize_game_state
import yaml

def test_save_load_system():
    """Test the save/load functionality"""
    print("🧪 Testing Save/Load System...")
    
    # Create a mock GUI object for testing
    class MockGUI:
        def __init__(self):
            self.current_biome = 'desert'
            self.game_state = initialize_game_state()
    
    mock_gui = MockGUI()
    save_manager = SaveLoadManager(mock_gui)
    
    # Create a test hero with some progress
    test_hero = {
        'name': 'Test Warrior',
        'class': 'Warrior', 
        'level': 5,
        'xp': 18,
        'hp': 30,
        'maxhp': 35,
        'attack': 15,
        'defense': 12,
        'gold': 250,
        'lives_left': 2,
        'age': 28,
        'weapon': 'Steel Sword',
        'armour': 'Chain Mail',
        'item': {
            'name': 'Health Potion',
            'effect': 'restore_hp',
            'amount': 15
        },
        'quests': [
            {
                'quest_type': 'kill_monster',
                'target': 'Cyclops',
                'description': 'Defeat the mighty Cyclops in the desert',
                'reward_xp': 15,
                'completed': False,
                'status': 'active'
            }
        ]
    }
    
    print("📄 Test Hero Created:")
    print(f"   Name: {test_hero['name']} (Level {test_hero['level']})")
    print(f"   Location: {mock_gui.current_biome}")
    print(f"   Gold: {test_hero['gold']}")
    print(f"   Quests: {len(test_hero['quests'])}")
    
    # Test save
    print("\n💾 Testing Save...")
    save_result = save_manager.save_game(test_hero, mock_gui.current_biome, "test_save")
    
    if save_result['success']:
        print(f"✅ Save successful: {save_result['filename']}")
        
        # Check the saved file
        with open(save_result['path'], 'r') as f:
            saved_data = yaml.safe_load(f)
        
        print("📋 Saved data structure:")
        print(f"   Hero name: {saved_data['hero']['name']}")
        print(f"   Hero level: {saved_data['hero']['level']}")
        print(f"   Current biome: {saved_data['game_state']['current_biome']}")
        print(f"   Save date: {saved_data['save_metadata']['save_date'][:19]}")
        
        # Test load
        print("\n📁 Testing Load...")
        load_result = save_manager.load_game(save_result['path'])
        
        if load_result['success']:
            print("✅ Load successful!")
            loaded_hero = load_result['hero']
            
            print("🔍 Verifying loaded data:")
            print(f"   Name: {loaded_hero['name']} ✓" if loaded_hero['name'] == test_hero['name'] else f"   Name: {loaded_hero['name']} ❌")
            print(f"   Level: {loaded_hero['level']} ✓" if loaded_hero['level'] == test_hero['level'] else f"   Level: {loaded_hero['level']} ❌")
            print(f"   Gold: {loaded_hero['gold']} ✓" if loaded_hero['gold'] == test_hero['gold'] else f"   Gold: {loaded_hero['gold']} ❌")
            print(f"   Biome: {load_result['current_biome']} ✓" if load_result['current_biome'] == mock_gui.current_biome else f"   Biome: {load_result['current_biome']} ❌")
            
            # Check quests
            if len(loaded_hero['quests']) == len(test_hero['quests']):
                print(f"   Quests: {len(loaded_hero['quests'])} ✅")
            else:
                print(f"   Quests: {len(loaded_hero['quests'])} vs {len(test_hero['quests'])} ❌")
            
            print("\n🎉 Save/Load system test completed successfully!")
            
        else:
            print(f"❌ Load failed: {load_result['error']}")
    else:
        print(f"❌ Save failed: {save_result['error']}")
    
    # Test get available saves
    print("\n📂 Testing Save File Detection...")
    available_saves = save_manager.get_available_saves()
    print(f"Found {len(available_saves)} save file(s):")
    for save_info in available_saves:
        print(f"   - {save_info['hero_name']} (L{save_info['level']}) - {save_info['filename']}")

if __name__ == "__main__":
    test_save_load_system()