"""
Test script to verify monster attack image path generation
"""

def test_monster_attack_paths():
    """Test the fixed attack image path generation"""
    print("Testing Monster Attack Image Path Generation")
    print("=" * 50)
    
    # Test monsters (examples from different biomes)
    test_monsters = [
        {
            'name': 'Almighty Kraken',
            'art': 'art/kraken_monster.png',
            'biome': 'ocean'
        },
        {
            'name': 'Enchanted Mermaid', 
            'art': 'art/mermaid_monster.png',
            'biome': 'ocean'
        },
        {
            'name': 'Mermaid Wrangler',
            'art': 'art/merman_king_monster.png',
            'biome': 'ocean'
        },
        {
            'name': 'Cyclops',
            'art': 'art/cyclops_monster.png',
            'biome': 'dungeon'
        },
        {
            'name': 'Some Monster',  # Test fallback
            'biome': 'grassland'
        }
    ]
    
    # Test both old and new methods
    def old_method(monster):
        """Old method that was causing the issue"""
        monster_name = monster.get('name', 'Unknown').lower()
        return f"art/{monster_name}_attack.png"
    
    def new_method(monster):
        """New fixed method with both naming pattern support"""
        if 'art' in monster and monster['art']:
            base_art_path = monster['art']
            # Try the direct replacement first
            attack_image_path = base_art_path.replace('.png', '_attack.png')
            
            # If that doesn't exist, try removing "_monster" from the path
            import os
            if not os.path.exists(attack_image_path):
                alt_path = base_art_path.replace('_monster.png', '_attack.png')
                if os.path.exists(alt_path):
                    attack_image_path = alt_path
            
            return attack_image_path
        else:
            # Fallback to old method if no art field
            monster_name = monster.get('name', 'Unknown').lower()
            return f"art/{monster_name}_attack.png"
    
    print("Monster Attack Path Comparison:")
    print("-" * 50)
    
    for monster in test_monsters:
        print(f"\n🐉 {monster['name']} ({monster.get('biome', 'unknown')})")
        print(f"   Regular art: {monster.get('art', 'No art field')}")
        
        old_path = old_method(monster)
        new_path = new_method(monster)
        
        print(f"   Old method: {old_path}")
        print(f"   New method: {new_path}")
        
        # Check if files exist
        import os
        old_exists = os.path.exists(old_path) if old_path else False
        new_exists = os.path.exists(new_path) if new_path else False
        
        print(f"   Old exists: {'✅' if old_exists else '❌'}")
        print(f"   New exists: {'✅' if new_exists else '❌'}")
        
        if old_path != new_path:
            if new_exists and not old_exists:
                print(f"   🎉 FIXED: New method finds the correct file!")
            elif not new_exists and not old_exists:
                print(f"   ⚠️  Neither method finds file - may need to create attack art")
            else:
                print(f"   🤔 Different paths, need to verify which is correct")

if __name__ == "__main__":
    test_monster_attack_paths()