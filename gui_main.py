"""
Main GUI class for the monster game
"""
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
from time import sleep
import yaml

import config
from logger_utils import get_logger
from resource_utils import get_resource_path, resource_exists
from game_state import initialize_game_state
from gui_audio import Audio
from gui_combat import CombatGUI
from gui_shop import ShopGUI
from gui_blacksmith import BlacksmithGUI
from gui_inventory import InventoryGUI
from gui_monster_encounter import MonsterEncounterGUI
from gui_quests import QuestManager
from gui_save_load import SaveLoadManager
from gui_town import TownGUI
from gui_tavern import TavernGUI
from gui_image_manager import ImageManager
from gui_background_manager import BackgroundManager
from gui_achievements import AchievementManager

logger = get_logger(__name__)


class GameGUI:
    """Graphical User Interface for the monster game"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("MonsterGame")
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.root.configure(bg=config.COLOR_BACKGROUND)
        
        # Additional window management for foreground display
        try:
            # Ensure window appears in front and gets focus
            self.root.deiconify()  # Make sure window is not minimized
            self.root.lift()       # Bring to front
            self.root.attributes('-topmost', True)  # Temporarily on top
            self.root.focus_force()  # Force focus
            
            # Remove topmost after initial display
            self.root.after(config.VERY_SHORT_DELAY, lambda: self.root.attributes('-topmost', False))
        except Exception as e:
            logger.warning(f"Could not configure window display: {e}")
        
        # Enable keyboard shortcuts
        self.root.bind('<KeyPress>', self._handle_keypress)
        self.root.focus_set()  # Make sure window can receive key events
        
        # Keyboard shortcut state
        self.keyboard_enabled = True
        self.current_selected_button = 1  # Track which button is selected for arrow navigation
        
        # Game state
        self.game_state = None
        self.audio = Audio()
        self.combat = None
        self.shop = None
        self.blacksmith = None
        self.inventory = None
        self.monster_encounter = None
        self.quest_manager = None
        self.save_load_manager = None
        self.town = None
        
        # Create main layout
        self._create_widgets()
        
        # Start game initialization
        self.root.after(100, self.initialize_game)
    
    def _create_widgets(self):
        """Create the GUI widgets"""
        # Top frame container for the canvas - fixed size container
        self.image_frame = tk.Frame(
            self.root, 
            relief='flat',
            bd=0,
            highlightthickness=0
        )
        
        # Create canvas for proper image compositing without transparency issues
        # Fixed size canvas that won't resize with window
        self.image_canvas = tk.Canvas(
            self.image_frame,
            highlightthickness=0,
            relief='flat',
            bd=0,
            width=config.CANVAS_WIDTH,
            height=config.CANVAS_HEIGHT
        )
        self.image_frame.pack(pady=10, padx=5)  # Removed fill=tk.BOTH to prevent expansion
        
        # Pack the canvas with fixed size (no expand or fill)
        self.image_canvas.pack()
        
        # Set background image for the canvas
        self._set_frame_background()
        
        # Text output area (read-only)
        self.text_area = scrolledtext.ScrolledText(
            self.root, 
            wrap=tk.WORD,
            width=config.TEXT_AREA_WIDTH,
            height=config.TEXT_AREA_HEIGHT,
            bg=config.COLOR_TEXT_AREA_BG,
            fg=config.COLOR_TEXT_DEFAULT,
            font=('Courier', 10),
            state=tk.DISABLED,  # Make read-only
            cursor='arrow'  # Change cursor to indicate non-editable
        )
        self.text_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Button frame container
        self.button_frame = tk.Frame(self.root, bg=config.COLOR_BACKGROUND)
        self.button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Dynamic button list (will be created as needed)
        self.buttons = []
        self.button_rows = []  # Track button row frames
        
        self.current_action = None
        
        # Initialize managers after all UI components are created
        self.image_manager = ImageManager(self.image_canvas, self.print_text)
        
        self.background_manager = BackgroundManager(
            image_canvas=self.image_canvas,
            audio_manager=self.audio,
            print_text_callback=self.print_text,
            lock_interface_callback=self.lock_interface,
            clear_text_callback=self.clear_text,
            main_menu_callback=self.main_menu
        )
        
        # Link background manager to image manager for floor offset positioning
        self.image_manager.background_manager = self.background_manager
    
    @property
    def current_biome(self):
        """Get current biome from BackgroundManager"""
        return self.background_manager.current_biome
    
    @current_biome.setter  
    def current_biome(self, value):
        """Set current biome in BackgroundManager"""
        self.background_manager.current_biome = value
    
    @property
    def last_biome(self):
        """Get last biome from BackgroundManager"""
        return self.background_manager.last_biome
    
    @last_biome.setter
    def last_biome(self, value):
        """Set last biome in BackgroundManager"""
        self.background_manager.last_biome = value
    
    def _set_frame_background(self):
        """Set the background image using canvas for proper compositing"""
        # Schedule background setup after the canvas is properly sized
        self.root.after(100, self._update_canvas_background)
    
    def _update_canvas_background(self):
        """Update the canvas background using BackgroundManager"""
        self.background_manager.initialize_default_background()
    
    def set_background_image(self, background_path, fallback_color='#4a7c59'):
        """Set a custom background image for the canvas"""
        self.background_manager.set_background_image(background_path, fallback_color)
    
    def reset_background(self):
        """Reset to the default biome background"""
        self.background_manager.reset_background()
    
    def set_biome_background(self, biome_name='grassland'):
        """Set background based on biome type"""
        self.background_manager.set_biome_background(biome_name)
    
    def set_shop_background(self):
        """Set the shop-specific background (not part of biome system)"""
        self.background_manager.set_shop_background()
    
    def set_blacksmith_background(self):
        """Set the blacksmith-specific background (not part of biome system)"""
        self.background_manager.set_blacksmith_background()
    
    def set_town_background(self):
        """Set the town-specific background"""
        self.background_manager.set_town_background()
    
    def set_tavern_background(self):
        """Set the tavern-specific background"""
        self.background_manager.set_tavern_background()
    
    def _get_canvas_dimensions(self):
        """Get fixed canvas dimensions"""
        return self.image_manager.get_canvas_dimensions()
    
    def _add_canvas_image(self, image_path, x, y, width=None, height=None, tags="foreground"):
        """Add an image to the canvas at the specified position"""
        return self.image_manager.add_canvas_image(image_path, x, y, width, height, tags)
    
    def _clear_foreground_images(self):
        """Clear all foreground images from canvas"""
        self.image_manager.clear_foreground_images()
    
    def _create_buttons(self, count):
        """Create the specified number of buttons in rows of 3"""
        # Clear existing buttons
        self._clear_buttons()
        
        # Calculate number of rows needed (3 buttons per row)
        buttons_per_row = config.BUTTONS_PER_ROW
        num_rows = (count + buttons_per_row - 1) // buttons_per_row
        
        # Create button rows
        for row in range(num_rows):
            # Create frame for this row
            row_frame = tk.Frame(self.button_frame, bg=config.COLOR_BACKGROUND)
            row_frame.pack(pady=2, fill=tk.X)
            self.button_rows.append(row_frame)
            
            # Calculate buttons for this row
            start_btn = row * buttons_per_row
            end_btn = min(start_btn + buttons_per_row, count)
            buttons_in_row = end_btn - start_btn
            
            # Create buttons for this row
            for i in range(start_btn, end_btn):
                btn = tk.Button(
                    row_frame,
                    text=f"Option {i+1}",
                    command=lambda idx=i+1: self.current_action(idx) if self.current_action else None,
                    bg=config.COLOR_BUTTON_BG,
                    fg=config.COLOR_BUTTON_FG,
                    font=('Arial', 11, 'bold'),
                    width=config.BUTTON_WIDTH,
                    height=config.BUTTON_HEIGHT,
                    state=tk.DISABLED
                )
                
                # Center buttons in row - calculate padding
                if buttons_in_row < buttons_per_row:
                    # For partial rows, add extra spacing to center buttons
                    side_padding = 10
                else:
                    side_padding = 5
                
                btn.pack(side=tk.LEFT, padx=side_padding, expand=True, fill=tk.X)
                self.buttons.append(btn)
    
    def _clear_buttons(self):
        """Remove all existing buttons and row frames"""
        for btn in self.buttons:
            btn.destroy()
        self.buttons = []
        
        # Clear button row frames
        for row_frame in self.button_rows:
            row_frame.destroy()
        self.button_rows = []
    
    def show_image(self, image_path):
        """Display a single image using canvas for proper background compositing"""
        self.image_manager.show_image(image_path)
    
    def show_images(self, image_paths, layout="auto"):
        """Display multiple images using canvas for proper background compositing
        
        Args:
            image_paths: List of image file paths
            layout: "horizontal", "vertical", "grid", or "auto" (default)
        """
        self.image_manager.show_images(image_paths, layout)
    
    def _reset_image_layout(self):
        """Reset to single image layout using canvas"""
        self.image_manager.reset_image_layout()
    
    def _clear_image_area(self):
        """Clear all foreground images from canvas, preserving background"""
        self.image_manager.clear_image_area()
        
        # Re-set the background if needed
        if hasattr(self, 'bg_label'):
            self.bg_label.lower()
    
    def _create_horizontal_layout(self, image_paths):
        """Legacy method - now handled by ImageManager"""
        self.image_manager.create_horizontal_layout(image_paths)
    
    def _create_vertical_layout(self, image_paths):
        """Legacy method - now handled by ImageManager"""
        self.image_manager.create_vertical_layout(image_paths)
    
    def _create_grid_layout(self, image_paths):
        """Legacy method - now handled by ImageManager"""
        self.image_manager.create_grid_layout(image_paths)
    
    def _load_image_to_label(self, image_path, label, size=(200, 150)):
        """Legacy method - now handled by ImageManager"""
        self.image_manager.load_image_to_label(image_path, label, size)
    
    def print_text(self, text, color='#00ff00'):
        """Print text to the text area with color support"""
        self.text_area.config(state=tk.NORMAL)  # Temporarily enable for writing
        
        # Process text for variable coloring
        colored_text = self._process_text_colors(text)
        
        # Insert text with appropriate colors
        for text_part, text_color in colored_text:
            # Create or get color tag
            tag_name = f"color_{text_color.replace('#', '')}"
            self.text_area.tag_config(tag_name, foreground=text_color)
            
            # Insert text with color tag
            start_index = self.text_area.index(tk.END + "-1c")
            self.text_area.insert(tk.END, text_part)
            end_index = self.text_area.index(tk.END + "-1c")
            self.text_area.tag_add(tag_name, start_index, end_index)
        
        # Add newline with default color
        self.text_area.insert(tk.END, '\n')
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)  # Disable again
        self.root.update()
    
    def _process_text_colors(self, text):
        """Process text and return list of (text, color) tuples"""
        import re
        
        # Define color mapping for different types of variables
        color_patterns = {
            # Health and HP related
            r'\b(\d+)\s*HP\b': config.COLOR_HP,
            r'\bhp:\s*(\d+)': config.COLOR_HP,
            r'\b(\d+)/(\d+)\s*HP\b': config.COLOR_HP,
            
            # Damage numbers
            r'\b(\d+)\s*damage\b': config.COLOR_DAMAGE,
            r'\bfor\s+(\d+)\s+damage': config.COLOR_DAMAGE,
            
            # Gold and currency
            r'💰\s*(\d+)': config.COLOR_GOLD,
            r'\b(\d+)\s*gold\b': config.COLOR_GOLD,
            
            # Experience and levels
            r'\bLevel\s*(\d+)': config.COLOR_LEVEL,
            r'\blevel:\s*(\d+)': config.COLOR_LEVEL,
            r'\b(\d+)\s*XP\b': config.COLOR_XP,
            r'\bxp:\s*(\d+)': config.COLOR_XP,
            
            # Attack and Defense stats
            r'\bAttack:\s*(\d+)': config.COLOR_ATTACK,
            r'\battack:\s*(\d+)': config.COLOR_ATTACK,
            r'\bDefense:\s*(\d+)': config.COLOR_DEFENSE,
            r'\bdefense:\s*(\d+)': config.COLOR_DEFENSE,
            
            # Names and important identifiers
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b': '#ffaa00',  # Orange for character names (2+ words)
            r'⚔️\s*([^!]+)!': '#ffaa00',  # Orange for monster names in encounters
        }
        
        result = []
        last_end = 0
        
        # Find all matches and sort by position
        all_matches = []
        for pattern, color in color_patterns.items():
            for match in re.finditer(pattern, text, re.IGNORECASE):
                all_matches.append((match.start(), match.end(), match.group(), color))
        
        # Sort matches by start position
        all_matches.sort()
        
        # Remove overlapping matches (keep first one)
        filtered_matches = []
        for start, end, group, color in all_matches:
            # Check if this match overlaps with any previous match
            overlap = False
            for prev_start, prev_end, _, _ in filtered_matches:
                if start < prev_end and end > prev_start:  # Overlapping
                    overlap = True
                    break
            if not overlap:
                filtered_matches.append((start, end, group, color))
        
        # Build result with colored segments
        for start, end, group, color in filtered_matches:
            # Add text before match with default color
            if start > last_end:
                result.append((text[last_end:start], '#00ff00'))
            
            # Add matched text with special color
            result.append((text[start:end], color))
            last_end = end
        
        # Add remaining text with default color
        if last_end < len(text):
            result.append((text[last_end:], '#00ff00'))
        
        # If no matches found, return entire text with default color
        if not result:
            result.append((text, '#00ff00'))
        
        return result
    
    def print_combat_damage(self, message, damage_amount, attacker_name):
        """Print combat damage with extra visual emphasis"""
        # Use bright, vibrant colors for combat damage
        damage_color = '#ff0000'  # Bright red for maximum visibility
        
        # Create emphasized damage text with surrounding symbols
        damage_text = f"💥 {damage_amount} DAMAGE! 💥"
        
        # Split the message to insert the emphasized damage
        if "damage!" in message.lower():
            base_message = message.replace("damage!", "").replace("DAMAGE!", "")
        else:
            base_message = message
        
        # Create the colored parts with extra emphasis
        parts = [
            (base_message, "#00ff00"),  # Default green for text
            (damage_text, damage_color)   # Bright red for damage with emphasis
        ]
        
        self._print_colored_parts(parts)
    
    def print_colored_value(self, text, value, value_type='default', custom_color=None):
        """Print text with a colored value embedded"""
        color_map = {
            'hp': config.COLOR_HP,
            'damage': config.COLOR_DAMAGE,
            'gold': config.COLOR_GOLD,
            'xp': config.COLOR_XP,
            'level': config.COLOR_LEVEL,
            'attack': config.COLOR_ATTACK,
            'defense': config.COLOR_DEFENSE,
            'name': '#ffaa00',  # Orange for names
            'default': config.COLOR_TEXT_DEFAULT
        }
        
        # Use custom color if provided, otherwise use color map
        color = custom_color if custom_color else color_map.get(value_type, color_map['default'])
        
        # Create colored segments
        parts = []
        if '{value}' in text:
            # Split around the placeholder
            before, after = text.split('{value}', 1)
            parts.append((before, '#00ff00'))  # Default color for text
            parts.append((str(value), color))   # Special color for value
            parts.append((after, '#00ff00'))   # Default color for remaining text
        else:
            # No placeholder, treat as label + value
            parts.append((text, '#00ff00'))  # Default color for label
            parts.append((str(value), color))  # Special color for value
        
        # Print using the enhanced method
        self._print_colored_parts(parts)
    
    def _print_colored_parts(self, parts):
        """Internal method to print pre-processed colored parts"""
        self.text_area.config(state=tk.NORMAL)
        
        for text_part, text_color in parts:
            if text_part:  # Only process non-empty strings
                # Create or get color tag
                tag_name = f"color_{text_color.replace('#', '')}"
                self.text_area.tag_config(tag_name, foreground=text_color)
                
                # Insert text with color tag
                start_index = self.text_area.index(tk.END + "-1c")
                self.text_area.insert(tk.END, text_part)
                end_index = self.text_area.index(tk.END + "-1c")
                self.text_area.tag_add(tag_name, start_index, end_index)
        
        # Add newline
        self.text_area.insert(tk.END, '\n')
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)
        self.root.update()
    
    def clear_text(self):
        """Clear the text area"""
        self.text_area.config(state=tk.NORMAL)  # Temporarily enable for clearing
        self.text_area.delete(1.0, tk.END)
        self.text_area.config(state=tk.DISABLED)  # Disable again

    def _handle_keypress(self, event):
        """Handle keyboard shortcuts"""
        if not self.keyboard_enabled:
            return
        
        key = event.keysym.lower()
        
        # Universal shortcuts
        if key == 'escape':
            self._handle_escape()
        elif key == 'space':
            self._handle_space()
        elif key == 'f1':
            self._show_help()
            
        # Button shortcuts (1, 2, 3, 4, 5, 6, 7, 8, 9, 0) - support up to 10 buttons
        elif key in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            if key == '0':
                button_num = 10  # 0 key represents button 10
            else:
                button_num = int(key)
            
            # Check if we have enough buttons and if this button is enabled
            if (self.current_action and 
                hasattr(self, 'buttons') and 
                len(self.buttons) >= button_num and 
                self._is_button_enabled(button_num)):
                self._highlight_button(button_num)
                self.root.after(100, lambda: self.current_action(button_num) if self.current_action else None)
                
        # Arrow key navigation (grid-based)
        elif key == 'left':
            self._navigate_buttons_grid('left')
        elif key == 'right':
            self._navigate_buttons_grid('right')
        elif key == 'up':
            self._navigate_buttons_grid('up')
        elif key == 'down':
            self._navigate_buttons_grid('down')
        elif key == 'return':  # Enter key
            if self.current_action and self._is_button_enabled(self.current_selected_button):
                self._highlight_button(self.current_selected_button)
                self.root.after(100, lambda: self.current_action(self.current_selected_button) if self.current_action else None)
                
        # Audio controls
        elif key == 'm':
            self._toggle_audio()
        elif key == 'plus' or key == 'equal':
            self.audio.adjust_volume(0.1)
            self.print_text(f"🔊 Volume: {int(self.audio.get_volume() * 100)}%")
        elif key == 'minus':
            self.audio.adjust_volume(-0.1) 
            self.print_text(f"🔉 Volume: {int(self.audio.get_volume() * 100)}%")
            
        # Biome switching (for testing)
        elif key == 'b':
            self._cycle_biomes()

    def _handle_escape(self):
        """Handle ESC key - go back or show main menu"""
        # For now, just show main menu - can be enhanced later
        if hasattr(self, 'main_menu'):
            self.main_menu()

    def _handle_space(self):
        """Handle SPACE key - continue or activate first enabled button"""
        if self.current_action:
            # Find first enabled button
            for i in range(1, len(self.buttons) + 1):
                if self._is_button_enabled(i):
                    self._highlight_button(i)
                    self.root.after(100, lambda btn=i: self.current_action(btn) if self.current_action else None)
                    break

    def _show_help(self):
        """Show keyboard shortcuts help"""
        help_text = """
