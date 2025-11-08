"""
Demo showing enhanced button system with more than 3 buttons
Demonstrates the new variable button capability
"""
import tkinter as tk
from gui_main import GameGUI
from game_state import initialize_game_state

def demo_enhanced_buttons():
    """Demo enhanced button system"""
    root = tk.Tk()
    game_gui = GameGUI(root)
    
    def setup_demo():
        # Initialize game state for demo
        if not game_gui.game_state.hero or 'lives_left' not in game_gui.game_state.hero:
            hero_name = list(game_gui.game_state.heros.keys())[0]
            game_gui.game_state.hero = game_gui.game_state.heros[hero_name].copy()
            game_gui.game_state.hero['name'] = hero_name
            game_gui.game_state.hero['lives_left'] = 3
            game_gui.game_state.hero['gold'] = 50
            game_gui.game_state.hero['level'] = 1
            game_gui.game_state.hero['xp'] = 0
        
        show_enhanced_menu()
    
    def show_enhanced_menu():
        """Show enhanced main menu with more options"""
        game_gui.clear_text()
        game_gui.show_image(f"art/{game_gui.game_state.hero['class']}.png")
        
        game_gui.print_text("\n" + "=" * 60)
        game_gui.print_text("🎮  ENHANCED PYQUEST MENU  🎮")
        game_gui.print_text("=" * 60)
        game_gui.print_text("Now supporting variable button counts!")
        game_gui.print_text("Choose from the expanded options below:")
        
        def on_enhanced_menu_select(choice):
            if choice == 1:
                show_shop_demo()
            elif choice == 2:
                show_combat_demo()
            elif choice == 3:
                show_inventory_demo()
            elif choice == 4:
                show_stats_demo()
            elif choice == 5:
                show_settings_demo()
            elif choice == 6:
                show_help_demo()
        
        # Enhanced menu with 6 buttons!
        game_gui.set_buttons([
            "🛒 Shop",
            "⚔️ Fight Monster", 
            "🧪 Use Item",
            "📊 Hero Stats",
            "⚙️ Settings",
            "❓ Help"
        ], on_enhanced_menu_select)
    
    def show_shop_demo():
        """Demo shop with variable buttons"""
        game_gui.clear_text()
        game_gui.print_text("\n🛒 Enhanced Shop Demo")
        game_gui.print_text("Multiple item categories:")
        
        def on_shop_choice(choice):
            categories = ["Weapons", "Armor", "Potions", "Accessories", "Rare Items"]
            if choice <= len(categories):
                game_gui.print_text(f"\n✓ Selected: {categories[choice-1]}")
                root.after(2000, show_enhanced_menu)
        
        game_gui.set_buttons([
            "⚔️ Weapons",
            "🛡️ Armor", 
            "🧪 Potions",
            "💎 Accessories",
            "✨ Rare Items"
        ], on_shop_choice)
    
    def show_combat_demo():
        """Demo combat with more action options"""
        game_gui.clear_text()
        game_gui.print_text("\n⚔️ Enhanced Combat Demo")
        game_gui.print_text("More tactical options available:")
        
        def on_combat_choice(choice):
            actions = ["Attack", "Defend", "Use Item", "Special Ability", "Run Away"]
            if choice <= len(actions):
                game_gui.print_text(f"\n💥 Used: {actions[choice-1]}")
                root.after(2000, show_enhanced_menu)
        
        game_gui.set_buttons([
            "⚔️ Attack",
            "🛡️ Defend",
            "🧪 Use Item", 
            "✨ Special Ability",
            "🏃 Run Away"
        ], on_combat_choice)
    
    def show_inventory_demo():
        """Demo inventory with item management"""
        game_gui.clear_text()
        game_gui.print_text("\n🎒 Enhanced Inventory Demo")
        game_gui.print_text("Advanced inventory management:")
        
        def on_inventory_choice(choice):
            actions = ["Use Item", "Equip Item", "Drop Item", "Sort Items"]
            if choice <= len(actions):
                game_gui.print_text(f"\n📦 Action: {actions[choice-1]}")
                root.after(2000, show_enhanced_menu)
        
        game_gui.set_buttons([
            "🧪 Use Item",
            "⚙️ Equip Item",
            "🗑️ Drop Item",
            "📊 Sort Items"
        ], on_inventory_choice)
    
    def show_stats_demo():
        """Demo stats with detailed breakdown"""
        game_gui.clear_text()
        game_gui.print_text("\n📊 Enhanced Stats Demo")
        game_gui.print_text("Detailed character information:")
        
        for key, value in game_gui.game_state.hero.items():
            if key in ['hp', 'maxhp']:
                game_gui.print_colored_value(f"  {key}: ", value, 'hp')
            elif key == 'attack':
                game_gui.print_colored_value(f"  {key}: ", value, 'attack')
            elif key == 'defense':
                game_gui.print_colored_value(f"  {key}: ", value, 'defense')
            elif key == 'level':
                game_gui.print_colored_value(f"  {key}: ", value, 'level')
            elif key == 'gold':
                game_gui.print_colored_value(f"  {key}: ", value, 'gold')
            else:
                game_gui.print_text(f"  {key}: {value}")
        
        def on_stats_choice(choice):
            game_gui.print_text("\n📈 Stats viewed!")
            root.after(2000, show_enhanced_menu)
        
        game_gui.set_buttons(["🔙 Back to Menu"], on_stats_choice)
    
    def show_settings_demo():
        """Demo settings panel"""
        game_gui.clear_text()
        game_gui.print_text("\n⚙️ Settings Demo")
        game_gui.print_text("Game configuration options:")
        
        def on_setting_choice(choice):
            settings = ["Audio Volume", "Display Mode", "Controls", "Difficulty"]
            if choice <= len(settings):
                game_gui.print_text(f"\n⚙️ Changed: {settings[choice-1]}")
                root.after(2000, show_enhanced_menu)
        
        game_gui.set_buttons([
            "🔊 Audio",
            "🖥️ Display",
            "🎮 Controls",
            "⚡ Difficulty"
        ], on_setting_choice)
    
    def show_help_demo():
        """Demo help system"""
        game_gui.clear_text()
        game_gui.print_text("\n❓ Help System Demo")
        game_gui.print_text("Get assistance with:")
        
        def on_help_choice(choice):
            topics = ["Combat", "Items", "Keyboard Shortcuts"]
            if choice <= len(topics):
                game_gui.print_text(f"\n📖 Help topic: {topics[choice-1]}")
                root.after(2000, show_enhanced_menu)
        
        game_gui.set_buttons([
            "⚔️ Combat Help",
            "🧪 Items Help", 
            "⌨️ Keyboard Shortcuts"
        ], on_help_choice)
    
    # Wait for initialization, then start demo
    root.after(3000, setup_demo)
    
    root.mainloop()

if __name__ == "__main__":
    demo_enhanced_buttons()