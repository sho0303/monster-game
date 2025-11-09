"""
Inventory system for GUI
"""


class InventoryGUI:
    """Inventory system for GUI"""
    def __init__(self, gui):
        self.gui = gui
    
    def use_item(self):
        """Show inventory and allow player to choose which item to use"""
        hero = self.gui.game_state.hero
        
        # Migrate old single item system to new multi-item system
        if 'item' in hero and hero['item'] is not None:
            if 'items' not in hero:
                hero['items'] = {}
            old_item = hero['item']
            item_name = old_item['name']
            hero['items'][item_name] = {'data': old_item, 'quantity': 1}
            del hero['item']
        
        # Check if hero has any items
        if 'items' not in hero or not hero['items']:
            self.gui.print_text("\n❌ You don't have any items!")
            self.gui.root.after(2000, self.gui.main_menu)
            return
        
        # Show available items
        self.gui.clear_text()
        self.gui.print_text("\n🎒 Your Inventory:")
        self.gui.print_text("=" * 40)
        
        item_list = list(hero['items'].items())
        for i, (item_name, item_info) in enumerate(item_list, 1):
            quantity = item_info.get('quantity', 1)
            if quantity > 1:
                self.gui.print_text(f"{i}. {item_name} (x{quantity})")
            else:
                self.gui.print_text(f"{i}. {item_name}")
        
        self.gui.print_text("\nWhich item would you like to use?")
        
        def on_item_select(choice):
            if choice <= len(item_list):
                item_name, item_info = item_list[choice - 1]
                self._use_specific_item(item_name, item_info)
            else:
                self.gui.main_menu()
        
        # Create buttons for each item + back button
        button_labels = [f"{i}. Use {name}" for i, (name, _) in enumerate(item_list, 1)]
        button_labels.append("🔙 Back")
        
        self.gui.set_buttons(button_labels, on_item_select)
    
    def _use_specific_item(self, item_name, item_info):
        """Use a specific item and handle its effects"""
        # Lock interface to prevent button spamming during item use
        self.gui.lock_interface()
        
        hero = self.gui.game_state.hero
        item_data = item_info['data']
        
        self.gui.clear_text()
        
        if item_name == 'Health Potion':
            # Play gulp sound when drinking the potion
            self.gui.audio.play_sound_effect('gulp.mp3')
            old_hp = hero['hp']
            hero['hp'] = hero['maxhp']
            healed = hero['hp'] - old_hp
            
            if healed > 0:
                self.gui.print_text(f"\n✨ Used {item_name}!")
                heal_parts = [
                    ("💖 Restored ", "#ffffff"),
                    (f"{healed} HP", "#ff4444"),
                    (f" (HP: {old_hp} → {hero['hp']})", "#ffffff")
                ]
                self.gui._print_colored_parts(heal_parts)
            else:
                self.gui.print_text(f"\n✨ Used {item_name}!")
                self.gui.print_text("💖 You're already at full health!")
        
        else:
            # Handle other item types here as they're added
            self.gui.print_text(f"\n✨ Used {item_name}!")
            self.gui.print_text("   (Effect not yet implemented)")
        
        # Reduce quantity or remove item
        item_info['quantity'] -= 1
        if item_info['quantity'] <= 0:
            del hero['items'][item_name]
            self.gui.print_text(f"\n📦 {item_name} consumed!")
        else:
            remaining_parts = [
                (f"📦 Remaining {item_name}s: ", "#ffffff"),
                (f"{item_info['quantity']}", "#ffaa00")
            ]
            self.gui._print_colored_parts(remaining_parts)
        
        self.gui.root.after(3000, self.gui.main_menu)
