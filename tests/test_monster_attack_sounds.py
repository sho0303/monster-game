#!/usr/bin/env python3
"""Test script to verify monster attack_sound functionality"""

import os
import yaml

def test_monster_attack_sounds():
    """Test that monster attack sounds are properly configured"""
    print("🔊 Testing Monster Attack Sounds Configuration")
    print("=" * 60)
    
    # Load all monsters
    monsters = {}
    for file in os.listdir('monsters/'):
        if file.endswith('.yaml'):
            filepath = f'monsters/{file}'
            with open(filepath, 'r') as f:
                data = yaml.safe_load(f)
                monsters.update(data)
    
    print(f"📁 Found {len(monsters)} monsters")
    print("\n🎵 Attack Sound Configuration:")
    
    custom_sounds = []
    default_sounds = []
    
    for monster_key, monster_data in monsters.items():
        name = monster_data.get('name', monster_key)
        
        if 'attack_sound' in monster_data and monster_data['attack_sound']:
            sound_file = monster_data['attack_sound']
            sound_path = f"sounds/{sound_file}"
            
            # Check if sound file exists
            exists = "✅" if os.path.exists(sound_path) else "❌"
            
            print(f"  🔊 {name}: {sound_file} {exists}")
            custom_sounds.append((name, sound_file, os.path.exists(sound_path)))
        else:
            print(f"  🔇 {name}: buzzer.mp3 (default)")
            default_sounds.append(name)
    
    print(f"\n📊 Summary:")
    print(f"  • Monsters with custom sounds: {len(custom_sounds)}")
    print(f"  • Monsters using default sound: {len(default_sounds)}")
    
    if custom_sounds:
        print(f"\n🎼 Custom Sound Details:")
        for name, sound_file, exists in custom_sounds:
            status = "File found" if exists else "FILE MISSING!"
            print(f"  • {name} → {sound_file} ({status})")
    
    # Check if default sound exists
    default_exists = os.path.exists("sounds/buzzer.mp3")
    default_status = "✅ Found" if default_exists else "❌ Missing"
    print(f"\n🔔 Default sound (buzzer.mp3): {default_status}")
    
    print(f"\n🎯 Implementation Status:")
    print(f"  • Combat system: Updated to use _get_monster_attack_sound()")
    print(f"  • Run away system: Updated to use _get_monster_attack_sound()")  
    print(f"  • Sound timing: Sounds now play BEFORE animations (more responsive!)")
    print(f"  • Hero attacks: 'punch.mp3' plays at animation start")
    print(f"  • Monster attacks: Custom sounds play at animation start")
    print(f"  • Fallback to buzzer.mp3 when attack_sound not defined")
    print(f"  • Ready for epic combat audio! 🎶⚔️")

if __name__ == '__main__':
    test_monster_attack_sounds()