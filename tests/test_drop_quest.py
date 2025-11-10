"""
Test script for the drop quest functionality
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui_quests import QuestManager, Quest

class MockGUI:
    """Mock GUI for testing"""
    def __init__(self):
        self.current_biome = 'grassland'
        
    class GameState:
        def __init__(self):
            self.monsters = {
                'Wolf': {'biome': 'grassland', 'xp': 5, 'hp': 10, 'attack': 3},
                'Bear': {'biome': 'grassland', 'xp': 8, 'hp': 15, 'attack': 5},
                'Goblin': {'biome': 'dungeon', 'xp': 3, 'hp': 8, 'attack': 2}
            }
            self.hero = {
                'name': 'Test Hero',
                'hp': 100,
                'xp': 0,
                'quests': []
            }
    
    def __init__(self):
        self.current_biome = 'grassland'
        self.game_state = self.GameState()

def test_drop_quest():
    """Test the drop quest functionality"""
    print("Testing Drop Quest Functionality")
    print("=" * 40)
    
    # Create mock GUI and quest manager
    gui = MockGUI()
    quest_manager = QuestManager(gui)
    hero = gui.game_state.hero
    
    # Initialize hero quests
    quest_manager.initialize_hero_quests(hero)
    
    # Create and add some test quests
    quest1 = Quest('kill_monster', 'Wolf', 5, 'Hunt a Wolf in the grasslands')
    quest2 = Quest('kill_monster', 'Bear', 8, 'Defeat a Bear in the grasslands')
    quest3 = Quest('kill_monster', 'Goblin', 3, 'Slay a Goblin in the dark dungeons')
    
    quest_manager.add_quest(hero, quest1)
    quest_manager.add_quest(hero, quest2)
    quest_manager.add_quest(hero, quest3)
    
    print(f"Added 3 quests. Total quests: {len(hero['quests'])}")
    
    # Display active quests
    active_quests = quest_manager.get_active_quests(hero)
    print(f"Active quests: {len(active_quests)}")
    for i, quest in enumerate(active_quests):
        print(f"  {i+1}. {quest.description} (Reward: {quest.reward_xp} XP)")
    
    # Test dropping quest at index 1 (Bear quest)
    print(f"\nDropping quest at index 1 (Bear quest)...")
    success = quest_manager.drop_quest(hero, 1)
    
    if success:
        print("✅ Quest dropped successfully!")
    else:
        print("❌ Failed to drop quest!")
    
    # Display remaining active quests
    active_quests = quest_manager.get_active_quests(hero)
    print(f"Remaining active quests: {len(active_quests)}")
    for i, quest in enumerate(active_quests):
        print(f"  {i+1}. {quest.description} (Reward: {quest.reward_xp} XP)")
    
    # Test dropping quest at invalid index
    print(f"\nTrying to drop quest at invalid index 10...")
    success = quest_manager.drop_quest(hero, 10)
    if not success:
        print("✅ Correctly rejected invalid index!")
    else:
        print("❌ Should have rejected invalid index!")
    
    # Test dropping all remaining quests
    print(f"\nDropping all remaining quests...")
    while True:
        active_quests = quest_manager.get_active_quests(hero)
        if not active_quests:
            break
        success = quest_manager.drop_quest(hero, 0)
        if not success:
            break
    
    active_quests = quest_manager.get_active_quests(hero)
    print(f"Final active quests: {len(active_quests)}")
    
    if len(active_quests) == 0:
        print("✅ All quests successfully dropped!")
    else:
        print("❌ Some quests remain!")
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_drop_quest()