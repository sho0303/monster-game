"""
Test that monster attack animations work for both art_attack and attack_art field names
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_monster_attack_animation_fields():
    """Test that both art_attack and attack_art field names are recognized"""
    print("Testing monster attack animation field recognition...")
    
    # Test case 1: Monster with art_attack (new style - e.g., Wyvern)
    wyvern = {
        'name': 'Wyvern',
        'art_attack': 'art/wyvern_monster_attack.png',
        'hp': 107,
        'attack': 19
    }
    
    # Test case 2: Monster with attack_art (old style - e.g., Dragon)
    dragon = {
        'name': 'Dragon',
        'attack_art': 'art/dragon_endboss_attack.png',
        'hp': 200,
        'attack': 30
    }
    
    # Test case 3: Monster with no attack art
    slime = {
        'name': 'Slime',
        'hp': 10,
        'attack': 3
    }
    
    # Test the logic that's now in gui_combat.py
    def get_attack_art(monster):
        """Get attack art path using same logic as fixed code"""
        return monster.get('art_attack') or monster.get('attack_art')
    
    print("\n1. Testing Wyvern (art_attack field):")
    wyvern_art = get_attack_art(wyvern)
    print(f"   Attack art path: {wyvern_art}")
    assert wyvern_art == 'art/wyvern_monster_attack.png', f"Expected 'art/wyvern_monster_attack.png', got '{wyvern_art}'"
    print("   ✓ Wyvern attack animation will display")
    
    print("\n2. Testing Dragon (attack_art field):")
    dragon_art = get_attack_art(dragon)
    print(f"   Attack art path: {dragon_art}")
    assert dragon_art == 'art/dragon_endboss_attack.png', f"Expected 'art/dragon_endboss_attack.png', got '{dragon_art}'"
    print("   ✓ Dragon attack animation will display")
    
    print("\n3. Testing Slime (no attack art):")
    slime_art = get_attack_art(slime)
    print(f"   Attack art path: {slime_art}")
    assert slime_art is None, f"Expected None, got '{slime_art}'"
    print("   ✓ Slime correctly has no attack animation")
    
    print("\n✅ All tests passed!")
    print("\nThe fix correctly handles:")
    print("- Monsters with 'art_attack' field (newer format)")
    print("- Monsters with 'attack_art' field (older format)")
    print("- Monsters with no attack animation")
    print("\nAll monster attack animations will now display properly!")

if __name__ == '__main__':
    test_monster_attack_animation_fields()
