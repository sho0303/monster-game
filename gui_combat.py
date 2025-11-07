"""
Combat system for GUI
"""
import random


class CombatGUI:
    """Combat system for GUI"""
    def __init__(self, gui):
        self.gui = gui
    
    def fight(self, hero, monster, callback):
        """Execute fight with GUI updates"""
        self.gui.clear_text()
        # Show monster art during combat if available
        if 'art' in monster and monster['art']:
            self.gui.show_image(monster['art'])
        else:
            self.gui.show_image('art/crossed_swords.png')
        self.gui.print_text("\n⚔️  FIGHT! ⚔️\n")
        
        round_num = 1
        while hero['hp'] > 0 and monster['hp'] > 0:
            self.gui.print_text(f"--- Round {round_num} ---")
            
            # Hero attacks
            damage = self.calculate_damage(hero['attack'], monster['defense'])
            self.gui.print_text(f"You hit for {damage} damage!")
            monster['hp'] = max(0, monster['hp'] - damage)
            
            if monster['hp'] <= 0:
                break
            
            # Monster attacks
            damage = self.calculate_damage(monster['attack'], hero['defense'])
            self.gui.print_text(f"{monster['name']} hit for {damage} damage!")
            hero['hp'] = max(0, hero['hp'] - damage)
            
            self.gui.print_text(f"Your HP: {hero['hp']} | {monster['name']} HP: {monster['hp']}\n")
            round_num += 1
        
        result = 'won' if hero['hp'] > 0 else 'lost'
        callback(result)
    
    def calculate_damage(self, attack, defense):
        strike = random.randint(1, max(1, attack)) * 2
        damage = strike - defense
        return max(1, damage)
