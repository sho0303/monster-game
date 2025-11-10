#!/usr/bin/env python3
"""Test script to show the new level range system"""

def test_level_ranges():
    """Test the new level range system"""
    print("⚔️ New Monster Level Range System")
    print("=" * 50)
    
    print("📐 Formula: max(1, hero_level - 2) ≤ monster_level ≤ hero_level + 1")
    print()
    
    # Test different hero levels
    test_levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    print("🎯 Level Ranges by Hero Level:")
    print("-" * 40)
    
    for hero_level in test_levels:
        min_monster_level = max(1, hero_level - 2)
        max_monster_level = hero_level + 1
        
        print(f"  Hero Level {hero_level:2d}: Monsters Level {min_monster_level:2d}-{max_monster_level:2d}")
    
    print()
    print("📊 Key Improvements:")
    print("  ✅ Level 1 heroes: Face monsters level 1-2 (was 1-4)")
    print("  ✅ Level 2 heroes: Face monsters level 1-3 (was 1-5)")  
    print("  ✅ Level 3 heroes: Face monsters level 1-4 (was 1-6)")
    print("  ✅ Maximum challenge: Only 1 level above (was 3 levels)")
    print("  ✅ Minimum challenge: Up to 2 levels below for variety")
    print("  ✅ Never below level 1 monsters")
    
    print()
    print("🎮 Benefits:")
    print("  • Much fairer for new players")
    print("  • Gradual difficulty progression")
    print("  • Still allows some challenge (+1 level)")
    print("  • Maintains variety with lower-level monsters")
    print("  • High-level players can still access end-game content")

if __name__ == '__main__':
    test_level_ranges()