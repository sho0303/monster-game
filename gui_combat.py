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
        
        if hero_goes_first:
            # Hero attacks - show attack animation, then damage
            hero_damage = self.calculate_damage(hero['attack'], monster['defense'])
            self._show_hero_attack_animation(hero)
            
            # After hero animation completes, show damage and finish round
            self.gui.root.after(1500, lambda: self._complete_hero_attack_finish_round(
                hero_damage, monster, hero, "⚡ You attack for {damage} damage!", self.round_num))
        else:
            # Monster attacks - show attack animation, then damage
            monster_damage = self.calculate_damage(monster['attack'], hero['defense'])
            self._show_monster_attack_animation(monster)
            
            # After monster animation completes, show damage and finish round
            self.gui.root.after(1500, lambda: self._complete_monster_attack_finish_round(
                monster_damage, monster, hero, f"💀 {monster['name']} attacks for {{damage}} damage!", self.round_num))

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
        self.gui.print_text(message_template.format(damage=damage))
        monster['hp'] = max(0, monster['hp'] - damage)
        
        # Return to normal display
        self._return_to_monster_view(monster)

    def _complete_hero_attack_finish_round(self, hero_damage, monster, hero, message_template, round_num):
        """Complete hero attack and finish the round"""
        # Play attack sound and show hero damage
        self.gui.audio.play_sound_effect('punch.mp3')
        self.gui.print_text(message_template.format(damage=hero_damage))
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

    def _complete_monster_attack_finish_round(self, monster_damage, monster, hero, message_template, round_num):
        """Complete monster attack and finish the round"""
        # Play monster attack sound and show damage
        self.gui.audio.play_sound_effect('buzzer.mp3')
        self.gui.print_text(message_template.format(damage=monster_damage))
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
        self.gui.print_text(f"Your HP: {hero['hp']} | {monster['name']} HP: {monster['hp']}\n")
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
