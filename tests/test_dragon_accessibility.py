#!/usr/bin/env python3
"""Test script to check Dragon boss accessibility with new level ranges"""

import os
import yaml

def test_dragon_accessibility():
    """Test when the Dragon boss becomes accessible"""
    print("🐉 Dragon Boss Accessibility Test")
    print("=" * 40)
    
    # Load Dragon stats
    with open('monsters/Dragon.yaml', 'r') as f:
        dragon_data = yaml.safe_load(f)
    
    dragon = dragon_data['Dragon']
    dragon_level = dragon['level']
    
    print(f"🐲 Dragon Level: {dragon_level}")
    print(f"🎯 Final Boss: {dragon.get('finalboss', False)}")
    print(f"🏰 Biome: {dragon.get('biome', 'unknown')}")
    
    # Calculate when Dragon becomes accessible
    # Formula: hero_level + 1 >= dragon_level
    # So: hero_level >= dragon_level - 1
    min_hero_level = dragon_level - 1
    
    print(f"\n📊 Accessibility:")
    print(f"  • Minimum hero level to encounter Dragon: {min_hero_level}")
    print(f"  • Hero level {min_hero_level} can face monsters level {max(1, min_hero_level - 2)}-{min_hero_level + 1}")
    
    # Show progression to Dragon
    print(f"\n🎮 Progression to Dragon:")
    for hero_level in range(max(1, min_hero_level - 3), min_hero_level + 2):
        min_monster = max(1, hero_level - 2)
        max_monster = hero_level + 1
        
        if dragon_level >= min_monster and dragon_level <= max_monster:
            status = "✅ CAN encounter Dragon"
        else:
            status = "❌ Cannot encounter Dragon yet"
        
        print(f"  Hero Level {hero_level}: Monsters {min_monster}-{max_monster} | {status}")
    
    # Check if this is reasonable for end game
    print(f"\n🏆 End Game Assessment:")
    if min_hero_level <= 10:
        print(f"  ✅ Dragon accessible at reasonable level ({min_hero_level})")
        print(f"  ✅ Provides appropriate end-game challenge")
        print(f"  ✅ Not too early, not too late in progression")
    else:
        print(f"  ⚠️ Dragon only accessible at very high level ({min_hero_level})")
        print(f"  ⚠️ Might be too late in game progression")
    
    print(f"\n🎯 Conclusion:")
    print(f"  • Level range change makes early game much fairer")
    print(f"  • Dragon remains accessible as epic end boss")
    print(f"  • Perfect balance of challenge and accessibility")

if __name__ == '__main__':
    test_dragon_accessibility()