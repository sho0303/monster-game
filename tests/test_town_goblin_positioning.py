#!/usr/bin/env python3
"""
Test that the goblin assault positioning works correctly with the new town background
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from gui_main import GameGUI

def test_town_goblin_positioning():
    """Test goblin assault with new floor positioning"""
    print("🧪 Testing Town Goblin Assault Positioning")
    print("=" * 60)
    
    root = tk.Tk()
    try:
        game_gui = GameGUI(root)
        
        def setup_test():
            if not (game_gui.game_state and game_gui.town):
                root.after(100, setup_test)
                return
            
            print("✅ Game systems initialized")
            
            # Setup hero
            hero_name = list(game_gui.game_state.heros.keys())[0]
            game_gui.game_state.hero = game_gui.game_state.heros[hero_name].copy()
            game_gui.game_state.hero['name'] = hero_name
            game_gui.game_state.hero['lives_left'] = 3
            game_gui.game_state.hero['gold'] = 100
            game_gui.game_state.hero['level'] = 1
            game_gui.game_state.hero['xp'] = 0
            
            print(f"✅ Hero setup: {hero_name}")
            
            # Check floor offset configuration
            print("\n🏗️ Checking biome floor offsets:")
            for biome_name in ['grassland', 'desert', 'dungeon', 'ocean', 'town']:
                offset = game_gui.background_manager.get_floor_offset(biome_name)
                print(f"   {biome_name}: {offset}px offset")
            
            # Force goblin assault by calling it directly
            print("\n⚔️ Forcing goblin assault encounter...")
            game_gui.set_town_background()  # Set town background first
            game_gui.town._goblin_assault()
            
            print("\n✓ Goblin assault triggered!")
            print("📊 Visual check: Goblins should be positioned on the cobblestone floor")
            print("   (not floating above it)")
            
        # Start test after initialization
        root.after(100, setup_test)
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        root.destroy()

if __name__ == '__main__':
    test_town_goblin_positioning()
