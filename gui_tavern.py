"""
Tavern system for GUI - drink purchasing and atmosphere
"""
import yaml
import os
from typing import TYPE_CHECKING
from resource_utils import resource_exists, get_resource_path

if TYPE_CHECKING:
    from gui_interfaces import GameContextProtocol


class TavernGUI:
    """Tavern system for GUI"""
    def __init__(self, gui: 'GameContextProtocol'):
        """Initialize with game context.
        
        Args:
            gui: Game context providing UI, state, and subsystem access
        """
        self.gui = gui
        self.tavern_data = None
    
    def open(self):
        """Open tavern"""
        # Load tavern data
        if self.tavern_data is None:
            self._load_tavern()
        
        # Set the tavern-specific background
        self.gui.set_tavern_background()
        
        self.gui.clear_text()
        self.gui.print_text("\n🍺 Welcome to The Prancing Pony Tavern! 🍺\n")
        
        # Display gold with colored value
        gold_amount = self.gui.game_state.hero.get('gold', 0)
        self.gui.print_colored_value("💰 Your Gold: ", gold_amount, 'gold')
        self.gui.print_text("")  # Empty line
        
        self.gui.print_text("🍻 The tavern is warm and inviting.")
        self.gui.print_text("🎵 Cheerful music fills the air as patrons enjoy their drinks.")
        self.gui.print_text("🔥 A fire crackles in the stone hearth nearby.")
        self.gui.print_text("")
        
        self._show_drinks()
    
    def _load_tavern(self):
        """Load tavern data from YAML"""
        try:
            with open(get_resource_path('tavern.yaml'), 'r', encoding='utf-8') as f:
                self.tavern_data = yaml.safe_load(f)
        except Exception as e:
            self.gui.print_text(f"❌ Error loading tavern menu: {e}")
            self.tavern_data = {}
    
    def _show_drinks(self):
        """Display available drinks"""
        self.gui.print_text("=" * 60)
        self.gui.print_text("🍺 DRINK MENU 🍺")
        self.gui.print_text("=" * 60)
        
        if not self.tavern_data or 'Drinks' not in self.tavern_data:
            self.gui.print_text("❌ No drinks available!")
            self.gui.root.after(2000, self._return_to_town)
            return
        
        drinks = self.tavern_data.get('Drinks', [])
        
        if not drinks:
            self.gui.print_text("❌ The barkeeper is out of drinks!")
            self.gui.root.after(2000, self._return_to_town)
            return
        
        # Show drink images if available
        drink_images = []
        for drink in drinks:
            # Use sudsy beer image for beer drinks, or fallback to any art specified
            if 'beer' in drink['name'].lower():
                if resource_exists('art/sudsy_beer.png'):
                    drink_images.append('art/sudsy_beer.png')
            elif 'ascii_art' in drink and resource_exists(drink['ascii_art']):
                drink_images.append(drink['ascii_art'])
        
        if drink_images:
            # Show multiple images based on count
            if len(drink_images) == 1:
                self.gui.show_image(drink_images[0])
            elif len(drink_images) <= 2:
                self.gui.show_images(drink_images, "horizontal")
            else:
                self.gui.show_images(drink_images, "grid")
        
        # Show up to 6 drinks
        for i, drink in enumerate(drinks[:6], 1):
            self.gui.print_text(f"\n{i}. {drink['name']} - 💰 {drink['cost']} gold")
            
            # Add flavor text for drinks
            if 'beer' in drink['name'].lower():
                self.gui.print_text(f"   🍺 A refreshing pint of golden ale")
            elif 'wine' in drink['name'].lower():
                self.gui.print_text(f"   🍷 Fine vintage from the local vineyards")
            elif 'mead' in drink['name'].lower():
                self.gui.print_text(f"   🍯 Sweet honey wine, a tavern favorite")
            elif 'whiskey' in drink['name'].lower() or 'whisky' in drink['name'].lower():
                self.gui.print_text(f"   🥃 Strong spirits to warm your bones")
            else:
                self.gui.print_text(f"   🍻 A fine beverage to quench your thirst")
        
        self.gui.print_text("\n" + "=" * 60)
        self.gui.print_text("The friendly bartender awaits your order!")
        
        # Set buttons for drink interaction
        def on_drink_action(choice):
            if choice <= len(drinks):
                # Buy selected drink and show its image
                selected_drink = drinks[choice - 1]
                # Show beer image for beer drinks
                if 'beer' in selected_drink['name'].lower() and resource_exists('art/sudsy_beer.png'):
                    self.gui.show_image('art/sudsy_beer.png')
                elif 'ascii_art' in selected_drink and resource_exists(selected_drink['ascii_art']):
                    self.gui.show_image(selected_drink['ascii_art'])
                self._purchase_drink(selected_drink)
            elif choice == len(drinks) + 1:
                # Reminisce (view achievements)
                self._show_achievements()
            elif choice == len(drinks) + 2:
                # Go back to town (always the last button)
                self._return_to_town()
        
        # Set button labels - show all available drinks plus reminisce and back button
        button_labels = []
        for drink in drinks:
            button_labels.append(f"🍻 Order {drink['name']}")
        button_labels.append("🏆 Reminisce")
        button_labels.append("🚪 Leave Tavern")
        
        self.gui.set_buttons(button_labels, on_drink_action)
    
    def _purchase_drink(self, drink):
        """Handle drink purchase"""
        # Lock interface to prevent double-purchases or button spamming
        self.gui.lock_interface()
        
        hero = self.gui.game_state.hero
        drink_cost = drink['cost']
        hero_gold = hero.get('gold', 0)
        
        # Check if hero has enough gold
        if hero_gold < drink_cost:
            self.gui.clear_text()
            self.gui.print_text(f"\n❌ Not enough gold for {drink['name']}!")
            self.gui.print_text(f"   You have: 💰 {hero_gold}")
            self.gui.print_text(f"   You need: 💰 {drink_cost}")
            self.gui.print_text(f"   Short by: 💰 {drink_cost - hero_gold}")
            self.gui.print_text("\n🍺 \"Come back when you have more coin!\" says the barkeeper.")
            self.gui.root.after(2500, self._show_drinks)
            return
        
        # Deduct gold
        hero['gold'] -= drink_cost
        
        # Show drink art if available
        if 'beer' in drink['name'].lower() and resource_exists('art/sudsy_beer.png'):
            self.gui.show_image('art/sudsy_beer.png')
        elif 'ascii_art' in drink and resource_exists(drink['ascii_art']):
            self.gui.show_image(drink['ascii_art'])
        
        self.gui.clear_text()
        
        # Purchase success message with colored drink name
        purchase_parts = [
            ("\n🍻 You order a ", "#00ff00"),
            (drink['name'], "#ffaa00"),
            ("!", "#00ff00")
        ]
        self.gui._print_colored_parts(purchase_parts)
        
        # Gold remaining with colored amount
        self.gui.print_colored_value("💰 Gold remaining: ", hero['gold'], 'gold')
        
        # Apply drink effects - small HP restoration and flavor text
        heal_amount = 2  # Drinks provide small healing
        if hero['hp'] < hero['maxhp']:
            actual_heal = min(heal_amount, hero['maxhp'] - hero['hp'])
            hero['hp'] += actual_heal
            
            heal_parts = [
                ("\n🌟 The ", "#00ff00"),
                (drink['name'], "#ffaa00"),
                (" restores ", "#00ff00"),
                (str(actual_heal), "#ffdd00"),
                (" HP!", "#00ff00")
            ]
            self.gui._print_colored_parts(heal_parts)
            
            hp_parts = [
                ("Your HP: ", "#00ff00"),
                (str(hero['hp']), "#00ff00"),
                ("/", "#ffffff"),
                (str(hero['maxhp']), "#00ff00")
            ]
            self.gui._print_colored_parts(hp_parts)
        else:
            self.gui.print_text("\n💚 You're already at full health, but the drink")
            self.gui.print_text("   tastes delicious and lifts your spirits!")
        
        # Flavor text based on drink type
        if 'beer' in drink['name'].lower():
            self.gui.print_text("\n🍺 The golden ale is perfectly chilled and refreshing.")
            self.gui.print_text("   The foam tickles your nose as you take a sip.")
        elif 'wine' in drink['name'].lower():
            self.gui.print_text("\n🍷 The wine has a rich, complex flavor.")
            self.gui.print_text("   You savor each sip as warmth spreads through you.")
        elif 'mead' in drink['name'].lower():
            self.gui.print_text("\n🍯 The sweet honey mead is smooth and warming.")
            self.gui.print_text("   Ancient recipes make this a tavern specialty.")
        else:
            self.gui.print_text(f"\n🍻 The {drink['name']} hits the spot perfectly.")
            self.gui.print_text("   You feel refreshed and ready for adventure!")
        
        self.gui.print_text("\n🎵 The tavern music seems a bit merrier now.")
        self.gui.print_text("   Other patrons nod approvingly at your choice.")
        
        # Play gulp sound effect for drinking
        self.gui.audio.play_sound_effect('gulp.mp3')
        
        # Unlock interface and return to drink menu after delay
        self.gui.unlock_interface()
        self.gui.root.after(4000, self._show_drinks)
    
    def _return_to_town(self):
        """Return to town menu"""
        self.gui.clear_text()
        self.gui.print_text("🚪 You bid farewell to the friendly bartender")
        self.gui.print_text("   and leave the warm, cozy tavern.")
        self.gui.print_text("\n🍺 \"Come back anytime!\" calls the barkeeper.")
        
        # Return to town after 2 seconds
        self.gui.root.after(2000, self.gui.town.enter_town)
    
    def _show_achievements(self):
        """Display player's achievements and completed quests"""
        self.gui.clear_text()
        
        # Check if achievements system exists
        if not hasattr(self.gui, 'achievements') or not self.gui.achievements:
            self.gui.print_text("\n🏆 REMINISCE 🏆")
            self.gui.print_text("=" * 60)
            self.gui.print_text("\nYou sit by the fire and reflect on your adventures...")
            self.gui.print_text("But your memory seems a bit hazy.")
            self.gui.print_text("\n(Achievement system not available)")
            
            def go_back(choice):
                self._show_drinks()
            
            self.gui.set_buttons(["🔙 Back"], go_back)
            return
        
        # Display reminisce header
        self.gui.print_text("\n🏆 REMINISCE - YOUR JOURNEY 🏆")
        self.gui.print_text("=" * 60)
        self.gui.print_text("\nYou sit by the fireplace with a mug in hand,")
        self.gui.print_text("reminiscing about your adventures and accomplishments...")
        self.gui.print_text("")
        
        # Get completed quests
        hero = self.gui.game_state.hero
        completed_quest_targets = hero.get('completed_quests', [])
        
        # Show completed quests section
        if completed_quest_targets:
            self.gui.print_text("=" * 60)
            self.gui.print_text("\n📜 COMPLETED QUESTS 📜")
            self.gui.print_text("")
            
            quest_count_parts = [
                ("   You have completed ", "#ffffff"),
                (f"{len(completed_quest_targets)}", "#ffdd00"),
                (" quest(s)!", "#ffffff")
            ]
            self.gui._print_colored_parts(quest_count_parts)
            self.gui.print_text("")
            
            # Show completed quest monsters
            for i, monster_name in enumerate(completed_quest_targets, 1):
                quest_parts = [
                    (f"   {i}. ", "#ffffff"),
                    ("Defeated ", "#aaaaaa"),
                    (monster_name, "#00ff00")
                ]
                self.gui._print_colored_parts(quest_parts)
            
            self.gui.print_text("")
        
        # Get all visible achievements
        visible_achievements = self.gui.achievements.get_visible_achievements()
        completed_achievements = [ach for ach in visible_achievements if ach.completed]
        
        # Show achievement section header
        self.gui.print_text("=" * 60)
        self.gui.print_text("\n🏆 ACHIEVEMENTS 🏆")
        self.gui.print_text("")
        
        # Show completion stats
        completion_percentage = self.gui.achievements.get_completion_percentage()
        
        stats_parts = [
            ("   Progress: ", "#ffffff"),
            (f"{len(completed_achievements)}/{len(visible_achievements)}", "#ffdd00"),
            (f" ({completion_percentage:.1f}%)", "#00ff00")
        ]
        self.gui._print_colored_parts(stats_parts)
        self.gui.print_text("")
        
        if not completed_achievements:
            self.gui.print_text("   You haven't unlocked any achievements yet!")
            self.gui.print_text("   Go on adventures to earn your first achievement!")
            self.gui.print_text("")
        else:
            # Group achievements by category
            categories = {}
            for ach in completed_achievements:
                if ach.category not in categories:
                    categories[ach.category] = []
                categories[ach.category].append(ach)
            
            # Display by category
            category_emojis = {
                'combat': '',
                'exploration': '',
                'collection': '',
                'progression': '',
                'special': ''
            }
            
            for category, achievements in sorted(categories.items()):
                emoji = category_emojis.get(category, '🏆')
                self.gui.print_text("")
                
                category_header = [
                    (f"{emoji} ", "#ffdd00"),
                    (category.upper(), "#00ff00"),
                    (f" {emoji}", "#ffdd00")
                ]
                self.gui._print_colored_parts(category_header)
                self.gui.print_text("")
                
                for ach in sorted(achievements, key=lambda x: x.completed_at or ""):
                    achievement_parts = [
                        ("   ✓ ", "#ffdd00"),
                        (ach.name, "#00ff00")
                    ]
                    self.gui._print_colored_parts(achievement_parts)
                    
                    self.gui.print_text(f"      {ach.description}")
                    
                    # Show reward if applicable
                    if ach.reward_type == "gold" and ach.reward_value > 0:
                        self.gui.print_text(f"      Reward: {ach.reward_value} gold")
                    elif ach.reward_type == "stat_bonus" and ach.reward_value > 0:
                        self.gui.print_text(f"      Reward: +{ach.reward_value} permanent stat bonus")
                    elif ach.reward_type == "title":
                        self.gui.print_text(f"      Reward: Title earned")
                    
                    self.gui.print_text("")
        
        self.gui.print_text("=" * 60)
        self.gui.print_text("\nYou finish your drink and smile at the memories.")
        
        # Back button only
        def go_back(choice):
            self._show_drinks()
        
        self.gui.set_buttons(["🔙 Back"], go_back)

