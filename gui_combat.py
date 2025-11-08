"""
Combat system for GUI
"""
import random


class CombatGUI:
    """Combat system for GUI"""
    def __init__(self, gui):
        self.gui = gui
    
    def fight(self, hero, monster, callback):
        """Execute fight with GUI updates and attack animations"""
        self.gui.clear_text()
        
        # Lock interface to prevent interruptions during combat
        self.gui.lock_interface()
        
        # Display hero and monster side by side for combat
        self._display_combat_images(hero, monster)
        
        self.gui.print_text("\n⚔️  FIGHT! ⚔️\n")
        
        # Store callback and fight participants for async combat
        self.fight_callback = callback
        self.current_hero = hero
        self.current_monster = monster
        self.round_num = 1
        
        # Start the first round
        self._start_combat_round()

    def _start_combat_round(self):
        """Start a new combat round with proper timing"""
        hero = self.current_hero
        monster = self.current_monster
        
        # Check if combat should continue
        if hero['hp'] <= 0 or monster['hp'] <= 0:
            self._end_combat()
            return
        
        self.gui.print_text(f"--- Round {self.round_num} ---")
        
        # Random initiative - determine who attacks first this round
        hero_goes_first = random.choice([True, False])
        
        # Calculate damage for both attacks
        hero_damage = self.calculate_damage(hero['attack'], monster['defense'])
        monster_damage = self.calculate_damage(monster['attack'], hero['defense'])
        
        if hero_goes_first:
            # Hero attacks first, then monster attacks
            self._show_hero_attack_animation(hero)
            
            # After hero animation completes, apply damage and start monster attack
            self.gui.root.after(1500, lambda: self._complete_hero_attack_start_monster(
                hero_damage, monster_damage, monster, hero, "⚡ You attack for {damage} damage!", self.round_num))
        else:
            # Monster attacks first, then hero attacks
            self._show_monster_attack_animation(monster)
            
            # After monster animation completes, apply damage and start hero attack
            self.gui.root.after(1500, lambda: self._complete_monster_attack_start_hero(
                monster_damage, hero_damage, monster, hero, f"💀 {monster['name']} attacks for {{damage}} damage!", self.round_num))

    def _end_combat(self):
        """End combat and show results"""
        hero = self.current_hero
        monster = self.current_monster
        
        result = 'won' if hero['hp'] > 0 else 'lost'
        
        # Show final result image
        if result == 'won':
            self.gui.show_image('art/you_won.png')
            self.gui.audio.play_sound_effect('win.mp3')
        else:
            self.gui.show_image('art/you_lost.png')
            self.gui.audio.play_sound_effect('death.mp3')
        
        # Unlock interface before calling callback (so next screen can set buttons)
        self.gui.unlock_interface()
        
        self.fight_callback(result)
    
    def _display_combat_images(self, hero, monster):
        """Display hero and monster images side by side for combat"""
        image_paths = []
        
        # Get hero image path
        hero_class = hero.get('class', 'Warrior').lower()
        hero_image_path = f"art/{hero_class.capitalize()}.png"
        
        try:
            import os
            if os.path.exists(hero_image_path):
                image_paths.append(hero_image_path)
            else:
                image_paths.append('art/crossed_swords.png')
        except:
            image_paths.append('art/crossed_swords.png')
        
        # Get monster image path
        if 'art' in monster and monster['art']:
            try:
                if os.path.exists(monster['art']):
                    image_paths.append(monster['art'])
                else:
                    image_paths.append('art/crossed_swords.png')
            except:
                image_paths.append('art/crossed_swords.png')
        else:
            image_paths.append('art/crossed_swords.png')
        
        # Display both images side by side
        self.gui.show_images(image_paths, layout="horizontal")
        
        # Store current images for animation switching
        self.current_hero_image = image_paths[0]
        self.current_monster_image = image_paths[1] if len(image_paths) > 1 else 'art/crossed_swords.png'

    def _show_hero_attack_animation(self, hero):
        """Show hero attack animation - toggle between normal and attack 3 times"""
        hero_class = hero.get('class', 'Warrior').lower()
        attack_image_path = f"art/{hero_class}_attack.png"
        
        try:
            import os
            if os.path.exists(attack_image_path):
                # Start the toggle animation sequence
                self._toggle_attack_animation(0, attack_image_path, self.current_hero_image, self.current_monster_image)
            else:
                # Fallback - keep current display
                self.gui.show_images([self.current_hero_image, self.current_monster_image], layout="horizontal")
        except Exception as e:
            # Fallback - keep current display
            self.gui.show_images([self.current_hero_image, self.current_monster_image], layout="horizontal")

    def _toggle_attack_animation(self, toggle_count, attack_image, normal_image, monster_image):
        """Toggle between normal and attack images with quarter-second delay"""
        if toggle_count < 6:  # 3 complete toggles (normal->attack->normal = 6 steps)
            if toggle_count % 2 == 0:
                # Even count: show attack image
                self.gui.show_images([attack_image, monster_image], layout="horizontal")
            else:
                # Odd count: show normal image
                self.gui.show_images([normal_image, monster_image], layout="horizontal")
            
            # Schedule next toggle after 250ms (quarter second)
            self.gui.root.after(250, lambda: self._toggle_attack_animation(
                toggle_count + 1, attack_image, normal_image, monster_image))
        else:
            # Animation complete - ensure we end with normal hero image
            self.gui.show_images([normal_image, monster_image], layout="horizontal")

    def _complete_hero_attack(self, damage, monster, message_template):
        """Complete hero attack after animation - show damage text and sound"""
        # Play attack sound and show damage
        self.gui.audio.play_sound_effect('punch.mp3')
        
        # Display attack damage with enhanced visual impact
        base_message = message_template.replace("{damage}", "")
        self.gui.print_combat_damage(base_message, damage, "Hero")
        monster['hp'] = max(0, monster['hp'] - damage)
        
        # Return to normal display
        self._return_to_monster_view(monster)

    def _complete_hero_attack_start_monster(self, hero_damage, monster_damage, monster, hero, message_template, round_num):
        """Complete hero attack and start monster counter-attack"""
        # Play attack sound and show hero damage
        self.gui.audio.play_sound_effect('punch.mp3')
        
        # Display damage message with enhanced visual impact
        base_message = message_template.replace("{damage}", "")
        self.gui.print_combat_damage(base_message, hero_damage, "Hero")
        monster['hp'] = max(0, monster['hp'] - hero_damage)
        
        # Check if monster is still alive to counter-attack
        if monster['hp'] <= 0:
            self.gui.root.after(1000, lambda: self._end_combat())
        else:
            # Monster counter-attacks after a brief pause
            self.gui.root.after(1000, lambda: self._start_monster_counter_attack(monster_damage, monster, hero, round_num))
    
    def _start_monster_counter_attack(self, monster_damage, monster, hero, round_num):
        """Start monster counter-attack animation"""
        self._show_monster_attack_animation(monster)
        
        # After monster animation completes, apply damage and finish round
        self.gui.root.after(1500, lambda: self._complete_monster_counter_attack_finish_round(
            monster_damage, monster, hero, f"💀 {monster['name']} counter-attacks for {{damage}} damage!", round_num))
    
    def _complete_hero_attack_finish_round(self, hero_damage, monster, hero, message_template, round_num):
        """Complete hero attack and finish the round (legacy method for single attack rounds)"""
        # Play attack sound and show hero damage
        self.gui.audio.play_sound_effect('punch.mp3')
        
        # Display hero attack damage with enhanced visual impact
        base_message = message_template.replace("{damage}", "")
        self.gui.print_combat_damage(base_message, hero_damage, "Hero")
        monster['hp'] = max(0, monster['hp'] - hero_damage)
        
        # Finish round and show status, then continue to next round
        self._finish_round_status(hero, monster, round_num)
        
        if monster['hp'] <= 0:
            self.gui.root.after(1000, lambda: self._end_combat())
        else:
            self.round_num += 1
            self.gui.root.after(1500, lambda: self._start_combat_round())
    
    def _show_monster_attack_animation(self, monster):
        """Show monster attack animation - toggle between normal and attack 3 times"""
        monster_name = monster.get('name', 'Unknown').lower()
        attack_image_path = f"art/{monster_name}_attack.png"
        
        try:
            import os
            if os.path.exists(attack_image_path):
                # Start the toggle animation sequence for monster
                self._toggle_monster_attack_animation(0, attack_image_path, self.current_monster_image, self.current_hero_image)
            else:
                # Fallback - keep current display
                self.gui.show_images([self.current_hero_image, self.current_monster_image], layout="horizontal")
        except Exception as e:
            # Fallback - keep current display
            self.gui.show_images([self.current_hero_image, self.current_monster_image], layout="horizontal")

    def _toggle_monster_attack_animation(self, toggle_count, attack_image, normal_image, hero_image):
        """Toggle between normal and attack images for monster with quarter-second delay"""
        if toggle_count < 6:  # 3 complete toggles (normal->attack->normal = 6 steps)
            if toggle_count % 2 == 0:
                # Even count: show monster attack image
                self.gui.show_images([hero_image, attack_image], layout="horizontal")
            else:
                # Odd count: show normal monster image
                self.gui.show_images([hero_image, normal_image], layout="horizontal")
            
            # Schedule next toggle after 500ms (slower for visibility)
            self.gui.root.after(500, lambda: self._toggle_monster_attack_animation(
                toggle_count + 1, attack_image, normal_image, hero_image))
        else:
            # Animation complete - ensure we end with normal monster image
            self.gui.show_images([hero_image, normal_image], layout="horizontal")

    def _complete_monster_attack_start_hero(self, monster_damage, hero_damage, monster, hero, message_template, round_num):
        """Complete monster attack and start hero counter-attack"""
        # Play monster attack sound and show damage
        self.gui.audio.play_sound_effect('buzzer.mp3')
        
        # Display damage message with enhanced visual impact  
        base_message = message_template.replace("{damage}", "")
        self.gui.print_combat_damage(base_message, monster_damage, monster['name'])
        hero['hp'] = max(0, hero['hp'] - monster_damage)
        
        # Check if hero is still alive to counter-attack
        if hero['hp'] <= 0:
            self.gui.root.after(1000, lambda: self._end_combat())
        else:
            # Hero counter-attacks after a brief pause
            self.gui.root.after(1000, lambda: self._start_hero_counter_attack(hero_damage, monster, hero, round_num))
    
    def _start_hero_counter_attack(self, hero_damage, monster, hero, round_num):
        """Start hero counter-attack animation"""
        self._show_hero_attack_animation(hero)
        
        # After hero animation completes, apply damage and finish round
        self.gui.root.after(1500, lambda: self._complete_hero_counter_attack_finish_round(
            hero_damage, monster, hero, "⚡ You counter-attack for {damage} damage!", round_num))
    
    def _complete_hero_counter_attack_finish_round(self, hero_damage, monster, hero, message_template, round_num):
        """Complete hero counter-attack and finish the round"""
        # Play attack sound and show hero damage
        self.gui.audio.play_sound_effect('punch.mp3')
        
        # Display counter-attack damage with enhanced visual impact
        base_message = message_template.replace("{damage}", "")
        self.gui.print_combat_damage(base_message, hero_damage, "Hero")
        monster['hp'] = max(0, monster['hp'] - hero_damage)
        
        # Finish round and show status, then continue to next round
        self._finish_round_status(hero, monster, round_num)
        
        if monster['hp'] <= 0:
            self.gui.root.after(1000, lambda: self._end_combat())
        else:
            self.round_num += 1
            self.gui.root.after(1500, lambda: self._start_combat_round())
    
    def _complete_monster_counter_attack_finish_round(self, monster_damage, monster, hero, message_template, round_num):
        """Complete monster counter-attack and finish the round"""
        # Play monster attack sound and show damage
        self.gui.audio.play_sound_effect('buzzer.mp3')
        
        # Display monster counter-attack damage with enhanced visual impact
        base_message = message_template.replace("{damage}", "")
        self.gui.print_combat_damage(base_message, monster_damage, monster['name'])
        hero['hp'] = max(0, hero['hp'] - monster_damage)
        
        # Finish round and show status, then continue to next round
        self._finish_round_status(hero, monster, round_num)
        
        if hero['hp'] <= 0:
            self.gui.root.after(1000, lambda: self._end_combat())
        else:
            self.round_num += 1
            self.gui.root.after(1500, lambda: self._start_combat_round())
    
    def _complete_monster_attack_finish_round(self, monster_damage, monster, hero, message_template, round_num):
        """Complete monster attack and finish the round (legacy method for single attack rounds)"""
        # Play monster attack sound and show damage
        self.gui.audio.play_sound_effect('buzzer.mp3')
        
        # Display monster attack damage with enhanced visual impact
        base_message = message_template.replace("{damage}", "")
        self.gui.print_combat_damage(base_message, monster_damage, monster['name'])
        hero['hp'] = max(0, hero['hp'] - monster_damage)
        
        # Finish round and show status, then continue to next round
        self._finish_round_status(hero, monster, round_num)
        
        if hero['hp'] <= 0:
            self.gui.root.after(1000, lambda: self._end_combat())
        else:
            self.round_num += 1
            self.gui.root.after(1500, lambda: self._start_combat_round())

    def _finish_round_status(self, hero, monster, round_num):
        """Show round status and return to normal display"""
        # Display HP status with colored values
        status_parts = [
            ("Your HP: ", "#00ff00"),
            (str(hero['hp']), "#ff4444"),
            (" | ", "#00ff00"),
            (monster['name'], "#ffaa00"),
            (" HP: ", "#00ff00"),
            (str(monster['hp']), "#ff4444"),
            ("\n", "#00ff00")
        ]
        self.gui._print_colored_parts(status_parts)
        self._return_to_monster_view(monster)

    def _return_to_monster_view(self, monster):
        """Return to normal hero and monster display after attack"""
        try:
            # Return to normal hero and monster images
            self.gui.show_images([self.current_hero_image, self.current_monster_image], layout="horizontal")
        except Exception as e:
            # Fallback - show both as crossed swords
            self.gui.show_images(['art/crossed_swords.png', 'art/crossed_swords.png'], layout="horizontal")

    def calculate_damage(self, attack, defense):
        strike = random.randint(1, max(1, attack)) * 2
        damage = strike - defense
        return max(1, damage)
