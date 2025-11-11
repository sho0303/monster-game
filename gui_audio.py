"""
Enhanced Audio handler for the game GUI
Supports simultaneous background music and sound effects
"""
from pygame import mixer
import os
from pathlib import Path


class Audio:
    """Enhanced audio handler with background music and sound effects support"""
    
    def __init__(self):
        self.initialized = False
        self.background_music_playing = False
        self.current_background_music = None
        self.sound_cache = {}  # Cache for sound effects
        self.music_volume = 0.5  # Background music volume (0.0 to 1.0)
        self.sfx_volume = 0.8    # Sound effects volume (0.0 to 1.0)
        
        self._initialize_mixer()
    
    def _initialize_mixer(self):
        """Initialize pygame mixer with optimal settings to prevent crackling"""
        try:
            # Use larger buffer size to prevent crackling/distortion
            # Lower frequency and larger buffer for better stability
            mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=2048)
            mixer.init()
            mixer.set_num_channels(6)  # Reduce simultaneous channels to prevent overload
            self.initialized = True
        except Exception as e:
            print(f"Warning: Could not initialize audio system: {e}")
            self.initialized = False
    
    def play_background_music(self, music_file, loop=True, volume=None):
        """
        Play background music (looping by default)
        
        Args:
            music_file: Name of music file in sounds/ directory
            loop: Whether to loop the music (default: True)
            volume: Volume level 0.0-1.0 (default: uses self.music_volume)
        """
        if not self.initialized:
            return False
            
        try:
            music_path = f'./sounds/{music_file}'
            if not Path(music_path).exists():
                print(f"Warning: Music file not found: {music_path}")
                return False
            
            # Stop current background music if playing
            if self.background_music_playing:
                mixer.music.stop()
            
            # Load and play new background music
            mixer.music.load(music_path)
            volume_level = volume if volume is not None else self.music_volume
            mixer.music.set_volume(volume_level)
            
            loops = -1 if loop else 0  # -1 = infinite loop, 0 = play once
            mixer.music.play(loops)
            
            self.background_music_playing = True
            self.current_background_music = music_file
            return True
            
        except Exception as e:
            print(f"Warning: Could not play background music: {e}")
            return False
    
    def stop_background_music(self, fade_out_ms=1000):
        """
        Stop background music with optional fade out
        
        Args:
            fade_out_ms: Fade out duration in milliseconds (default: 1000ms)
        """
        if not self.initialized or not self.background_music_playing:
            return
            
        try:
            if fade_out_ms > 0:
                mixer.music.fadeout(fade_out_ms)
            else:
                mixer.music.stop()
            
            self.background_music_playing = False
            self.current_background_music = None
        except Exception as e:
            print(f"Warning: Could not stop background music: {e}")
    
    def play_sound_effect(self, sound_file, volume=None, max_duration_ms=None):
        """
        Play a sound effect (can play simultaneously with background music)
        
        Args:
            sound_file: Name of sound file in sounds/ directory
            volume: Volume level 0.0-1.0 (default: uses self.sfx_volume)
            max_duration_ms: Maximum duration in milliseconds (None = no limit)
        """
        if not self.initialized:
            return False
            
        try:
            sound_path = f'./sounds/{sound_file}'
            if not Path(sound_path).exists():
                print(f"Warning: Sound file not found: {sound_path}")
                return False
            
            # Use cached sound or load new one
            if sound_file not in self.sound_cache:
                sound = mixer.Sound(sound_path)
                self.sound_cache[sound_file] = sound
            else:
                sound = self.sound_cache[sound_file]
            
            # Set volume and play
            volume_level = volume if volume is not None else self.sfx_volume
            sound.set_volume(volume_level)
            channel = sound.play()
            
            # Limit duration if max_duration_ms is set (only for attack sounds)
            if channel and max_duration_ms is not None and max_duration_ms > 0:
                # Use a timer to stop the sound after max_duration_ms
                import threading

                def stop_after_delay():
                    import time
                    time.sleep(max_duration_ms / 1000.0)
                    if channel.get_busy():
                        channel.fadeout(100)  # 100ms fadeout
                threading.Thread(target=stop_after_delay, daemon=True).start()
            
            return True
            
        except Exception as e:
            print(f"Warning: Could not play sound effect: {e}")
            return False
    
    def play_sound(self, name):
        """
        Legacy method for backwards compatibility
        Determines if it's background music or sound effect based on file name
        """
        if not self.initialized:
            return
            
        # Check if this is background music (longer audio files)
        music_keywords = ['music', 'background', 'bgm', 'theme', 'ambient']
        sound_file_lower = name.lower()
        
        is_background_music = any(keyword in sound_file_lower for keyword in music_keywords)
        
        if is_background_music or name == 'start.mp3':
            # Treat as background music
            self.play_background_music(name, loop=True)
        else:
            # Treat as sound effect
            self.play_sound_effect(name)
    
    def set_music_volume(self, volume):
        """Set background music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        if self.background_music_playing:
            mixer.music.set_volume(self.music_volume)
    
    def set_sfx_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def is_music_playing(self):
        """Check if background music is currently playing"""
        return self.initialized and self.background_music_playing and mixer.music.get_busy()
    
    def pause_music(self):
        """Pause background music"""
        if self.initialized and self.background_music_playing:
            mixer.music.pause()
    
    def unpause_music(self):
        """Resume paused background music"""
        if self.initialized and self.background_music_playing:
            mixer.music.unpause()
    
    def get_current_music(self):
        """Get the name of currently playing background music"""
        return self.current_background_music if self.background_music_playing else None
    
    def get_volume(self):
        """Get current music volume (0.0 to 1.0)"""
        return self.music_volume
    
    def set_volume(self, volume):
        """Set overall volume (affects music)"""
        self.set_music_volume(volume)
    
    def adjust_volume(self, delta):
        """Adjust volume by delta amount"""
        new_volume = max(0.0, min(1.0, self.music_volume + delta))
        self.set_music_volume(new_volume)
    
    def toggle_mute(self):
        """Toggle mute on/off"""
        if self.music_volume > 0:
            self._saved_volume = self.music_volume
            self.set_music_volume(0)
        else:
            restored_volume = getattr(self, '_saved_volume', 0.5)
            self.set_music_volume(restored_volume)
    
    def reset_audio(self):
        """Reset audio system to fix crackling/distortion issues"""
        try:
            # Stop all sounds
            mixer.stop()
            if self.background_music_playing:
                mixer.music.stop()
            
            # Clear sound cache to free memory
            self.sound_cache.clear()
            
            # Reinitialize mixer with anti-crackling settings
            mixer.quit()
            mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=2048)
            mixer.init()
            mixer.set_num_channels(6)
            
            # Reset state
            self.background_music_playing = False
            self.current_background_music = None
            
            print("🔊 Audio system reset to fix crackling")
            return True
            
        except Exception as e:
            print(f"Warning: Could not reset audio system: {e}")
            return False
