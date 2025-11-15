"""
Test backward compatibility - loading old save files without art fields
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from gui_main import GameGUI
import yaml

def test_backward_compatibility():
    """Test that old saves without art fields get them restored from templates"""
    print("Testing backward compatibility with old save files...")
    
    root = tk.Tk()
    gui = GameGUI(root)
    
    # Wait for initialization to complete
    def run_tests():
        try:
            # Create a fake old save file (without art fields)
            print("\n1. Creating simulated old save file (missing art fields)...")
            old_save_data = {
                'hero': {
                    'name': 'Shadow Billy Bob',
                    'class': 'Ninja',
                    'level': 3,
                    'xp': 15,
                    'hp': 20,
                    'maxhp': 25,
                    'attack': 8,
                    'defense': 12,
                    'gold': 150,
                    'lives_left': 3,
                    'age': 16,
                    'weapon': 'Ninja Stars',
                    'armour': 'Students Robe',
                    'item': None,
                    'items': {},
                    'quests': [],
                    'completed_quests': []
                    # Note: No 'art', 'art_attack', 'art_death', or 'attack_sound' fields
                },
                'game_state': {
                    'current_biome': 'grassland',
                    'last_biome': 'grassland'
                },
                'save_metadata': {
                    'save_date': '2025-11-15T09:00:00',
                    'game_version': '1.0',
                    'save_name': 'test_old_save.yaml'
                }
            }
            
            # Save the old format file
            old_save_path = 'saves/test_old_save.yaml'
            with open(old_save_path, 'w', encoding='utf-8') as f:
                yaml.dump(old_save_data, f, default_flow_style=False, allow_unicode=True, indent=2)
            
            print(f"   ✓ Created old save: {old_save_path}")
            print("   - Missing: art, art_attack, art_death, attack_sound")
            
            # Load the old save file
            print("\n2. Loading old save file through save_load_manager...")
            load_result = gui.save_load_manager.load_game(old_save_path)
            assert load_result['success'], f"Load failed: {load_result.get('error')}"
            
            loaded_hero = load_result['hero']
            print(f"   ✓ Loaded hero: {loaded_hero['name']}")
            
            # Verify art fields were restored from template
            print("\n3. Verifying art fields were restored from hero template:")
            print(f"   art: {loaded_hero.get('art', 'MISSING')}")
            print(f"   art_attack: {loaded_hero.get('art_attack', 'MISSING')}")
            print(f"   art_death: {loaded_hero.get('art_death', 'MISSING')}")
            print(f"   attack_sound: {loaded_hero.get('attack_sound', 'MISSING')}")
            
            assert 'art' in loaded_hero, "Art field should be restored"
            assert loaded_hero['art'] == 'art/ninja_hero.png', f"Expected 'art/ninja_hero.png', got '{loaded_hero.get('art')}'"
            assert 'art_attack' in loaded_hero, "art_attack field should be restored"
            assert loaded_hero['art_attack'] == 'art/ninja_hero_attack.png', f"Expected 'art/ninja_hero_attack.png', got '{loaded_hero.get('art_attack')}'"
            assert 'art_death' in loaded_hero, "art_death field should be restored"
            assert loaded_hero['art_death'] == 'art/ninja_hero_death.png', f"Expected 'art/ninja_hero_death.png', got '{loaded_hero.get('art_death')}'"
            assert 'attack_sound' in loaded_hero, "attack_sound field should be restored"
            assert loaded_hero['attack_sound'] == 'ninja-attack.mp3', f"Expected 'ninja-attack.mp3', got '{loaded_hero.get('attack_sound')}'"
            
            # Verify other hero data was preserved
            assert loaded_hero['level'] == 3, f"Level should be 3, got {loaded_hero['level']}"
            assert loaded_hero['gold'] == 150, f"Gold should be 150, got {loaded_hero['gold']}"
            
            # Clean up test save file
            if os.path.exists(old_save_path):
                os.remove(old_save_path)
                print(f"\n4. Cleaned up test file: test_old_save.yaml")
            
            print("\n✅ Backward compatibility test passed!")
            print("\nExisting save files will work correctly:")
            print("- Old saves without art fields will have them restored from hero templates")
            print("- Art paths will be correctly matched to hero names")
            print("- All hero images will display properly after loading old saves")
            
            root.destroy()
        except Exception as e:
            print(f"\n❌ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
            root.destroy()
    
    # Wait for game to initialize, then run tests
    root.after(2000, run_tests)
    root.mainloop()

if __name__ == '__main__':
    test_backward_compatibility()
