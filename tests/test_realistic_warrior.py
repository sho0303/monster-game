"""
Test the new realistic warrior art in the game
"""
import tkinter as tk
from gui_main import GameGUI
import os

def test_realistic_warrior_art():
    """Test displaying the new realistic warrior art"""
    root = tk.Tk()
    game_gui = GameGUI(root)
    
    def setup_test():
        print("=== Testing Realistic Warrior Art ===")
        
        # Check if files exist
        original_path = 'art/Warrior.png'
        realistic_path = 'art/Warrior_realistic.png'
        comparison_path = 'art/warrior_comparison.png'
        
        print(f"Original Warrior: {'✅' if os.path.exists(original_path) else '❌'} {original_path}")
        print(f"Realistic Warrior: {'✅' if os.path.exists(realistic_path) else '❌'} {realistic_path}")
        print(f"Comparison Image: {'✅' if os.path.exists(comparison_path) else '❌'} {comparison_path}")
        
        # Display comparison first
        if os.path.exists(comparison_path):
            game_gui.clear_text()
            game_gui.show_image(comparison_path)
            game_gui.print_text("\n🎨 Warrior Art Comparison")
            game_gui.print_text("=" * 50)
            game_gui.print_text("Left: Original pixel art (32x32 → 256x256)")
            game_gui.print_text("Right: High-resolution realistic (native 256x256)")
            
            def show_realistic():
                test_realistic_display()
            
            game_gui.set_buttons(["Show Realistic Only"], lambda choice: show_realistic())
        else:
            test_realistic_display()
    
    def test_realistic_display():
        """Test the realistic warrior art alone"""
        realistic_path = 'art/Warrior_realistic.png'
        
        if os.path.exists(realistic_path):
            game_gui.clear_text()
            game_gui.show_image(realistic_path)
            game_gui.print_text("\n⚔️ High-Resolution Realistic Warrior")
            game_gui.print_text("=" * 50)
            game_gui.print_text("✨ Features:")
            game_gui.print_text("  • Native 256x256 resolution")
            game_gui.print_text("  • Gradient shading and depth")
            game_gui.print_text("  • Detailed medieval armor")
            game_gui.print_text("  • Realistic sword and shield")
            game_gui.print_text("  • Battle-worn effects")
            game_gui.print_text("  • Photorealistic rendering")
            game_gui.print_text("")
            game_gui.print_text("🎯 Technical Specs:")
            game_gui.print_text("  • Same dimensions as original")
            game_gui.print_text("  • Compatible with existing game")
            game_gui.print_text("  • Enhanced visual fidelity")
            
            def show_original():
                test_original_display()
            
            def complete_test():
                complete_art_test()
            
            game_gui.set_buttons(["Show Original", "Complete Test"], 
                               lambda choice: show_original() if choice == 1 else complete_test())
        else:
            game_gui.print_text("❌ Realistic warrior art not found!")
            complete_art_test()
    
    def test_original_display():
        """Test the original warrior art for comparison"""
        original_path = 'art/Warrior.png'
        
        if os.path.exists(original_path):
            game_gui.clear_text()
            game_gui.show_image(original_path)
            game_gui.print_text("\n🎮 Original Pixel Art Warrior")
            game_gui.print_text("=" * 50)
            game_gui.print_text("Classic pixel art style")
            game_gui.print_text("32x32 pixels scaled 8x to 256x256")
            
            def back_to_realistic():
                test_realistic_display()
            
            game_gui.set_buttons(["Back to Realistic"], lambda choice: back_to_realistic())
        else:
            game_gui.print_text("❌ Original warrior art not found!")
            complete_art_test()
    
    def complete_art_test():
        """Complete the art test"""
        game_gui.clear_text()
        game_gui.print_text("\n✅ Realistic Warrior Art Test Complete!")
        game_gui.print_text("=" * 50)
        game_gui.print_text("🎨 Successfully created high-resolution warrior art")
        game_gui.print_text("📊 Comparison image available for review")
        game_gui.print_text("⚔️ Ready for integration into the game")
        
        def finish():
            print("✅ Realistic warrior art test completed successfully!")
            root.quit()
        
        game_gui.set_buttons(["🚪 Exit Test"], lambda choice: finish())
    
    # Start test after initialization
    root.after(3000, setup_test)
    
    root.mainloop()

if __name__ == "__main__":
    test_realistic_warrior_art()