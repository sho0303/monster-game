"""
Interface protocols for GUI dependency injection.

This module defines clear contracts for what GUI modules need,
reducing tight coupling and improving testability.
"""
from typing import Protocol, Callable, Optional, List, Any
from tkinter import Misc


class TextDisplayProtocol(Protocol):
    """Interface for text display operations"""
    
    def print_text(self, text: str, color: Optional[str] = None) -> None:
        """Print text to the display area"""
        ...
    
    def clear_text(self) -> None:
        """Clear the text display area"""
        ...


class ImageDisplayProtocol(Protocol):
    """Interface for image display operations"""
    
    def show_image(self, image_path: str) -> None:
        """Display a single image"""
        ...
    
    def show_images(self, image_paths: List[str], layout: str = "auto") -> None:
        """Display multiple images with specified layout"""
        ...
    
    def show_background(self, background_path: str) -> None:
        """Set background image"""
        ...


class BackgroundManagerProtocol(Protocol):
    """Interface for background management"""
    
    current_biome: str
    last_biome: str
    
    def set_background_image(self, background_path: str, fallback_color: str = '#4a7c59') -> None:
        """Set a custom background image"""
        ...
    
    def reset_background(self) -> None:
        """Reset to default biome background"""
        ...
    
    def set_biome_background(self, biome_name: str = 'grassland') -> None:
        """Set background based on biome type"""
        ...
    
    def set_shop_background(self) -> None:
        """Set shop-specific background"""
        ...
    
    def set_blacksmith_background(self) -> None:
        """Set blacksmith-specific background"""
        ...
    
    def set_town_background(self) -> None:
        """Set town-specific background"""
        ...
    
    def set_tavern_background(self) -> None:
        """Set tavern-specific background"""
        ...


class AudioProtocol(Protocol):
    """Interface for audio operations"""
    
    def play_sound_effect(self, sound_file: str, volume: float = 1.0) -> None:
        """Play a sound effect"""
        ...
    
    def play_background_music(self, music_file: str, loop: bool = False, volume: float = 0.5) -> None:
        """Play background music"""
        ...
    
    def stop_music(self) -> None:
        """Stop background music"""
        ...


class GameStateProtocol(Protocol):
    """Interface for game state access"""
    
    hero: dict
    monsters: dict
    heros: dict
    choices: dict


class ButtonManagerProtocol(Protocol):
    """Interface for button management"""
    
    def set_buttons(self, button_labels: List[str], callback: Callable[[int], None]) -> None:
        """Set button labels and callback"""
        ...
    
    def show_buttons(self, button_configs: List[tuple]) -> None:
        """Show buttons with configurations"""
        ...
    
    def lock_interface(self) -> None:
        """Disable all buttons/inputs"""
        ...
    
    def unlock_interface(self) -> None:
        """Enable all buttons/inputs"""
        ...


class TimerProtocol(Protocol):
    """Interface for scheduling callbacks"""
    
    def after(self, ms: int, func: Callable) -> str:
        """Schedule a function to be called after delay"""
        ...


class NavigationProtocol(Protocol):
    """Interface for navigation between screens"""
    
    def main_menu(self) -> None:
        """Return to main menu"""
        ...


# Composite interfaces for common use cases

class UIManagerProtocol(TextDisplayProtocol, ImageDisplayProtocol, 
                       ButtonManagerProtocol, Protocol):
    """Combined interface for UI operations (text, images, buttons)"""
    pass


class GameContextProtocol(Protocol):
    """Complete game context with all dependencies - use this for modules that need broad access"""
    
    # Core systems
    game_state: GameStateProtocol
    audio: AudioProtocol
    background_manager: BackgroundManagerProtocol
    root: TimerProtocol
    
    # Subsystems (for cross-module communication)
    combat: Any
    shop: Any
    blacksmith: Any
    inventory: Any
    tavern: Any
    town: Any
    quest_manager: Any
    save_load_manager: Any
    monster_encounter: Any
    achievements: Any
    
    # UI operations
    def print_text(self, text: str, color: Optional[str] = None) -> None:
        ...
    
    def clear_text(self) -> None:
        ...
    
    def show_image(self, image_path: str) -> None:
        ...
    
    def show_images(self, image_paths: List[str], layout: str = "auto") -> None:
        ...
    
    def set_buttons(self, button_labels: List[str], callback: Callable[[int], None]) -> None:
        ...
    
    def show_buttons(self, button_configs: List[tuple]) -> None:
        ...
    
    def lock_interface(self) -> None:
        ...
    
    def unlock_interface(self) -> None:
        ...
    
    def main_menu(self) -> None:
        ...
