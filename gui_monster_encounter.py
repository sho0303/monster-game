"""
Monster encounter system for GUI
"""
import os
import random


class MonsterEncounterGUI:
    """Monster encounter for GUI"""
    def __init__(self, gui):
        self.gui = gui
    
    def start(self):
        """Start monster encounter"""
        monster = self._select_random_monster()
        if not monster:
            return
        
        # Set the dungeon background for monster encounters
        self.gui.set_background_image('art/dungeon_background.png', '#2d1f1a')
        
        self.gui.clear_text()
        
        # Display hero and monster images side by side in top frame
        hero = self.gui.game_state.hero
        self._display_hero_vs_monster_images(hero, monster)
        
        self.gui.print_text(f"\n⚠️  A {monster['name']} appeared! ⚠️\n")
        
        # Display hero and monster stats side by side
        self._display_vs_stats(hero, monster)
        
        def on_choice(choice):
            if choice == 1:
                # Lock interface immediately when fight is chosen to prevent double-clicks
                self.gui.lock_interface()
                
                def after_fight(result):
                    if result == 'won':
                        # Victory message with colored gold reward
                        victory_parts = [
                            ("\n🎉 Victory! You earned ", "#00ff00"),
                            (str(monster['gold']), "#ffdd00"),
                            (" gold!", "#00ff00")
                        ]
                        self.gui._print_colored_parts(victory_parts)
                        self.gui.game_state.hero['gold'] += monster['gold']
                        self.gui.game_state.hero['xp'] += monster.get('xp', 1)  # Default 1 XP if not specified
                        
                        # Check for quest completion
                        completed_quests = self.gui.quest_manager.check_quest_completion(
                            self.gui.game_state.hero, monster['name']
                        )
                        
                        if completed_quests:
                            for quest in completed_quests:
                                # Show XP before quest completion
                                xp_before = self.gui.game_state.hero['xp'] - quest.reward_xp
                                xp_after = self.gui.game_state.hero['xp']
                                current_level = self.gui.game_state.hero['level']
                                xp_needed_to_level = current_level * 5
                                
                                quest_parts = [
                                    ("\n🏆 Quest Completed: ", "#00ff00"),
                                    (quest.description, "#ffffff"),
                                    (f" (+{quest.reward_xp} XP)", "#ffdd00")
                                ]
                                self.gui._print_colored_parts(quest_parts)
                                
                                # Show detailed XP information
                                if xp_after >= xp_needed_to_level:
                                    level_up_parts = [
                                        ("   💫 Ready to level up! ", "#ffaa00"),
                                        (f"XP: {xp_before} → {xp_after} ", "#8844ff"),
                                        (f"(Need {xp_needed_to_level} for Level {current_level + 1})", "#ffffff")
                                    ]
                                    self.gui._print_colored_parts(level_up_parts)
                                else:
                                    xp_progress_parts = [
                                        ("   📊 XP Progress: ", "#ffffff"),
                                        (f"{xp_before} → {xp_after}", "#8844ff"),
                                        (f"/{xp_needed_to_level} ", "#ffffff"),
                                        (f"({xp_needed_to_level - xp_after} XP to Level {current_level + 1})", "#888888")
                                    ]
                                    self.gui._print_colored_parts(xp_progress_parts)
                            
                            # Clean up completed quests
                            self.gui.quest_manager.clear_completed_quests(self.gui.game_state.hero)
                    else:
                        self.gui.print_text(f"\n💀 Defeat! You lost all your gold!")
                        self.gui.game_state.hero['gold'] = 0
                        self.gui.game_state.hero['lives_left'] -= 1
                        self.gui.game_state.hero['hp'] = self.gui.game_state.hero['maxhp']
                    
                    # Check if game is over (0 lives left)
                    if self.gui.check_game_over():
                        return
                    
                    # Wait before returning to main menu, interface unlocks when main_menu sets buttons
                    self.gui.root.after(3000, self.gui.main_menu)
                
                self.gui.combat.fight(self.gui.game_state.hero, monster, after_fight)
            else:
                # Attempt to run away with 50% chance of monster attack
                self._attempt_run_away(monster)
        
        self.gui.set_buttons(["⚔️ Fight", "🏃 Run"], on_choice)
    
    def _attempt_run_away(self, monster):
        """Attempt to run away with 50% chance of monster attack"""
        # Lock interface during run attempt
        self.gui.lock_interface()
        
        # 50% chance of monster getting an attack in
        monster_attacks = random.choice([True, False])
        
        if monster_attacks:
            self.gui.print_text("\n🏃 You try to run away...")
            self.gui.print_text(f"💀 But {monster['name']} attacks as you flee!")
            
            # Use combat system's damage calculation
            hero = self.gui.game_state.hero
            damage = self.gui.combat.calculate_damage(monster['attack'], hero['defense'])
            
            # Show monster attack animation
            self.gui.combat.current_hero_image = self.current_hero_image
            self.gui.combat.current_monster_image = self.current_monster_image
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
        
        # Play attack sound and show damage
        self.gui.audio.play_sound_effect('buzzer.mp3')
        
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
            self.gui.print_text("\n💀 You collapsed while trying to escape!")
            self.gui.game_state.hero['gold'] = 0
            self.gui.game_state.hero['lives_left'] -= 1
            self.gui.game_state.hero['hp'] = self.gui.game_state.hero['maxhp']
            
            # Check if game is over (0 lives left)
            if self.gui.check_game_over():
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
        img_size = min(canvas_width // 3, canvas_height // 2, 120)
        spacing_x = canvas_width // 3
        start_y = (canvas_height - img_size) // 2
        
        # Final positions for hero (left) and monster (right)
        hero_final_x = spacing_x - img_size // 2
        monster_final_x = 2 * spacing_x - img_size // 2
        final_y = start_y
        
        # Starting positions (off-screen)
        hero_start_x = -img_size  # Off-screen left
        monster_start_x = canvas_width  # Off-screen right
        
        # Animation parameters
        self.animation_step = 0
        self.animation_steps = 15  # Number of animation frames (reduced for faster entrance)
        self.hero_current_x = hero_start_x
        self.monster_current_x = monster_start_x
        
        # Calculate movement per step
        self.hero_step_x = (hero_final_x - hero_start_x) / self.animation_steps
        self.monster_step_x = (monster_final_x - monster_start_x) / self.animation_steps
        
        # Store final positions and image size for animation
        self.hero_final_x = hero_final_x
        self.monster_final_x = monster_final_x
        self.final_y = final_y
        self.img_size = img_size
        
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
        hero_start_x = -self.img_size
        monster_start_x = self.gui._get_canvas_dimensions()[0]
        
        self.hero_current_x = hero_start_x + (self.hero_final_x - hero_start_x) * eased_progress
        self.monster_current_x = monster_start_x + (self.monster_final_x - monster_start_x) * eased_progress
        
        # Add hero image at current position
        hero_id = self.gui._add_canvas_image(
            self.current_hero_image, 
            int(self.hero_current_x), 
            self.final_y, 
            self.img_size, 
            self.img_size
        )
        
        # Add monster image at current position
        monster_id = self.gui._add_canvas_image(
            self.current_monster_image, 
            int(self.monster_current_x), 
            self.final_y, 
            self.img_size, 
            self.img_size
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
                self.img_size, 
                self.img_size
            )
            self.gui._add_canvas_image(
                self.current_monster_image, 
                self.monster_final_x, 
                self.final_y, 
                self.img_size, 
                self.img_size
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

    def _select_random_monster(self):
        """Select random monster"""
        attempts = 0
        while attempts < 100:
            key, value = random.choice(list(self.gui.game_state.monsters.items()))
            hero_level = self.gui.game_state.hero['level']
            if value['level'] <= hero_level * 2 and value['level'] >= hero_level - 1:
                return value.copy()
            attempts += 1
        return None
