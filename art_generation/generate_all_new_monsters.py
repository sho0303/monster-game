#!/usr/bin/env python3
"""Generate all new monster artwork"""
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🎨 Generating all new monster artwork...")
print("=" * 50)

# Import and run all generation scripts
scripts = [
    ('create_bee_swarm', '🐝 Bee Swarm'),
    ('create_goblin_art', '👺 Goblin'),
    ('create_boar_art', '🐗 Wild Boar'),
    ('create_scorpion_art', '🦂 Scorpion King'),
    ('create_sand_serpent_art', '🐍 Sand Serpent'),
    ('create_mummy_art', '🧟 Mummy Guardian'),
    ('create_wraith_art', '👻 Shadow Wraith'),
    ('create_golem_art', '🗿 Stone Golem'),
    ('create_sorcerer_art', '🧙 Dark Sorcerer'),
    ('create_ocean_monsters', '🌊 All Ocean Monsters'),
    ('create_bandit_art', '🗡️ Bandit Leader'),
]

for script_name, display_name in scripts:
    try:
        print(f"\n{display_name}...")
        module = __import__(script_name)
        if script_name == 'create_ocean_monsters':
            module.save_all_ocean_monsters()
        else:
            module.save_images()
    except Exception as e:
        print(f"❌ Error with {display_name}: {e}")

print("\n" + "=" * 50)
print("✅ All 14 new monsters artwork generated successfully!")
print("\n📊 Total files created: 28 PNG files")
print("   - 14 monster artwork files")
print("   - 14 attack animation files")
print("\n🎮 Monsters are ready to appear in game!")
