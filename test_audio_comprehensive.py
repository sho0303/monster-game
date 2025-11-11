#!/usr/bin/env python3
"""
Comprehensive test for fixed audio distortion issues
"""
import tkinter as tk
from gui_main import GameGUI
from game_state import initialize_game_state

def test_audio_fixes():
    """Comprehensive test for all audio distortion fixes"""
    root = tk.Tk()
    gui = GameGUI(root)
    root.update()
    
    # Initialize game state
    gui.game_state = initialize_game_state()
    
    print("🔊 COMPREHENSIVE AUDIO FIX TEST")
    print("="*50)
    
    # Display current audio settings
    print(f"🎵 Audio initialized: {gui.audio.initialized}")
    print(f"🔊 Music volume: {int(gui.audio.music_volume * 100)}%")
    print(f"🔊 SFX volume: {int(gui.audio.sfx_volume * 100)}%")
    print(f"⏱️ Sound cooldown: {gui.audio.sound_cooldown_ms}ms")
    print()
    
    # Test sequence
    test_steps = [
        (1000, "🔊 Testing basic sound effects", lambda: gui.audio.play_sound_effect('punch.mp3')),
        (2000, "🐉 Testing dragon attack (3s limit)", lambda: gui.audio.play_sound_effect('dragon-growl.mp3', max_duration_ms=3000)),
        (4000, "⚔️ Testing sword clash", lambda: gui.audio.play_sound_effect('sword-clash.mp3')),
        (5000, "🎵 Starting background music", lambda: gui.audio.play_background_music('start.mp3', volume=0.4)),
        (6000, "🏆 Testing victory sound over music", lambda: gui.audio.play_sound_effect('win.mp3')),
        (7500, "💫 Testing teleport sound", lambda: gui.audio.play_sound_effect('teleport.mp3')),
        (9000, "⚡ Testing rapid sounds (cooldown protection)", lambda: _rapid_sound_spam_test(gui)),
        (12000, "🔄 Testing audio reset", lambda: gui.audio.reset_audio()),
        (13000, "🎉 Final test sound", lambda: gui.audio.play_sound_effect('tada.mp3')),
    ]
    
    for delay, description, action in test_steps:
        root.after(delay, lambda desc=description, act=action: _execute_test_step(desc, act))
    
    # Display instructions
    print("🎧 LISTENING TEST INSTRUCTIONS:")
    print("✅ Audio should be clear and crisp")
    print("❌ No crackling, popping, or distortion")
    print("⚡ Rapid sounds should be protected by cooldown")
    print("🎵 Background music + sound effects should work together")
    print("🔄 Audio reset should restore clean audio")
    print()
    print("If you hear any distortion, press 'R' in the game to reset audio!")
    print("Close window when done testing.")
    
    root.mainloop()

def _execute_test_step(description, action):
    """Execute a test step with description"""
    print(description)
    try:
        action()
    except Exception as e:
        print(f"❌ Error in test step: {e}")

def _rapid_sound_spam_test(gui):
    """Test rapid sound spam to verify cooldown protection works"""
    print("   Spamming punch.mp3 rapidly (should be filtered by cooldown)...")
    # Try to play the same sound 10 times rapidly
    for i in range(10):
        gui.audio.play_sound_effect('punch.mp3')
    
    # Also test different sounds rapidly (should all play)
    sounds = ['buzzer.mp3', 'gulp.mp3', 'sword-clash.mp3']
    for i, sound in enumerate(sounds):
        gui.root.after(i * 200, lambda s=sound: gui.audio.play_sound_effect(s))

if __name__ == '__main__':
    test_audio_fixes()