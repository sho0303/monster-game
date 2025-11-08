"""
Inventory system for GUI
"""


class InventoryGUI:
    """Inventory system for GUI"""
    def __init__(self, gui):
        self.gui = gui
    
    def use_item(self):
        """Use item"""
        # Lock interface to prevent button spamming during item use
        self.gui.lock_interface()
        
        hero = self.gui.game_state.hero
        if hero.get('item') is None:
            self.gui.print_text("\n❌ You don't have any items!")
            self.gui.root.after(2000, self.gui.main_menu)
            return
        
        if hero['item']['name'] == 'Health Potion':
            # Play gulp sound when drinking the potion
            self.gui.audio.play_sound_effect('gulp.mp3')
            hero['hp'] = hero['maxhp']
            self.gui.print_text(f"\n✓ Used {hero['item']['name']}! HP restored to {hero['hp']}!")
            hero['item'] = None
        
        self.gui.root.after(2000, self.gui.main_menu)
