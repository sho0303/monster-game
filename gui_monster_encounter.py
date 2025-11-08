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
                        self.gui.game_state.hero['xp'] += monster['xp']
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
        
        # Display both images side by side in the top frame
        self.gui.show_images(image_paths, layout="horizontal")
        
        # Store current images for combat animations
        self.current_hero_image = image_paths[0]
        self.current_monster_image = image_paths[1] if len(image_paths) > 1 else 'art/crossed_swords.png'

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
