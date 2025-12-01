import os
import sys
import time
import pygame

# Add parent directory to path to import config/gui_audio
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui_audio import Audio
import config

def test_sounds():
    print("Initializing Audio...")
    pygame.init()
    audio = Audio()
    
    if not audio.initialized:
        print("❌ Audio failed to initialize")
        return

    sounds_to_test = [
        config.SOUND_BLACKSMITH_HAMMER,
        config.SOUND_BLACKSMITH_SHARPEN
    ]

    for sound_file in sounds_to_test:
        print(f"\nTesting {sound_file}...")
        path = os.path.join("sounds", sound_file)
        if not os.path.exists(path):
            print(f"❌ File not found: {path}")
            continue
            
        print(f"File exists at: {path}")
        
        try:
            print("Attempting to play...")
            success = audio.play_sound_effect(sound_file)
            if success:
                print("✅ Play call successful")
                # Wait a bit to hear it
                time.sleep(2)
            else:
                print("❌ Play call returned False")
        except Exception as e:
            print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_sounds()
