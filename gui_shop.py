"""
Shop system for GUI
"""
import yaml
import os


class ShopGUI:
    """Shop system for GUI"""
    def __init__(self, gui):
        self.gui = gui
        self.store_data = None
        self.current_category = None
    
    def open(self):
        """Open shop"""
        # Load store data
        if self.store_data is None:
            self._load_store()
        
        # Set the shop-specific background
        self.gui.set_shop_background()
        
        self.gui.clear_text()
        #self.gui.show_image('art/pymart.txt')
        self.gui.print_text("\n🛒 Welcome to MonsterMart! 🛒\n")
        
        # Display gold with colored value
        gold_amount = self.gui.game_state.hero.get('gold', 0)
        self.gui.print_colored_value("💰 Your Gold: ", gold_amount, 'gold')
        self.gui.print_text("")  # Empty line
        self._select_category()
    
    def _load_store(self):
        """Load store data from YAML"""
        try:
            with open('store.yaml', 'r', encoding='utf-8') as f:
                self.store_data = yaml.safe_load(f)
        except Exception as e:
            self.gui.print_text(f"❌ Error loading store: {e}")
            self.store_data = {}
    
    def _select_category(self):
        """Display categories and let user select"""
        #self.gui.show_image('art/monstermart.png')
        self.gui.print_text("=" * 60)
        self.gui.print_text("Select a category:")
        self.gui.print_text("=" * 60)
        
        if self.store_data:
            categories = list(self.store_data.keys())
            
            # Show available categories
            for i, category in enumerate(categories[:3], 1):
                self.gui.print_text(f"{i}. {category}")
            
            self.gui.print_text("\n" + "=" * 60)
            self.gui.print_text("Tip: Use the '🏠 Main Menu' button to exit shop")
            
            def on_category_select(choice):
                if choice <= len(categories):
                    self.current_category = categories[choice - 1]
                    self._show_items()
                elif choice == len(categories) + 1:
                    # Main menu button is always the last button
                    self.gui.main_menu()
            
            # Set buttons for categories - add all categories plus main menu button
            button_labels = []
            for category in categories:
                button_labels.append(category)
            button_labels.append("🏠 Main Menu")
            
            self.gui.set_buttons(button_labels, on_category_select)
        else:
            self.gui.print_text("❌ Store is empty!")
            self.gui.root.after(2000, self.gui.main_menu)
    
    def _show_items(self):
        """Display items in selected category"""
        self.gui.clear_text()
        self.gui.print_text(f"\n🛒 {self.current_category} 🛒\n")
        self.gui.print_text(f"💰 Your Gold: {self.gui.game_state.hero.get('gold', 0)}\n")
        self.gui.print_text("=" * 60)
        
        hero_class = self.gui.game_state.hero.get('class', '')
        items = self.store_data.get(self.current_category, [])
        
        # Filter items for hero's class
        available_items = [
            item for item in items 
            if item.get('class') == hero_class or item.get('class') == 'All'
        ]
        
        if not available_items:
            self.gui.print_text(f"❌ No {self.current_category.lower()} available for {hero_class} class!")
            self.gui.root.after(2000, self._select_category)
            return
        
        # Show multiple images of available items using the same logic as show_category_preview
        item_images = []
        for item in available_items:
            if 'ascii_art' in item and os.path.exists(item['ascii_art']):
                item_images.append(item['ascii_art'])
        
        if item_images:
            # Show multiple images based on count
            if len(item_images) == 1:
                self.gui.show_image(item_images[0])
            elif len(item_images) <= 2:
                self.gui.show_images(item_images, "horizontal")
            else:
                self.gui.show_images(item_images, "grid")
        
        # Show up to 3 items
        for i, item in enumerate(available_items[:3], 1):
            self.gui.print_text(f"\n{i}. {item['name']} - 💰 {item['cost']} gold")
            
            # Show stats
            if 'attack' in item:
                self.gui.print_text(f"   ⚔️  Attack: +{item['attack']}")
            if 'defense' in item:
                self.gui.print_text(f"   🛡️  Defense: +{item['defense']}")
            if 'type' in item:
                self.gui.print_text(f"   🧪 Type: {item['type']}")
        
        self.gui.print_text("\n" + "=" * 60)
        self.gui.print_text("Select an item to purchase")
        
        # Set buttons for item interaction
        def on_item_action(choice):
            if choice <= len(available_items):
                # Buy selected item and show its image
                selected_item = available_items[choice - 1]
                if 'ascii_art' in selected_item and os.path.exists(selected_item['ascii_art']):
                    self.gui.show_image(selected_item['ascii_art'])
                self._purchase_item(selected_item)
            elif choice == len(available_items) + 1:
                # Go back to category selection (always the last button)
                self._select_category()
        
        # Set button labels - show all available items plus back button
        button_labels = []
        for item in available_items:
            button_labels.append(f"Buy {item['name']}")
        button_labels.append("🔙 Back to Categories")
        
        self.gui.set_buttons(button_labels, on_item_action)
    
    def _purchase_item(self, item):
        """Handle item purchase"""
        # Lock interface to prevent double-purchases or button spamming
        self.gui.lock_interface()
        
        hero = self.gui.game_state.hero
        item_cost = item['cost']
        hero_gold = hero.get('gold', 0)
        
        # Check if hero has enough gold
        if hero_gold < item_cost:
            self.gui.clear_text()
            self.gui.print_text(f"\n❌ Not enough gold!")
            self.gui.print_text(f"   You have: 💰 {hero_gold}")
            self.gui.print_text(f"   You need: 💰 {item_cost}")
            self.gui.print_text(f"   Short by: 💰 {item_cost - hero_gold}")
            self.gui.root.after(2500, self._show_items)
            return
        
        # Deduct gold
        hero['gold'] -= item_cost
        
        # Show item art if available
        if 'ascii_art' in item and os.path.exists(item['ascii_art']):
            self.gui.show_image(item['ascii_art'])
        
        self.gui.clear_text()
        
        # Purchase success message with colored item name
        purchase_parts = [
            ("\n✅ Purchased: ", "#00ff00"),
            (item['name'], "#ffaa00"),
            ("!", "#00ff00")
        ]
        self.gui._print_colored_parts(purchase_parts)
        
        # Gold remaining with colored amount
        self.gui.print_colored_value("💰 Gold remaining: ", hero['gold'], 'gold')
        
        # Apply item effects based on category
        if self.current_category == 'Weapons':
            # Check if player already owns this specific weapon
            current_weapon = hero.get('weapon', 'None')
            if current_weapon == item['name']:
                self.gui.clear_text()
                self.gui.print_text(f"\n❌ You already own {item['name']}!")
                self.gui.print_text("   You cannot purchase the same weapon again.")
                # Refund the gold since we already deducted it
                hero['gold'] += item_cost
                # Unlock interface and return to shop after delay
                self.gui.unlock_interface()
                self.gui.root.after(2500, self._show_items)
                return
            
            # Update weapon and attack
            old_weapon = current_weapon
            
            # Store base attack if not already stored
            if 'base_attack' not in hero:
                hero['base_attack'] = hero.get('attack', 5)
            
            # Set new weapon and recalculate attack
            hero['weapon'] = item['name']
            old_attack = hero.get('attack', 0)
            hero['attack'] = hero['base_attack'] + item.get('attack', 0)
            
            self.gui.print_text(f"⚔️  Equipped {item['name']}! (was: {old_weapon})")
            self.gui.print_text(f"⚔️  Attack: {old_attack} → {hero['attack']}")
            
        elif self.current_category == 'Armour':
            # Check if player already owns this specific armor
            current_armour = hero.get('armour', 'None')
            if current_armour == item['name']:
                self.gui.clear_text()
                self.gui.print_text(f"\n❌ You already own {item['name']}!")
                self.gui.print_text("   You cannot purchase the same armor again.")
                # Refund the gold since we already deducted it
                hero['gold'] += item_cost
                # Unlock interface and return to shop after delay
                self.gui.unlock_interface()
                self.gui.root.after(2500, self._show_items)
                return
            
            # Update armour and defense
            old_armour = current_armour
            
            # Store base defense if not already stored
            if 'base_defense' not in hero:
                hero['base_defense'] = hero.get('defense', 5)
            
            # Set new armour and recalculate defense
            hero['armour'] = item['name']
            old_defense = hero.get('defense', 0)
            hero['defense'] = hero['base_defense'] + item.get('defense', 0)
            
            self.gui.print_text(f"🛡️  Equipped {item['name']}! (was: {old_armour})")
            self.gui.print_text(f"🛡️  Defense: {old_defense} → {hero['defense']}")
            
        elif self.current_category == 'Items':
            # Add to inventory (new multi-item system)
            if 'items' not in hero:
                hero['items'] = {}
            
            item_name = item['name']
            if item_name in hero['items']:
                # Increase quantity
                hero['items'][item_name]['quantity'] += 1
                self.gui.print_text(f"🧪 Added {item['name']} to inventory!")
                self.gui.print_text(f"   You now have {hero['items'][item_name]['quantity']} {item_name}s")
            else:
                # Add new item
                hero['items'][item_name] = {'data': item, 'quantity': 1}
                self.gui.print_text(f"🧪 Added {item['name']} to inventory!")
                self.gui.print_text(f"   Use it from the main menu")
        
        # Play purchase sound effect (won't interrupt background music)
        self.gui.audio.play_sound_effect('store.mp3')  # Use celebration sound for purchases
        
        # Return to store category selection after delay
        self.gui.root.after(3000, self._select_category)
