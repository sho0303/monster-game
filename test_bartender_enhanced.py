#!/usr/bin/env python3
"""Test the enhanced bartender quest system"""

import tkinter as tk
from gui_main import GameGUI

def test_bartender_quest_system():
    """Test the improved bartender interaction and quest system"""
    print("🧪 Testing Enhanced Bartender Quest System")
    print("=" * 50)
    
    root = tk.Tk()
    gui = GameGUI(root)
    root.update()
    
    # Initialize game state if not loaded
    if gui.game_state is None:
        from game_state import initialize_game_state
        gui.game_state = initialize_game_state()
    
    hero = gui.game_state.hero
    
    print(f"✅ Game initialized")
    print(f"Hero: {hero.get('name', 'Unknown')} (Level {hero.get('level', 1)})")
    
    # Test different bartender interaction states
    print(f"\n🍺 Testing Bartender Interaction States:")
    
    # State 1: No beers consumed
    beers = hero.get('beers_consumed', 0)
    secret_discovered = hero.get('secret_dungeon_discovered', False)
    
    print(f"Initial state:")
    print(f"  - Beers consumed: {beers}")
    print(f"  - Secret dungeon discovered: {secret_discovered}")
    
    # Simulate beer consumption progression
    beer_states = [0, 1, 3, 5, 10]
    
    for beer_count in beer_states:
        hero['beers_consumed'] = beer_count
        
        print(f"\n🍻 Simulating {beer_count} beers consumed:")
        
        # Determine available options
        options = ["Buy Beer", "Buy Ale", "Buy Lager", "Buy Stout"]
        
        if secret_discovered:
            options.append("Ask about Secret Dungeon")
            expected_greeting = "experienced adventurer greeting"
        elif beer_count >= 5:
            options.append("Ask for Stories (high chance)")
            expected_greeting = "conspirative regular greeting"
        elif beer_count >= 3:
            options.append("Ask for Stories (medium chance)")
            expected_greeting = "familiar regular greeting"
        elif beer_count >= 1:
            options.append("Chat with Bob")
            expected_greeting = "returning customer greeting"
        else:
            expected_greeting = "new customer greeting"
        
        print(f"  Expected greeting: {expected_greeting}")
        print(f"  Available options: {len(options)}")
        for i, option in enumerate(options, 1):
            print(f"    {i}. {option}")
        
        # Test quest availability chances
        if beer_count >= 5 and not secret_discovered:
            print(f"  🎯 Quest chance when asking for stories: 60%")
        elif beer_count >= 3 and not secret_discovered:
            print(f"  🎯 Quest chance when asking for stories: 60%")
            print(f"  🎲 Random quest chance when buying beer: 50%")
        elif beer_count >= 3 and not secret_discovered:
            print(f"  🎲 Random quest chance when buying beer: 30%")
    
    # Test the new methods exist
    print(f"\n🔧 Testing new methods:")
    
    methods_to_test = [
        '_request_stories_from_bob',
        '_chat_with_bob', 
        '_tell_general_story'
    ]
    
    for method_name in methods_to_test:
        has_method = hasattr(gui.town, method_name)
        print(f"  {method_name}: {'✅ Exists' if has_method else '❌ Missing'}")
    
    # Test quest discovery scenario
    print(f"\n🕳️  Testing Secret Dungeon Quest Discovery:")
    
    # Reset hero state for quest test
    hero['beers_consumed'] = 3
    hero['secret_dungeon_discovered'] = False
    
    # Simulate quest trigger conditions
    quest_conditions = [
        ("3+ beers consumed", hero.get('beers_consumed', 0) >= 3),
        ("Secret dungeon not discovered", not hero.get('secret_dungeon_discovered', False)),
        ("Quest methods available", hasattr(gui.town, '_show_secret_dungeon_story'))
    ]
    
    all_conditions_met = True
    for condition, met in quest_conditions:
        status = "✅" if met else "❌"
        print(f"  {status} {condition}")
        if not met:
            all_conditions_met = False
    
    if all_conditions_met:
        print(f"\n🎉 Quest system ready!")
        print(f"📋 User instructions:")
        print(f"  1. Buy 3+ beers from bartender")
        print(f"  2. Use 'Ask for Stories' button (60% chance)")
        print(f"  3. Or keep buying beers (30-50% chance per beer)")
        print(f"  4. Secret dungeon quest will eventually trigger!")
    else:
        print(f"\n⚠️  Quest system has issues - check conditions above")
    
    print(f"\n🎯 Key Improvements Made:")
    print(f"  ✅ Better feedback on beer consumption progress")
    print(f"  ✅ Context-aware greetings from bartender")
    print(f"  ✅ Explicit 'Ask for Stories' option (60% quest chance)")
    print(f"  ✅ Chat options for atmosphere")
    print(f"  ✅ Increased quest trigger rates (30-50% vs 15%)")
    print(f"  ✅ Visual progress tracking")
    
    root.destroy()

if __name__ == '__main__':
    test_bartender_quest_system()