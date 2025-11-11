#!/usr/bin/env python3
"""
Test improved audio system fixes for distortion
"""
import tkinter as tk
from gui_main import GameGUI
from game_state import initialize_game_state

def test_improved_audio():
    """Test if audio distortion is fixed with improved system"""
    root = tk.Tk()
    gui = GameGUI(root)
    root.update()
    
    # Initialize game state
    gui.game_state = initialize_game_state()
    
    print("🔊 Testing Improved Audio System...")
    print("="*50)
    
    # Test 1: Regular sound effects
    print("✅ Test 1: Regular sound effects")
    gui.audio.play_sound_effect('punch.mp3')
    root.after(800, lambda: gui.audio.play_sound_effect('win.mp3'))
    
    # Test 2: Monster attack sounds with max_duration (should be smooth now)
    print("✅ Test 2: Monster attack sounds with duration limits")
    root.after(2000, lambda: gui.audio.play_sound_effect('dragon-growl.mp3', max_duration_ms=3000))
    root.after(3000, lambda: gui.audio.play_sound_effect('cyclops-attack.mp3', max_duration_ms=2500))
    
    # Test 3: Rapid sound effects (stress test)
    print("✅ Test 3: Rapid succession sounds")
    root.after(6000, lambda: _rapid_sounds_test_improved(gui))
    
    # Test 4: Background music + sound effects
    print("✅ Test 4: Background music + sound effects")
    root.after(8000, lambda: gui.audio.play_background_music('start.mp3', volume=0.3))
    root.after(9000, lambda: gui.audio.play_sound_effect('sword-clash.mp3'))
    root.after(10000, lambda: gui.audio.play_sound_effect('teleport.mp3'))
    
    # Test 5: Audio reset functionality
    print("✅ Test 5: Audio reset")
    root.after(12000, lambda: gui.audio.reset_audio())
    root.after(13000, lambda: gui.audio.play_sound_effect('tada.mp3'))
    
    print("🎵 Listen for clear, crisp audio without distortion")
    print("❌ If you still hear crackling, press 'R' in-game to reset audio")
    print("Close window when testing is complete")
    
    root.mainloop()

def _rapid_sounds_test_improved(gui):
    """Test rapid succession of sounds with improved system"""
    sounds = ['punch.mp3', 'sword-clash.mp3', 'buzzer.mp3', 'gulp.mp3', 'teleport.mp3']
    for i, sound in enumerate(sounds):
        gui.root.after(i * 300, lambda s=sound: gui.audio.play_sound_effect(s))

if __name__ == '__main__':
    test_improved_audio()