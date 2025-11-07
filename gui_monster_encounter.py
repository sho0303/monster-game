"""
Monster encounter system for GUI
"""
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
        # Show monster art if available, otherwise show default crossed swords
        if 'art' in monster and monster['art']:
            self.gui.show_image(monster['art'])
        else:
            self.gui.show_image('art/crossed_swords.png')
        
        self.gui.print_text(f"\n⚠️  A {monster['name']} appeared! ⚠️\n")
        
        # Display hero and monster stats side by side
        hero = self.gui.game_state.hero
        self._display_vs_stats(hero, monster)
        
        def on_choice(choice):
            if choice == 1:
                def after_fight(result):
                    if result == 'won':
                        self.gui.print_text(f"\n🎉 Victory! You earned {monster['gold']} gold!")
                        self.gui.game_state.hero['gold'] += monster['gold']
                        self.gui.game_state.hero['xp'] += monster['xp']
                    else:
                        self.gui.print_text(f"\n💀 Defeat! You lost all your gold!")
                        self.gui.game_state.hero['gold'] = 0
                        self.gui.game_state.hero['lives_left'] -= 1
                        self.gui.game_state.hero['hp'] = self.gui.game_state.hero['maxhp']
                    
                    self.gui.root.after(3000, self.gui.main_menu)
                
                self.gui.combat.fight(self.gui.game_state.hero, monster, after_fight)
            else:
                self.gui.print_text("\nYou ran away!")
                self.gui.root.after(1500, self.gui.main_menu)
        
        self.gui.set_buttons(["⚔️ Fight", "🏃 Run", ""], on_choice)
    
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
