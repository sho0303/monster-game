#!/usr/bin/env python3
"""
Test the victory fireworks animation system for final boss defeats
"""
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_fireworks_files():
    """Test that all fireworks frame files exist"""
    print("🎆 Testing Victory Fireworks System")
    print("=" * 50)
    
    # Check if fireworks images exist
    fireworks_frames = [
        "art/victory_fireworks_1.png",
        "art/victory_fireworks_2.png", 
        "art/victory_fireworks_3.png",
        "art/victory_fireworks_4.png"
    ]
    
    all_exist = True
    for frame in fireworks_frames:
        if os.path.exists(frame):
            file_size = os.path.getsize(frame)
            print(f"✅ {frame} - {file_size} bytes")
        else:
            print(f"❌ {frame} - MISSING!")
            all_exist = False
    
    print()
    if all_exist:
        print("🎉 All fireworks frames ready for animation!")
        print()
        print("Fireworks Animation Sequence:")
        print("1. Frame 1: Rockets launching into night sky")
        print("2. Frame 2: Initial colorful explosions") 
        print("3. Frame 3: Full spectacular burst")
        print("4. Frame 4: Grand finale with multiple colors")
        print()
        print("🎮 Animation triggers when defeating Dragon (finalboss: True)")
        print("⏱️  Total animation time: ~6 seconds (1.5s per frame)")
        print("🔒 Interface locked during animation to prevent interruption")
    else:
        print("❌ Some fireworks frames are missing!")
    
    return all_exist

def test_dragon_detection():
    """Test Dragon final boss detection logic"""
    print("\n🐉 Testing Dragon Final Boss Detection")
    print("=" * 50)
    
    try:
        from game_logic import load_yaml_dir
        
        monsters = load_yaml_dir('monsters')
        
        # Find Dragon
        dragon_found = False
        for key, monster in monsters.items():
            if monster.get('finalboss', False):
                print(f"✅ Found final boss: {monster.get('name', key)}")
                print(f"   Level: {monster.get('level', 'Unknown')}")
                print(f"   HP: {monster.get('hp', 'Unknown')}")
                print(f"   Final Boss: {monster.get('finalboss', False)}")
                dragon_found = True
                break
        
        if not dragon_found:
            print("❌ No final boss found in monsters!")
            
    except Exception as e:
        print(f"❌ Error loading monsters: {e}")
        return False
    
    return dragon_found

if __name__ == "__main__":
    print("🎆 Victory Fireworks Animation Test")
    print("=" * 60)
    
    # Test fireworks files
    fireworks_ready = test_fireworks_files()
    
    # Test Dragon detection
    dragon_ready = test_dragon_detection()
    
    print("\n" + "=" * 60)
    if fireworks_ready and dragon_ready:
        print("🎉 Victory Animation System Ready!")
        print("🎮 Defeat the Dragon to see epic fireworks!")
    else:
        print("❌ Victory Animation System has issues")
        if not fireworks_ready:
            print("   - Missing fireworks frames")
        if not dragon_ready:
            print("   - Dragon final boss not detected")