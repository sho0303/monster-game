#!/usr/bin/env python3
"""Test the enhanced bartender quest system in action"""

import tkinter as tk
from gui_main import GameGUI

def test_bartender_in_action():
    """Test the bartender system by actually running it"""
    print("🧪 Testing Enhanced Bartender System in Action")
    print("=" * 60)
    
    root = tk.Tk()
    gui = GameGUI(root)
    root.update()
    
    # Initialize game state if needed
    if gui.game_state is None:
        from game_state import initialize_game_state
        gui.game_state = initialize_game_state()
    
    hero = gui.game_state.hero
    
    print(f"✅ Game initialized")
    print(f"Hero: {hero.get('name', 'Unknown')} (Level {hero.get('level', 1)})")
    
    # Set hero to test state
    hero['beers_consumed'] = 0
    hero['secret_dungeon_discovered'] = False
    hero['gold'] = 1000  # Give plenty of gold for testing
    
    print(f"\n🍺 Testing Bartender System:")
    print(f"Starting state:")
    print(f"  - Beers consumed: {hero.get('beers_consumed', 0)}")
    print(f"  - Gold: {hero.get('gold', 0)}")
    print(f"  - Secret discovered: {hero.get('secret_dungeon_discovered', False)}")
    
    # Test progression through beer consumption
    print(f"\n📊 Simulating beer consumption progression:")
    
    for beers in [0, 1, 2, 3, 5, 10]:
        hero['beers_consumed'] = beers
        
        print(f"\n🍻 At {beers} beers consumed:")
        
        # Check what greeting we'd get
        if hero.get('secret_dungeon_discovered', False):
            expected_greeting = "experienced adventurer"
        elif beers >= 5:
            expected_greeting = "conspirative regular"
        elif beers >= 3:
            expected_greeting = "familiar regular"
        elif beers >= 1:
            expected_greeting = "returning customer"
        else:
            expected_greeting = "new customer"
        
        print(f"  Expected greeting type: {expected_greeting}")
        
        # Check available actions
        available_actions = ["Buy Beer", "Buy Ale", "Buy Lager", "Buy Stout"]
        
        if beers >= 3:
            available_actions.append("Ask for Stories")
            print(f"  ✨ 'Ask for Stories' option now available! (60% quest chance)")
        
        if beers >= 1 and beers < 3:
            available_actions.append("Chat with Bob")
        
        print(f"  Available actions ({len(available_actions)}):")
        for i, action in enumerate(available_actions, 1):
            print(f"    {i}. {action}")
    
    # Test quest trigger logic
    print(f"\n🎯 Quest Trigger Analysis:")
    
    quest_scenarios = [
        ("New customer (0 beers)", 0, "Only beer purchases"),
        ("Returning (1-2 beers)", 2, "Chat option + beer purchases"),
        ("Regular (3-4 beers)", 3, "Stories option (60% chance) + random beer chance (50%)"),
        ("Loyal regular (5+ beers)", 5, "Stories option (60% chance) + random beer chance (30%)")
    ]
    
    for scenario, beers, expected in quest_scenarios:
        print(f"\n  📋 {scenario}:")
        print(f"     Beer count: {beers}")
        print(f"     Quest opportunities: {expected}")
        
        if beers >= 3:
            print(f"     🎲 'Ask for Stories' button: 60% quest chance")
        if beers >= 3:
            print(f"     🎲 Random beer purchase: {'30%' if beers >= 5 else '50%'} quest chance")
    
    # Test method availability
    print(f"\n🔧 Enhanced Method Availability:")
    
    methods_to_check = [
        ('_talk_to_bartender', "Main bartender interaction"),
        ('_request_stories_from_bob', "Explicit story request (60% chance)"),
        ('_chat_with_bob', "Casual conversation option"),
        ('_tell_general_story', "Fallback story when no quest"),
        ('_show_secret_dungeon_story', "Secret dungeon quest story")
    ]
    
    for method_name, description in methods_to_check:
        has_method = hasattr(gui.town, method_name)
        status = "✅" if has_method else "❌"
        print(f"  {status} {method_name}: {description}")
    
    # Test actual bartender interaction
    print(f"\n🧪 Live Bartender Test:")
    print(f"Opening actual bartender interface...")
    
    # This will show the actual bartender interface
    # User can interact with it to test the new features
    print(f"\n📋 Test Instructions:")
    print(f"  1. The bartender interface will open")
    print(f"  2. Buy several beers to increase consumption count")
    print(f"  3. Watch for new 'Ask for Stories' button at 3+ beers")
    print(f"  4. Watch for 'Chat with Bob' option at 1-2 beers")
    print(f"  5. Try the 'Ask for Stories' option for 60% quest chance")
    print(f"  6. Close the window when done testing")
    
    # Set up proper town navigation
    gui.town.enter_town()
    
    # Start main loop for interactive testing
    print(f"\n🚀 Starting interactive test - bartender interface should appear!")
    root.mainloop()

if __name__ == '__main__':
    test_bartender_in_action()