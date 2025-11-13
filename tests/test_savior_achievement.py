"""
Test the Savior of Monster World achievement
Verifies that defeating the final boss triggers the achievement
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gui_achievements import AchievementManager
from game_state import GameState
import yaml

def test_savior_achievement():
    """Test that the Savior of Monster World achievement exists and triggers correctly"""
    
    print("=" * 60)
    print("Testing Savior of Monster World Achievement")
    print("=" * 60)
    
    # Initialize game state and achievement manager
    from game_state import initialize_game_state
    game_state = initialize_game_state()
    
    achievement_manager = AchievementManager(game_state=game_state)
    
    # Check that the achievement exists
    print("\n1. Checking if achievement exists...")
    savior_achievement = achievement_manager.achievements.get("savior_of_monster_world")
    
    if savior_achievement:
        print("   ✅ Achievement found!")
        print(f"   Name: {savior_achievement.name}")
        print(f"   Description: {savior_achievement.description}")
        print(f"   Category: {savior_achievement.category}")
        print(f"   Hidden: {savior_achievement.hidden}")
        print(f"   Reward Type: {savior_achievement.reward_type}")
    else:
        print("   ❌ Achievement not found!")
        return
    
    # Load Dragon data to verify final boss flag
    print("\n2. Checking Dragon final boss flag...")
    dragon_path = 'monsters/Dragon.yaml'
    if os.path.exists(dragon_path):
        with open(dragon_path, 'r') as f:
            dragon_data = yaml.safe_load(f)
            dragon = dragon_data.get('Dragon', {})
            is_final_boss = dragon.get('finalboss', False)
            print(f"   Dragon finalboss flag: {is_final_boss}")
            if is_final_boss:
                print("   ✅ Dragon is correctly marked as final boss")
            else:
                print("   ❌ Dragon is NOT marked as final boss")
    
    # Test achievement tracking
    print("\n3. Testing achievement tracking...")
    print(f"   Initial progress: {savior_achievement.current_progress}/{savior_achievement.target_value}")
    print(f"   Initial completed: {savior_achievement.completed}")
    
    # Simulate defeating the final boss
    print("\n4. Simulating final boss defeat...")
    achievement_manager.track_monster_defeat(
        monster_name="Dragon Nightmare",
        biome="dungeon",
        is_final_boss=True
    )
    
    # Check if achievement was completed
    savior_achievement = achievement_manager.achievements.get("savior_of_monster_world")
    print(f"   Final progress: {savior_achievement.current_progress}/{savior_achievement.target_value}")
    print(f"   Completed: {savior_achievement.completed}")
    
    if savior_achievement.completed:
        print("\n   ✅ SUCCESS! Achievement unlocked when defeating final boss!")
        if savior_achievement.completed_at:
            print(f"   Completed at: {savior_achievement.completed_at}")
    else:
        print("\n   ❌ FAILED! Achievement not completed")
    
    # Test that regular monsters don't trigger it
    print("\n5. Testing that regular monsters don't trigger achievement...")
    achievement_manager2 = AchievementManager(game_state=game_state)
    achievement_manager2.track_monster_defeat(
        monster_name="Goblin",
        biome="grassland",
        is_final_boss=False
    )
    
    regular_check = achievement_manager2.achievements.get("savior_of_monster_world")
    if not regular_check.completed:
        print("   ✅ Correct! Regular monsters don't trigger the achievement")
    else:
        print("   ❌ Error! Regular monster triggered the achievement")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)

if __name__ == '__main__':
    test_savior_achievement()
