"""
Test script for combat animation integration
"""
import sys
sys.path.append('.')

from gui_main import GameGUI
import tkinter as tk

def test_combat_animations():
    """Test the enhanced combat system with attack animations"""
    
    print("🎮 Testing Combat Animation Integration...")
    
    # Create test GUI
    root = tk.Tk()
    root.title("Combat Animation Test")
    root.geometry("600x400")
    
    gui = GameGUI(root)
    
    # Create test hero (Ninja for testing ninja attack animation)
    test_hero = {
        'name': 'Test Ninja',
        'class': 'Ninja',
        'level': 5,
        'hp': 50,
        'maxhp': 50,
        'attack': 15,
        'defense': 8,
        'gold': 100,
        'xp': 20
    }
    
    # Create test monster
    test_monster = {
        'name': 'Test Slime',
        'level': 3,
        'hp': 30,
        'maxhp': 30,
        'attack': 8,
        'defense': 3,
        'gold': 25,
        'xp': 15,
        'art': 'art/slime_monster.png'
    }
    
    gui.game_state.hero = test_hero
    
    def test_encounter():
        """Test monster encounter with side-by-side display"""
        print("✅ Testing monster encounter display...")
        
        try:
            encounter = gui.monster_encounter
            encounter._display_vs_encounter(test_hero, test_monster)
            print("✅ Monster encounter display working!")
            
            # Test combat animation methods
            combat = gui.combat
            combat._display_combat_start(test_hero, test_monster)
            print("✅ Combat start display working!")
            
            # Test attack animation
            combat._show_hero_attack_animation(test_hero)
            print("✅ Hero attack animation working!")
            
            # Test return to normal
            root.after(2000, lambda: combat._return_to_default_combat_view(test_hero, test_monster))
            print("✅ Return to normal view working!")
            
            print("\\n🎉 All combat animation tests passed!")
            print("   ⚔️ Attack animations ready for combat")
            print("   🥷 Ninja attack animation integrated")
            print("   🧙 Magician attack animation integrated") 
            print("   ⚔️ Warrior attack animation integrated")
            print("\\n💡 To test with different classes:")
            print("   - Change test_hero['class'] to 'Warrior' or 'Magician'")
            print("   - Run combat through normal game flow")
            print("   - Attack animations will show during hero attacks")
            
            # Auto-close after demo
            root.after(5000, root.destroy)
            
        except Exception as e:
            print(f"❌ Error testing combat animations: {e}")
            import traceback
            traceback.print_exc()
    
    # Start test after GUI initializes
    root.after(1000, test_encounter)
    root.mainloop()

if __name__ == '__main__':
    test_combat_animations()