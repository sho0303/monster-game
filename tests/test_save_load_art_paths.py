"""
Test that hero art paths are preserved through save/load cycles
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from gui_main import GameGUI

def test_save_load_art_paths():
    """Test that art paths are correctly saved and loaded"""
    print("Testing save/load art path preservation...")
    
    root = tk.Tk()
    gui = GameGUI(root)
    
    # Wait for initialization to complete
    def run_tests():
        try:
            # Select a hero
            gui.game_state.hero = gui.game_state.heros['Shadow Billy Bob'].copy()
            
            # Verify hero has art paths initially
            print(f"\n1. Initial hero art paths:")
            print(f"   art: {gui.game_state.hero.get('art', 'MISSING')}")
            print(f"   art_attack: {gui.game_state.hero.get('art_attack', 'MISSING')}")
            print(f"   art_death: {gui.game_state.hero.get('art_death', 'MISSING')}")
            print(f"   attack_sound: {gui.game_state.hero.get('attack_sound', 'MISSING')}")
            
            assert 'art' in gui.game_state.hero, "Hero should have 'art' field"
            assert gui.game_state.hero['art'] == 'art/ninja_hero.png', f"Expected 'art/ninja_hero.png', got '{gui.game_state.hero['art']}'"
            
            # Modify hero to have some game progress
            gui.game_state.hero['level'] = 5
            gui.game_state.hero['gold'] = 250
            gui.game_state.hero['hp'] = 25
            gui.game_state.hero['maxhp'] = 30
            
            # Save the game
            print("\n2. Saving game...")
            result = gui.save_load_manager.save_game(gui.game_state.hero, 'grassland', 'test_art_paths')
            assert result['success'], f"Save failed: {result.get('error')}"
            print(f"   ✓ Saved to: {result['filename']}")
            
            # Load the YAML file and verify art paths were saved
            import yaml
            with open(result['path'], 'r', encoding='utf-8') as f:
                save_data = yaml.safe_load(f)
            
            print("\n3. Checking saved YAML file:")
            hero_data = save_data['hero']
            print(f"   art: {hero_data.get('art', 'NOT SAVED')}")
            print(f"   art_attack: {hero_data.get('art_attack', 'NOT SAVED')}")
            print(f"   art_death: {hero_data.get('art_death', 'NOT SAVED')}")
            print(f"   attack_sound: {hero_data.get('attack_sound', 'NOT SAVED')}")
            
            assert 'art' in hero_data, "Art field should be saved in YAML"
            assert hero_data['art'] == 'art/ninja_hero.png', f"Art path should be 'art/ninja_hero.png', got '{hero_data.get('art')}'"
            
            # Clear current hero
            gui.game_state.hero = {}
            
            # Load the game
            print("\n4. Loading game from save file...")
            load_result = gui.save_load_manager.load_game(result['path'])
            assert load_result['success'], f"Load failed: {load_result.get('error')}"
            
            loaded_hero = load_result['hero']
            print(f"   ✓ Loaded hero: {loaded_hero['name']}")
            
            # Verify art paths were restored
            print("\n5. Checking loaded hero art paths:")
            print(f"   art: {loaded_hero.get('art', 'MISSING')}")
            print(f"   art_attack: {loaded_hero.get('art_attack', 'MISSING')}")
            print(f"   art_death: {loaded_hero.get('art_death', 'MISSING')}")
            print(f"   attack_sound: {loaded_hero.get('attack_sound', 'MISSING')}")
            
            assert 'art' in loaded_hero, "Loaded hero should have 'art' field"
            assert loaded_hero['art'] == 'art/ninja_hero.png', f"Loaded art path should be 'art/ninja_hero.png', got '{loaded_hero.get('art')}'"
            assert 'art_attack' in loaded_hero, "Loaded hero should have 'art_attack' field"
            assert 'art_death' in loaded_hero, "Loaded hero should have 'art_death' field"
            assert 'attack_sound' in loaded_hero, "Loaded hero should have 'attack_sound' field"
            
            # Verify game progress was also preserved
            assert loaded_hero['level'] == 5, f"Level should be 5, got {loaded_hero['level']}"
            assert loaded_hero['gold'] == 250, f"Gold should be 250, got {loaded_hero['gold']}"
            
            # Clean up test save file
            import os
            if os.path.exists(result['path']):
                os.remove(result['path'])
                print(f"\n6. Cleaned up test file: {result['filename']}")
            
            print("\n✅ All tests passed! Art paths are correctly preserved through save/load.")
            print("\nThe bug is fixed:")
            print("- Art paths are now saved in the YAML file")
            print("- Art paths are correctly restored when loading")
            print("- Heroes loaded from saves will display images correctly")
            
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
    test_save_load_art_paths()
