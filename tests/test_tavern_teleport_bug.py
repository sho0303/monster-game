"""
Test script to verify that accepting tavern quests doesn't break teleportation
"""
import tkinter as tk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui_main import GameGUI


def test_tavern_teleport_bug():
    """Test that accepting a quest from tavern doesn't break teleportation"""
    root = tk.Tk()
    root.withdraw()  # Hide the window for testing
    
    try:
        gui = GameGUI(root)
        # Let the initialization complete
        root.update()
        
        # Wait for game initialization to complete
        gui.initialize_game()
        root.update()
        
        # Setup test hero (modify existing hero)
        gui.game_state.hero.update({
            'name': 'TestHero',
            'level': 10,  # High level to unlock all biomes
            'hp': 50,
            'maxhp': 50,
            'attack': 25,
            'defense': 15,
            'gold': 1000,  # Give plenty of gold
            'xp': 100,
            'class': 'Warrior',
            'weapon': 'Test Sword',
            'armour': 'Test Armor'
        })
        
        print("✅ Test setup complete")
        print(f"Hero: {gui.game_state.hero['name']}")
        print(f"Gold: {gui.game_state.hero['gold']}")
        
        # Test 1: Visit tavern
        print("\n🍺 Testing tavern visit...")
        gui.town.enter_town()
        root.update()
        
        # Manually trigger an NPC encounter (simulate accepting a quest)
        print("\n🤝 Simulating NPC encounter and quest acceptance...")
        gui.town._accept_side_quest("merchant_caravan", 200, "desert")
        root.update()
        
        print("✅ Quest accepted successfully")
        
        # Check if side quests were added
        if 'side_quests' in gui.game_state.hero:
            print(f"📜 Side quests: {len(gui.game_state.hero['side_quests'])}")
            for quest in gui.game_state.hero['side_quests']:
                print(f"   - {quest['name']} ({quest['target_biome']})")
        
        # Test 2: Try teleportation after quest acceptance
        print("\n🌀 Testing teleportation after quest acceptance...")
        try:
            # Check if interface is locked (this was the bug)
            interface_locked = hasattr(gui, '_interface_locked') and gui._interface_locked
            print(f"Interface locked: {interface_locked}")
            
            if interface_locked:
                print("❌ BUG: Interface is still locked after quest acceptance!")
                return False
            else:
                print("✅ Interface is properly unlocked")
            
            # Try to teleport multiple times to ensure it works
            original_biome = gui.background_manager.current_biome
            print(f"Current biome: {original_biome}")
            
            teleports_successful = 0
            teleports_attempted = 5
            
            for attempt in range(teleports_attempted):
                try:
                    print(f"  Teleport attempt {attempt + 1}...")
                    
                    # Check hero's available biomes
                    available_biomes = gui.quest_manager.get_available_biomes_for_hero(gui.game_state.hero)
                    print(f"    Available biomes: {available_biomes}")
                    
                    gui.teleport_to_random_biome()
                    
                    # Process any pending events (including animations)
                    for i in range(10):  # Give more time for teleport processing
                        root.update()
                        
                    new_biome = gui.background_manager.current_biome
                    print(f"    Result: {original_biome} -> {new_biome}")
                    
                    if new_biome != original_biome:
                        teleports_successful += 1
                        original_biome = new_biome  # Update for next attempt
                        
                except Exception as e:
                    print(f"    ❌ Teleport attempt {attempt + 1} failed: {e}")
                    return False
            
            print(f"Successful teleports: {teleports_successful}/{teleports_attempted}")
            
            if teleports_successful > 0:
                print("✅ Teleportation works correctly after quest acceptance!")
                return True
            else:
                print("❌ Teleportation failed all attempts")
                return False
                
        except Exception as e:
            print(f"❌ Error during teleportation test: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        root.quit()
        root.destroy()


if __name__ == '__main__':
    print("🧪 Testing Tavern Teleport Bug Fix")
    print("=" * 50)
    
    success = test_tavern_teleport_bug()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 TEST PASSED: Teleportation works after quest acceptance!")
    else:
        print("💥 TEST FAILED: Bug still exists!")
    
    print("=" * 50)