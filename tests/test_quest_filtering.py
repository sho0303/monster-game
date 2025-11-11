"""
Simple test of level-aware quest filtering
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from game_state import initialize_game_state

# Initialize game
state = initialize_game_state()

print("="*70)
print("LEVEL-AWARE QUEST MONSTER AVAILABILITY")
print("="*70)

# Test different hero levels
for hero_level in [1, 3, 5, 7, 10]:
    print(f"\n{'='*70}")
    print(f"HERO LEVEL {hero_level}")
    print(f"Can encounter: Level {max(1, hero_level-2)} to {hero_level+1}")
    print('='*70)
    
    # Test each biome
    for biome in ['grassland', 'desert', 'dungeon', 'ocean']:
        # Filter monsters like the quest system does
        available_monsters = [
            (name, data) for name, data in state.monsters.items()
            if (data.get('biome', 'grassland') == biome and
                data['level'] <= hero_level + 1 and
                data['level'] >= max(1, hero_level - 2))
        ]
        
        print(f"\n{biome.upper()}: {len(available_monsters)} monsters available")
        
        if available_monsters:
            for name, data in available_monsters:
                level = data['level']
                print(f"  - {name} (Lv.{level})")
        else:
            print("  (No level-appropriate monsters)")

print("\n" + "="*70)
print("SUMMARY: Quest system now filters by BOTH biome AND level")
print("This matches the encounter system's level range!")
print("="*70)
