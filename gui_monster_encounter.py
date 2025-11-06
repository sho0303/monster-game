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
        self.gui.show_image('ascii_art/crossed_swords.png')
        self.gui.print_text(f"\n⚠️  A {monster['name']} appeared! ⚠️\n")
        self.gui.print_text(f"Level: {monster['level']}")
        self.gui.print_text(f"HP: {monster['hp']}")
        self.gui.print_text(f"Attack: {monster['attack']}")
        self.gui.print_text(f"Defense: {monster['defense']}")
        
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
