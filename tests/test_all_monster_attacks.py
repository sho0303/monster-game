"""
Comprehensive test to find all monsters with missing attack images
"""
import yaml
import os
import glob

def comprehensive_monster_attack_test():
    """Test all monsters to find missing attack images"""
    print("Comprehensive Monster Attack Image Test")
    print("=" * 50)
    
    # Load all monster files
    monster_files = glob.glob("monsters/*.yaml")
    
    print(f"Found {len(monster_files)} monster files to check...")
    print()
    
    missing_attacks = []
    working_attacks = []
    fixed_by_update = []
    
    for monster_file in monster_files:
        with open(monster_file, 'r') as f:
            try:
                monsters = yaml.safe_load(f)
                if not monsters:
                    continue
                    
                for monster_key, monster_data in monsters.items():
                    if not isinstance(monster_data, dict):
                        continue
                    
                    monster_name = monster_data.get('name', monster_key)
                    biome = monster_data.get('biome', 'unknown')
                    art_path = monster_data.get('art', '')
                    
                    # Test old method
                    old_attack_path = f"art/{monster_name.lower()}_attack.png"
                    
                    # Test new method
                    if art_path:
                        # Try direct replacement first
                        new_attack_path = art_path.replace('.png', '_attack.png')
                        
                        # If doesn't exist, try removing "_monster"
                        if not os.path.exists(new_attack_path):
                            alt_path = art_path.replace('_monster.png', '_attack.png')
                            if os.path.exists(alt_path):
                                new_attack_path = alt_path
                    else:
                        new_attack_path = old_attack_path
                    
                    # Check results
                    old_exists = os.path.exists(old_attack_path)
                    new_exists = os.path.exists(new_attack_path)
                    
                    status = "✅ Working" if new_exists else "❌ Missing"
                    fixed = not old_exists and new_exists
                    
                    result = {
                        'name': monster_name,
                        'biome': biome,
                        'file': monster_file,
                        'art': art_path,
                        'old_path': old_attack_path,
                        'new_path': new_attack_path,
                        'old_exists': old_exists,
                        'new_exists': new_exists,
                        'fixed': fixed,
                        'status': status
                    }
                    
                    if new_exists:
                        working_attacks.append(result)
                        if fixed:
                            fixed_by_update.append(result)
                    else:
                        missing_attacks.append(result)
                        
            except yaml.YAMLError as e:
                print(f"Error reading {monster_file}: {e}")
                continue
    
    # Report results by biome
    print("RESULTS BY BIOME:")
    print("=" * 20)
    
    biomes = ['ocean', 'grassland', 'desert', 'dungeon', 'unknown']
    
    for biome in biomes:
        print(f"\n🏞️  {biome.upper()}")
        print("-" * 15)
        
        biome_working = [m for m in working_attacks if m['biome'] == biome]
        biome_missing = [m for m in missing_attacks if m['biome'] == biome]
        biome_fixed = [m for m in fixed_by_update if m['biome'] == biome]
        
        print(f"✅ Working: {len(biome_working)}")
        print(f"❌ Missing: {len(biome_missing)}")
        print(f"🔧 Fixed by update: {len(biome_fixed)}")
        
        if biome_fixed:
            print("   Fixed monsters:")
            for monster in biome_fixed:
                print(f"      • {monster['name']}")
        
        if biome_missing:
            print("   Still missing:")
            for monster in biome_missing:
                print(f"      • {monster['name']} (needs {monster['new_path']})")
    
    # Summary
    print(f"\n📊 SUMMARY:")
    print("=" * 12)
    total_monsters = len(working_attacks) + len(missing_attacks)
    print(f"Total monsters: {total_monsters}")
    print(f"✅ Working attacks: {len(working_attacks)} ({len(working_attacks)/total_monsters*100:.1f}%)")
    print(f"❌ Missing attacks: {len(missing_attacks)} ({len(missing_attacks)/total_monsters*100:.1f}%)")
    print(f"🔧 Fixed by this update: {len(fixed_by_update)}")
    
    if fixed_by_update:
        print(f"\n🎉 OCEAN BIOME ISSUE RESOLVED!")
        print("The following ocean monsters now have working attack animations:")
        for monster in fixed_by_update:
            if monster['biome'] == 'ocean':
                print(f"   ✅ {monster['name']}")

if __name__ == "__main__":
    comprehensive_monster_attack_test()