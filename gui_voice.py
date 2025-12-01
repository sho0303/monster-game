"""
Voice/Text-to-Speech Manager for the game
Handles threaded speech generation using Edge TTS (Neural Voices)
"""
import threading
import queue
import asyncio
import edge_tts
import tempfile
import os
import pygame
import time
from logger_utils import get_logger

logger = get_logger(__name__)

class VoiceManager:
    """
    Manages Text-to-Speech generation in a separate thread using Edge TTS.
    """
    def __init__(self):
        self.queue = queue.Queue()
        self.enabled = True
        # Use a high-quality English voice
        self.voice_name = "en-GB-SoniaNeural"  # British female, very clear for fantasy
        # Alternatives: en-US-ChristopherNeural (Male), en-US-AriaNeural (Female)
        
        self.current_channel = None
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        logger.info("VoiceManager (Edge TTS) initialized")

    def _run_loop(self):
        """Worker thread loop for processing speech requests"""
        # Create a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        while True:
            text = self.queue.get()
            if text is None:
                break
            
            if self.enabled:
                try:
                    # Run the async generation synchronously in this thread
                    loop.run_until_complete(self._generate_and_play(text))
                except Exception as e:
                    logger.error(f"TTS Error during playback: {e}")
            
            self.queue.task_done()
        
        loop.close()

    async def _generate_and_play(self, text):
        """Generate MP3 and play it"""
        temp_file = None
        try:
            # Create a temporary file for the audio
            fd, temp_path = tempfile.mkstemp(suffix='.mp3')
            os.close(fd)
            temp_file = temp_path
            
            # Generate audio using Edge TTS
            communicate = edge_tts.Communicate(text, self.voice_name)
            await communicate.save(temp_path)
            
            # Play using pygame mixer
            if pygame.mixer.get_init():
                # Use Sound object to allow mixing with background music
                sound = pygame.mixer.Sound(temp_path)
                
                # Adjust volume (voice should be clear)
                sound.set_volume(1.0)
                
                # Play and wait for it to finish
                channel = sound.play()
                self.current_channel = channel
                
                # Wait for playback to finish while keeping GUI responsive
                # (This thread is separate from GUI thread, so blocking here is fine)
                if channel:
                    while channel.get_busy():
                        pygame.time.wait(100)
                
                self.current_channel = None
            else:
                logger.warning("Pygame mixer not initialized, cannot play voice")
                
        except Exception as e:
            logger.error(f"Edge TTS generation failed: {e}")
        finally:
            # Clean up temp file
            if temp_file and os.path.exists(temp_file):
                try:
                    # Small delay to ensure file handle is released by pygame
                    time.sleep(0.1) 
                    os.remove(temp_file)
                except Exception as e:
                    logger.warning(f"Could not remove temp voice file: {e}")

    def speak(self, text):
        """
        Queue text to be spoken.
        
        Args:
            text (str): The text to speak
        """
        if self.enabled and text:
            # Clean up text
            clean_text = self._clean_text(text)
            if clean_text:
                self.queue.put(clean_text)
    
    def _clean_text(self, text):
        """Remove emojis and extra whitespace for cleaner speech"""
        # Edge TTS handles most things well, but let's strip excessive whitespace
        return " ".join(text.split())

    def interrupt(self):
        """Stop current speech and clear queue"""
        # Clear queue
        while not self.queue.empty():
            try:
                self.queue.get_nowait()
                self.queue.task_done()
            except queue.Empty:
                break
        
        # Stop current playback
        if self.current_channel:
            self.current_channel.stop()

    def stop(self):
        """Stop the voice manager thread"""
        self.queue.put(None)
        if self.thread.is_alive():
            self.thread.join(timeout=1.0)

    def toggle(self):
        """Toggle voice on/off"""
        self.enabled = not self.enabled
        return self.enabled
