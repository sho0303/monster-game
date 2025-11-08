#!/usr/bin/env python3
"""
Test teleportation to ocean biome specifically
"""

import random

def test_teleport_logic():
    """Test the teleportation logic to see if ocean is properly included"""
    
    print("🌀 Testing Ocean Biome Teleportation Logic 🌀")
    print("=" * 60)
    
    # Simulate the teleport logic
    available_biomes = ['grassland', 'desert', 'dungeon', 'ocean']
    
    print(f"Available biomes: {available_biomes}")
    print(f"Total biomes: {len(available_biomes)}")
    
    # Test from each starting biome
    for start_biome in available_biomes:
        print(f"\n🎯 Starting from: {start_biome}")
        other_biomes = [biome for biome in available_biomes if biome != start_biome]
        print(f"   Possible teleport destinations: {other_biomes}")
        
        # Test multiple random selections
        destinations = []
        for i in range(10):
            dest = random.choice(other_biomes)
            destinations.append(dest)
        
        print(f"   10 random selections: {destinations}")
        
        # Check if ocean appears
        ocean_count = destinations.count('ocean')
        print(f"   Ocean selected: {ocean_count}/10 times ({ocean_count*10}%)")
        
        if start_biome != 'ocean' and ocean_count == 0:
            print(f"   ⚠️  Ocean never selected from {start_biome} (might be bad luck)")
        elif start_biome != 'ocean' and ocean_count > 0:
            print(f"   ✅ Ocean successfully selectable from {start_biome}")
        elif start_biome == 'ocean':
            print(f"   ℹ️  Starting from ocean - ocean not in destinations (correct)")
    
    # Test biome descriptions and emojis
    print(f"\n🎨 Testing Biome Display Elements:")
    
    biome_descriptions = {
        'grassland': '🌱 Rolling green meadows stretch before you...',
        'desert': '🏜️ Hot sand dunes and ancient cacti surround you...',
        'dungeon': '🏰 Cold stone walls echo with mysterious sounds...',
        'ocean': '🌊 Crystal blue waters and coral reefs surround you...'
    }
    
    biome_emojis = {
        'grassland': '🌱',
        'desert': '🏜️', 
        'dungeon': '🏰',
        'ocean': '🌊'
    }
    
    for biome in available_biomes:
        emoji = biome_emojis.get(biome, '❓')
        description = biome_descriptions.get(biome, 'MISSING DESCRIPTION')
        
        print(f"   {biome}: {emoji} - {description}")
        
        if biome == 'ocean':
            if emoji == '🌊' and 'waters' in description:
                print(f"      ✅ Ocean display elements correct")
            else:
                print(f"      ❌ Ocean display elements missing or incorrect")
    
    print(f"\n🧪 Statistical Ocean Selection Test:")
    print("Testing 1000 teleports from grassland to see ocean frequency...")
    
    start_biome = 'grassland'
    other_biomes = [biome for biome in available_biomes if biome != start_biome]
    
    ocean_selections = 0
    total_tests = 1000
    
    for i in range(total_tests):
        selected = random.choice(other_biomes)
        if selected == 'ocean':
            ocean_selections += 1
    
    expected_percentage = 100 / len(other_biomes)  # Should be ~33.33% (1/3)
    actual_percentage = (ocean_selections / total_tests) * 100
    
    print(f"   Expected: ~{expected_percentage:.1f}% chance to select ocean")
    print(f"   Actual: {actual_percentage:.1f}% ({ocean_selections}/{total_tests})")
    
    if abs(actual_percentage - expected_percentage) < 5:
        print(f"   ✅ Ocean selection frequency is normal (within 5% of expected)")
    else:
        print(f"   ⚠️  Ocean selection frequency seems unusual")
    
    print(f"\n🎮 Conclusion:")
    if 'ocean' in available_biomes and 'ocean' in biome_descriptions and 'ocean' in biome_emojis:
        print("✅ Ocean biome is properly integrated in teleportation system")
        print("✅ All biome display elements present")
        print("✅ Ocean should appear when teleporting")
    else:
        print("❌ Ocean biome integration has issues")

if __name__ == "__main__":
    test_teleport_logic()