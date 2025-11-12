"""
Monster encounter system for GUI
"""
import os
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui_interfaces import GameContextProtocol


class MonsterEncounterGUI:
    """Monster encounter for GUI"""
    def __init__(self, gui: 'GameContextProtocol'):
        """Initialize with game context.
        
        Args:
            gui: Game context providing UI, state, and subsystem access
        """
        self.gui = gui
    
    def set_background(self, biome_name):
        """Set background for monster encounters (called when biome changes)"""
        # If we're currently in a monster encounter, update the background
        # This method is called from the biome cycling system
        if hasattr(self.gui, 'current_action') and self.gui.current_action:
            self.gui.set_biome_background(biome_name)
    
    def start(self):
        """Start monster encounter"""
        monster_result = self._select_random_monster()
        if not monster_result:
            self._show_no_monsters_message()
            return
        
        # Unpack monster type and data
        monster_type, monster = monster_result
        
        # Store monster data for Dragon boss detection
        self.current_monster_data = monster
        
        # Keep the current biome background for immersive encounters
        # (Don't change the background - use whatever biome the player is in)
        
        self.gui.clear_text()
        
        # Display hero and monster images side by side in top frame
        hero = self.gui.game_state.hero
        self._display_hero_vs_monster_images(hero, monster)
        
        # Show biome-specific encounter message
        current_biome = getattr(self.gui, 'current_biome', 'grassland')
        biome_emojis = {
            'grassland': '🌱',
            'desert': '🏜️', 
            'dungeon': '🏰',
            'ocean': '🌊'
        }
        biome_encounters = {
            'grassland': 'emerges from the tall grass',
            'desert': 'rises from the sand dunes', 
            'dungeon': 'lurks in the shadows',
            'ocean': 'surfaces from the depths'
        }
        
        emoji = biome_emojis.get(current_biome, '🌍')
        encounter_desc = biome_encounters.get(current_biome, 'appears before you')
        
        encounter_parts = [
            (f"\n{emoji} A ", "#ffffff"),
            (monster['name'], "#ffaa00"),
            (f" {encounter_desc}! {emoji}\n", "#ffffff")
        ]
        self.gui._print_colored_parts(encounter_parts)
        
        # Show current quest summary before the fight
        self._display_quest_summary(monster_type)
        
        # Display hero and monster stats side by side
        self._display_vs_stats(hero, monster)
        
        def on_choice(choice):
            if choice == 1:
                self._handle_fight_choice(monster, monster_type)
            else:
                self._handle_run_choice(monster)
        
        self.gui.set_buttons(["⚔️ Fight", "🏃 Run"], on_choice)
    
    def _get_monster_attack_sound(self, monster):
        """Get the appropriate attack sound for the monster"""
        # Check if monster has custom attack_sound defined
        if 'attack_sound' in monster and monster['attack_sound']:
            return monster['attack_sound']
        else:
            # Use default monster attack sound
            return 'buzzer.mp3'
    
    def _show_no_monsters_message(self):
        """Show message when no level-appropriate monsters are available in current biome"""
        current_biome = getattr(self.gui, 'current_biome', 'grassland')
        hero_level = self.gui.game_state.hero['level']
        
        # Get biome info for display
        biome_emojis = {
            'grassland': '🌱',
            'desert': '🏜️', 
            'dungeon': '🏰',
            'ocean': '🌊',
            'town': '🏘️'
        }
        
        biome_descriptions = {
            'grassland': 'rolling meadows',
            'desert': 'sandy dunes',
            'dungeon': 'dark corridors', 
            'ocean': 'crystal waters',
            'town': 'peaceful streets'
        }
        
        emoji = biome_emojis.get(current_biome, '🌍')
        description = biome_descriptions.get(current_biome, 'this area')
        
        self.gui.clear_text()
        
        # Show "no monsters" message with biome context
        no_monsters_parts = [
            (f"\n{emoji} ", "#ffffff"),
            ("No Suitable Monsters Found", "#ffaa00"),
            (f" {emoji}\n", "#ffffff")
        ]
        self.gui._print_colored_parts(no_monsters_parts)
        
        explanation_parts = [
            ("The ", "#ffffff"),
            (description, "#cccccc"),
            (f" of {current_biome.title()}", "#ffffff"),
            (" seem peaceful right now.\n", "#cccccc")
        ]
        self.gui._print_colored_parts(explanation_parts)
        
        level_parts = [
            ("No monsters within your level range ", "#ffffff"),
            (f"({hero_level-1} to {hero_level*2})", "#ffdd00"),
            (" are currently active in this biome.\n", "#ffffff")
        ]
        self.gui._print_colored_parts(level_parts)
        
        suggestion_parts = [
            ("💡 Try ", "#888888"),
            ("teleporting", "#88ff88"),
            (" to a different biome, or ", "#888888"),
            ("leveling up", "#88ff88"),
            (" to access stronger monsters!", "#888888")
        ]
        self.gui._print_colored_parts(suggestion_parts)
        
        # Return to main menu after showing message
        def return_to_menu():
            self.gui.main_menu()
        
        self.gui.set_buttons(["🏠 Return to Menu"], lambda choice: return_to_menu())
    
    def _handle_fight_choice(self, monster, monster_type):
        """Handle when player chooses to fight the monster"""
        # Lock interface immediately when fight is chosen to prevent double-clicks
        self.gui.lock_interface()
        
        # Create callback for after the fight is complete
        after_fight_callback = self._create_after_fight_callback(monster, monster_type)
        
        # Start the combat
        self.gui.combat.fight(self.gui.game_state.hero, monster, after_fight_callback)
    
    def _handle_run_choice(self, monster):
        """Handle when player chooses to run away"""
        self._attempt_run_away(monster)
    
    def _create_after_fight_callback(self, monster, monster_type):
        """Create callback function for handling post-fight results"""
        def after_fight(result):
            if result == 'won':
                self._handle_victory(monster, monster_type)
            else:
                self._handle_defeat()
            
            # Check if game is over (0 lives left)
            if self.gui.check_game_over():
                # Don't return to main menu if game is over - let game over screen stay
                return
            
            # For final boss victories, the fireworks animation handles timing and return to menu
            # For regular victories, wait before returning to main menu
            is_final_boss_victory = (result == 'won' and monster.get('finalboss', False))
            
            if not is_final_boss_victory:
                # Standard delay for regular victories/defeats - interface unlocks when main_menu sets buttons
                self.gui.root.after(3000, self.gui.main_menu)
            else:
                # Final boss victory - fireworks animation will handle the return to main menu
                # Add extra delay for epic victory celebration, then return to main menu
                self.gui.root.after(8000, self.gui.main_menu)  # 6 seconds for fireworks + 2 second buffer
        
        return after_fight
    
    def _handle_victory(self, monster, monster_type):
        """Handle victory rewards and quest completion"""
        hero = self.gui.game_state.hero
        
        # Award gold and XP
        self._award_victory_rewards(monster)
        
        # Check and handle quest completion
        self._process_quest_completion(monster_type)
    
    def _apply_gold_loss_on_death(self, death_message="💀 Defeat!"):
        """Apply gold loss on death, with Miser Coin Purse protection if available"""
        hero = self.gui.game_state.hero
        
        # Check if hero has Miser Coin Purse for reduced gold loss
        has_coin_purse = False
        if 'items' in hero and hero['items']:
            has_coin_purse = 'Miser Coin Purse' in hero['items']
        
        original_gold = hero['gold']
        if has_coin_purse and original_gold > 0:
            # Only lose 50% of gold with coin purse
            gold_lost = original_gold // 2
            hero['gold'] = original_gold - gold_lost
            
            # Show protected gold message
            protection_parts = [
                (f"\n{death_message} Your ", "#ffffff"),
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
            self.gui.print_text(f"\n{death_message} You lost all your gold!")
            hero['gold'] = 0

    def _handle_defeat(self):
        """Handle defeat consequences"""
        hero = self.gui.game_state.hero
        
        # Apply gold loss with potential coin purse protection
        self._apply_gold_loss_on_death()
        
        hero['lives_left'] -= 1
        hero['hp'] = hero['maxhp']
    
    def _award_victory_rewards(self, monster):
        """Award gold and XP for defeating monster"""
        hero = self.gui.game_state.hero
        
        # Victory message with colored gold reward
        victory_parts = [
            ("\n🎉 Victory! You earned ", "#00ff00"),
            (str(monster['gold']), "#ffdd00"),
            (" gold!", "#00ff00")
        ]
        self.gui._print_colored_parts(victory_parts)
        
        # Award rewards
        hero['gold'] += monster['gold']
        hero['xp'] += monster.get('xp', 1)  # Default 1 XP if not specified
    
    def _process_quest_completion(self, monster_type):
        """Process quest completion and display results"""
        hero = self.gui.game_state.hero
        
        # Check for quest completion using monster type (not display name)
        completed_quests = self.gui.quest_manager.check_quest_completion(hero, monster_type)
        
        if completed_quests:
            for quest in completed_quests:
                self._display_quest_completion(quest)
            
            # Clean up completed quests
            self.gui.quest_manager.clear_completed_quests(hero)
    
    def _display_quest_completion(self, quest):
        """Display quest completion message and XP progress"""
        hero = self.gui.game_state.hero
        
        # Calculate XP progression
        xp_before = hero['xp'] - quest.reward_xp
        xp_after = hero['xp']
        current_level = hero['level']
        xp_needed_to_level = current_level * 5
        
        # Show quest completion message
        quest_parts = [
            ("\n🏆 Quest Completed: ", "#00ff00"),
            (quest.description, "#ffffff"),
            (f" (+{quest.reward_xp} XP)", "#ffdd00")
        ]
        self.gui._print_colored_parts(quest_parts)
        
        # Show XP progression details
        if xp_after >= xp_needed_to_level:
            self._display_level_up_message(xp_before, xp_after, xp_needed_to_level, current_level)
        else:
            self._display_xp_progress(xp_before, xp_after, xp_needed_to_level, current_level)
    
    def _display_level_up_message(self, xp_before, xp_after, xp_needed_to_level, current_level):
        """Display level up ready message"""
        level_up_parts = [
            ("   💫 Ready to level up! ", "#ffaa00"),
            (f"XP: {xp_before} → {xp_after} ", "#8844ff"),
            (f"(Need {xp_needed_to_level} for Level {current_level + 1})", "#ffffff")
        ]
        self.gui._print_colored_parts(level_up_parts)
    
    def _display_xp_progress(self, xp_before, xp_after, xp_needed_to_level, current_level):
        """Display XP progress towards next level"""
        xp_progress_parts = [
            ("   📊 XP Progress: ", "#ffffff"),
            (f"{xp_before} → {xp_after}", "#8844ff"),
            (f"/{xp_needed_to_level} ", "#ffffff"),
            (f"({xp_needed_to_level - xp_after} XP to Level {current_level + 1})", "#888888")
        ]
        self.gui._print_colored_parts(xp_progress_parts)
    
    def _attempt_run_away(self, monster):
        """Attempt to run away with 50% chance of monster attack"""
        # Lock interface during run attempt
        self.gui.lock_interface()
        
        # 50% chance of monster getting an attack in
        monster_attacks = random.choice([True, False])
        
        if monster_attacks:
            self.gui.print_text("\n🏃 You try to run away...")
            self.gui.print_text(f"💀 But {monster['name']} attacks as you flee!")
            
            # Use combat system's damage calculation (with level consideration)
            hero = self.gui.game_state.hero
            hero_level = hero.get('level', 1)
            monster_level = monster.get('level', 1)
            damage = self.gui.combat.calculate_damage(monster['attack'], hero['defense'], monster_level, hero_level)
            
            # Show monster attack animation
            self.gui.combat.current_hero_image = self.current_hero_image
            self.gui.combat.current_monster_image = self.current_monster_image
            self.gui.combat.current_monster_data = monster  # Ensure monster data is available for sound
            self.gui.combat._show_monster_attack_animation(monster)
            
            # After animation, show damage and complete run away
            self.gui.root.after(1500, lambda: self._complete_run_away_with_damage(damage, monster))
        else:
            self.gui.print_text("\n🏃 You successfully ran away!")
            self.gui.root.after(1500, self.gui.main_menu)
    
    def _complete_run_away_with_damage(self, damage, monster):
        """Complete run away after taking damage from monster attack"""
        hero = self.gui.game_state.hero
        
        # Apply damage
        hero['hp'] = max(0, hero['hp'] - damage)
        
        # Show damage (sound already played at start of animation)
        
        # Display damage message with colored values
        damage_parts = [
            ("💔 ", "#00ff00"),
            (monster['name'], "#ffaa00"),
            (" hits you for ", "#00ff00"),
            (str(damage), "#ff8800"),
            (" damage as you escape!", "#00ff00")
        ]
        self.gui._print_colored_parts(damage_parts)
        
        # Display HP with colored value
        hp_parts = [
            ("Your HP: ", "#00ff00"),
            (str(hero['hp']), "#ff4444")
        ]
        self.gui._print_colored_parts(hp_parts)
        
        # Check if hero died while running away
        if hero['hp'] <= 0:
            # Apply gold loss with potential coin purse protection
            self._apply_gold_loss_on_death("💀 You collapsed while trying to escape!")
            self.gui.game_state.hero['lives_left'] -= 1
            self.gui.game_state.hero['hp'] = self.gui.game_state.hero['maxhp']
            
            # Check if game is over (0 lives left)
            if self.gui.check_game_over():
                # Don't return to main menu if game is over - let game over screen stay
                return
        else:
            self.gui.print_text("\n🏃 You managed to escape, but not unscathed!")
        
        self.gui.root.after(2500, self.gui.main_menu)
    
    def _display_hero_vs_monster_images(self, hero, monster):
        """Display hero and monster images side by side in top frame"""
        image_paths = []
        
        # Get hero image path
        hero_class = hero.get('class', 'Warrior').lower()
        hero_image_path = f"art/{hero_class.capitalize()}.png"
        
        try:
            # Check if hero image exists
            if os.path.exists(hero_image_path):
                image_paths.append(hero_image_path)
            else:
                # Use crossed swords as fallback for hero
                image_paths.append('art/crossed_swords.png')
        except:
            image_paths.append('art/crossed_swords.png')
        
        # Get monster image path
        if 'art' in monster and monster['art']:
            try:
                if os.path.exists(monster['art']):
                    image_paths.append(monster['art'])
                else:
                    # Use crossed swords as fallback for monster
                    image_paths.append('art/crossed_swords.png')
            except:
                image_paths.append('art/crossed_swords.png')
        else:
            # Default monster image
            image_paths.append('art/crossed_swords.png')
        
        # Store images for animated entrance
        self.current_hero_image = image_paths[0]
        self.current_monster_image = image_paths[1] if len(image_paths) > 1 else 'art/crossed_swords.png'
        
        # Start animated entrance instead of static display
        self._animate_character_entrances()
    
    def _animate_character_entrances(self):
        """Animate hero and monster walking in from opposite sides"""
        # Clear the canvas first
        self.gui._clear_foreground_images()
        
        # Get canvas dimensions for positioning
        canvas_width, canvas_height = self.gui._get_canvas_dimensions()
        
        # Calculate final positions (same as horizontal layout in show_images)
        base_img_size = min(canvas_width // 3, canvas_height // 2, 120)
        
        # Special handling for double-resolution Dragon final boss
        monster_data = getattr(self, 'current_monster_data', {})
        is_dragon_boss = (monster_data.get('finalboss', False) and 
                         'dragon_endboss' in self.current_monster_image.lower())
        
        # Use larger size for Dragon boss to show its high-resolution art
        hero_img_size = base_img_size
        monster_img_size = int(base_img_size * 1.8) if is_dragon_boss else base_img_size
        
        spacing_x = canvas_width // 3
        start_y = (canvas_height - max(hero_img_size, monster_img_size)) // 2
        
        # Final positions for hero (left) and monster (right)
        hero_final_x = spacing_x - hero_img_size // 2
        monster_final_x = 2 * spacing_x - monster_img_size // 2
        final_y = start_y
        
        # Starting positions (off-screen)
        hero_start_x = -hero_img_size  # Off-screen left
        monster_start_x = canvas_width  # Off-screen right
        
        # Animation parameters
        self.animation_step = 0
        self.animation_steps = 15  # Number of animation frames (reduced for faster entrance)
        self.hero_current_x = hero_start_x
        self.monster_current_x = monster_start_x
        
        # Calculate movement per step
        self.hero_step_x = (hero_final_x - hero_start_x) / self.animation_steps
        self.monster_step_x = (monster_final_x - monster_start_x) / self.animation_steps
        
        # Store final positions and image sizes for animation
        self.hero_final_x = hero_final_x
        self.monster_final_x = monster_final_x
        self.final_y = final_y
        self.hero_img_size = hero_img_size
        self.monster_img_size = monster_img_size
        
        # Start the animation
        self._update_entrance_animation()
    
    def _update_entrance_animation(self):
        """Update one frame of the entrance animation"""
        # Clear previous frame
        self.gui._clear_foreground_images()
        
        # Calculate animation progress (0.0 to 1.0)
        progress = self.animation_step / self.animation_steps
        
        # Apply easing for smoother animation (ease-out effect)
        eased_progress = 1 - (1 - progress) ** 2
        
        # Calculate current positions using eased progress
        hero_start_x = -self.hero_img_size
        monster_start_x = self.gui._get_canvas_dimensions()[0]
        
        self.hero_current_x = hero_start_x + (self.hero_final_x - hero_start_x) * eased_progress
        self.monster_current_x = monster_start_x + (self.monster_final_x - monster_start_x) * eased_progress
        
        # Add hero image at current position
        hero_id = self.gui._add_canvas_image(
            self.current_hero_image, 
            int(self.hero_current_x), 
            self.final_y, 
            self.hero_img_size, 
            self.hero_img_size
        )
        
        # Add monster image at current position (larger for Dragon boss)
        monster_id = self.gui._add_canvas_image(
            self.current_monster_image, 
            int(self.monster_current_x), 
            self.final_y, 
            self.monster_img_size, 
            self.monster_img_size
        )
        
        # Continue animation or finish
        self.animation_step += 1
        if self.animation_step < self.animation_steps:
            # Schedule next frame
            self.gui.root.after(40, self._update_entrance_animation)  # 40ms per frame for smoother animation
        else:
            # Animation complete - ensure final positions are exact
            self.gui._clear_foreground_images()
            self.gui._add_canvas_image(
                self.current_hero_image, 
                self.hero_final_x, 
                self.final_y, 
                self.hero_img_size, 
                self.hero_img_size
            )
            self.gui._add_canvas_image(
                self.current_monster_image, 
                self.monster_final_x, 
                self.final_y, 
                self.monster_img_size, 
                self.monster_img_size
            )
            
            # Optional: Play a subtle encounter sound when animation completes
            # (You can uncomment this if you want sound feedback)
            # self.gui.audio.play_sound_effect('encounter.mp3')

    def _display_vs_stats(self, hero, monster):
        """Display hero and monster stats side by side"""
        # Create formatted side-by-side display
        separator = "    VS    "
        
        # Header line
        self.gui.print_text("=" * 60)
        hero_header = f"🛡️  {hero.get('name', 'Hero')} ({hero['class']})"
        monster_header = f"💀  {monster['name']}"
        header_line = f"{hero_header:<25}{separator}{monster_header}"
        self.gui.print_text(header_line)
        self.gui.print_text("=" * 60)
        
        # Stats comparison
        stats = [
            ("Level", hero['level'], monster['level']),
            ("HP", f"{hero['hp']}/{hero['maxhp']}", f"{monster['hp']}/{monster['maxhp']}"),
            ("Attack", hero['attack'], monster['attack']),
            ("Defense", hero['defense'], monster['defense'])
        ]
        
        for stat_name, hero_val, monster_val in stats:
            hero_stat = f"{stat_name}: {hero_val}"
            monster_stat = f"{stat_name}: {monster_val}"
            
            # Add visual indicators for advantage/disadvantage
            if stat_name in ["Attack", "Defense", "Level"]:
                try:
                    hero_num = int(str(hero_val).split('/')[0])
                    monster_num = int(str(monster_val).split('/')[0])
                    if hero_num > monster_num:
                        hero_stat += " ✓"
                    elif monster_num > hero_num:
                        monster_stat += " ✓"
                except (ValueError, IndexError):
                    pass
            
            stat_line = f"{hero_stat:<25}{separator}{monster_stat}"
            self.gui.print_text(stat_line)
        
        # Additional hero info
        if hero.get('gold', 0) > 0:
            self.gui.print_text(f"\n💰 Your Gold: {hero['gold']}")
        if hero.get('xp', 0) > 0:
            self.gui.print_text(f"⭐ Your XP: {hero['xp']}/{hero['level'] * 5}")
        
        # Potential rewards
        self.gui.print_text(f"\n🏆 Victory Rewards: {monster.get('gold', 0)} gold, {monster.get('xp', 0)} XP")
        self.gui.print_text("=" * 60 + "\n")

    def _display_quest_summary(self, current_monster_type=None):
        """Display current active quests at the start of encounter"""
        active_quests = self.gui.quest_manager.get_active_quests(self.gui.game_state.hero)
        
        if active_quests:
            # Show quest summary header
            quest_header_parts = [
                ("\n📜 ", "#ffffff"),
                ("Active Quests", "#ffaa00"),
                (" (", "#ffffff"),
                (f"{len(active_quests)}/3", "#88ff88"),
                ("):", "#ffffff")
            ]
            self.gui._print_colored_parts(quest_header_parts)
            
            # Show each active quest with progress indicators
            for i, quest in enumerate(active_quests, 1):
                # Get biome emoji for quest context
                biome_emojis = {'grassland': '🌱', 'desert': '🏜️', 'dungeon': '🏰', 'ocean': '🌊'}
                
                # Determine biome from quest description
                quest_biome = 'grassland'  # default
                if 'desert sands' in quest.description.lower():
                    quest_biome = 'desert'
                elif 'dark dungeons' in quest.description.lower():
                    quest_biome = 'dungeon'
                elif 'ocean depths' in quest.description.lower():
                    quest_biome = 'ocean'
                elif 'grasslands' in quest.description.lower():
                    quest_biome = 'grassland'
                
                biome_emoji = biome_emojis.get(quest_biome, '🎯')
                
                # Check if this quest matches the current monster
                is_matching_quest = (current_monster_type and 
                                   quest.quest_type == 'kill_monster' and 
                                   quest.target == current_monster_type)
                
                if is_matching_quest:
                    # Highlight matching quest
                    quest_parts = [
                        (f"  ⭐ ", "#ffaa00"),
                        (f"{biome_emoji} ", "#ffffff"),
                        (quest.description, "#00ff00"),
                        (" → ", "#ffaa00"),
                        (f"{quest.reward_xp} XP", "#ffdd00"),
                        (" ⭐ THIS FIGHT!", "#ffaa00")
                    ]
                else:
                    # Normal quest display
                    quest_parts = [
                        (f"  • ", "#888888"),
                        (f"{biome_emoji} ", "#ffffff"),
                        (quest.description, "#cccccc"),
                        (" → ", "#888888"),
                        (f"{quest.reward_xp} XP", "#ffdd00")
                    ]
                self.gui._print_colored_parts(quest_parts)
        else:
            # No active quests message
            no_quest_parts = [
                ("\n📜 ", "#ffffff"),
                ("No active quests", "#888888"),
                (" - Visit Quests menu for objectives!", "#888888")
            ]
            self.gui._print_colored_parts(no_quest_parts)

    def _select_random_monster(self):
        """Select random monster based on current biome from YAML biome field"""
        import random
        current_biome = getattr(self.gui, 'current_biome', 'grassland')
        hero_level = self.gui.game_state.hero['level']
        
        # Get all monsters for this biome
        biome_specific_monsters = [
            (key, value) for key, value in self.gui.game_state.monsters.items()
            if value.get('biome', 'grassland') == current_biome
        ]
        
        # Try to find level-appropriate monsters in current biome first
        # Reasonable level range: maximum 1 level above, minimum 2 levels below (but never below 1)
        level_appropriate_monsters = [
            (key, value) for key, value in biome_specific_monsters
            if value['level'] <= hero_level + 1 and value['level'] >= max(1, hero_level - 2)
        ]
        
        if level_appropriate_monsters:
            key, value = random.choice(level_appropriate_monsters)
            monster_data = value.copy()
            return (key, monster_data)
        
        # No level-appropriate monsters found in this biome
        return None

