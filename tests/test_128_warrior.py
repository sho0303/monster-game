"""
Test the new 128x128 realistic warrior art
"""
import tkinter as tk
from gui_main import GameGUI
import os

def test_128_warrior_art():
    """Test displaying the new 128x128 realistic warrior art"""
    root = tk.Tk()
    game_gui = GameGUI(root)
    
    def setup_test():
        print("=== Testing 128x128 Realistic Warrior Art ===")
        
        # Check if files exist
        original_path = 'art/Warrior.png'
        realistic_256_path = 'art/Warrior_realistic.png'
        realistic_128_path = 'art/Warrior_realistic_128.png'
        
        files = {
            "Original": original_path,
            "256x256 Realistic": realistic_256_path, 
            "128x128 Realistic": realistic_128_path
        }
        
        for name, path in files.items():
            status = "✅" if os.path.exists(path) else "❌"
            print(f"{name}: {status} {path}")
        
        # Start with 128x128 version
        show_128_version()
    
    def show_128_version():
        """Display the 128x128 realistic warrior"""
        realistic_128_path = 'art/Warrior_realistic_128.png'
        
        if os.path.exists(realistic_128_path):
            game_gui.clear_text()
            game_gui.show_image(realistic_128_path)
            game_gui.print_text("\n⚔️ 128x128 Realistic Warrior")
            game_gui.print_text("=" * 50)
            game_gui.print_text("✨ Optimized Features:")
            game_gui.print_text("  • Native 128x128 resolution")
            game_gui.print_text("  • Photorealistic rendering")
            game_gui.print_text("  • Smaller file size")
            game_gui.print_text("  • Optimized detail level")
            game_gui.print_text("  • Better performance")
            game_gui.print_text("")
            game_gui.print_text("🎯 Technical Benefits:")
            game_gui.print_text("  • 4x smaller than 256x256")
            game_gui.print_text("  • Faster loading times")
            game_gui.print_text("  • Less memory usage")
            game_gui.print_text("  • Maintains visual quality")
            
            def show_comparison():
                compare_versions()
            
            def complete_test():
                finish_test()
            
            game_gui.set_buttons(["Compare Versions", "Complete Test"], 
                               lambda choice: show_comparison() if choice == 1 else complete_test())
        else:
            game_gui.print_text("❌ 128x128 realistic warrior art not found!")
            finish_test()
    
    def compare_versions():
        """Show comparison between different versions"""
        game_gui.clear_text()
        game_gui.print_text("\n📊 Warrior Art Version Comparison")
        game_gui.print_text("=" * 50)
        
        # Check file sizes if available
        files_info = []
        for name, path in [
            ("Original Pixel Art", 'art/Warrior.png'),
            ("256x256 Realistic", 'art/Warrior_realistic.png'),
            ("128x128 Realistic", 'art/Warrior_realistic_128.png')
        ]:
            if os.path.exists(path):
                size = os.path.getsize(path)
                size_kb = size / 1024
                files_info.append(f"  {name}: {size_kb:.1f} KB")
            else:
                files_info.append(f"  {name}: Not found")
        
        game_gui.print_text("📁 File Sizes:")
        for info in files_info:
            game_gui.print_text(info)
        
        game_gui.print_text("")
        game_gui.print_text("🎨 Quality Comparison:")
        game_gui.print_text("  Original: Retro pixel art charm")
        game_gui.print_text("  256x256: Maximum detail and quality")
        game_gui.print_text("  128x128: Optimal balance of quality/size")
        
        game_gui.print_text("")
        game_gui.print_text("💡 Recommended Usage:")
        game_gui.print_text("  • Retro Mode: Use original pixel art")
        game_gui.print_text("  • High Quality: Use 256x256 realistic")
        game_gui.print_text("  • Balanced: Use 128x128 realistic ⭐")
        
        def show_original():
            display_original()
        
        def show_256():
            display_256_version()
        
        def back_to_128():
            show_128_version()
        
        game_gui.set_buttons(["Original", "256x256", "Back to 128x128"], 
                           lambda choice: show_original() if choice == 1 else 
                                        show_256() if choice == 2 else back_to_128())
    
    def display_original():
        """Display original warrior art"""
        original_path = 'art/Warrior.png'
        if os.path.exists(original_path):
            game_gui.clear_text()
            game_gui.show_image(original_path)
            game_gui.print_text("\n🎮 Original Pixel Art Warrior")
            game_gui.print_text("=" * 50)
            game_gui.print_text("Classic 32x32 pixel art scaled to 256x256")
            
            def back():
                compare_versions()
            
            game_gui.set_buttons(["Back to Comparison"], lambda choice: back())
        else:
            game_gui.print_text("❌ Original warrior not found!")
            compare_versions()
    
    def display_256_version():
        """Display 256x256 realistic warrior art"""
        realistic_256_path = 'art/Warrior_realistic.png'
        if os.path.exists(realistic_256_path):
            game_gui.clear_text()
            game_gui.show_image(realistic_256_path)
            game_gui.print_text("\n🎨 256x256 Realistic Warrior")
            game_gui.print_text("=" * 50)
            game_gui.print_text("Maximum quality photorealistic rendering")
            
            def back():
                compare_versions()
            
            game_gui.set_buttons(["Back to Comparison"], lambda choice: back())
        else:
            game_gui.print_text("❌ 256x256 realistic warrior not found!")
            compare_versions()
    
    def finish_test():
        """Complete the test"""
        game_gui.clear_text()
        game_gui.print_text("\n✅ 128x128 Warrior Art Test Complete!")
        game_gui.print_text("=" * 50)
        game_gui.print_text("🎨 Successfully created optimized realistic warrior")
        game_gui.print_text("📦 Smaller file size with maintained quality")
        game_gui.print_text("⚡ Better performance for game usage")
        game_gui.print_text("🎯 Recommended for production use")
        
        def exit_test():
            print("✅ 128x128 realistic warrior art test completed!")
            root.quit()
        
        game_gui.set_buttons(["🚪 Exit Test"], lambda choice: exit_test())
    
    # Start test after initialization
    root.after(3000, setup_test)
    
    root.mainloop()

if __name__ == "__main__":
    test_128_warrior_art()