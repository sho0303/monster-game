#!/usr/bin/env python3
"""Check monster levels across all biomes to help with level progression"""

import yaml
import os

def analyze_monster_levels():
    """Analyze monster levels in each biome"""
    print("🗺️  Monster Level Analysis by Biome")
    print("=" * 50)
    
    monsters_dir = "monsters"
    biome_monsters = {}
    
    # Load all monsters
    for filename in os.listdir(monsters_dir):
        if filename.endswith('.yaml'):
            filepath = os.path.join(monsters_dir, filename)
            with open(filepath, 'r') as f:
                monster_data = yaml.safe_load(f)
                
            for monster_name, data in monster_data.items():
                level = data.get('level', 1)
                biome = data.get('biome', 'grassland')
                
                if biome not in biome_monsters:
                    biome_monsters[biome] = []
                
                biome_monsters[biome].append({
                    'name': monster_name,
                    'level': level,
                    'hp': data.get('hp', 0),
                    'attack': data.get('attack', 0)
                })
    
    # Sort and display by biome
    biome_order = ['grassland', 'desert', 'ocean', 'dungeon']
    
    for biome in biome_order:
        if biome in biome_monsters:
            monsters = sorted(biome_monsters[biome], key=lambda x: x['level'])
            print(f"\n🌍 {biome.upper()}:")
            
            for monster in monsters:
                print(f"  Lv.{monster['level']}: {monster['name']} (HP: {monster['hp']}, ATK: {monster['attack']})")
            
            levels = [m['level'] for m in monsters]
            print(f"  📊 Level range: {min(levels)}-{max(levels)}")
    
    # Recommendations for level 4 player
    print(f"\n🎯 Recommendations for Level 4 Player:")
    print(f"   (Game spawns monsters within ±2 levels, so Lv.2-6)")
    
    suitable_biomes = []
    for biome, monsters in biome_monsters.items():
        suitable_monsters = [m for m in monsters if 2 <= m['level'] <= 6]
        if suitable_monsters:
            levels = [m['level'] for m in suitable_monsters]
            suitable_biomes.append((biome, len(suitable_monsters), min(levels), max(levels)))
    
    suitable_biomes.sort(key=lambda x: -x[1])  # Sort by number of suitable monsters
    
    for biome, count, min_lv, max_lv in suitable_biomes:
        print(f"   {biome.capitalize()}: {count} monsters (Lv.{min_lv}-{max_lv})")

if __name__ == '__main__':
    analyze_monster_levels()