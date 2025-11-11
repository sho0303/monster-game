#!/usr/bin/env python3
"""
Test bee attack sound specifically
"""
import sys
import os
import tkinter as tk

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from gui_audio import Audio

def test_bee_sound():
    """Test the bee attack sound file"""
    print("🐝 Testing Bee Attack Sound")
    print("=" * 50)
    
    # Initialize audio system
    audio = Audio()
    
    if not audio.initialized:
        print("❌ Audio system not initialized")
        return
    
    print("✅ Audio system initialized")
    
    # Test bee-attack.mp3 specifically
    bee_sound = "bee-attack.mp3"
    
    # Check if file exists
    import pathlib
    sound_path = pathlib.Path(f"sounds/{bee_sound}")
    if sound_path.exists():
        print(f"✅ Sound file exists: {sound_path}")
    else:
        print(f"❌ Sound file missing: {sound_path}")
        return
    
    print(f"\n🔊 Playing {bee_sound}...")
    success = audio.play_sound_effect(bee_sound)
    
    if success:
        print("✅ Sound played successfully!")
        print("   (You should hear buzzing/bee sounds)")
    else:
        print("❌ Failed to play sound")
    
    # Also test the fallback buzzer sound
    print(f"\n🔊 Testing fallback sound (buzzer.mp3)...")
    success2 = audio.play_sound_effect("buzzer.mp3")
    
    if success2:
        print("✅ Buzzer sound played successfully!")
    else:
        print("❌ Failed to play buzzer sound")
    
    # Wait a moment for sounds to play
    import time
    print("\n⏱️ Waiting 5 seconds for sounds to complete...")
    time.sleep(5)
    
    print("\n🐝 Bee sound test completed!")

if __name__ == '__main__':
    test_bee_sound()