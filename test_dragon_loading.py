#!/usr/bin/env python3
"""Test script to check Dragon loading and monster conflicts"""

import os
import yaml

def test_dragon_loading():
    print("=== DRAGON LOADING TEST ===\n")
    
    # Load all monsters
    monsters = {}
    for file in os.listdir('monsters/'):
        if file.endswith('.yaml'):
            filepath = f'monsters/{file}'
            print(f"Loading: {filepath}")
            with open(filepath, 'r') as f:
                data = yaml.safe_load(f)
                print(f"  Data keys: {list(data.keys())}")
                monsters.update(data)
    
    print(f"\nTotal monsters loaded: {len(monsters)}")
    print("\nAll loaded monsters:")
    for key, monster in monsters.items():
        name = monster.get('name', 'NO NAME')
        level = monster.get('level', 'NO LEVEL')
        biome = monster.get('biome', 'NO BIOME')
        finalboss = monster.get('finalboss', False)
        print(f"  {key}: {name} - Level {level} - Biome: {biome} - Final Boss: {finalboss}")
    
    # Check specifically for Dragon
    print(f"\n=== DRAGON CHECK ===")
    if 'Dragon' in monsters:
        dragon = monsters['Dragon']
        print(f"Dragon found in loaded monsters:")
        print(f"   Name: {dragon.get('name', 'MISSING')}")
        print(f"   Level: {dragon.get('level', 'MISSING')}")
        print(f"   Biome: {dragon.get('biome', 'MISSING')}")
        print(f"   Final Boss: {dragon.get('finalboss', 'MISSING')}")
        print(f"   HP: {dragon.get('hp', 'MISSING')}")
        print(f"   Attack: {dragon.get('attack', 'MISSING')}")
    else:
        print("Dragon NOT found in loaded monsters!")
    
    # Check for duplicate Dragon keys
    dragon_files = []
    for file in os.listdir('monsters/'):
        if file.endswith('.yaml'):
            filepath = f'monsters/{file}'
            with open(filepath, 'r') as f:
                data = yaml.safe_load(f)
                if 'Dragon' in data:
                    dragon_files.append(file)
    
    print(f"\n=== DRAGON KEY CONFLICTS ===")
    print(f"Files containing 'Dragon' key: {dragon_files}")
    
    if len(dragon_files) > 1:
        print("WARNING: Multiple files contain 'Dragon' key - later files overwrite earlier ones!")
        for file in dragon_files:
            with open(f'monsters/{file}', 'r') as f:
                data = yaml.safe_load(f)
                dragon_data = data.get('Dragon', {})
                print(f"  {file}: {dragon_data.get('name', 'NO NAME')} - Level {dragon_data.get('level', 'NO LEVEL')}")

if __name__ == '__main__':
    test_dragon_loading()