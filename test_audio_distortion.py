#!/usr/bin/env python3
"""
Test audio distortion issues
"""
import tkinter as tk
from gui_main import GameGUI
from game_state import initialize_game_state

def test_audio_distortion():
    """Test if audio distortion occurs during multiple sound effects"""
    root = tk.Tk()
    gui = GameGUI(root)
    root.update()
    
    # Initialize game state
    gui.game_state = initialize_game_state()
    
    print("🔊 Testing Audio Distortion...")
    print("="*50)
    
    # Test regular sound effects
    print("Testing regular sound effects:")
    gui.audio.play_sound_effect('punch.mp3')
    root.after(500, lambda: gui.audio.play_sound_effect('win.mp3'))
    root.after(1000, lambda: gui.audio.play_sound_effect('teleport.mp3'))
    
    # Test monster attack sounds with max_duration (problematic)
    print("Testing monster attack sounds with max_duration:")
    root.after(2000, lambda: gui.audio.play_sound_effect('dragon-growl.mp3', max_duration_ms=3000))
    root.after(3000, lambda: gui.audio.play_sound_effect('cyclops-attack.mp3', max_duration_ms=3000))
    root.after(4000, lambda: gui.audio.play_sound_effect('kraken-attack.mp3', max_duration_ms=3000))
    
    # Test rapid sound effects (can cause distortion)
    print("Testing rapid sound effects:")
    root.after(6000, lambda: _rapid_sounds_test(gui))
    
    print("Listen for crackling, distortion, or audio artifacts...")
    print("Close window when testing is complete")
    
    root.mainloop()

def _rapid_sounds_test(gui):
    """Test rapid succession of sounds"""
    sounds = ['punch.mp3', 'sword-clash.mp3', 'buzzer.mp3', 'gulp.mp3']
    for i, sound in enumerate(sounds):
        gui.root.after(i * 200, lambda s=sound: gui.audio.play_sound_effect(s))

if __name__ == '__main__':
    test_audio_distortion()