🎮 Keyboard Shortcuts:
━━━━━━━━━━━━━━━━━━━━━━━
⌨️  General:
   ESC - Back/Main Menu
   SPACE - Continue/First Option
   F1 - Show this help

🎯 Navigation:
   1-9, 0 - Select buttons directly (0 = button 10)
   ← → ↑ ↓ - Navigate button grid (3 buttons per row)
   ENTER - Activate selected button

🔊 Audio:
   M - Mute/Unmute
   + - Volume up
   - - Volume down

🏜️ Testing:
   B - Cycle biomes (Grassland → Desert → Dungeon → Ocean → Town)

💡 Tip: Look for button highlights to see
   which option is currently selected!
"""
        self.print_text(help_text)
        
    def _cycle_biomes(self):
        """Cycle through available biomes for testing"""
        next_biome = self.background_manager.cycle_biomes()
        
        # Also update any active encounter screens
        if hasattr(self, 'monster_encounter') and self.monster_encounter:
            self.monster_encounter.set_background(next_biome)
    
    def teleport_to_random_biome(self):
        """Teleport to a random biome different from the current one"""
        self.background_manager.teleport_to_random_biome()

    def _navigate_buttons(self, direction):
        """Legacy navigation - now uses grid navigation"""
        if direction == -1:
            self._navigate_buttons_grid('left')
        elif direction == 1:
            self._navigate_buttons_grid('right')
    
    def _navigate_buttons_grid(self, direction):
        """Navigate between buttons in grid layout with arrow keys"""
        if not self.current_action or not self.buttons:
            return
        
        button_count = len(self.buttons)
        buttons_per_row = 3
        
        # Get current position (0-based for calculations)
        current_index = self.current_selected_button - 1
        current_row = current_index // buttons_per_row
        current_col = current_index % buttons_per_row
        
        # Calculate new position based on direction
        new_row = current_row
        new_col = current_col
        
        if direction == 'left':
            new_col -= 1
            if new_col < 0:
                # Wrap to end of previous row
                new_row -= 1
                if new_row < 0:
                    # Wrap to last row
                    new_row = (button_count - 1) // buttons_per_row
                new_col = min(buttons_per_row - 1, (button_count - 1) % buttons_per_row if new_row == (button_count - 1) // buttons_per_row else buttons_per_row - 1)
                
        elif direction == 'right':
            new_col += 1
            max_col_in_row = min(buttons_per_row - 1, (button_count - 1) % buttons_per_row if current_row == (button_count - 1) // buttons_per_row else buttons_per_row - 1)
            if new_col > max_col_in_row:
                # Wrap to start of next row
                new_row += 1
                new_col = 0
                if new_row * buttons_per_row >= button_count:
                    # Wrap to first row
                    new_row = 0
                    
        elif direction == 'up':
            new_row -= 1
            if new_row < 0:
                # Wrap to last row, same column if possible
                new_row = (button_count - 1) // buttons_per_row
                # Adjust column if last row doesn't have enough buttons
                max_col_in_last_row = (button_count - 1) % buttons_per_row
                if new_col > max_col_in_last_row:
                    new_col = max_col_in_last_row
                    
        elif direction == 'down':
            new_row += 1
            max_row = (button_count - 1) // buttons_per_row
            if new_row > max_row:
                # Wrap to first row
                new_row = 0
            else:
                # Check if new position exists (for partial last row)
                max_col_in_row = (button_count - 1) % buttons_per_row if new_row == max_row else buttons_per_row - 1
                if new_col > max_col_in_row:
                    new_col = max_col_in_row
        
        # Convert back to 1-based button number
        new_button_index = new_row * buttons_per_row + new_col
        if 0 <= new_button_index < button_count:
            new_button = new_button_index + 1
            
            # Check if button is enabled and update selection
            if self._is_button_enabled(new_button):
                self.current_selected_button = new_button
                self._update_button_selection()

    def _is_button_enabled(self, button_num):
        """Check if a button is enabled"""
        if 1 <= button_num <= len(self.buttons):
            return self.buttons[button_num - 1]['state'] == tk.NORMAL
        return False

    def _highlight_button(self, button_num):
        """Briefly highlight a button when activated"""
        if 1 <= button_num <= len(self.buttons):
            button = self.buttons[button_num - 1]
            try:
                original_bg = button['bg']
                button.configure(bg='#ffaa00')  # Orange highlight
                
                # Safe reset function that checks if button still exists
                def safe_reset():
                    try:
                        # Check if button still exists and hasn't been destroyed
                        if button.winfo_exists():
                            button.configure(bg=original_bg)
                    except tk.TclError:
                        # Button was destroyed, ignore the error
                        pass
                
                self.root.after(200, safe_reset)
            except tk.TclError:
                # Button was destroyed before we could highlight it, ignore
                pass

    def _update_button_selection(self):
        """Update visual indication of which button is selected"""
        for i, button in enumerate(self.buttons, 1):
            if i == self.current_selected_button and self._is_button_enabled(i):
                button.configure(relief='raised', bd=3)
            else:
                button.configure(relief='flat', bd=1)

    def _toggle_audio(self):
        """Toggle audio on/off"""
        if hasattr(self.audio, 'toggle_mute'):
            self.audio.toggle_mute()
        else:
            # Fallback implementation
            current_vol = self.audio.get_volume()
            if current_vol > 0:
                self.audio.set_volume(0)
                self.print_text("🔇 Audio muted")
            else:
                self.audio.set_volume(0.5)
                self.print_text("🔊 Audio enabled")

    def set_buttons(self, labels, action_callback):
        """Set button labels and action"""
        # Unlock interface when new buttons are being set
        self.keyboard_enabled = True
        
        # Filter out empty labels to get actual button count
        filtered_labels = [label for label in labels if label and label.strip()]
        
        # Create the right number of buttons
        self._create_buttons(len(filtered_labels))
        
        # Configure buttons with labels
        for i, label in enumerate(filtered_labels):
            if i < len(self.buttons):
                # Add keyboard shortcut hint to button text
                shortcut_label = f"[{i+1}] {label}"
                self.buttons[i].config(text=shortcut_label, state=tk.NORMAL)
        
        self.current_action = action_callback
        
        # Reset selection to first enabled button
        self.current_selected_button = 1
        for i in range(1, len(self.buttons) + 1):
            if self._is_button_enabled(i):
                self.current_selected_button = i
                break
        
        # Update visual selection
        self._update_button_selection()
    
    def lock_interface(self):
        """Lock the interface during combat/animations to prevent interruptions"""
        self.keyboard_enabled = False
        
        # Disable all buttons and show locked state
        for btn in self.buttons:
            btn.config(state=tk.DISABLED, text="🔒 Processing...")
        
        # Clear current action to prevent button clicks
        self.current_action = None
        
    def unlock_interface(self):
        """Unlock the interface after combat/animations complete"""
        self.keyboard_enabled = True
        
        # Note: Buttons will be re-enabled when set_buttons is called next
        # This prevents stale button states from previous screens
    
    def show_processing_status(self, message="Processing..."):
        """Show a processing status message to user during locked interface"""
        if not self.keyboard_enabled:
            self.print_text(f"⏳ {message}")
    
    def is_interface_locked(self):
        """Check if interface is currently locked"""
        return not self.keyboard_enabled
    
    def initialize_game(self):
        """Initialize the game"""
        # Start background music that will loop continuously
        self.audio.play_background_music('start.mp3', loop=True, volume=0.4)
        
        # Initialize game state first (needed for game systems)
        self.game_state = initialize_game_state()
        
        # Initialize game systems with dependency injection
        self.combat = CombatGUI(
            text_display=self,
            image_display=self,
            audio=self.audio,
            interface_control=self,
            timer=self.root,
            game_state=self.game_state
        )
        self.shop = ShopGUI(self)
        self.blacksmith = BlacksmithGUI(self)
        self.inventory = InventoryGUI(self)
        self.monster_encounter = MonsterEncounterGUI(self)
        self.quest_manager = QuestManager(self)
        self.save_load_manager = SaveLoadManager(self)
        self.town = TownGUI(self)
        self.tavern = TavernGUI(self)
        self.achievements = AchievementManager(game_state=self.game_state)
        
        # Show story prologue first
        self.show_story_prologue()
    
    def show_story_prologue(self):
        """Display the story prologue before the title screen"""
        try:
            # Load story from YAML file
            with open(get_resource_path('story.yaml'), 'r', encoding='utf-8') as f:
                story_data = yaml.safe_load(f)
            
            prologue_lines = story_data.get('Prologue', [])
            
            if prologue_lines:
                # Set attractive story background image
                self.background_manager.set_background_image('art/story_background.png')
                
                # Display story text on canvas
                self.image_manager.show_story_text(
                    text_lines=prologue_lines,
                    font_size=28,
                    text_color='#ffdd00',
                    shadow_color='#000000',
                    line_spacing=50
                )
                
                # Show message in text area
                self.print_text("=" * 60)
                self.print_text("📖  The Story Begins...")
                self.print_text("=" * 60)
                self.print_text("\n(Press any button to continue)")
                
                # Set up button to continue to title screen
                self.set_buttons(["Continue"], lambda choice: self.show_title_screen())
            else:
                # No prologue found, go straight to title
                self.show_title_screen()
                
        except FileNotFoundError:
            logger.warning("story.yaml not found, skipping prologue")
            self.show_title_screen()
        except Exception as e:
            logger.error(f"Error loading story prologue: {e}")
            self.show_title_screen()
    
    def show_title_screen(self):
        """Display the title screen and welcome message"""
        self.clear_text()
        self.show_image('art/pyquest.png')
        self.print_text("=" * 60)
        self.print_text("Welcome to Monster Game!")
        self.print_text("=" * 60)
        self.print_text("⌨️  Keyboard shortcuts enabled! Press F1 for help")
        self.print_text("   Use 1-3 keys, arrows, SPACE, or ESC to navigate")
        self.print_text("")
        
        # Start hero selection
        self.select_hero()
    
    def select_hero(self):
        """Handle hero selection"""
        self.clear_text()
        self.print_text("\n⚔️  Choose Your Hero ⚔️\n")
        
        for i, (hero_name, hero_data) in enumerate(self.game_state.heros.items(), 1):
            self.print_text(f"\n{i}. {hero_name}")
            for key, value in hero_data.items():
                # Skip internal/technical fields and titles (shown in tavern)
                if key in ('attack_sound', 'titles', 'earned_titles'):
                    continue
                self.print_text(f"   {key}: {value}")
        
        # Check for existing saves to show load option
        available_saves = self.save_load_manager.get_available_saves()
        if available_saves:
            load_info_parts = [
                (f"\n📁 Found {len(available_saves)} saved game(s) - ", "#888888"),
                ("use Load option to continue existing adventure!", "#ffaa00")
            ]
            self._print_colored_parts(load_info_parts)
        
        def on_hero_select(choice):
            if choice <= 3:
                # Create new hero
                hero_name = self.game_state.choices.get(str(choice))
                if hero_name:
                    self.game_state.hero = self.game_state.heros[hero_name].copy()
                    self.game_state.hero['name'] = hero_name
                    self.game_state.hero['lives_left'] = 3
                    self.game_state.hero['gold'] = 50
                    self.game_state.hero['level'] = 1
                    self.game_state.hero['xp'] = 0
                    # Initialize items as dictionary for multiple items
                    if 'items' not in self.game_state.hero:
                        self.game_state.hero['items'] = {}
                    # Migrate old 'item' to new 'items' system if present
                    if 'item' in self.game_state.hero and self.game_state.hero['item'] is not None:
                        old_item = self.game_state.hero['item']
                        item_name = old_item['name']
                        self.game_state.hero['items'][item_name] = {'data': old_item, 'quantity': 1}
                        del self.game_state.hero['item']
                    
                    # Initialize quest system for hero
                    self.quest_manager.initialize_hero_quests(self.game_state.hero)
                    
                    self.print_text(f"\n✓ You chose: {hero_name}!\n")
                    sleep(0.5)
                    self.main_menu()
            elif choice == 4:
                # Load saved game
                self.save_load_manager.show_load_interface()
        
        self.set_buttons(["Hero 1", "Hero 2", "Hero 3", "📁 Load Saved Game"], on_hero_select)
    
    def hero_level(self):
        """Handle hero leveling up"""
        if self.game_state.hero['xp'] >= self.game_state.hero['level'] * 5:
            # Store XP before leveling for display
            excess_xp = self.game_state.hero['xp']
            xp_used = self.game_state.hero['level'] * 5
            remaining_xp = excess_xp - xp_used
            
            self.clear_text()
            self.print_text("\n🎉  Level Up! 🎉\n")
            self.audio.play_sound_effect('levelup.wav')
            
            # Show XP consumption
            xp_parts = [
                ("Used ", "#ffffff"),
                (f"{xp_used} XP", "#8844ff"),
                (" to level up from ", "#ffffff"),
                (f"Level {self.game_state.hero['level']}", "#00aaff"),
                (" to ", "#ffffff"),
                (f"Level {self.game_state.hero['level'] + 1}", "#00aaff"),
                ("!", "#ffffff")
            ]
            self._print_colored_parts(xp_parts)
            
            if remaining_xp > 0:
                remaining_parts = [
                    ("Excess XP carried over: ", "#ffffff"),
                    (f"{remaining_xp} XP", "#8844ff")
                ]
                self._print_colored_parts(remaining_parts)
            
            self.game_state.hero['level'] += 1
            self.game_state.hero['xp'] = remaining_xp  # Carry over any excess XP
            self.game_state.hero['maxhp'] += 5
            self.game_state.hero['hp'] = self.game_state.hero['maxhp']
            self.game_state.hero['attack'] += 2
            self.game_state.hero['defense'] += 2
            self.print_text(f"\n⭐ Your hero has reached level {self.game_state.hero['level']}! ⭐")
            
            # Show stat improvements
            stat_parts = [
                ("📈 Stats improved: ", "#ffffff"),
                ("HP +5", "#ff4444"),
                (", ", "#ffffff"),
                ("Attack +2", "#ff6600"),
                (", ", "#ffffff"),
                ("Defense +2", "#0088ff")
            ]
            self._print_colored_parts(stat_parts)
            
            sleep(3)  # Give more time to read the level up message

    
    def main_menu(self):
        """Display main menu"""
        """Check for level up event first"""
        self.hero_level()
        
        # Reset to default grassy background when returning to main menu
        self.reset_background()
        
        self.clear_text()
        # Use hero art field from YAML or fallback to class-based path
        hero_image = self.game_state.hero.get('art', f"art/{self.game_state.hero['class']}.png")
        self.show_image(hero_image)
        
        self.print_text("\n" + "=" * 60)
        self.print_text("⚔️  Hero Stats ⚔️")
        self.print_text("=" * 60)
        
        # Track if we've already displayed hp/maxhp
        hp_displayed = False
        
        for key, value in self.game_state.hero.items():
            # Skip displaying quests in hero stats - they have their own section
            # Also skip internal/technical fields and titles (shown in tavern)
            if key in ('quests', 'completed_quests', 'attack_sound', 'titles', 'earned_titles', 'art', 'art_attack', 'art_death'):
                continue
            elif key == 'hp':
                # Display HP as "hp: current/max" with color coding
                if not hp_displayed:
                    hp_current = value
                    hp_max = self.game_state.hero.get('maxhp', value)
                    hp_text = "  hp: "
                    
                    # Color code based on HP percentage
                    hp_percent = (hp_current / hp_max) if hp_max > 0 else 0
                    if hp_percent > 0.6:
                        hp_color = '#00ff00'  # Bright green for healthy
                        hp_font = ('Consolas', 10, 'bold')  # Bold when healthy
                    elif hp_percent > 0.3:
                        hp_color = '#ffaa00'  # Orange for wounded
                        hp_font = ('Consolas', 10)
                    else:
                        hp_color = '#ff4444'  # Red for critical
                        hp_font = ('Consolas', 10)
                    
                    self.text_area.config(state=tk.NORMAL)
                    self.text_area.insert(tk.END, hp_text, 'hp_label')
                    self.text_area.tag_config('hp_label', foreground='#00ff00')
                    
                    self.text_area.insert(tk.END, str(hp_current), 'hp_current')
                    self.text_area.tag_config('hp_current', foreground=hp_color, font=hp_font)
                    
                    self.text_area.insert(tk.END, "/", 'hp_slash')
                    self.text_area.tag_config('hp_slash', foreground='#00ff00')
                    
                    self.text_area.insert(tk.END, str(hp_max), 'hp_max')
                    self.text_area.tag_config('hp_max', foreground='#00ff00')
                    
                    self.text_area.insert(tk.END, '\n')
                    self.text_area.see(tk.END)
                    self.text_area.config(state=tk.DISABLED)
                    
                    hp_displayed = True
            elif key == 'maxhp':
                # Skip maxhp since it's now shown with hp
                continue
            elif key == 'xp':
                # Special handling for XP with colored values
                xp_text = f"  {key}: "
                xp_current = str(value)
                xp_max = str(self.game_state.hero['level']*5)
                
                self.text_area.config(state=tk.NORMAL)
                self.text_area.insert(tk.END, xp_text, 'default_color')
                self.text_area.tag_config('default_color', foreground='#00ff00')
                
                self.text_area.insert(tk.END, xp_current, 'xp_color')
                self.text_area.tag_config('xp_color', foreground='#8844ff')
                
                self.text_area.insert(tk.END, "/", 'default_color')
                
                self.text_area.insert(tk.END, xp_max, 'xp_color')
                
                self.text_area.insert(tk.END, '\n')
                self.text_area.see(tk.END)
                self.text_area.config(state=tk.DISABLED)
                
            elif key == 'items' and value:
                # Display items with quantities
                item_names = []
                for item_name, item_info in value.items():
                    quantity = item_info.get('quantity', 1)
                    if quantity > 1:
                        item_names.append(f"{item_name} x{quantity}")
                    else:
                        item_names.append(item_name)
                if item_names:
                    self.print_colored_value(f"  items: ", ", ".join(item_names), 'name')
            elif key == 'item' and value is not None:
                # Legacy support for old save files
                self.print_colored_value(f"  {key}: ", value['name'], 'name')
            elif key == 'attack':
                self.print_colored_value(f"  {key}: ", value, 'attack')
            elif key == 'defense':
                self.print_colored_value(f"  {key}: ", value, 'defense')
            elif key == 'level':
                self.print_colored_value(f"  {key}: ", value, 'level')
            elif key == 'gold':
                self.print_colored_value(f"  {key}: ", value, 'gold')
            elif key == 'lives_left':
                # Special color coding for lives - red when low
                if value <= 1:
                    lives_color = '#ff4444'  # Red for critical
                elif value <= 2:
                    lives_color = '#ffaa00'  # Orange for warning  
                else:
                    lives_color = '#00ff00'  # Green for safe
                self.print_colored_value(f"  {key}: ", value, 'custom', lives_color)
            else:
                self.print_text(f"  {key}: {value}")
        
        self.print_text("=" * 60)
        
        # Display current biome location
        biome_emojis = {
            'grassland': '🌱',
            'desert': '🏜️', 
            'dungeon': '🏰',
            'ocean': '🌊',
            'town': '🏘️'
        }
        biome_colors = {
            'grassland': '#4a7c59',
            'desert': '#daa520', 
            'dungeon': '#8b4513',
            'ocean': '#0077be',
            'town': '#2B4C3D'
        }
        
        current_biome = getattr(self, 'current_biome', 'grassland')
        biome_emoji = biome_emojis.get(current_biome, '🌍')
        biome_color = biome_colors.get(current_biome, '#00ff00')
        
        location_parts = [
            ("📍 Current Location: ", "#ffffff"),
            (f"{biome_emoji} {current_biome.title()}", biome_color)
        ]
        self._print_colored_parts(location_parts)
        self.print_text("")
        
        # Display active quests (only show non-completed quests)
        active_quests = self.quest_manager.get_active_quests(self.game_state.hero)
        if active_quests:
            self.print_text("\n📜 Active Quests:")
            for i, quest in enumerate(active_quests[:3], 1):  # Show max 3 quests
                quest_parts = [
                    (f"  {i}. ", "#ffffff"),
                    (quest.description, "#ffaa00"),
                    (f" ({quest.reward_xp} XP)", "#8844ff")
                ]
                self._print_colored_parts(quest_parts)
        else:
            quest_parts = [
                ("📜 No active quests - visit ", "#ffffff"),
                ("Quests", "#ffaa00"),
                (" to get started!", "#ffffff")
            ]
            self._print_colored_parts(quest_parts)
            
        self.print_text("\nWhat would you like to do?")
        
        def on_menu_select(choice):
            if choice == 1:
                self.town.enter_town()
            elif choice == 2:
                # Check if hero has "Savior of Monster World" achievement
                if hasattr(self, 'achievements') and self.achievements:
                    savior_achievement = self.achievements.achievements.get('savior_of_monster_world')
                    if savior_achievement and savior_achievement.completed:
                        # Trigger special wagon death event
                        self.combat.start_wagon_death_event(self.game_state.hero)
                        return
                
                # Normal monster encounter
                self.monster_encounter.start()
            elif choice == 3:
                self.inventory.use_item()
            elif choice == 4:
                self.show_quests()
            elif choice == 5:
                self.teleport_to_random_biome()
            elif choice == 6:
                self.save_load_manager.show_save_interface()
        
        self.set_buttons(["🏘️ Town", "⚔️ Fight Monster", "🧪 Use Item", "📜 Quests", "🌀 Teleport", "💾 Save Game"], on_menu_select)

    def show_quests(self):
        """Display quest interface - main entry point"""
        self.clear_text()
        hero = self.game_state.hero
        self.quest_manager.initialize_hero_quests(hero)
        
        self.print_text("📜 QUESTS 📜\n")
        
        active_quests = self.quest_manager.get_active_quests(hero)
        
        if not active_quests:
            self._show_no_quests_screen()
        else:
            self._show_active_quests_screen(active_quests)
    
    def _show_no_quests_screen(self):
        """Display screen when hero has no active quests"""
        self.print_text("No active quests.\n")
        self.print_text("Would you like to take on a new quest?")
        
        def on_quest_choice(choice):
            if choice == 1:
                self._handle_accept_new_quest()
            elif choice == 2:
                self.main_menu()
        
        self.set_buttons(["✅ Accept New Quest", "🔙 Back"], on_quest_choice)
    
    def _show_active_quests_screen(self, active_quests):
        """Display screen when hero has active quests"""
        # Display quest list
        for i, quest in enumerate(active_quests, 1):
            quest_parts = [
                (f"{i}. ", "#ffffff"),
                (quest.description, "#00ff00"),
                (f" (Reward: {quest.reward_xp} XP)", "#ffdd00")
            ]
            self._print_colored_parts(quest_parts)
        
        self.print_text(f"\nYou have {len(active_quests)} active quest(s).")
        
        # Build button list and handler
        buttons = self._build_quest_menu_buttons(active_quests)
        handler = self._create_quest_menu_handler(active_quests)
        
        self.set_buttons(buttons, handler)
    
    def _build_quest_menu_buttons(self, active_quests):
        """Build button list for quest menu based on current state"""
        buttons = []
        
        if len(active_quests) < 3:
            buttons.append("➕ Take Another Quest")
        
        buttons.append("🗑️ Drop Quest")
        buttons.append("🔙 Back")
        
        return buttons
    
    def _create_quest_menu_handler(self, active_quests):
        """Create button handler for quest menu with proper index mapping"""
        def on_quest_menu_choice(choice):
            button_index = 0
            
            # Take Another Quest option (only if < 3 quests)
            if len(active_quests) < 3:
                if choice == button_index + 1:
                    self._handle_take_another_quest()
                    return
                button_index += 1
            
            # Drop Quest option
            if choice == button_index + 1:
                self.show_drop_quest_menu()
                return
            button_index += 1
            
            # Back option
            if choice == button_index + 1:
                self.main_menu()
                return
        
        return on_quest_menu_choice
    
    def _handle_accept_new_quest(self):
        """Handle accepting a new quest when hero has no quests"""
        hero = self.game_state.hero
        new_quest = self.quest_manager.generate_kill_monster_quest()
        
        if isinstance(new_quest, str):
            self._handle_quest_generation_error(new_quest, stay_in_menu=True)
        elif new_quest:
            self._add_and_display_new_quest(hero, new_quest, stay_in_menu=True)
        else:
            self.print_text("❌ Could not generate quest (no monsters available)")
            self.root.after(2000, self.main_menu)
    
    def _handle_take_another_quest(self):
        """Handle taking an additional quest when hero already has quests"""
        hero = self.game_state.hero
        new_quest = self.quest_manager.generate_kill_monster_quest()
        
        if isinstance(new_quest, str):
            self._handle_quest_generation_error(new_quest, stay_in_menu=False)
        elif new_quest:
            self._add_and_display_new_quest(hero, new_quest, stay_in_menu=True)
        else:
            self.print_text("❌ Could not generate quest")
            self.root.after(1500, self.main_menu)
    
    def _handle_quest_generation_error(self, error_code, stay_in_menu=False):
        """Display appropriate error message for quest generation failures"""
        if error_code == "NO_QUESTS_AVAILABLE_BIOME":
            current_biome = getattr(self, 'current_biome', 'grassland')
            error_parts = [
                ("❌ No quests available! ", "#ff6666"),
                (f"All monsters in {current_biome} already have active quests.", "#ffffff")
            ]
            self._print_colored_parts(error_parts)
            self.print_text("💡 Complete existing quests or explore other biomes!")
        elif error_code == "NO_QUESTS_AVAILABLE_ALL":
            error_parts = [
                ("❌ No quests available! ", "#ff6666"),
                ("You have active quests for all available monsters.", "#ffffff")
            ]
            self._print_colored_parts(error_parts)
            self.print_text("💡 Complete some existing quests first!")
        else:
            self.print_text("❌ Could not generate quest (unknown error)")
        
        # Return to appropriate screen
        if stay_in_menu:
            self.root.after(2500, self.show_quests)
        else:
            self.root.after(2000, self.main_menu)
    
    def _add_and_display_new_quest(self, hero, new_quest, stay_in_menu=False):
        """Add a new quest to hero's journal and display confirmation"""
        self.quest_manager.add_quest(hero, new_quest)
        
        quest_parts = [
            ("🆕 New Quest: ", "#00ff00"),
            (new_quest.description, "#ffffff"),
            (f" (Reward: {new_quest.reward_xp} XP)", "#ffdd00")
        ]
        self._print_colored_parts(quest_parts)
        
        self.print_text("\nQuest added to your journal!")
        
        # Return to quest menu to show updated list
        if stay_in_menu:
            self.root.after(1500, self.show_quests)
        else:
            self.root.after(1500, self.main_menu)

    def show_drop_quest_menu(self):
        """Display quest dropping interface"""
        self.clear_text()
        
        hero = self.game_state.hero
        active_quests = self.quest_manager.get_active_quests(hero)
        
        self.print_text("🗑️ DROP QUEST 🗑️\n")
        
        if not active_quests:
            self.print_text("No active quests to drop.")
            self.root.after(1500, self.show_quests)
            return
        
        self.print_text("Select a quest to drop:\n")
        
        # Display active quests with numbers
        for i, quest in enumerate(active_quests, 1):
            quest_parts = [
                (f"{i}. ", "#ffffff"),
                (quest.description, "#ff6666"),  # Red color to indicate dropping
                (f" (Reward: {quest.reward_xp} XP)", "#ffdd00")
            ]
            self._print_colored_parts(quest_parts)
        
        self.print_text("\n⚠️ Warning: Dropped quests cannot be recovered!")
        
        def on_drop_choice(choice):
            if choice <= len(active_quests):
                # Drop the selected quest (choice is 1-indexed)
                quest_to_drop = active_quests[choice - 1]
                if self.quest_manager.drop_quest(hero, choice - 1):
                    drop_parts = [
                        ("🗑️ Dropped quest: ", "#ff6666"),
                        (quest_to_drop.description, "#ffffff")
                    ]
                    self._print_colored_parts(drop_parts)
                    self.print_text("Quest removed from your journal.")
                    self.root.after(2000, self.show_quests)
                else:
                    self.print_text("❌ Failed to drop quest.")
                    self.root.after(1500, self.show_quests)
            else:
                # Back button
                self.show_quests()
        
        # Create buttons for each quest plus back button
        buttons = []
        for i, quest in enumerate(active_quests, 1):
            # Truncate long quest descriptions for button text
            short_desc = quest.description
            if len(short_desc) > 25:
                short_desc = short_desc[:22] + "..."
            buttons.append(f"🗑️ {short_desc}")
        buttons.append("🔙 Back")
        
        self.set_buttons(buttons, on_drop_choice)

    def game_over(self):
        """Handle game over when hero has 0 lives left"""
        self.clear_text()
        self.lock_interface()
        
        # Display game over message
        self.print_text("\n" + "=" * 60)
        self.print_text("💀  GAME OVER  💀")
        self.print_text("=" * 60)
        self.print_text("\nYou are out of lives! The adventure ends here...")
        self.print_text("Thank you for playing MonsterGame!")
        self.print_text("=" * 60)
        
        # Show hero death image (death sound already played in combat sequence)
        self._show_hero_death_game_over()
        
        # Close the game after 5 seconds
        self.root.after(5000, self._close_game)
    
    def _show_hero_death_game_over(self):
        """Show hero-specific death image during game over"""
        try:
            # Get death image from YAML or construct fallback
            death_image_path = self.game_state.hero.get('art_death', '')
            
            if not death_image_path:
                # Fallback to class-based path if art_death field missing
                hero_class = self.game_state.hero.get('class', 'Warrior').lower()
                death_image_path = f"art/{hero_class}_death.png"
            
            # Try to load class-specific death image
            if resource_exists(death_image_path):
                self.show_image(death_image_path)
            else:
                # Fallback to generic you_lost image if class-specific doesn't exist
                logger.info(f"Death image not found: {death_image_path}, using generic")
                self.show_image('art/you_lost.png')
        except Exception as e:
            logger.warning(f"Error loading game over death image: {e}")
            self.show_image('art/you_lost.png')
    
    def _close_game(self):
        """Close the game application"""
        self.root.quit()
        self.root.destroy()
    
    def check_game_over(self):
        """Check if hero has 0 lives left and trigger game over if needed"""
        if self.game_state.hero['lives_left'] <= 0:
            self.game_over()
            return True
        return False
