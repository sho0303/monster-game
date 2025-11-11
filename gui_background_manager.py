"""
GUI Background & Biome Manager

Handles all background image management, biome switching, and location-specific functionality.
Extracted from gui_main.py to reduce complexity and improve maintainability.
"""

import tkinter as tk
from PIL import Image, ImageTk
import random


class BackgroundManager:
    """
    Manages background images, biome switching, and location-specific functionality.
    
    This class handles:
    - Background image loading and display
    - Biome configuration and switching
    - Last biome tracking for teleportation
    - Location-specific backgrounds (shop, town)
    - Teleportation functionality with exclusion logic
    - Canvas background management
    """
    
    def __init__(self, image_canvas, audio_manager=None, print_text_callback=None, 
                 lock_interface_callback=None, clear_text_callback=None, main_menu_callback=None):
        """
        Initialize the Background Manager.
        
        Args:
            image_canvas: The tkinter Canvas widget for background display
            audio_manager: Audio manager for sound effects (optional)
            print_text_callback: Function to call for text output (optional)
            lock_interface_callback: Function to lock UI during operations (optional)
            clear_text_callback: Function to clear text display (optional)
            main_menu_callback: Function to return to main menu (optional)
        """
        self.image_canvas = image_canvas
        self.audio = audio_manager
        self.print_text = print_text_callback or self._default_print_text
        self.lock_interface = lock_interface_callback or self._default_lock_interface
        self.clear_text = clear_text_callback or self._default_clear_text
        self.main_menu = main_menu_callback or self._default_main_menu
        
        # Biome state tracking
        self.current_biome = 'grassland'
        self.last_biome = 'grassland'
        
        # Background image reference (prevent garbage collection)
        self.bg_photo = None
        
        # Biome configuration
        self.biome_configs = {
            'grassland': {
                'background': 'art/grassy_background.png',
                'fallback_color': '#4a7c59'
            },
            'desert': {
                'background': 'art/desert_background.png', 
                'fallback_color': '#daa520'
            },
            'dungeon': {
                'background': 'art/dungeon_background.png',
                'fallback_color': '#2d1f1a'
            },
            'ocean': {
                'background': 'art/ocean_background.png',
                'fallback_color': '#0077be'
            },
            'town': {
                'background': 'art/town_background.png',
                'fallback_color': '#2B4C3D'
            },
            'secret_dungeon': {
                'background': 'art/secret_dungeon_background.png',
                'fallback_color': '#1a0d0d'
            }
        }
        
        # Combat biomes (excludes safe zones)
        self.combat_biomes = ['grassland', 'desert', 'dungeon', 'ocean', 'secret_dungeon']
        self.all_biomes = ['grassland', 'desert', 'dungeon', 'ocean', 'town', 'secret_dungeon']
    
    def _default_print_text(self, text, color='#00ff00'):
        """Default print function if none provided"""
        print(f"BackgroundManager: {text}")
    
    def _default_lock_interface(self):
        """Default interface lock function if none provided"""
        pass
    
    def _default_clear_text(self):
        """Default clear text function if none provided"""
        pass
    
    def _default_main_menu(self):
        """Default main menu function if none provided"""
        pass
    
    def set_background_image(self, background_path, fallback_color='#4a7c59'):
        """Set a custom background image for the canvas
        
        Args:
            background_path: Path to the background image file
            fallback_color: Hex color to use if image loading fails
        """
        try:
            # Use fixed canvas dimensions (800x400)
            canvas_width = 800
            canvas_height = 400
                
            # Load and resize the background image
            bg_img = Image.open(background_path)
            bg_img_resized = bg_img.resize((canvas_width, canvas_height), Image.Resampling.NEAREST)
            self.bg_photo = ImageTk.PhotoImage(bg_img_resized)
            
            # Clear canvas and draw new background
            self.image_canvas.delete("all")
            self.image_canvas.create_image(0, 0, image=self.bg_photo, anchor='nw', tags="background")
            
        except Exception as e:
            self.print_text(f"Warning: Could not load background image {background_path}: {e}")
            # Fallback to solid color
            self.image_canvas.configure(bg=fallback_color)
    
    def set_biome_background(self, biome_name='grassland'):
        """Set background based on biome type
        
        Args:
            biome_name: Name of the biome ('grassland', 'desert', 'dungeon', 'ocean', 'town')
        """
        if biome_name in self.biome_configs:
            # Track previous biome before changing - but only if we're actually changing biomes
            if self.current_biome != biome_name:
                self.last_biome = self.current_biome
                
                # Track biome visit for achievements
                if hasattr(self, 'gui') and hasattr(self.gui, 'achievement_manager'):
                    self.gui.achievement_manager.track_biome_visit(biome_name)
                    # Check for secret dungeon discovery
                    if biome_name == 'secret_dungeon':
                        self.gui.achievement_manager.track_secret_dungeon_discovery()
            # If current_biome == biome_name, keep the existing last_biome
            
            self.current_biome = biome_name
            config = self.biome_configs[biome_name]
            self.set_background_image(config['background'], config['fallback_color'])
        else:
            # Default to grassland - only update last_biome if we're changing
            if self.current_biome != 'grassland':
                self.last_biome = self.current_biome
                
                # Track biome visit for achievements
                if hasattr(self, 'gui') and hasattr(self.gui, 'achievement_manager'):
                    self.gui.achievement_manager.track_biome_visit('grassland')
            # If already grassland, keep the existing last_biome
            
            self.current_biome = 'grassland'
            self.set_background_image('art/grassy_background.png', '#4a7c59')
    
    def reset_background(self):
        """Reset to the default biome background"""
        self.set_biome_background(self.current_biome)
    
    def set_shop_background(self):
        """Set the shop-specific background (not part of biome system)"""
        self.set_background_image('art/shop_background.png', '#654321')
    
    def set_blacksmith_background(self):
        """Set the blacksmith-specific background (not part of biome system)"""
        self.set_background_image('art/blacksmith_background.png', '#404050')
    
    def set_town_background(self):
        """Set the town-specific background"""
        self.set_background_image('art/town_background.png', '#2B4C3D')
    
    def set_secret_dungeon_background(self):
        """Set the secret dungeon background"""
        self.set_background_image('art/secret_dungeon_background.png', '#1a0d0d')
    
    def cycle_biomes(self, available_biomes=None):
        """Cycle through available biomes for testing/debugging
        
        Args:
            available_biomes: List of biomes to cycle through (default: all biomes)
        
        Returns:
            str: The new biome name
        """
        # Use provided biomes or default to all biomes
        biomes_to_cycle = available_biomes if available_biomes else self.all_biomes
        
        current_index = biomes_to_cycle.index(self.current_biome) if self.current_biome in biomes_to_cycle else 0
        next_index = (current_index + 1) % len(biomes_to_cycle)
        next_biome = biomes_to_cycle[next_index]
        
        # Set the new biome
        self.set_biome_background(next_biome)
        
        # Show feedback message
        biome_emojis = {
            'grassland': '🌱',
            'desert': '🏜️', 
            'dungeon': '🏰',
            'ocean': '🌊',
            'town': '🏘️',
            'secret_dungeon': '🕳️'
        }
        emoji = biome_emojis.get(next_biome, '🌍')
        self.print_text(f"{emoji} Biome switched to: {next_biome.title().replace('_', ' ')}")
        
        return next_biome
    
    def teleport_to_random_biome(self, exclude_current=True, exclude_last=True, combat_only=True, hero_available_biomes=None):
        """Teleport to a random biome with exclusion logic
        
        Args:
            exclude_current: Whether to exclude the current biome (default: True)
            exclude_last: Whether to exclude the last biome to prevent loops (default: True)
            combat_only: Whether to only include combat biomes (default: True)
            hero_available_biomes: List of biomes available to hero (includes secret areas) (default: None)
        
        Returns:
            str: The new biome name
        """
        # Lock interface to prevent interruptions during teleportation
        self.lock_interface()
        
        # Choose biome pool based on what's available to the hero
        if hero_available_biomes:
            if combat_only:
                # Filter to only combat biomes that the hero can access
                available_biomes = [biome for biome in hero_available_biomes if biome in self.combat_biomes]
            else:
                available_biomes = hero_available_biomes
        else:
            # Fallback to default biome pool
            available_biomes = self.combat_biomes if combat_only else self.all_biomes
        
        # Build exclusion set
        excluded_biomes = set()
        if exclude_current:
            excluded_biomes.add(self.current_biome)
        if exclude_last and hasattr(self, 'last_biome') and self.last_biome:
            excluded_biomes.add(self.last_biome)
        
        # Filter available biomes
        other_biomes = [biome for biome in available_biomes if biome not in excluded_biomes]
        
        # Fallback: if we've excluded too many biomes, just exclude current biome
        if not other_biomes:
            other_biomes = [biome for biome in available_biomes if biome != self.current_biome]
        
        # Select random biome from remaining options
        new_biome = random.choice(other_biomes)
        
        # Set the new biome
        self.set_biome_background(new_biome)
        
        # Show teleport message with dramatic effect
        self._show_teleport_animation(new_biome)
        
        return new_biome
    
    def _show_teleport_animation(self, new_biome):
        """Show teleportation animation and messages
        
        Args:
            new_biome: The biome being teleported to
        """
        biome_descriptions = {
            'grassland': '🌱 Rolling green meadows stretch before you...',
            'desert': '🏜️ Hot sand dunes and ancient cacti surround you...',
            'dungeon': '🏰 Cold stone walls echo with mysterious sounds...',
            'ocean': '🌊 Crystal blue waters and coral reefs surround you...',
            'secret_dungeon': '🕳️ Ancient shadows whisper forgotten secrets...'
        }
        
        biome_emojis = {
            'grassland': '🌱',
            'desert': '🏜️', 
            'dungeon': '🏰',
            'ocean': '🌊',
            'secret_dungeon': '🕳️'
        }
        
        emoji = biome_emojis.get(new_biome, '🌍')
        description = biome_descriptions.get(new_biome, 'You find yourself in a strange new place...')
        
        # Clear screen for dramatic effect
        self.clear_text()
        self.print_text("✨ TELEPORTING... ✨")
        
        # Play sound effect if audio manager is available
        if self.audio:
            try:
                self.audio.play_sound_effect('teleport.mp3')
            except:
                pass  # Ignore audio errors
        
        # Show teleport result after brief delay
        def show_teleport_result():
            self.print_text(f"\n{emoji} ═══════════════════════════════════════════════ {emoji}")
            self.print_text("🌀 TELEPORTATION COMPLETE 🌀")
            self.print_text(f"{emoji} ═══════════════════════════════════════════════ {emoji}")
            self.print_text(f"\n{description}")
            self.print_text(f"\n📍 Current location: {new_biome.title()}")
            
            # Return to main menu after showing result
            if self.main_menu:
                # Use root.after if available, otherwise just call directly
                try:
                    self.image_canvas.after(3000, self.main_menu)
                except:
                    self.main_menu()
        
        # Show result after teleportation delay
        try:
            self.image_canvas.after(1000, show_teleport_result)
        except:
            show_teleport_result()  # Fallback to immediate call
    
    def get_current_biome(self):
        """Get the current biome name
        
        Returns:
            str: Current biome name
        """
        return self.current_biome
    
    def get_last_biome(self):
        """Get the last biome name
        
        Returns:
            str: Last biome name
        """
        return self.last_biome
    
    def set_biome_state(self, current_biome, last_biome=None):
        """Set biome state (useful for save/load)
        
        Args:
            current_biome: The current biome name
            last_biome: The last biome name (optional)
        """
        self.current_biome = current_biome
        if last_biome is not None:
            self.last_biome = last_biome
    
    def get_biome_config(self, biome_name):
        """Get configuration for a specific biome
        
        Args:
            biome_name: Name of the biome
            
        Returns:
            dict: Biome configuration or None if not found
        """
        return self.biome_configs.get(biome_name)
    
    def get_available_biomes(self, combat_only=False):
        """Get list of available biomes
        
        Args:
            combat_only: Whether to only return combat biomes (default: False)
            
        Returns:
            list: List of biome names
        """
        return self.combat_biomes.copy() if combat_only else self.all_biomes.copy()
    
    def is_combat_biome(self, biome_name=None):
        """Check if a biome allows combat
        
        Args:
            biome_name: Biome to check (default: current biome)
            
        Returns:
            bool: True if combat is allowed in this biome
        """
        if biome_name is None:
            biome_name = self.current_biome
        return biome_name in self.combat_biomes
    
    def initialize_default_background(self):
        """Initialize the default background (called during startup)"""
        try:
            # Use fixed canvas dimensions (800x400)
            canvas_width = 800
            canvas_height = 400
                
            # Load the grassy background image
            bg_img = Image.open('art/grassy_background.png')
            
            # Resize to fixed canvas dimensions
            bg_img_resized = bg_img.resize((canvas_width, canvas_height), Image.Resampling.NEAREST)
            self.bg_photo = ImageTk.PhotoImage(bg_img_resized)
            
            # Clear canvas and draw background
            self.image_canvas.delete("all")
            self.image_canvas.create_image(0, 0, image=self.bg_photo, anchor='nw', tags="background")
            
        except Exception as e:
            self.print_text(f"Warning: Could not load background image: {e}")
            # Fallback to solid color
            self.image_canvas.configure(bg='#4a7c59')