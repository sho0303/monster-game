#!/usr/bin/env python3
"""
Town GUI for the monster game - handles town menu and activities
"""

import tkinter as tk
from tkinter import scrolledtext

class TownGUI:
    """GUI for town activities and menu"""
    
    def __init__(self, gui):
        self.gui = gui
    
    def enter_town(self):
        """Enter the town and show town menu"""
        self.gui.clear_text()
        self.gui.lock_interface()
        
        # Set town background
        self.gui.set_town_background()
        
        # Show welcome message
        self.gui.print_text("🏘️  WELCOME TO TOWN  🏘️")
        self.gui.print_text("=" * 60)
        self.gui.print_text("\nYou enter the bustling town square.")
        self.gui.print_text("Medieval buildings line the cobblestone streets,")
        self.gui.print_text("market stalls offer their wares, and a fountain")
        self.gui.print_text("sparkles in the center of the square.")
        self.gui.print_text("\nWhat would you like to do in town?")
        
        def on_town_select(choice):
            if choice == 1:
                self._visit_shop()
            elif choice == 2:
                self._visit_tavern()
            elif choice == 3:
                self._visit_blacksmith()
            elif choice == 4:
                self._visit_fountain()
            elif choice == 5:
                self._leave_town()
        
        # Town menu options
        town_buttons = [
            "🛒 Visit Shop", 
            "🍺 Visit Tavern", 
            "⚒️ Visit Blacksmith", 
            "⛲ Town Fountain",
            "🚪 Leave Town"
        ]
        
        self.gui.set_buttons(town_buttons, on_town_select)
        self.gui.unlock_interface()
    
    def _visit_shop(self):
        """Visit the shop (existing shop functionality)"""
        self.gui.clear_text()
        self.gui.print_text("🛒 Entering the shop...")
        self.gui.print_text("The shopkeeper greets you warmly.")
        
        # Use existing shop system
        self.gui.shop.open()
    
    def _visit_tavern(self):
        """Visit the tavern and access bounty board"""
        self.gui.clear_text()
        self.gui.lock_interface()
        
        self.gui.print_text("🍺  THE PRANCING PONY TAVERN  🍺")
        self.gui.print_text("=" * 60)
        self.gui.print_text("\nYou enter the warm, cozy tavern.")
        self.gui.print_text("The smell of roasted meat and ale fills the air.")
        self.gui.print_text("Adventurers gather around wooden tables,")
        self.gui.print_text("sharing tales of their exploits.")
        self.gui.print_text("\nA large wooden board on the wall displays")
        self.gui.print_text("various bounty notices offering rewards.")
        
        def on_tavern_choice(choice):
            if choice == 1:
                self.gui.bounty_manager.show_bounty_board()
            else:
                self.enter_town()
        
        tavern_buttons = [
            "📜 Check Bounty Board",
            "🚪 Leave Tavern"
        ]
        
        self.gui.set_buttons(tavern_buttons, on_tavern_choice)
        self.gui.unlock_interface()
    
    def _visit_blacksmith(self):
        """Visit the blacksmith"""
        self.gui.clear_text()
        self.gui.print_text("⚒️ Entering the blacksmith...")
        self.gui.print_text("You hear the ring of hammer on anvil.")
        
        # Use blacksmith system
        self.gui.blacksmith.open()
    
    def _visit_fountain(self):
        """Visit the town fountain"""
        self.gui.clear_text()
        self.gui.lock_interface()
        
        self.gui.print_text("⛲  TOWN FOUNTAIN  ⛲")
        self.gui.print_text("=" * 60)
        self.gui.print_text("\nYou approach the sparkling fountain.")
        self.gui.print_text("Crystal clear water bubbles up from the center,")
        self.gui.print_text("creating gentle ripples across the surface.")
        self.gui.print_text("Local legend says this fountain has healing properties.")
        
        # Small HP restoration
        hero = self.gui.game_state.hero
        if hero['hp'] < hero['maxhp']:
            heal_amount = min(3, hero['maxhp'] - hero['hp'])  # Heal up to 3 HP
            hero['hp'] += heal_amount
            
            heal_parts = [
                ("\n✨ The magical waters restore ", "#00ff00"),
                (str(heal_amount), "#ffdd00"),
                (" HP! ✨", "#00ff00")
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
            self.gui.print_text("\n💚 You are already at full health.")
            self.gui.print_text("The fountain's magic has no effect.")
        
        self.gui.print_text("\nYou feel refreshed by the peaceful atmosphere.")
        
        # Return to town after 3 seconds
        self.gui.root.after(3000, self.enter_town)
    
    def _leave_town(self):
        """Leave town and return to main menu"""
        self.gui.clear_text()
        self.gui.print_text("🚪 Leaving the town...")
        self.gui.print_text("You wave goodbye to the townspeople")
        self.gui.print_text("and head back to your adventures.")
        
        # Return to main menu after 2 seconds
        self.gui.root.after(2000, self.gui.main_menu)