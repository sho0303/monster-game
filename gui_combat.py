"""
Combat system for GUI
"""
import random
from typing import Callable, Dict, Any, Optional
from gui_interfaces import GameContextProtocol
from logger_utils import get_logger
from resource_utils import resource_exists, get_resource_path

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
                
                # Unlock interface before calling callback (so next screen can set buttons)
                self.interface_control.unlock_interface()
                
                self.fight_callback(result)
            else:
                # Hero died - show death in combat display
                # Play death sound immediately
                self.audio.play_sound_effect('death.mp3')
                
                # Replace hero image with death image in combat display
                self._show_hero_death_in_combat(hero)
                
                # Hold death scene for 3 seconds, then transition
                self.timer.after(3000, lambda: self._complete_death_sequence(result))
    
    def _display_combat_images(self, hero, monster):
        """Display hero and monster images side by side for combat with Dragon boss special sizing"""
        # Get hero image path from YAML or construct fallback
        hero_image_path = hero.get('art', '')
        
        try:
            if hero_image_path and resource_exists(hero_image_path):
                self.current_hero_image = hero_image_path
            else:
                # Fallback to class-based path if art field missing
                hero_class = hero.get('class', 'Warrior').lower()
                fallback_path = f"art/{hero_class.capitalize()}.png"
                if resource_exists(fallback_path):
                    self.current_hero_image = fallback_path
                else:
                    self.current_hero_image = 'art/crossed_swords.png'
        except (OSError, TypeError) as e:
            logger.debug(f"Could not access hero image, using fallback: {e}")
            self.current_hero_image = 'art/crossed_swords.png'
        
        # Get monster image path
        if 'art' in monster and monster['art']:
            try:
                if resource_exists(monster['art']):
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
    
    def _get_hero_attack_sound(self, hero):
        """Get the appropriate attack sound for the hero"""
        # Check if hero has custom attack_sound defined
        if 'attack_sound' in hero and hero['attack_sound']:
            return hero['attack_sound']
        else:
            # Use default hero attack sound
            return 'punch.mp3'
    
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
        
        # Apply biome-specific floor offset for proper positioning
        floor_offset = self.image_display.background_manager.get_floor_offset()
        start_y += floor_offset
        
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
        """Show hero attack animation with jump forward, attack, and jump back"""
        # Start with jump forward animation
        self._animate_hero_jump_forward(hero)
    
    def _animate_hero_jump_forward(self, hero):
        """Animate hero jumping forward toward monster"""
        # Calculate jump distance (move 30% toward monster)
        jump_distance = int((self.combat_monster_x - self.combat_hero_x) * 0.3)
        
        # Store original position
        self.hero_original_x = self.combat_hero_x
        
        # Animate jump in 3 steps (150ms total)
        self._jump_step(self.combat_hero_x, jump_distance, 3, 0, 'hero', 
                       lambda: self._start_hero_attack_after_jump(hero))
    
    def _start_hero_attack_after_jump(self, hero):
        """Start hero attack animation after jump forward"""
        # Play hero-specific attack sound at the start of animation
        hero_attack_sound = self._get_hero_attack_sound(hero)
        self.audio.play_sound_effect(hero_attack_sound)
        
        # Get attack image from YAML or construct fallback
        attack_image_path = hero.get('art_attack', '')
        
        try:
            if not attack_image_path:
                # Fallback to class-based path if art_attack field missing
                hero_class = hero.get('class', 'Warrior').lower()
                attack_image_path = f"art/{hero_class}_attack.png"
            
            if resource_exists(attack_image_path):
                # Start the toggle animation sequence
                self._toggle_hero_attack_animation(0, attack_image_path, self.current_hero_image)
            else:
                # Fallback - jump back without attack animation
                self._animate_hero_jump_back()
        except Exception as e:
            # Fallback - jump back without attack animation
            self._animate_hero_jump_back()
    
    def _toggle_hero_attack_animation(self, toggle_count, attack_image, normal_image):
        """Toggle between normal and attack images for hero"""
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
                self.current_monster_image, 
                self.combat_monster_x, 
                self.combat_y, 
                self.monster_img_size, 
                self.monster_img_size
            )
            
            # Schedule next toggle after 250ms (quarter second)
            self.timer.after(250, lambda: self._toggle_hero_attack_animation(
                toggle_count + 1, attack_image, normal_image))
        else:
            # Animation complete - jump back
            self._animate_hero_jump_back()
    
    def _animate_hero_jump_back(self):
        """Animate hero jumping back to original position"""
        # Calculate distance to jump back
        jump_distance = self.hero_original_x - self.combat_hero_x
        
        # Animate jump back in 3 steps (150ms total)
        self._jump_step(self.combat_hero_x, jump_distance, 3, 0, 'hero', 
                       self._display_combat_images_with_sizing)
    
    def _jump_step(self, start_x, total_distance, total_steps, current_step, attacker_type, callback):
        """Animate a single jump step"""
        if current_step < total_steps:
            # Calculate new position
            step_distance = total_distance // total_steps
            new_x = start_x + step_distance
            
            # Update position
            if attacker_type == 'hero':
                self.combat_hero_x = new_x
            else:  # monster
                self.combat_monster_x = new_x
            
            # Redraw images at new position
            self.image_display._clear_foreground_images()
            self.image_display._add_canvas_image(
                self.current_hero_image, 
                self.combat_hero_x, 
                self.combat_y, 
                self.hero_img_size, 
                self.hero_img_size
            )
            self.image_display._add_canvas_image(
                self.current_monster_image, 
                self.combat_monster_x, 
                self.combat_y, 
                self.monster_img_size, 
                self.monster_img_size
            )
            
            # Schedule next step after 50ms
            self.timer.after(50, lambda: self._jump_step(
                new_x, total_distance - step_distance, total_steps, current_step + 1, 
                attacker_type, callback))
        else:
            # Jump complete - call callback
            callback()

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
        """Show monster attack animation with jump forward, attack, and jump back"""
        # Start with jump forward animation
        self._animate_monster_jump_forward(monster)
    
    def _animate_monster_jump_forward(self, monster):
        """Animate monster jumping forward toward hero"""
        # Calculate jump distance (move 30% toward hero)
        jump_distance = int((self.combat_hero_x - self.combat_monster_x) * 0.3)
        
        # Store original position
        self.monster_original_x = self.combat_monster_x
        
        # Animate jump in 3 steps (150ms total)
        self._jump_step(self.combat_monster_x, jump_distance, 3, 0, 'monster', 
                       lambda: self._start_monster_attack_after_jump(monster))
    
    def _start_monster_attack_after_jump(self, monster):
        """Start monster attack animation after jump forward"""
        # Play monster attack sound at the start of animation (limited to 3 seconds)
        attack_sound = self._get_monster_attack_sound(monster)
        self.audio.play_sound_effect(attack_sound, max_duration_ms=3000)
        
        # Get monster attack image if available - check both field names for compatibility
        attack_art_path = monster.get('art_attack') or monster.get('attack_art')
        
        if attack_art_path:
            try:
                if resource_exists(attack_art_path):
                    # Start the toggle animation sequence
                    self._toggle_monster_attack_animation(0, attack_art_path, self.current_monster_image)
                else:
                    # No attack art - jump back without animation
                    self._animate_monster_jump_back()
            except Exception as e:
                # Fallback - jump back without animation
                self._animate_monster_jump_back()
        else:
            # No attack art - jump back without animation
            self._animate_monster_jump_back()
    
    def _toggle_monster_attack_animation(self, toggle_count, attack_image, normal_image):
        """Toggle between normal and attack images for monster"""
        if toggle_count < 6:  # 3 complete toggles (normal->attack->normal = 6 steps)
            # Clear and redraw with appropriate image
            self.image_display._clear_foreground_images()
            
            if toggle_count % 2 == 0:
                # Even count: show attack image
                monster_image = attack_image
            else:
                # Odd count: show normal image
                monster_image = normal_image
            
            # Display with custom sizing for Dragon boss
            self.image_display._add_canvas_image(
                self.current_hero_image, 
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
            self.timer.after(250, lambda: self._toggle_monster_attack_animation(
                toggle_count + 1, attack_image, normal_image))
        else:
            # Animation complete - jump back
            self._animate_monster_jump_back()
    
    def _animate_monster_jump_back(self):
        """Animate monster jumping back to original position"""
        # Calculate distance to jump back
        jump_distance = self.monster_original_x - self.combat_monster_x
        
        # Animate jump back in 3 steps (150ms total)
        self._jump_step(self.combat_monster_x, jump_distance, 3, 0, 'monster', 
                       self._display_combat_images_with_sizing)

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
            
            # Apply biome-specific floor offset
            floor_offset = self.image_display.background_manager.get_floor_offset()
            start_y += floor_offset
            
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
    
    def _show_hero_death_in_combat(self, hero):
        """Replace hero image with death image in combat display, keeping monster visible"""
        try:
            # Get death image from YAML or construct fallback
            death_image_path = hero.get('art_death', '')
            
            if not death_image_path:
                # Fallback to class-based path if art_death field missing
                hero_class = hero.get('class', 'Warrior').lower()
                death_image_path = f"art/{hero_class}_death.png"
            
            # Check if death image exists
            if not resource_exists(death_image_path):
                logger.debug(f"Death image not found: {death_image_path}, using generic")
                death_image_path = 'art/you_lost.png'
            
            # Update the current hero image to the death image
            self.current_hero_image = death_image_path
            
            # Redisplay combat images with hero now showing death pose
            self._display_combat_images_with_sizing()
            
        except Exception as e:
            logger.debug(f"Error loading death image in combat: {e}")
            # Fallback to showing you_lost full screen
            self.image_display.show_image('art/you_lost.png')
    
    def _complete_death_sequence(self, result):
        """Complete the death sequence and return control"""
        # Unlock interface before calling callback
        self.interface_control.unlock_interface()
        
        # Call the fight callback with defeat result
        self.fight_callback(result)
    
    def start_wagon_death_event(self, hero):
        """Special event: Wagon runs over the hero who saved the world"""
        self.text_display.clear_text()
        
        # Lock interface during the event
        self.interface_control.lock_interface()
        
        # Clear any existing images
        self.image_display._clear_foreground_images()
        
        # Get canvas dimensions for positioning
        canvas_width, canvas_height = self.image_display._get_canvas_dimensions()
        
        # Get hero class for death image later
        hero_class = hero.get('class', 'Warrior').lower()
        
        # Display hero on the left (normal position)
        hero_image_path = hero.get('art', '')
        if not hero_image_path:
            # Fallback to class-based path if art field missing
            hero_image_path = f'art/{hero_class}.png'
        
        # Calculate base image size (same as combat)
        base_img_size = min(canvas_width // 3, canvas_height // 2, 120)
        
        # Calculate vertical position (same centering logic as combat)
        start_y = (canvas_height - base_img_size) // 2
        
        # Apply biome-specific floor offset
        floor_offset = self.image_display.background_manager.get_floor_offset()
        start_y += floor_offset
        
        # Position hero on left side (same horizontal spacing as combat)
        spacing_x = canvas_width // 3
        hero_x = spacing_x - base_img_size // 2
        hero_y = start_y
        
        self.image_display._add_canvas_image(hero_image_path, hero_x, hero_y, tags='hero')
        
        # Display wagon on the right side (will animate left)
        wagon_start_x = canvas_width - 50  # Start from right edge
        wagon_y = start_y
        wagon_image_id = self.image_display._add_canvas_image('art/wagon.png', wagon_start_x, wagon_y, tags='wagon')
        
        # Play honk sound before wagon starts moving
        self.audio.play_sound_effect('honk.mp3')
        
        # Calculate target position (just past the hero)
        target_x = hero_x - 20  # Overlap slightly for collision effect
        
        # Start wagon animation
        self._animate_wagon(wagon_image_id, wagon_start_x, wagon_y, target_x, hero, hero_class, hero_x, hero_y)
    
    def _animate_wagon(self, wagon_id, current_x, wagon_y, target_x, hero, hero_class, hero_x, hero_y):
        """Animate wagon moving left towards hero"""
        step_size = 10  # Pixels per frame
        
        if current_x > target_x:
            # Continue moving left
            new_x = current_x - step_size
            
            # Update wagon position on canvas
            canvas = self.image_display.image_canvas
            canvas.coords(wagon_id, new_x, wagon_y)
            
            # Schedule next frame (30 FPS = ~33ms per frame)
            self.timer.after(33, lambda: self._animate_wagon(wagon_id, new_x, wagon_y, target_x, hero, hero_class, hero_x, hero_y))
        else:
            # Wagon has reached hero - trigger death
            self._trigger_wagon_death(hero, hero_class, hero_x, hero_y)
    
    def _trigger_wagon_death(self, hero, hero_class, hero_x, hero_y):
        """Trigger hero death after wagon collision"""
        # Play death sound
        self.audio.play_sound_effect('death.mp3')
        
        # Display special message in larger font
        self.text_display.clear_text()
        self.text_display.text_area.config(state='normal')
        
        # Insert message with larger font
        message = "OH NO!  You've been run over by Truck-kun, errrrrrr, I mean Wagon-kun"
        self.text_display.text_area.insert('end', '\n\n' + message, 'large_death_text')
        self.text_display.text_area.tag_config('large_death_text', 
                                               foreground='#ff4444', 
                                               font=('Consolas', 16, 'bold'),
                                               justify='center')
        
        self.text_display.text_area.config(state='disabled')
        
        # Get death image from hero YAML or use fallback
        death_image_path = hero.get('art_death', '')
        if not death_image_path:
            # Fallback to class-based path if art_death field missing
            death_images = {
                'warrior': 'art/warrior_death.png',
                'ninja': 'art/ninja_death.png',
                'magician': 'art/magician_death.png'
            }
            death_image_path = death_images.get(hero_class, 'art/warrior_death.png')
        
        # Remove hero image and replace with death image
        canvas = self.image_display.image_canvas
        canvas.delete('hero')
        
        # Add death image at same position as hero was
        self.image_display._add_canvas_image(death_image_path, hero_x, hero_y, tags='hero_death')
        
        # After a delay, trigger the Shiva divine intervention scene (4.5 seconds to give time to read)
        self.timer.after(8000, self._show_shiva_divine_intervention)
    
    def _show_shiva_divine_intervention(self):
        """Show Shiva's divine intervention after wagon death"""
        # Clear all foreground images
        self.image_display._clear_foreground_images()
        
        # Show Shiva mountains background
        self.image_display.set_background_image('art/shiva_mountains_background.png')
        
        # Clear and update text with Shiva's message
        self.text_display.clear_text()
        self.text_display.text_area.config(state='normal')
        
        # Insert Shiva's divine message with same large font style
        shiva_message = ("I am the earth god Shiva.  I have summoned you to our world to face a great evil.  "
                        "Find and face the evil orange one.  If you fail our world will perish.  "
                        "If you succeed you will be hailed forever as the savior of earth!  "
                        "Do you accept this task brave hero?")
        
        self.text_display.text_area.insert('end', '\n\n' + shiva_message, 'shiva_text')
        self.text_display.text_area.tag_config('shiva_text', 
                                               foreground='#ff4444', 
                                               font=('Consolas', 16, 'bold'),
                                               justify='center')
        
        self.text_display.text_area.config(state='disabled')
        
        # Offer "choices" to the player (all lead to same outcome)
        self.interface_control.set_buttons(
            ["Yes", "Absolutely", "Uh-huh", "I live to serve"],
            lambda choice: self._show_isekai_story()
        )
        
        # Unlock interface to allow button clicks
        self.interface_control.unlock_interface()
    
    def _show_isekai_story(self):
        """Display the Isekai story section after accepting Shiva's quest"""
        import yaml
        
        # Lock interface during story display
        self.interface_control.lock_interface()
        
        try:
            # Load story from YAML file
            with open(get_resource_path('story.yaml'), 'r', encoding='utf-8') as f:
                story_data = yaml.safe_load(f)
            
            isekai_lines = story_data.get('Isekai', [])
            
            if isekai_lines:
                # Clear displays
                self.text_display.clear_text()
                self.image_display._clear_foreground_images()
                
                # Set story background (same as prologue)
                self.image_display.set_background_image('art/story_background.png')
                
                # Display Isekai story text on canvas (same style as prologue)
                self.image_display.image_manager.show_story_text(
                    text_lines=isekai_lines,
                    font_size=28,
                    text_color='#ffdd00',
                    shadow_color='#000000',
                    line_spacing=50
                )
                
                # Show message in text area
                self.text_display.print_text("=" * 60)
                self.text_display.print_text("🌍  A New World Awaits...")
                self.text_display.print_text("=" * 60)
                
                # Game state frozen here - to be continued later
                
        except FileNotFoundError:
            logger.warning("story.yaml not found, skipping Isekai story")

