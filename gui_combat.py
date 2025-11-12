"""
Combat system for GUI
"""
import random
from typing import Callable, Dict, Any, Optional
from gui_interfaces import GameContextProtocol
from logger_utils import get_logger

logger = get_logger(__name__)


class CombatGUI:
    """Combat system for GUI using dependency injection"""
    def __init__(self, 
                 text_display,
                 image_display, 
                 audio,
                 interface_control,
                 timer,
                 game_state):
        """Initialize combat system with specific dependencies.
        
        Args:
            text_display: Object with print_text(), clear_text(), print_combat_damage(), _print_colored_parts()
            image_display: Object with show_image(), _clear_foreground_images(), _add_canvas_image(), _get_canvas_dimensions()
            audio: Object with play_sound_effect() method
            interface_control: Object with lock_interface(), unlock_interface() methods
            timer: Object with after() method for scheduling callbacks (typically tkinter root)
            game_state: Object with game state data
        """
        self.text_display = text_display
        self.image_display = image_display
        self.audio = audio
        self.interface_control = interface_control
        self.timer = timer
        self.game_state = game_state
    
    def fight(self, hero, monster, callback):
        """Execute fight with GUI updates and attack animations"""
        self.text_display.clear_text()
        
        # Lock interface to prevent interruptions during combat
        self.interface_control.lock_interface()
        
        # Display hero and monster side by side for combat
        self._display_combat_images(hero, monster)
        
        self.text_display.print_text("\n⚔️  FIGHT! ⚔️\n")
        
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
        
        self.text_display.print_text(f"--- Round {self.round_num} ---")
        
        # Random initiative - determine who attacks first this round
        hero_goes_first = random.choice([True, False])
        
        # Calculate damage for both attacks (with level consideration)
        hero_level = hero.get('level', 1)
        monster_level = monster.get('level', 1)
        hero_damage = self.calculate_damage(hero['attack'], monster['defense'], hero_level, monster_level)
        monster_damage = self.calculate_damage(monster['attack'], hero['defense'], monster_level, hero_level)
        
        if hero_goes_first:
            # Hero attacks first, then monster attacks
            self._show_hero_attack_animation(hero)
            
            # After hero animation completes, apply damage and start monster attack
            self.timer.after(1500, lambda: self._complete_hero_attack_start_monster(
                hero_damage, monster_damage, monster, hero, "⚡ You attack for {damage} damage!", self.round_num))
        else:
            # Monster attacks first, then hero attacks
            self._show_monster_attack_animation(monster)
            
            # After monster animation completes, apply damage and start hero attack
            self.timer.after(1500, lambda: self._complete_monster_attack_start_hero(
                monster_damage, hero_damage, monster, hero, f"💀 {monster['name']} attacks for {{damage}} damage!", self.round_num))

    def _end_combat(self):
        """End combat and show results"""
        hero = self.current_hero
        monster = self.current_monster
        
        result = 'won' if hero['hp'] > 0 else 'lost'
        
        # Check if this is a final boss victory for special animation
        monster_data = getattr(self, 'current_monster_data', {})
        is_final_boss_victory = (result == 'won' and 
                               monster_data.get('finalboss', False))
        
        if is_final_boss_victory:
            # For final boss victory, start epic fireworks animation with interface locked
            self._start_victory_fireworks_animation()
        else:
            # Standard victory/defeat handling
            if result == 'won':
                self.image_display.show_image('art/you_won.png')
                self.audio.play_sound_effect('win.mp3')
            else:
                self.image_display.show_image('art/you_lost.png')
                self.audio.play_sound_effect('death.mp3')
            
            # Unlock interface before calling callback (so next screen can set buttons)
            self.interface_control.unlock_interface()
            
            self.fight_callback(result)
    
    def _display_combat_images(self, hero, monster):
        """Display hero and monster images side by side for combat with Dragon boss special sizing"""
        # Get hero image path
        hero_class = hero.get('class', 'Warrior').lower()
        hero_image_path = f"art/{hero_class.capitalize()}.png"
        
        try:
            import os
            if os.path.exists(hero_image_path):
                self.current_hero_image = hero_image_path
            else:
                self.current_hero_image = 'art/crossed_swords.png'
        except (OSError, TypeError) as e:
            logger.debug(f"Could not access hero image, using fallback: {e}")
            self.current_hero_image = 'art/crossed_swords.png'
        
        # Get monster image path
        if 'art' in monster and monster['art']:
            try:
                if os.path.exists(monster['art']):
                    self.current_monster_image = monster['art']
                else:
                    self.current_monster_image = 'art/crossed_swords.png'
            except (OSError, TypeError) as e:
                logger.debug(f"Could not access monster image, using fallback: {e}")
                self.current_monster_image = 'art/crossed_swords.png'
        else:
            self.current_monster_image = 'art/crossed_swords.png'
        
        # Store monster data for Dragon boss detection
        self.current_monster_data = monster
        
        # Use custom display logic for Dragon boss sizing
        self._display_combat_images_with_sizing()
    
    def _get_monster_attack_sound(self, monster):
        """Get the appropriate attack sound for the monster"""
        # Check if monster has custom attack_sound defined
        if 'attack_sound' in monster and monster['attack_sound']:
            return monster['attack_sound']
        else:
            # Use default monster attack sound
            return 'buzzer.mp3'
    
    def _display_combat_images_with_sizing(self):
        """Display hero and monster images with special Dragon boss sizing"""
        # Clear existing foreground images
        self.image_display._clear_foreground_images()
        
        # Get canvas dimensions for positioning
        canvas_width, canvas_height = self.image_display._get_canvas_dimensions()
        
        # Calculate final positions (same logic as encounter system)
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
        
        # Store sizes for animation methods
        self.hero_img_size = hero_img_size
        self.monster_img_size = monster_img_size
        self.combat_hero_x = hero_final_x
        self.combat_monster_x = monster_final_x
        self.combat_y = final_y
        
        # Display both images with appropriate sizes
        self.image_display._add_canvas_image(
            self.current_hero_image, 
            hero_final_x, 
            final_y, 
            hero_img_size, 
            hero_img_size
        )
        self.image_display._add_canvas_image(
            self.current_monster_image, 
            monster_final_x, 
            final_y, 
            monster_img_size, 
            monster_img_size
        )

    def _show_hero_attack_animation(self, hero):
        """Show hero attack animation - toggle between normal and attack 3 times"""
        # Play hero attack sound at the start of animation
        self.audio.play_sound_effect('punch.mp3')
        
        hero_class = hero.get('class', 'Warrior').lower()
        attack_image_path = f"art/{hero_class}_attack.png"
        
        try:
            import os
            if os.path.exists(attack_image_path):
                # Start the toggle animation sequence
                self._toggle_attack_animation(0, attack_image_path, self.current_hero_image, self.current_monster_image)
            else:
                # Fallback - keep current display
                self._display_combat_images_with_sizing()
        except Exception as e:
            # Fallback - keep current display
            self._display_combat_images_with_sizing()

    def _toggle_attack_animation(self, toggle_count, attack_image, normal_image, monster_image):
        """Toggle between normal and attack images with quarter-second delay using custom sizing"""
        if toggle_count < 6:  # 3 complete toggles (normal->attack->normal = 6 steps)
            # Clear and redraw with appropriate image
            self.image_display._clear_foreground_images()
            
            if toggle_count % 2 == 0:
                # Even count: show attack image
                hero_image = attack_image
            else:
                # Odd count: show normal image
                hero_image = normal_image
            
            # Display with custom sizing for Dragon boss
            self.image_display._add_canvas_image(
                hero_image, 
                self.combat_hero_x, 
                self.combat_y, 
                self.hero_img_size, 
                self.hero_img_size
            )
            self.image_display._add_canvas_image(
                monster_image, 
                self.combat_monster_x, 
                self.combat_y, 
                self.monster_img_size, 
                self.monster_img_size
            )
            
            # Schedule next toggle after 250ms (quarter second)
            self.timer.after(250, lambda: self._toggle_attack_animation(
                toggle_count + 1, attack_image, normal_image, monster_image))
        else:
            # Animation complete - ensure we end with normal hero image
            self._display_combat_images_with_sizing()

    def _complete_hero_attack(self, damage, monster, message_template):
        """Complete hero attack after animation - show damage text"""
        # Show hero damage (sound already played at start of animation)
        
        # Display attack damage with enhanced visual impact
        base_message = message_template.replace("{damage}", "")
        self.text_display.print_combat_damage(base_message, damage, "Hero")
        monster['hp'] = max(0, monster['hp'] - damage)
        
        # Return to normal display
        self._return_to_monster_view(monster)

    def _complete_hero_attack_start_monster(self, hero_damage, monster_damage, monster, hero, message_template, round_num):
        """Complete hero attack and start monster counter-attack"""
        # Show hero damage (sound already played at start of animation)
        
        # Display damage message with enhanced visual impact
        base_message = message_template.replace("{damage}", "")
        self.text_display.print_combat_damage(base_message, hero_damage, "Hero")
        monster['hp'] = max(0, monster['hp'] - hero_damage)
        
        # Check if monster is still alive to counter-attack
        if monster['hp'] <= 0:
            self.timer.after(1000, lambda: self._end_combat())
        else:
            # Monster counter-attacks after a brief pause
            self.timer.after(1000, lambda: self._start_monster_counter_attack(monster_damage, monster, hero, round_num))
    
    def _start_monster_counter_attack(self, monster_damage, monster, hero, round_num):
        """Start monster counter-attack animation"""
        self._show_monster_attack_animation(monster)
        
        # After monster animation completes, apply damage and finish round
        self.timer.after(1500, lambda: self._complete_monster_counter_attack_finish_round(
            monster_damage, monster, hero, f"💀 {monster['name']} counter-attacks for {{damage}} damage!", round_num))
    
    def _complete_hero_attack_finish_round(self, hero_damage, monster, hero, message_template, round_num):
        """Complete hero attack and finish the round (legacy method for single attack rounds)"""
        # Show hero damage (sound already played at start of animation)
        
        # Display hero attack damage with enhanced visual impact
        base_message = message_template.replace("{damage}", "")
        self.text_display.print_combat_damage(base_message, hero_damage, "Hero")
        monster['hp'] = max(0, monster['hp'] - hero_damage)
        
        # Finish round and show status, then continue to next round
        self._finish_round_status(hero, monster, round_num)
        
        if monster['hp'] <= 0:
            self.timer.after(1000, lambda: self._end_combat())
        else:
            self.round_num += 1
            self.timer.after(1500, lambda: self._start_combat_round())
    
    def _show_monster_attack_animation(self, monster):
        """Show monster attack animation - toggle between normal and attack 3 times"""
        # Play monster attack sound at the start of animation (limited to 3 seconds)
        attack_sound = self._get_monster_attack_sound(monster)
        self.audio.play_sound_effect(attack_sound, max_duration_ms=3000)
        
        # Check for attack_art key first (preferred method)
        if 'attack_art' in monster and monster['attack_art']:
            attack_image_path = monster['attack_art']
        # Special handling for Dragon boss attack image (legacy)
        elif (getattr(self, 'current_monster_data', {}).get('finalboss', False) and 
              'dragon_endboss' in self.current_monster_image.lower()):
            attack_image_path = "art/dragon_endboss_attack.png"
        # Use the art field to derive attack image path (fallback for backwards compatibility)
        elif 'art' in monster and monster['art']:
            base_art_path = monster['art']
            # Try the direct replacement first (e.g., monster.png -> monster_attack.png)
            attack_image_path = base_art_path.replace('.png', '_attack.png')
            
            # If that doesn't exist, try removing "_monster" from the path
            import os
            if not os.path.exists(attack_image_path):
                # Try pattern like kraken_monster.png -> kraken_attack.png
                alt_path = base_art_path.replace('_monster.png', '_attack.png')
                if os.path.exists(alt_path):
                    attack_image_path = alt_path
        else:
            # Final fallback to old method if no art field
            monster_name = monster.get('name', 'Unknown').lower()
            attack_image_path = f"art/{monster_name}_attack.png"
        
        try:
            import os
            if os.path.exists(attack_image_path):
                # Start the toggle animation sequence for monster
                self._toggle_monster_attack_animation(0, attack_image_path, self.current_monster_image, self.current_hero_image)
            else:
                # Fallback - keep current display
                self._display_combat_images_with_sizing()
        except Exception as e:
            # Fallback - keep current display
            self._display_combat_images_with_sizing()

    def _toggle_monster_attack_animation(self, toggle_count, attack_image, normal_image, hero_image):
        """Toggle between normal and attack images for monster with quarter-second delay using custom sizing"""
        if toggle_count < 6:  # 3 complete toggles (normal->attack->normal = 6 steps)
            # Clear and redraw with appropriate image
            self.image_display._clear_foreground_images()
            
            if toggle_count % 2 == 0:
                # Even count: show monster attack image
                monster_image = attack_image
            else:
                # Odd count: show normal monster image
                monster_image = normal_image
            
            # Display with custom sizing for Dragon boss
            self.image_display._add_canvas_image(
                hero_image, 
                self.combat_hero_x, 
                self.combat_y, 
                self.hero_img_size, 
                self.hero_img_size
            )
            self.image_display._add_canvas_image(
                monster_image, 
                self.combat_monster_x, 
                self.combat_y, 
                self.monster_img_size, 
                self.monster_img_size
            )
            
            # Schedule next toggle after 500ms (slower for visibility)
            self.timer.after(500, lambda: self._toggle_monster_attack_animation(
                toggle_count + 1, attack_image, normal_image, hero_image))
        else:
            # Animation complete - ensure we end with normal monster image
            self._display_combat_images_with_sizing()

    def _complete_monster_attack_start_hero(self, monster_damage, hero_damage, monster, hero, message_template, round_num):
        """Complete monster attack and start hero counter-attack"""
        # Show damage (sound already played at start of animation)
        
        # Display damage message with enhanced visual impact  
        base_message = message_template.replace("{damage}", "")
        self.text_display.print_combat_damage(base_message, monster_damage, monster['name'])
        hero['hp'] = max(0, hero['hp'] - monster_damage)
        
        # Check if hero is still alive to counter-attack
        if hero['hp'] <= 0:
            self.timer.after(1000, lambda: self._end_combat())
        else:
            # Hero counter-attacks after a brief pause
            self.timer.after(1000, lambda: self._start_hero_counter_attack(hero_damage, monster, hero, round_num))
    
    def _start_hero_counter_attack(self, hero_damage, monster, hero, round_num):
        """Start hero counter-attack animation"""
        self._show_hero_attack_animation(hero)
        
        # After hero animation completes, apply damage and finish round
        self.timer.after(1500, lambda: self._complete_hero_counter_attack_finish_round(
            hero_damage, monster, hero, "⚡ You counter-attack for {damage} damage!", round_num))
    
    def _complete_hero_counter_attack_finish_round(self, hero_damage, monster, hero, message_template, round_num):
        """Complete hero counter-attack and finish the round"""
        # Show hero damage (sound already played at start of animation)
        
        # Display counter-attack damage with enhanced visual impact
        base_message = message_template.replace("{damage}", "")
        self.text_display.print_combat_damage(base_message, hero_damage, "Hero")
        monster['hp'] = max(0, monster['hp'] - hero_damage)
        
        # Finish round and show status, then continue to next round
        self._finish_round_status(hero, monster, round_num)
        
        if monster['hp'] <= 0:
            self.timer.after(1000, lambda: self._end_combat())
        else:
            self.round_num += 1
            self.timer.after(1500, lambda: self._start_combat_round())
    
    def _complete_monster_counter_attack_finish_round(self, monster_damage, monster, hero, message_template, round_num):
        """Complete monster counter-attack and finish the round"""
        # Show damage (sound already played at start of animation)
        
        # Display monster counter-attack damage with enhanced visual impact
        base_message = message_template.replace("{damage}", "")
        self.text_display.print_combat_damage(base_message, monster_damage, monster['name'])
        hero['hp'] = max(0, hero['hp'] - monster_damage)
        
        # Finish round and show status, then continue to next round
        self._finish_round_status(hero, monster, round_num)
        
        if hero['hp'] <= 0:
            self.timer.after(1000, lambda: self._end_combat())
        else:
            self.round_num += 1
            self.timer.after(1500, lambda: self._start_combat_round())
    
    def _complete_monster_attack_finish_round(self, monster_damage, monster, hero, message_template, round_num):
        """Complete monster attack and finish the round (legacy method for single attack rounds)"""
        # Show damage (sound already played at start of animation)
        
        # Display monster attack damage with enhanced visual impact
        base_message = message_template.replace("{damage}", "")
        self.text_display.print_combat_damage(base_message, monster_damage, monster['name'])
        hero['hp'] = max(0, hero['hp'] - monster_damage)
        
        # Finish round and show status, then continue to next round
        self._finish_round_status(hero, monster, round_num)
        
        if hero['hp'] <= 0:
            self.timer.after(1000, lambda: self._end_combat())
        else:
            self.round_num += 1
            self.timer.after(1500, lambda: self._start_combat_round())

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
        self.text_display._print_colored_parts(status_parts)
        self._return_to_monster_view(monster)

    def _return_to_monster_view(self, monster):
        """Return to normal hero and monster display after attack"""
        try:
            # Return to normal hero and monster images with custom sizing
            self._display_combat_images_with_sizing()
        except Exception as e:
            # Fallback - show both as crossed swords with normal sizing
            self.image_display._clear_foreground_images()
            canvas_width, canvas_height = self.image_display._get_canvas_dimensions()
            img_size = 120
            spacing_x = canvas_width // 3
            start_y = (canvas_height - img_size) // 2
            
            self.image_display._add_canvas_image('art/crossed_swords.png', spacing_x - img_size // 2, start_y, img_size, img_size)
            self.image_display._add_canvas_image('art/crossed_swords.png', 2 * spacing_x - img_size // 2, start_y, img_size, img_size)

    def calculate_damage(self, attack, defense, attacker_level=1, defender_level=1):
        """Improved damage calculation with level consideration"""
        import random
        
        # Base damage with controlled randomness (80-120% of attack)
        variance = random.uniform(0.8, 1.2)
        base_damage = attack * variance
        
        # Level differential bonus/penalty (±15% per level difference, capped at ±75%)
        level_diff = max(-5, min(5, attacker_level - defender_level))
        level_modifier = 1.0 + (level_diff * 0.15)
        base_damage *= level_modifier
        
        # Defense as damage reduction percentage (diminishing returns)
        defense_percentage = defense / (defense + 15)
        defense_percentage = min(0.85, defense_percentage)  # Cap at 85% reduction
        
        final_damage = base_damage * (1 - defense_percentage)
        
        # Minimum damage scales with attacker level
        min_damage = max(1, (attacker_level + 1) // 2)
        
        return max(min_damage, int(round(final_damage)))
    
    def _start_victory_fireworks_animation(self):
        """Start epic victory fireworks animation for final boss defeat"""
        # Keep interface locked during animation to prevent interruptions
        self.interface_control.lock_interface()
        
        # Play epic fireworks victory sound at start
        self.audio.play_sound_effect('win-fireworks.mp3')
        
        # Start fireworks animation sequence - 4 frames, 1.5 seconds each
        self._show_fireworks_frame(1)
    
    def _show_fireworks_frame(self, frame_number):
        """Show specific fireworks frame and schedule next one"""
        try:
            # Show the fireworks frame
            self.image_display.show_image(f'art/victory_fireworks_{frame_number}.png')
            
            if frame_number < 4:
                # Schedule next frame after 1.5 seconds
                self.timer.after(1500, lambda: self._show_fireworks_frame(frame_number + 1))
            else:
                # Animation complete - show final victory screen and end
                self.timer.after(1500, self._complete_victory_animation)
        except Exception as e:
            # Fallback if fireworks images not found
            self._complete_victory_animation()
    
    def _complete_victory_animation(self):
        """Complete the victory animation and return control"""
        # Show final victory screen
        self.image_display.show_image('art/you_won.png')
        
        # Unlock interface before calling callback
        self.interface_control.unlock_interface()
        
        # Call the fight callback with victory result
        self.fight_callback('won')
