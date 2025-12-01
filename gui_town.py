#!/usr/bin/env python3
"""
Town GUI for the monster game - handles town menu and activities
"""

import tkinter as tk
from tkinter import scrolledtext
import random
import os
from typing import TYPE_CHECKING
from resource_utils import resource_exists

import config
from game_enums import BiomeType

if TYPE_CHECKING:
    from gui_interfaces import GameContextProtocol


class TownGUI:
    """GUI for town activities and menu"""
    
    def __init__(self, gui: 'GameContextProtocol'):
        """Initialize with game context.
        
        Args:
            gui: Game context providing UI, state, and subsystem access
        """
        self.gui = gui
    
    def enter_town(self):
        """Enter the town and show town menu"""
        self.gui.clear_text()
        self.gui.lock_interface()
        
        # Set town background
        self.gui.set_town_background()
        
        # Ensure biome is set to town
        self.gui.current_biome = BiomeType.TOWN
        
        # 10% chance of goblin assault
        if random.random() < 0.10:
            self._goblin_assault()
            return
        
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
        """Visit the tavern"""
        self.gui.clear_text()
        self.gui.print_text("🍺 Entering the tavern...")
        self.gui.print_text("The friendly bartender welcomes you warmly.")
        
        # Use tavern system
        self.gui.tavern.open()
    
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
            heal_amount = min(config.FOUNTAIN_HEAL_AMOUNT, hero['maxhp'] - hero['hp'])
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
        
        def return_to_wild():
            # Restore previous biome (or default to grassland)
            bg_manager = self.gui.background_manager
            last_biome = getattr(bg_manager, 'last_biome', 'grassland')
            
            # If last biome was somehow town (shouldn't happen but safety check), use grassland
            if last_biome == 'town':
                last_biome = 'grassland'
                
            self.gui.set_biome_background(last_biome)
            self.gui.main_menu()
        
        # Return to main menu after 2 seconds
        self.gui.root.after(2000, return_to_wild)
    def _goblin_assault(self):
        """Handle goblin assault on the town - 10% chance when entering town"""
        self.gui.clear_text()
        
        # Display two goblin images side by side on the foreground
        goblin_image_path = 'art/goblin_monster.png'
        
        # Check if goblin image exists
        if resource_exists(goblin_image_path):
            # Display two goblins using the same method as monster encounters
            self.gui.image_manager.show_images([goblin_image_path, goblin_image_path])
        
        # Show dramatic assault message
        assault_parts = [
            ("\n⚔️ ", "#ff0000"),
            ("GOBLIN ASSAULT!", "#ff0000"),
            (" ⚔️\n", "#ff0000")
        ]
        self.gui._print_colored_parts(assault_parts)
        
        self.gui.print_text("=" * 60)
        
        warning_parts = [
            ("\n🚨 ", "#ffaa00"),
            ("THE TOWN IS UNDER ATTACK!", "#ffaa00"),
            (" 🚨\n", "#ffaa00")
        ]
        self.gui._print_colored_parts(warning_parts)
        
        self.gui.print_text("\nAs you approach the town gates, you hear screams!")
        self.gui.print_text("Two goblins are terrorizing the townspeople,")
        self.gui.print_text("smashing market stalls and causing chaos!")
        self.gui.print_text("\nThe town guards are overwhelmed and need your help!")
        
        # Show choice buttons
        def on_choice(choice):
            if choice == 1:
                self._fight_goblins()
            else:
                self._run_from_assault()
        
        self.gui.set_buttons(["⚔️ Save the Town", "🏃 Run"], on_choice)
        self.gui.unlock_interface()
    
    def _fight_goblins(self):
        """Fight two goblins back to back"""
        self.gui.clear_text()
        self.gui.lock_interface()
        
        # Create goblin monster from game data
        if 'Goblin' not in self.gui.game_state.monsters:
            self.gui.print_text("Error: Goblin data not found!")
            self.gui.root.after(2000, self.gui.main_menu)
            return
        
        # Store that we're in a goblin assault (for tracking)
        self.goblin_assault_active = True
        self.goblins_defeated = 0
        
        # Start first goblin fight
        self._start_goblin_fight(1)
    
    def _start_goblin_fight(self, goblin_number):
        """Start fight with a specific goblin"""
        self.gui.clear_text()
        
        # Create a copy of the goblin monster
        goblin_template = self.gui.game_state.monsters['Goblin']
        goblin = {
            'name': f'Goblin Raider #{goblin_number}',
            'hp': goblin_template['hp'],
            'maxhp': goblin_template['maxhp'],
            'attack': goblin_template['attack'],
            'defense': goblin_template['defense'],
            'gold': goblin_template['gold'],
            'level': goblin_template['level'],
            'xp': goblin_template['xp'],
            'art': goblin_template.get('art', 'art/goblin_monster.png'),
            'attack_art': goblin_template.get('attack_art', 'art/goblin_monster_attack.png'),
            'attack_sound': goblin_template.get('attack_sound', 'goblin-attack.mp3')
        }
        
        # Show encounter message
        encounter_parts = [
            (f"\n⚔️ Facing ", "#ffffff"),
            (goblin['name'], "#ffaa00"),
            ("! ⚔️\n", "#ffffff")
        ]
        self.gui._print_colored_parts(encounter_parts)
        
        # Start combat
        hero = self.gui.game_state.hero
        
        def on_goblin_defeat(result):
            if result == 'won':
                self._handle_goblin_victory(goblin_number)
            else:
                self._handle_goblin_defeat()
        
        self.gui.combat.fight(hero, goblin, on_goblin_defeat)
    
    def _handle_goblin_victory(self, goblin_number):
        """Handle victory over a goblin"""
        self.goblins_defeated += 1
        
        if self.goblins_defeated < 2:
            # More goblins to fight
            self.gui.clear_text()
            self.gui.print_text(f"\n✅ Goblin Raider #{goblin_number} defeated!")
            self.gui.print_text("\nBut there's still another goblin attacking the town!")
            self.gui.print_text("Prepare yourself for the next fight!")
            
            # Start next goblin fight after short delay
            self.gui.root.after(3000, lambda: self._start_goblin_fight(2))
        else:
            # All goblins defeated!
            self._handle_assault_victory()
    
    def _handle_assault_victory(self):
        """Handle complete victory over all goblins"""
        self.goblin_assault_active = False
        self.gui.clear_text()
        
        # Show victory message
        victory_parts = [
            ("\n🎉 ", "#00ff00"),
            ("VICTORY!", "#00ff00"),
            (" 🎉\n", "#00ff00")
        ]
        self.gui._print_colored_parts(victory_parts)
        
        self.gui.print_text("=" * 60)
        self.gui.print_text("\nYou have defeated both goblins!")
        self.gui.print_text("The townspeople cheer as the last goblin falls.")
        self.gui.print_text("The town is safe once again!")
        
        # Award Town Savior achievement
        if hasattr(self.gui, 'achievements') and self.gui.achievements:
            if self.gui.achievements.update_progress('town_savior', 1):
                achievement_parts = [
                    ("\n🏆 Achievement Unlocked: ", "#ffdd00"),
                    ("Town Savior", "#00ff00"),
                    (" 🏆", "#ffdd00")
                ]
                self.gui._print_colored_parts(achievement_parts)
        
        # Mayor's reward
        hero = self.gui.game_state.hero
        reward_gold = 100
        hero['gold'] += reward_gold
        
        self.gui.print_text("\n" + "=" * 60)
        self.gui.print_text("\n👑 The Town Mayor approaches you:")
        self.gui.print_text('"Hero! You saved our town from those vile goblins!"')
        self.gui.print_text('"Please accept this reward as a token of our gratitude."')
        
        reward_parts = [
            ("\n💰 Received ", "#00ff00"),
            (f"{reward_gold} gold", "#ffdd00"),
            (" from the Mayor! 💰", "#00ff00")
        ]
        self.gui._print_colored_parts(reward_parts)
        
        gold_parts = [
            ("Total Gold: ", "#ffffff"),
            (str(hero['gold']), "#ffdd00")
        ]
        self.gui._print_colored_parts(gold_parts)
        
        # Return to town menu after delay
        self.gui.print_text("\n" + "=" * 60)
        self.gui.print_text("\nThe town returns to normal...")
        self.gui.root.after(5000, self.enter_town)
    
    def _handle_goblin_defeat(self):
        """Handle defeat by goblins"""
        self.goblin_assault_active = False
        hero = self.gui.game_state.hero
        
        # Apply standard death penalties
        # Check if hero has Miser Coin Purse for reduced gold loss
        has_coin_purse = False
        if 'items' in hero and hero['items']:
            has_coin_purse = 'Miser Coin Purse' in hero['items']
        
        original_gold = hero['gold']
        if has_coin_purse and original_gold > 0:
            # Only lose 50% of gold with coin purse
            gold_lost = original_gold // 2
            hero['gold'] = original_gold - gold_lost
            
            self.gui.print_text("\n💀 The goblins have overwhelmed you...")
            
            # Show protected gold message
            protection_parts = [
                ("\nYour ", "#ffffff"),
                ("Miser Coin Purse", "#ffdd00"),
                (" protected you!", "#ffffff")
            ]
            self.gui._print_colored_parts(protection_parts)
            
            loss_parts = [
                ("💰 Lost ", "#ffffff"),
                (f"{gold_lost} gold", "#ff6666"),
                (f" (kept {hero['gold']} gold)", "#ffdd00")
            ]
            self.gui._print_colored_parts(loss_parts)
        else:
            # Lose all gold without protection
            self.gui.print_text("\n💀 The goblins have overwhelmed you...")
            self.gui.print_text("You lost all your gold!")
            hero['gold'] = 0
        
        # Deduct a life
        hero['lives_left'] -= 1
        
        # Restore HP to max for next attempt
        hero['hp'] = hero['maxhp']
        
        # Check for game over
        self.gui.root.after(3000, lambda: self._check_game_over_after_goblin_defeat())
    
    def _check_game_over_after_goblin_defeat(self):
        """Check if game is over after goblin defeat, or return to main menu"""
        if self.gui.check_game_over():
            # Game over screen will be shown
            return
        else:
            # Still have lives, return to main menu
            self.gui.main_menu()
    
    def _run_from_assault(self):
        """Run away from the goblin assault"""
        self.gui.clear_text()
        
        run_parts = [
            ("\n🏃 ", "#ffaa00"),
            ("You flee from the town!", "#ffaa00"),
            (" 🏃\n", "#ffaa00")
        ]
        self.gui._print_colored_parts(run_parts)
        
        self.gui.print_text("=" * 60)
        self.gui.print_text("\nYou turn and run from the goblin assault.")
        self.gui.print_text("The screams of the townspeople fade behind you.")
        self.gui.print_text("Perhaps you'll return when you're stronger...")
        
        shame_parts = [
            ("\n⚠️ ", "#888888"),
            ("You feel ashamed for abandoning the town.", "#888888"),
            (" ⚠️", "#888888")
        ]
        self.gui._print_colored_parts(shame_parts)
        
        # Return to main menu
        self.gui.root.after(config.LONG_DELAY, self.gui.main_menu)

