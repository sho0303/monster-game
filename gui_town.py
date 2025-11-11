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
        
        # Check for random NPC encounters (25% chance)
        if self._check_for_tavern_encounter():
            return  # NPC encounter takes over the interface
        
        # Normal tavern entry
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
        
        # Track beer consumption for achievements
        if hasattr(self.gui, 'achievement_manager'):
            self.gui.achievement_manager.track_beer_consumption()
        
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
    
    def _check_for_tavern_encounter(self):
        """Check if player encounters an NPC with a side quest (25% chance)"""
        import random
        
        # 25% chance for an NPC encounter
        if random.random() < 0.25:
            # Select a random NPC encounter
            encounters = [
                self._encounter_merchant_caravan,
                self._encounter_desperate_farmer,
                self._encounter_mysterious_scholar,
                self._encounter_traveling_minstrel,
                self._encounter_worried_mother,
                self._encounter_grizzled_veteran
            ]
            
            encounter = random.choice(encounters)
            encounter()
            return True
        
        return False
    
    def _encounter_merchant_caravan(self):
        """Encounter with a merchant whose caravan was attacked"""
        self.gui.print_text("\n🚛 TAVERN ENCOUNTER: DESPERATE MERCHANT")
        self.gui.print_text("=" * 60)
        
        self.gui.print_text("\nAs you enter, a well-dressed merchant")
        self.gui.print_text("frantically approaches you from a corner table.")
        
        self.gui.print_text("\n💰 Merchant: 'Adventurer! Thank the gods!'")
        self.gui.print_text("'My caravan was attacked by bandits on the")
        self.gui.print_text("road from Millhaven. They stole a precious")
        self.gui.print_text("shipment of rare gems worth 500 gold!'")
        
        self.gui.print_text("\n😰 'I saw them flee toward the desert.")
        self.gui.print_text("If you can recover even half my goods,")
        self.gui.print_text("I'll pay you 200 gold as a reward!'")
        
        self.gui.print_text("\n💎 SIDE QUEST: Recover stolen gems from bandits")
        self.gui.print_text("   Reward: 200 gold + experience")
        self.gui.print_text("   Location: Desert biome (Level 3+ required)")
        
        self._show_side_quest_choice("merchant_caravan", 200, "desert")
    
    def _encounter_desperate_farmer(self):
        """Encounter with a farmer whose crops are being destroyed"""
        self.gui.print_text("\n🌾 TAVERN ENCOUNTER: DESPERATE FARMER")
        self.gui.print_text("=" * 60)
        
        self.gui.print_text("\nA dirt-covered farmer rushes up to you")
        self.gui.print_text("as soon as you step through the door.")
        
        self.gui.print_text("\n🚜 Farmer: 'Please, you look like a capable")
        self.gui.print_text("fighter! Giant boars have been ravaging")
        self.gui.print_text("my fields for weeks. My family will starve")
        self.gui.print_text("if I can't harvest my crops!'")
        
        self.gui.print_text("\n🐗 'I can't pay much, but I'll give you")
        self.gui.print_text("150 gold and some of my best vegetables")
        self.gui.print_text("if you can clear out those beasts!'")
        
        self.gui.print_text("\n🌾 SIDE QUEST: Eliminate crop-destroying boars")
        self.gui.print_text("   Reward: 150 gold + food items")
        self.gui.print_text("   Location: Grassland biome (Level 1+)")
        
        self._show_side_quest_choice("desperate_farmer", 150, "grassland")
    
    def _encounter_mysterious_scholar(self):
        """Encounter with a scholar seeking ancient artifacts"""
        self.gui.print_text("\n📚 TAVERN ENCOUNTER: MYSTERIOUS SCHOLAR")
        self.gui.print_text("=" * 60)
        
        self.gui.print_text("\nA hooded figure in scholarly robes")
        self.gui.print_text("beckons you over to a dimly lit table.")
        
        self.gui.print_text("\n🔍 Scholar: 'I sense great potential in you...")
        self.gui.print_text("I seek ancient relics lost in the deepest")
        self.gui.print_text("dungeons. Dangerous work, but the knowledge")
        self.gui.print_text("contained within is invaluable.'")
        
        self.gui.print_text("\n⚡ 'Retrieve an ancient tome from the")
        self.gui.print_text("dungeon depths, and I shall reward you")
        self.gui.print_text("with 300 gold and... other secrets.'")
        
        self.gui.print_text("\n📜 SIDE QUEST: Recover ancient tome")
        self.gui.print_text("   Reward: 300 gold + magical knowledge")
        self.gui.print_text("   Location: Dungeon biome (Level 7+ required)")
        
        self._show_side_quest_choice("mysterious_scholar", 300, "dungeon")
    
    def _encounter_traveling_minstrel(self):
        """Encounter with a minstrel who lost his instrument"""
        self.gui.print_text("\n🎵 TAVERN ENCOUNTER: TRAVELING MINSTREL")
        self.gui.print_text("=" * 60)
        
        self.gui.print_text("\nA colorfully dressed minstrel sits sadly")
        self.gui.print_text("in the corner, nursing a mug of ale.")
        
        self.gui.print_text("\n🎭 Minstrel: 'Ah, a fellow wanderer!")
        self.gui.print_text("Perhaps you can help an artist in need.")
        self.gui.print_text("My precious lute was stolen by sea raiders")
        self.gui.print_text("near the coastal waters!'")
        
        self.gui.print_text("\n🎶 'Without it, I cannot perform for my")
        self.gui.print_text("living. Recover my instrument, and I'll")
        self.gui.print_text("compose a ballad of your deeds AND pay")
        self.gui.print_text("you 180 gold from my performance earnings!'")
        
        self.gui.print_text("\n🎵 SIDE QUEST: Recover the stolen lute")
        self.gui.print_text("   Reward: 180 gold + fame bonus")
        self.gui.print_text("   Location: Ocean biome (Level 5+ required)")
        
        self._show_side_quest_choice("traveling_minstrel", 180, "ocean")
    
    def _encounter_worried_mother(self):
        """Encounter with a mother whose child is missing"""
        self.gui.print_text("\n👩‍👧 TAVERN ENCOUNTER: WORRIED MOTHER")
        self.gui.print_text("=" * 60)
        
        self.gui.print_text("\nA tearful woman approaches you desperately")
        self.gui.print_text("as you enter the tavern.")
        
        self.gui.print_text("\n😢 Mother: 'Hero, please! My young son")
        self.gui.print_text("went exploring near the old ruins and")
        self.gui.print_text("hasn't returned. The monsters there...")
        self.gui.print_text("I fear the worst!'")
        
        self.gui.print_text("\n💝 'He's all I have left. I don't have")
        self.gui.print_text("much gold, but I'll give you everything")
        self.gui.print_text("I own - 250 gold - if you bring him")
        self.gui.print_text("home safely!'")
        
        self.gui.print_text("\n👨‍👩‍👧‍👦 SIDE QUEST: Rescue the missing child")
        self.gui.print_text("   Reward: 250 gold + heartfelt gratitude")
        self.gui.print_text("   Location: Dungeon biome (Level 7+ required)")
        
        self._show_side_quest_choice("worried_mother", 250, "dungeon")
    
    def _encounter_grizzled_veteran(self):
        """Encounter with a veteran warrior seeking revenge"""
        self.gui.print_text("\n⚔️ TAVERN ENCOUNTER: GRIZZLED VETERAN")
        self.gui.print_text("=" * 60)
        
        self.gui.print_text("\nAn old warrior with battle scars looks")
        self.gui.print_text("up from his drink as you approach the bar.")
        
        self.gui.print_text("\n🛡️ Veteran: 'You've got the look of a")
        self.gui.print_text("real fighter. I've been tracking a")
        self.gui.print_text("particular beast that cost me my leg")
        self.gui.print_text("and my adventuring days.'")
        
        self.gui.print_text("\n⚡ 'A massive desert wyrm lurks in the")
        self.gui.print_text("sandy wastes. Kill it for me, and I'll")
        self.gui.print_text("give you my finest weapon AND 400 gold.")
        self.gui.print_text("Consider it... professional courtesy.'")
        
        self.gui.print_text("\n🐲 SIDE QUEST: Slay the desert wyrm")
        self.gui.print_text("   Reward: 400 gold + legendary weapon")
        self.gui.print_text("   Location: Desert biome (Level 3+ required)")
        
        self._show_side_quest_choice("grizzled_veteran", 400, "desert")
    
    def _can_access_biome(self, biome):
        """Check if hero can access a specific biome based on level"""
        if not hasattr(self.gui, 'quest_manager') or not self.gui.quest_manager:
            return True  # Fallback to allow access if quest manager not available
        
        hero = self.gui.game_state.hero
        hero_level = hero.get('level', 1)
        required_level = self.gui.quest_manager.BIOME_UNLOCK_LEVELS.get(biome, 1)
        return hero_level >= required_level
    
    def _show_side_quest_choice(self, quest_id, reward_gold, target_biome):
        """Show options for accepting or declining a side quest"""
        
        # Check if hero can access the target biome
        hero = self.gui.game_state.hero
        hero_level = hero.get('level', 1)
        
        if not self._can_access_biome(target_biome):
            # Hero cannot access this biome yet - show level requirement
            required_level = self.gui.quest_manager.BIOME_UNLOCK_LEVELS.get(target_biome, 1)
            
            biome_names = {
                'grassland': 'Grasslands',
                'desert': 'Desert',
                'ocean': 'Ocean',
                'dungeon': 'Dungeons'
            }
            biome_name = biome_names.get(target_biome, target_biome.title())
            
            self.gui.print_text(f"\n⚠️  QUEST UNAVAILABLE")
            self.gui.print_text(f"You need to be level {required_level} to access the {biome_name}.")
            self.gui.print_text(f"Your current level: {hero_level}")
            self.gui.print_text("Come back when you're stronger!")
            
            # Return to normal tavern
            self.gui.unlock_interface()
            
            def on_return_choice(choice):
                if choice == 1:
                    self._show_normal_tavern()
            
            self.gui.set_buttons(["🍺 Return to Tavern"], on_return_choice)
            return
        
        # Unlock interface for NPC interaction
        self.gui.unlock_interface()
        
        button_labels = [
            "⚔️ Accept the Quest",
            "🤔 Ask for More Details",
            "😐 Politely Decline"
        ]
        
        def on_side_quest_choice(choice):
            if choice == 1:
                self._accept_side_quest(quest_id, reward_gold, target_biome)
            elif choice == 2:
                self._ask_side_quest_details(quest_id, reward_gold, target_biome)
            elif choice == 3:
                self._decline_side_quest()
        
        self.gui.set_buttons(button_labels, on_side_quest_choice)
    
    def _accept_side_quest(self, quest_id, reward_gold, target_biome):
        """Accept a side quest and add it to the quest log"""
        hero = self.gui.game_state.hero
        
        self.gui.clear_text()
        self.gui.set_background_image('art/tavern_background.png')
        
        self.gui.print_text("✅ SIDE QUEST ACCEPTED!")
        self.gui.print_text("=" * 40)
        
        quest_details = {
            "merchant_caravan": {
                "name": "Recover Stolen Gems",
                "description": "Find bandits in the desert and recover stolen gems",
                "npc": "the grateful merchant"
            },
            "desperate_farmer": {
                "name": "Clear the Fields", 
                "description": "Eliminate boars destroying the farmer's crops",
                "npc": "the relieved farmer"
            },
            "mysterious_scholar": {
                "name": "Ancient Tome Quest",
                "description": "Retrieve an ancient tome from dungeon depths",
                "npc": "the mysterious scholar"
            },
            "traveling_minstrel": {
                "name": "The Lost Lute",
                "description": "Recover the minstrel's stolen lute from sea raiders",
                "npc": "the grateful minstrel"
            },
            "worried_mother": {
                "name": "Rescue Mission",
                "description": "Find and rescue the missing child from ruins",
                "npc": "the tearful mother"
            },
            "grizzled_veteran": {
                "name": "Desert Revenge",
                "description": "Slay the desert wyrm that maimed the veteran",
                "npc": "the grizzled veteran"
            }
        }
        
        quest_info = quest_details[quest_id]
        
        self.gui.print_text(f"\n📜 Quest: {quest_info['name']}")
        self.gui.print_text(f"📍 Objective: {quest_info['description']}")
        self.gui.print_text(f"🏆 Reward: {reward_gold} gold")
        self.gui.print_text(f"🗺️ Location: {target_biome.title()} biome")
        
        # Add quest to hero's side quests (if not already tracked)
        if 'side_quests' not in hero:
            hero['side_quests'] = []
        
        # Check if quest already exists
        existing = [q for q in hero['side_quests'] if q['id'] == quest_id]
        if not existing:
            hero['side_quests'].append({
                'id': quest_id,
                'name': quest_info['name'],
                'description': quest_info['description'],
                'reward_gold': reward_gold,
                'target_biome': target_biome,
                'completed': False,
                'npc': quest_info['npc']
            })
            
            # Track NPC encounter for achievements
            if hasattr(self.gui, 'achievement_manager'):
                npc_name = quest_id  # Use quest_id as NPC identifier
                self.gui.achievement_manager.track_tavern_npc_encounter(npc_name)
        
        self.gui.print_text(f"\n✨ The quest has been added to your quest log!")
        self.gui.print_text(f"💡 TIP: Travel to the {target_biome} biome and")
        self.gui.print_text("complete battles to make progress!")
        
        self.gui.print_text(f"\n{quest_info['npc'].title()} nods gratefully")
        self.gui.print_text("and returns to their table.")
        
        # Continue with normal tavern
        self.gui.set_buttons(["🍺 Continue into Tavern"], lambda choice: self._show_normal_tavern())
    
    def _ask_side_quest_details(self, quest_id, reward_gold, target_biome):
        """Ask for more details about the side quest"""
        self.gui.clear_text()
        self.gui.set_background_image('art/tavern_background.png')
        
        self.gui.print_text("🤔 ASKING FOR MORE DETAILS")
        self.gui.print_text("=" * 40)
        
        details = {
            "merchant_caravan": "The merchant explains the bandits were led by a fierce warrior and had about 6 members. They're likely camped near an oasis.",
            "desperate_farmer": "The farmer mentions the boars are unusually large and aggressive - probably 3-4 giant boars led by a massive alpha.",
            "mysterious_scholar": "The scholar hints that the tome contains ancient magic spells, but warns of powerful guardians protecting it.",
            "traveling_minstrel": "The minstrel describes his lute as having magical properties that enhance performance, stolen by notorious sea pirates.",
            "worried_mother": "The mother tearfully explains her son is only 12 and went missing 2 days ago near the old temple ruins.",
            "grizzled_veteran": "The veteran shows his prosthetic leg and describes a massive wyrm with venomous fangs and armored scales."
        }
        
        self.gui.print_text(f"\n{details[quest_id]}")
        
        # Add biome and level information
        biome_names = {
            'grassland': 'Grasslands',
            'desert': 'Desert', 
            'ocean': 'Ocean',
            'dungeon': 'Dungeons'
        }
        biome_name = biome_names.get(target_biome, target_biome.title())
        required_level = self.gui.quest_manager.BIOME_UNLOCK_LEVELS.get(target_biome, 1)
        
        self.gui.print_text(f"\n🌍 Location: {biome_name}")
        if required_level > 1:
            self.gui.print_text(f"🎯 Required Level: {required_level}")
        
        hero = self.gui.game_state.hero
        hero_level = hero.get('level', 1)
        if hero_level >= required_level:
            self.gui.print_text("✅ You meet the requirements!")
        else:
            self.gui.print_text(f"⚠️  You need level {required_level} (current: {hero_level})")
        
        self.gui.print_text(f"\n💰 The reward of {reward_gold} gold is")
        self.gui.print_text("guaranteed upon successful completion.")
        
        self.gui.print_text("\n❓ Do you want to take on this quest?")
        
        # Show choice again
        button_labels = [
            "⚔️ Yes, I Accept!",
            "😐 No, Too Risky"
        ]
        
        def on_detailed_choice(choice):
            if choice == 1:
                self._accept_side_quest(quest_id, reward_gold, target_biome)
            else:
                self._decline_side_quest()
        
        self.gui.set_buttons(button_labels, on_detailed_choice)
    
    def _decline_side_quest(self):
        """Decline the side quest and continue to normal tavern"""
        self.gui.clear_text()
        self.gui.set_background_image('art/tavern_background.png')
        
        self.gui.print_text("😐 QUEST DECLINED")
        self.gui.print_text("=" * 30)
        
        self.gui.print_text("\nYou politely decline the quest.")
        self.gui.print_text("The NPC looks disappointed but")
        self.gui.print_text("understands your decision.")
        
        self.gui.print_text("\n💭 'Perhaps another adventurer")
        self.gui.print_text("will be able to help...'")
        
        self.gui.print_text("\nThey return to their table, and you")
        self.gui.print_text("continue into the main tavern area.")
        
        # Continue with normal tavern
        self.gui.set_buttons(["🍺 Continue into Tavern"], lambda choice: self._show_normal_tavern())
    
    def _show_normal_tavern(self):
        """Show the normal tavern interface after an NPC encounter"""
        self.gui.clear_text()
        self.gui.set_background_image('art/tavern_background.png')
        
        # Ensure interface is unlocked when entering normal tavern
        self.gui.unlock_interface()
        
        self.gui.print_text("🍺  THE PRANCING PONY TAVERN  🍺")
        self.gui.print_text("=" * 60)
        self.gui.print_text("\nYou enter the main area of the tavern.")
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
            elif choice == 3:
                self.enter_town()
        
        tavern_buttons = [
            "📋 Check Bounty Board",
            "🍺 Talk to Bartender", 
            "🚪 Leave Tavern"
        ]
        
        self.gui.set_buttons(tavern_buttons, on_tavern_choice)
    
    def _visit_blacksmith(self):
        """Visit the blacksmith"""
        self.gui.clear_text()
        self.gui.print_text("⚒️ Entering the blacksmith...")
        self.gui.print_text("You hear the ring of hammer on anvil.")
        
        # Track blacksmith visit for achievements
        if hasattr(self.gui, 'achievement_manager'):
            self.gui.achievement_manager.track_blacksmith_visit()
        
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
        
        # Track fountain visit for achievements
        if hasattr(self.gui, 'achievement_manager'):
            self.gui.achievement_manager.track_fountain_use()
        
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
        self.gui.print_text("Returning to town in a moment...")
        
        # Unlock interface immediately to prevent button lockup
        self.gui.unlock_interface()
        
        # Automatically return to town after 3 seconds
        self.gui.root.after(3000, self.enter_town)
    
    def _leave_town(self):
        """Leave town and return to main menu"""
        self.gui.clear_text()
        self.gui.print_text("🚪 Leaving the town...")
        self.gui.print_text("You wave goodbye to the townspeople")
        self.gui.print_text("and head back to your adventures.")
        
        # Return to main menu after 2 seconds
        self.gui.root.after(2000, self.gui.main_menu)