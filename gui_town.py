#!/usr/bin/env python3
"""
Town GUI for the monster game - handles town menu and activities
"""

import tkinter as tk
from tkinter import scrolledtext

class TownGUI:
    """GUI for town activities and menu"""
    
    def __init__(self, gui):
        self.gui = gui
    
    def enter_town(self):
        """Enter the town and show town menu"""
        self.gui.clear_text()
        self.gui.lock_interface()
        
        # Set town background
        self.gui.set_town_background()
        
        # Show welcome message
        self.gui.print_text("🏘️  WELCOME TO TOWN  🏘️")
        self.gui.print_text("=" * 60)
        self.gui.print_text("\nYou enter the bustling town square.")
        self.gui.print_text("Medieval buildings line the cobblestone streets,")
        self.gui.print_text("market stalls offer their wares, and a fountain")
        self.gui.print_text("sparkles in the center of the square.")
        self.gui.print_text("\nWhat would you like to do in town?")
        
        def on_town_select(choice):
            if choice == 1:
                self._visit_shop()
            elif choice == 2:
                self._visit_tavern()
            elif choice == 3:
                self._visit_blacksmith()
            elif choice == 4:
                self._visit_fountain()
            elif choice == 5:
                self._leave_town()
        
        # Town menu options
        town_buttons = [
            "🛒 Visit Shop", 
            "🍺 Visit Tavern", 
            "⚒️ Visit Blacksmith", 
            "⛲ Town Fountain",
            "🚪 Leave Town"
        ]
        
        self.gui.set_buttons(town_buttons, on_town_select)
        self.gui.unlock_interface()
    
    def _visit_shop(self):
        """Visit the shop (existing shop functionality)"""
        self.gui.clear_text()
        self.gui.print_text("🛒 Entering the shop...")
        self.gui.print_text("The shopkeeper greets you warmly.")
        
        # Use existing shop system
        self.gui.shop.open()
    
    def _visit_tavern(self):
        """Visit the tavern and access bounty board"""
        self.gui.clear_text()
        self.gui.set_background_image('art/tavern_background.png')
        self.gui.lock_interface()
        
        self.gui.print_text("🍺  THE PRANCING PONY TAVERN  🍺")
        self.gui.print_text("=" * 60)
        self.gui.print_text("\nYou enter the warm, cozy tavern.")
        self.gui.print_text("The smell of roasted meat and ale fills the air.")
        self.gui.print_text("Adventurers gather around wooden tables,")
        self.gui.print_text("sharing tales of their exploits.")
        self.gui.print_text("\nA large wooden board on the wall displays")
        self.gui.print_text("various bounty notices offering rewards.")
        self.gui.print_text("\nBehind the bar, a cheerful bartender polishes mugs")
        self.gui.print_text("and grins at you expectantly.")
        
        def on_tavern_choice(choice):
            if choice == 1:
                self.gui.bounty_manager.show_bounty_board()
            elif choice == 2:
                self._talk_to_bartender()
            else:
                self.enter_town()
        
        tavern_buttons = [
            "📜 Check Bounty Board",
            "🍻 Talk to Bartender",
            "🚪 Leave Tavern"
        ]
        
        self.gui.set_buttons(tavern_buttons, on_tavern_choice)
        self.gui.unlock_interface()
    
    def _talk_to_bartender(self):
        """Talk to the bartender who only sells beer"""
        self.gui.clear_text()
        self.gui.lock_interface()
        
        self.gui.print_text("🍻  BARTENDER BOB'S BEER EMPORIUM  🍻")
        self.gui.print_text("=" * 60)
        self.gui.print_text("\nThe jovial bartender Bob beams at you.")
        self.gui.print_text("'Welcome, friend! What can I get ya?'")
        self.gui.print_text("\nHe gestures proudly at his selection:")
        
        # Hero's current gold
        hero = self.gui.game_state.hero
        gold_parts = [
            ("Your gold: ", "#ffffff"),
            (str(hero.get('gold', 0)), "#ffdd00"),
            (" 💰", "#ffdd00")
        ]
        self.gui._print_colored_parts(gold_parts)
        self.gui.print_text("")
        
        # The "different" beer options (all cost 5 gold, all do the same thing)
        beer_options = [
            "🍺 Beer (Classic brew, recommended by Bob) - 5 gold",
            "🍺 Ale (It's beer, but fancier name) - 5 gold", 
            "🍺 Lager (Still beer, Bob assures you) - 5 gold",
            "🍺 Stout (Dark beer, but definitely beer) - 5 gold"
        ]
        
        for option in beer_options:
            self.gui.print_text(option)
        
        self.gui.print_text("\n'They're all beer,' Bob admits with a wink,")
        self.gui.print_text("'but each one restores 5 HP and gives you that'")
        self.gui.print_text("'warm fuzzy feeling! Pick your favorite!'")
        
        def on_beer_choice(choice):
            if choice <= 4:  # One of the beer options
                self._buy_beer(choice)
            else:  # Leave
                self._visit_tavern()
        
        beer_buttons = [
            "1. Buy Beer",
            "2. Buy Ale", 
            "3. Buy Lager",
            "4. Buy Stout",
            "🚪 Back to Tavern"
        ]
        
        self.gui.set_buttons(beer_buttons, on_beer_choice)
        self.gui.unlock_interface()
    
    def _buy_beer(self, beer_type):
        """Buy one of the 'different' beers (they're all the same)"""
        hero = self.gui.game_state.hero
        beer_cost = 5
        
        if hero.get('gold', 0) < beer_cost:
            self.gui.clear_text()
            self.gui.print_text("💸 Not enough gold!")
            self.gui.print_text("Bob shakes his head sympathetically.")
            self.gui.print_text("'Come back when you've got 5 gold, friend!'")
            self.gui.root.after(2000, self._talk_to_bartender)
            return
        
        # Deduct gold
        hero['gold'] -= beer_cost
        
        # Beer names for flavor text
        beer_names = ["Beer", "Ale", "Lager", "Stout"]
        chosen_beer = beer_names[beer_type - 1]
        
        self.gui.clear_text()
        self.gui.print_text(f"🍺 You purchased {chosen_beer}!")
        self.gui.print_text("=" * 60)
        
        # Fun flavor text based on choice
        flavor_texts = [
            "Bob slides you a frothy mug of classic beer.\n'The original and the best!' he declares.",
            "Bob pours you an 'ale' from the same tap as the beer.\n'Totally different!' he winks.",
            "Bob serves you a 'lager' that looks suspiciously like beer.\n'It's... uh... lighter?' he grins sheepishly.", 
            "Bob gives you a 'stout' that's definitely just dark beer.\n'The darkest beer I've got!' he says proudly."
        ]
        
        self.gui.print_text(flavor_texts[beer_type - 1])
        
        # Heal HP (same for all beers)
        heal_amount = 5
        if hero['hp'] < hero['maxhp']:
            actual_heal = min(heal_amount, hero['maxhp'] - hero['hp'])
            hero['hp'] += actual_heal
            
            heal_parts = [
                ("\n🍺 The refreshing ", "#00ff00"),
                (chosen_beer.lower(), "#ffdd00"),
                (f" restores {actual_heal} HP! 🍺", "#00ff00")
            ]
            self.gui._print_colored_parts(heal_parts)
        else:
            self.gui.print_text(f"\n🍺 The {chosen_beer.lower()} tastes great, but you're already at full health!")
        
        # Show current stats
        hp_parts = [
            ("HP: ", "#00ff00"),
            (str(hero['hp']), "#00ff00"),
            ("/", "#ffffff"),
            (str(hero['maxhp']), "#00ff00")
        ]
        self.gui._print_colored_parts(hp_parts)
        
        gold_parts = [
            ("Gold: ", "#ffffff"),
            (str(hero['gold']), "#ffdd00"),
            (" 💰", "#ffdd00")
        ]
        self.gui._print_colored_parts(gold_parts)
        
        # Secret dungeon hint and beer quest system
        import random
        
        # Track beer consumption
        if 'beers_consumed' not in hero:
            hero['beers_consumed'] = 0
        hero['beers_consumed'] += 1
        
        # Secret dungeon discovery (15% chance after 3+ beers)
        if (hero['beers_consumed'] >= 3 and 
            not hero.get('secret_dungeon_discovered', False) and 
            random.random() < 0.15):
            
            # Start the interactive secret dungeon discovery
            self._show_secret_dungeon_story()
            return  # Don't continue with normal beer flow
            
        # Regular beer quest (10% chance)
        elif random.random() < 0.1:
            self.gui.print_text("\n" + "="*60)
            self.gui.print_text("🎯 SECRET BEER QUEST UNLOCKED! 🎯")
            self.gui.print_text("Bob leans in conspiratorially...")
            self.gui.print_text("'Psst... if you can drink 10 of my beers")
            self.gui.print_text("(not all at once, mind you), I'll give")
            self.gui.print_text("you something special!' *wink*")
            
            if hero['beers_consumed'] >= 10:
                self.gui.print_text("\n🏆 BEER MASTER ACHIEVEMENT! 🏆")
                self.gui.print_text("Bob hands you a special 'Tavern Regular' badge!")
                hero['gold'] += 100  # Bonus gold
                self.gui.print_text("You earned 100 bonus gold!")
                hero['beers_consumed'] = 0  # Reset counter
            else:
                remaining = 10 - hero['beers_consumed']
                self.gui.print_text(f"Beers remaining: {remaining}")
        
        self.gui.print_text("\nBob grins: 'Come back anytime for more... beer!'")
        self.gui.root.after(3000, self._talk_to_bartender)
    
    def _show_secret_dungeon_story(self):
        """Show the interactive secret dungeon discovery story"""
        self.gui.clear_text()
        self.gui.set_background_image('art/tavern_background.png')
        
        self.gui.print_text("=" * 70)
        self.gui.print_text("🕳️ MYSTERIOUS DISCOVERY! 🕳️")
        self.gui.print_text("=" * 70)
        
        self.gui.print_text("\nBob's eyes suddenly grow wide and glassy...")
        self.gui.print_text("He glances around nervously, then leans in close.")
        
        self.gui.print_text("\n💭 Bob whispers:")
        self.gui.print_text("'You know... *hiccup* ...after a few drinks,")
        self.gui.print_text("old Bob remembers things he shouldn't...'")
        
        self.gui.print_text("\nHe looks around again, making sure no one")
        self.gui.print_text("else is listening, then continues:")
        
        self.gui.print_text("\n🗝️ 'There's an ancient passage... hidden behind")
        self.gui.print_text("the old stone well, just outside the town walls.")
        self.gui.print_text("Most folks don't even notice it anymore...'")
        
        self.gui.print_text("\nBob's voice drops to barely a whisper:")
        self.gui.print_text("'That passage leads to places that ain't on")
        self.gui.print_text("any map, friend. Deep, dark places where")
        self.gui.print_text("ancient things have been sleeping for ages.'")
        
        self.gui.print_text("\n💀 'But the treasure down there... oh my...'")
        self.gui.print_text("'Gold older than kingdoms, guarded by")
        self.gui.print_text("shadows that remember when the world was young.'")
        
        self.gui.print_text("\nBob straightens up and looks you in the eye:")
        self.gui.print_text("'I've never told anyone this before, but")
        self.gui.print_text("something about you... you seem different.'")
        self.gui.print_text("'Like maybe you're brave enough to face")
        self.gui.print_text("what's down there and live to tell about it.'")
        
        self.gui.print_text("\n" + "=" * 50)
        self.gui.print_text("🎯 QUEST OPPORTUNITY: THE SECRET DUNGEON")
        self.gui.print_text("=" * 50)
        
        # Show the quest acceptance options
        button_labels = [
            "🗝️ Accept the Quest",
            "🤔 Ask More Questions", 
            "😰 Decline (Too Dangerous)"
        ]
        
        def on_story_choice(choice):
            if choice == 1:
                self._accept_secret_dungeon_quest()
            elif choice == 2:
                self._ask_about_secret_dungeon()
            elif choice == 3:
                self._decline_secret_dungeon_quest()
        
        self.gui.set_buttons(button_labels, on_story_choice)
    
    def _accept_secret_dungeon_quest(self):
        """Accept the secret dungeon quest and unlock the area"""
        hero = self.gui.game_state.hero
        
        self.gui.clear_text()
        self.gui.set_background_image('art/tavern_background.png')
        
        self.gui.print_text("🏆 QUEST ACCEPTED: THE SECRET DUNGEON")
        self.gui.print_text("=" * 60)
        
        self.gui.print_text("\nYou nod firmly: 'Tell me where to find this passage.'")
        
        self.gui.print_text("\nBob grins and claps you on the shoulder:")
        self.gui.print_text("'I knew you had the look of a true adventurer!'")
        
        self.gui.print_text("\n🗺️ Bob draws a rough map on a napkin:")
        self.gui.print_text("'Exit the town through the north gate.")
        self.gui.print_text("Follow the old stone wall until you see")
        self.gui.print_text("the ancient well with strange markings.")
        self.gui.print_text("Push on the third stone from the left...'")
        
        self.gui.print_text("\n⚠️ 'But be warned, friend. The creatures")
        self.gui.print_text("down there are not like the ones you've")
        self.gui.print_text("faced before. They're ancient, powerful,")
        self.gui.print_text("and hungry for the blood of the living.'")
        
        self.gui.print_text("\n💰 'Still... the rewards are beyond measure.")
        self.gui.print_text("Ancient treasures, forgotten magics...")
        self.gui.print_text("Riches that could set you up for life!'")
        
        # Unlock the secret dungeon
        hero['secret_dungeon_discovered'] = True
        
        self.gui.print_text("\n🎉 SECRET DUNGEON UNLOCKED!")
        self.gui.print_text("✅ You can now access the Secret Dungeon via:")
        self.gui.print_text("   - Biome cycling (B key)")
        self.gui.print_text("   - Random teleportation (T key)")
        self.gui.print_text("   - Quest system missions")
        
        self.gui.print_text("\nBob raises his mug: 'To brave adventurers!")
        self.gui.print_text("May you return with tales worth telling!'")
        
        # Return to tavern after showing results
        self.gui.set_buttons(["🍺 Return to Tavern"], lambda choice: self._visit_tavern())
    
    def _ask_about_secret_dungeon(self):
        """Ask Bob more questions about the secret dungeon"""
        self.gui.clear_text()
        self.gui.set_background_image('art/tavern_background.png')
        
        self.gui.print_text("🤔 ASKING FOR MORE INFORMATION")
        self.gui.print_text("=" * 50)
        
        self.gui.print_text("\nYou lean forward: 'Tell me more about")
        self.gui.print_text("what I might face down there.'")
        
        self.gui.print_text("\nBob takes a long swig of his beer:")
        self.gui.print_text("'Well, if the old stories are true...'")
        
        self.gui.print_text("\n👻 'There are shadows that move without")
        self.gui.print_text("bodies, wraiths that feast on fear,")
        self.gui.print_text("and guardians older than memory.'")
        
        self.gui.print_text("\n⚔️ 'You'll want to be at least level 6")
        self.gui.print_text("before you even think about going down.")
        self.gui.print_text("Anything less and... well, we won't")
        self.gui.print_text("be having this conversation again.'")
        
        self.gui.print_text("\n💎 'But the rewards, friend! Ancient")
        self.gui.print_text("treasures worth hundreds of gold pieces,")
        self.gui.print_text("magical artifacts, maybe even legendary")
        self.gui.print_text("weapons forged in the old days!'")
        
        self.gui.print_text("\nBob looks at you seriously:")
        self.gui.print_text("'So... what'll it be? Are you brave")
        self.gui.print_text("enough to face the unknown?'")
        
        # Show options again
        button_labels = [
            "🗝️ Yes, I Accept the Quest!",
            "😰 No, Too Dangerous for Me"
        ]
        
        def on_final_choice(choice):
            if choice == 1:
                self._accept_secret_dungeon_quest()
            elif choice == 2:
                self._decline_secret_dungeon_quest()
        
        self.gui.set_buttons(button_labels, on_final_choice)
    
    def _decline_secret_dungeon_quest(self):
        """Decline the secret dungeon quest"""
        self.gui.clear_text()
        self.gui.set_background_image('art/tavern_background.png')
        
        self.gui.print_text("😰 QUEST DECLINED")
        self.gui.print_text("=" * 30)
        
        self.gui.print_text("\nYou shake your head: 'That sounds far")
        self.gui.print_text("too dangerous for me right now.'")
        
        self.gui.print_text("\nBob nods understandingly:")
        self.gui.print_text("'Aye, that's wisdom talking. No shame")
        self.gui.print_text("in knowing your limits, friend.'")
        
        self.gui.print_text("\n🍺 'Tell you what - come back and have")
        self.gui.print_text("a few more drinks with old Bob when")
        self.gui.print_text("you're feeling braver. This offer")
        self.gui.print_text("won't disappear anytime soon.'")
        
        self.gui.print_text("\n💭 Bob winks: 'Besides, a few more beers")
        self.gui.print_text("might give me more... inspiration... to")
        self.gui.print_text("share other interesting stories!'")
        
        # The quest opportunity remains available for future beer purchases
        self.gui.print_text("\n✨ The secret remains available...")
        self.gui.print_text("Perhaps another beer will unlock Bob's memory again!")
        
        # Return to tavern
        self.gui.set_buttons(["🍺 Return to Tavern"], lambda choice: self._visit_tavern())
    
    def _visit_blacksmith(self):
        """Visit the blacksmith"""
        self.gui.clear_text()
        self.gui.print_text("⚒️ Entering the blacksmith...")
        self.gui.print_text("You hear the ring of hammer on anvil.")
        
        # Use blacksmith system
        self.gui.blacksmith.open()
    
    def _visit_fountain(self):
        """Visit the town fountain"""
        self.gui.clear_text()
        self.gui.lock_interface()
        
        self.gui.print_text("⛲  TOWN FOUNTAIN  ⛲")
        self.gui.print_text("=" * 60)
        self.gui.print_text("\nYou approach the sparkling fountain.")
        self.gui.print_text("Crystal clear water bubbles up from the center,")
        self.gui.print_text("creating gentle ripples across the surface.")
        self.gui.print_text("Local legend says this fountain has healing properties.")
        
        # Small HP restoration
        hero = self.gui.game_state.hero
        if hero['hp'] < hero['maxhp']:
            heal_amount = min(3, hero['maxhp'] - hero['hp'])  # Heal up to 3 HP
            hero['hp'] += heal_amount
            
            heal_parts = [
                ("\n✨ The magical waters restore ", "#00ff00"),
                (str(heal_amount), "#ffdd00"),
                (" HP! ✨", "#00ff00")
            ]
            self.gui._print_colored_parts(heal_parts)
            
            hp_parts = [
                ("Your HP: ", "#00ff00"),
                (str(hero['hp']), "#00ff00"),
                ("/", "#ffffff"),
                (str(hero['maxhp']), "#00ff00")
            ]
            self.gui._print_colored_parts(hp_parts)
        else:
            self.gui.print_text("\n💚 You are already at full health.")
            self.gui.print_text("The fountain's magic has no effect.")
        
        self.gui.print_text("\nYou feel refreshed by the peaceful atmosphere.")
        
        # Return to town after 3 seconds
        self.gui.root.after(3000, self.enter_town)
    
    def _leave_town(self):
        """Leave town and return to main menu"""
        self.gui.clear_text()
        self.gui.print_text("🚪 Leaving the town...")
        self.gui.print_text("You wave goodbye to the townspeople")
        self.gui.print_text("and head back to your adventures.")
        
        # Return to main menu after 2 seconds
        self.gui.root.after(2000, self.gui.main_menu)