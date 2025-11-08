"""
Main GUI class for the monster game
"""
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
from time import sleep

from game_state import initialize_game_state
from gui_audio import Audio
from gui_combat import CombatGUI
from gui_shop import ShopGUI
from gui_inventory import InventoryGUI
from gui_monster_encounter import MonsterEncounterGUI


class GameGUI:
    """Graphical User Interface for the monster game"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("PyQuest - Monster Game")
        self.root.geometry("800x1000")
        self.root.configure(bg='#1a1a1a')
        
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
        self.inventory = None
        self.monster_encounter = None
        
        # Create main layout
        self._create_widgets()
        
        # Start game initialization
        self.root.after(100, self.initialize_game)
    
    def _create_widgets(self):
        """Create the GUI widgets"""
        # Top frame for images with enhanced background and visual styling
        self.image_frame = tk.Frame(
            self.root, 
            bg='#2d2d2d',  # Medium gray background
            height=250, 
            relief='groove',  # More attractive 3D effect
            bd=3,  # Slightly thicker border
            highlightbackground='#505050',  # Subtle highlight
            highlightthickness=1
        )
        self.image_frame.pack(fill=tk.BOTH, pady=10, padx=5)
        self.image_frame.pack_propagate(False)
        
        # Image labels - support for multiple images
        self.image_labels = []
        self.current_image_layout = "single"  # Track current layout mode
        
        # Default single image label with enhanced styling
        self.image_label = tk.Label(
            self.image_frame, 
            bg='#404040',  # Neutral gray background
            relief='sunken',  # Inset appearance for better depth
            bd=2,
            padx=15,
            pady=15,
            highlightbackground='#606060',
            highlightcolor='#808080',
            highlightthickness=1
        )
        self.image_label.pack(expand=True, padx=15, pady=15)
        self.image_labels.append(self.image_label)
        
        # Text output area (read-only)
        self.text_area = scrolledtext.ScrolledText(
            self.root, 
            wrap=tk.WORD,
            width=80,
            height=15,
            bg='#2a2a2a',
            fg='#00ff00',
            font=('Courier', 10),
            state=tk.DISABLED,  # Make read-only
            cursor='arrow'  # Change cursor to indicate non-editable
        )
        self.text_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Button frame
        self.button_frame = tk.Frame(self.root, bg='#1a1a1a')
        self.button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Dynamic button list (will be created as needed)
        self.buttons = []
        
        self.current_action = None
    
    def _create_buttons(self, count):
        """Create the specified number of buttons"""
        # Clear existing buttons
        self._clear_buttons()
        
        # Create new buttons
        for i in range(count):
            btn = tk.Button(
                self.button_frame,
                text=f"Option {i+1}",
                command=lambda idx=i+1: self.button_clicked(idx),
                bg='#4a4a4a',
                fg='#ffffff',
                font=('Arial', 12, 'bold'),
                width=15,
                state=tk.DISABLED
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.buttons.append(btn)
    
    def _clear_buttons(self):
        """Remove all existing buttons"""
        for btn in self.buttons:
            btn.destroy()
        self.buttons = []
    
    def show_image(self, image_path):
        """Display a single image in the image area (backwards compatible)"""
        if isinstance(image_path, list):
            # If a list is passed, use show_images instead
            self.show_images(image_path)
            return
            
        # Reset to single image layout
        self._reset_image_layout()
        
        try:
            # Handle text files (ASCII art)
            if image_path.endswith('.txt'):
                # For text files, create a simple text display
                with open(image_path, 'r', encoding='utf-8') as f:
                    ascii_art = f.read()
                # Create an image from text with enhanced background
                self.image_label.config(text=ascii_art, font=('Courier', 8), fg='#00ff00', bg='#303030')
                return
            
            # Handle image files
            img = Image.open(image_path)
            # Resize to fit the frame while maintaining aspect ratio
            img.thumbnail((400, 250), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo, text='')
            self.image_label.image = photo  # Keep a reference
        except Exception as e:
            self.print_text(f"Could not load image: {e}")
    
    def show_images(self, image_paths, layout="auto"):
        """Display multiple images in the image area
        
        Args:
            image_paths: List of image file paths
            layout: "horizontal", "vertical", "grid", or "auto" (default)
        """
        if not image_paths:
            return
        
        # If single image, fall back to show_image
        if len(image_paths) == 1:
            self.show_image(image_paths[0])
            return
        
        # Clear existing layout
        self._clear_image_area()
        
        # Determine layout
        num_images = len(image_paths)
        if layout == "auto":
            if num_images <= 2:
                layout = "horizontal"
            elif num_images <= 4:
                layout = "grid"
            else:
                layout = "grid"  # Handle more than 4 images in grid
        
        # Create layout
        if layout == "horizontal":
            self._create_horizontal_layout(image_paths)
        elif layout == "vertical":
            self._create_vertical_layout(image_paths)
        elif layout == "grid":
            self._create_grid_layout(image_paths)
        
        self.current_image_layout = layout
    
    def _reset_image_layout(self):
        """Reset to single image layout"""
        if self.current_image_layout != "single":
            self._clear_image_area()
            # Recreate single image label with enhanced styling
            self.image_label = tk.Label(
                self.image_frame, 
                bg='#404040',  # Neutral gray background
                relief='sunken',  # Inset appearance for better depth
                bd=2,
                padx=15,
                pady=15,
                highlightbackground='#606060',
                highlightcolor='#808080',
                highlightthickness=1
            )
            self.image_label.pack(expand=True, padx=15, pady=15)
            self.image_labels = [self.image_label]
            self.current_image_layout = "single"
    
    def _clear_image_area(self):
        """Clear all image widgets from the image frame"""
        for widget in self.image_frame.winfo_children():
            widget.destroy()
        self.image_labels.clear()
    
    def _create_horizontal_layout(self, image_paths):
        """Create horizontal layout for multiple images"""
        for i, image_path in enumerate(image_paths):
            label = tk.Label(
                self.image_frame, 
                bg='#404040',  # Neutral gray background
                relief='ridge',
                bd=1,
                padx=5,
                pady=5
            )
            label.pack(side=tk.LEFT, expand=True, padx=5, pady=10)
            self.image_labels.append(label)
            self._load_image_to_label(image_path, label, (180, 200))
    
    def _create_vertical_layout(self, image_paths):
        """Create vertical layout for multiple images"""
        for i, image_path in enumerate(image_paths):
            label = tk.Label(
                self.image_frame, 
                bg='#404040',  # Neutral gray background
                relief='ridge',
                bd=1,
                padx=5,
                pady=5
            )
            label.pack(side=tk.TOP, expand=True, padx=10, pady=5)
            self.image_labels.append(label)
            self._load_image_to_label(image_path, label, (350, 120))
    
    def _create_grid_layout(self, image_paths):
        """Create grid layout for multiple images"""
        import math
        
        # Calculate grid dimensions
        num_images = len(image_paths)
        cols = min(3, num_images)  # Max 3 columns
        rows = math.ceil(num_images / cols)
        
        # Create grid
        for i, image_path in enumerate(image_paths):
            row = i // cols
            col = i % cols
            
            label = tk.Label(
                self.image_frame, 
                bg='#404040',  # Neutral gray background
                relief='ridge',
                bd=1,
                padx=3,
                pady=3
            )
            label.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)
            self.image_labels.append(label)
            
            # Configure grid weights for even distribution
            self.image_frame.grid_rowconfigure(row, weight=1)
            self.image_frame.grid_columnconfigure(col, weight=1)
            
            # Smaller images for grid layout
            self._load_image_to_label(image_path, label, (120, 80))
    
    def _load_image_to_label(self, image_path, label, size=(200, 150)):
        """Load an image into a specific label with given size"""
        try:
            # Handle text files (ASCII art)
            if image_path.endswith('.txt'):
                with open(image_path, 'r', encoding='utf-8') as f:
                    ascii_art = f.read()
                label.config(text=ascii_art, font=('Courier', 6), fg='#00ff00', bg='#303030')
                return
            
            # Handle image files
            img = Image.open(image_path)
            img.thumbnail(size, Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            label.config(image=photo, text='')
            label.image = photo  # Keep a reference
        except Exception as e:
            label.config(text=f"Error:\n{image_path}\n{str(e)}", fg='#ff0000', bg='#1a1a1a')
    
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
            r'\b(\d+)\s*HP\b': '#ff4444',  # Red for HP values
            r'\bhp:\s*(\d+)': '#ff4444',   # Red for HP stats
            r'\b(\d+)/(\d+)\s*HP\b': '#ff4444',  # Red for HP fractions
            
            # Damage numbers
            r'\b(\d+)\s*damage\b': '#ff8800',  # Orange for damage
            r'\bfor\s+(\d+)\s+damage': '#ff8800',  # Orange for damage
            
            # Gold and currency
            r'💰\s*(\d+)': '#ffdd00',  # Gold for money
            r'\b(\d+)\s*gold\b': '#ffdd00',  # Gold for money
            
            # Experience and levels
            r'\bLevel\s*(\d+)': '#00aaff',  # Blue for levels
            r'\blevel:\s*(\d+)': '#00aaff',  # Blue for levels
            r'\b(\d+)\s*XP\b': '#8844ff',  # Purple for XP
            r'\bxp:\s*(\d+)': '#8844ff',   # Purple for XP
            
            # Attack and Defense stats
            r'\bAttack:\s*(\d+)': '#ff6600',  # Red-orange for attack
            r'\battack:\s*(\d+)': '#ff6600',  # Red-orange for attack
            r'\bDefense:\s*(\d+)': '#0088ff', # Blue for defense
            r'\bdefense:\s*(\d+)': '#0088ff', # Blue for defense
            
            # Names and important identifiers
            r'\b([A-Z][a-z]+ [A-Z][a-z]+)\b': '#ffaa00',  # Orange for character names
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
            'hp': '#ff4444',      # Red for health
            'damage': '#ff8800',  # Orange for damage  
            'gold': '#ffdd00',    # Gold for money
            'xp': '#8844ff',      # Purple for experience
            'level': '#00aaff',   # Blue for levels
            'attack': '#ff6600',  # Red-orange for attack
            'defense': '#0088ff', # Blue for defense
            'name': '#ffaa00',    # Orange for names
            'default': '#00ff00'  # Default green
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
            # No placeholder, just print normally
            parts.append((text + str(value), '#00ff00'))
        
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
        self.text_area.delete('1.0', tk.END)
        self.text_area.config(state=tk.DISABLED)  # Disable again
    
    def button_clicked(self, button_num):
        """Handle button clicks"""
        # Prevent clicks when interface is locked
        if not self.keyboard_enabled or not self.current_action:
            return
        
        # Only execute if the button is actually enabled
        if self._is_button_enabled(button_num):
            self.current_action(button_num)

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
            
        # Button shortcuts (1, 2, 3)
        elif key in ['1', '2', '3']:
            button_num = int(key)
            if self.current_action and self._is_button_enabled(button_num):
                self._highlight_button(button_num)
                self.root.after(100, lambda: self.current_action(button_num))
                
        # Arrow key navigation
        elif key == 'left':
            self._navigate_buttons(-1)
        elif key == 'right':
            self._navigate_buttons(1)
        elif key == 'return':  # Enter key
            if self.current_action and self._is_button_enabled(self.current_selected_button):
                self._highlight_button(self.current_selected_button)
                self.root.after(100, lambda: self.current_action(self.current_selected_button))
                
        # Audio controls
        elif key == 'm':
            self._toggle_audio()
        elif key == 'plus' or key == 'equal':
            self.audio.adjust_volume(0.1)
            self.print_text(f"🔊 Volume: {int(self.audio.get_volume() * 100)}%")
        elif key == 'minus':
            self.audio.adjust_volume(-0.1) 
            self.print_text(f"🔉 Volume: {int(self.audio.get_volume() * 100)}%")

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
                    self.root.after(100, lambda btn=i: self.current_action(btn))
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
   1, 2, 3 - Select buttons directly
   ← → - Navigate between buttons
   ENTER - Activate selected button

🔊 Audio:
   M - Mute/Unmute
   + - Volume up
   - - Volume down

💡 Tip: Look for button highlights to see
   which option is currently selected!
"""
        self.print_text(help_text)

    def _navigate_buttons(self, direction):
        """Navigate between buttons with arrow keys"""
        if not self.current_action or not self.buttons:
            return
            
        # Find current button and move selection
        new_button = self.current_selected_button + direction
        button_count = len(self.buttons)
        
        # Wrap around and find next enabled button
        for _ in range(button_count):  # Maximum button_count attempts to find enabled button
            if new_button < 1:
                new_button = button_count
            elif new_button > button_count:
                new_button = 1
                
            if self._is_button_enabled(new_button):
                self.current_selected_button = new_button
                self._update_button_selection()
                break
                
            new_button += direction

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
        self.show_image('art/pyquest.png')
        self.print_text("=" * 60)
        self.print_text("Welcome to Monster Game!")
        self.print_text("=" * 60)
        self.print_text("⌨️  Keyboard shortcuts enabled! Press F1 for help")
        self.print_text("   Use 1-3 keys, arrows, SPACE, or ESC to navigate")
        self.print_text("")
        
        # Initialize game state
        self.game_state = initialize_game_state()
        
        # Initialize game systems with GUI
        self.combat = CombatGUI(self)
        self.shop = ShopGUI(self)
        self.inventory = InventoryGUI(self)
        self.monster_encounter = MonsterEncounterGUI(self)
        
        # Start hero selection
        self.select_hero()
    
    def select_hero(self):
        """Handle hero selection"""
        self.clear_text()
        self.print_text("\n⚔️  Choose Your Hero ⚔️\n")
        
        for i, (hero_name, hero_data) in enumerate(self.game_state.heros.items(), 1):
            self.print_text(f"\n{i}. {hero_name}")
            for key, value in hero_data.items():
                self.print_text(f"   {key}: {value}")
        
        def on_hero_select(choice):
            hero_name = self.game_state.choices.get(str(choice))
            if hero_name:
                self.game_state.hero = self.game_state.heros[hero_name].copy()
                self.game_state.hero['name'] = hero_name
                self.game_state.hero['lives_left'] = 3
                self.game_state.hero['gold'] = 50
                self.game_state.hero['level'] = 1
                self.game_state.hero['xp'] = 0
                self.print_text(f"\n✓ You chose: {hero_name}!\n")
                sleep(0.5)
                self.main_menu()
        
        self.set_buttons(["Hero 1", "Hero 2", "Hero 3"], on_hero_select)
    
    def hero_level(self):
        """Handle hero leveling up"""
        if self.game_state.hero['xp'] >= self.game_state.hero['level'] * 5:
            self.clear_text()
            self.print_text("\n🎉  Level Up! 🎉\n")
            self.audio.play_sound_effect('levelup.wav')
            self.game_state.hero['level'] += 1
            self.game_state.hero['xp'] = 0
            self.game_state.hero['maxhp'] += 5
            self.game_state.hero['attack'] += 2
            self.game_state.hero['defense'] += 2
            self.print_text(f"Your hero has reached level {self.game_state.hero['level']}!")
            sleep(2)

    
    def main_menu(self):
        """Display main menu"""
        """Check for level up event first"""
        self.hero_level()
        self.clear_text()
        self.show_image(f"art/{self.game_state.hero['class']}.png")
        
        self.print_text("\n" + "=" * 60)
        self.print_text("⚔️  Hero Stats ⚔️")
        self.print_text("=" * 60)
        
        for key, value in self.game_state.hero.items():
            if key == 'xp':
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
                
            elif key == 'item' and value is not None:
                self.print_colored_value(f"  {key}: ", value['name'], 'name')
            elif key in ['hp', 'maxhp']:
                self.print_colored_value(f"  {key}: ", value, 'hp')
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
        self.print_text("\nWhat would you like to do?")
        
        def on_menu_select(choice):
            if choice == 1:
                self.shop.open()
            elif choice == 2:
                self.monster_encounter.start()
            elif choice == 3:
                self.inventory.use_item()
        
        self.set_buttons(["🛒 Shop", "⚔️ Fight Monster", "🧪 Use Item"], on_menu_select)

    def game_over(self):
        """Handle game over when hero has 0 lives left"""
        self.clear_text()
        self.lock_interface()
        
        # Show game over image
        self.show_image('art/you_lost.png')
        
        # Display game over message
        self.print_text("\n" + "=" * 60)
        self.print_text("💀  GAME OVER  💀")
        self.print_text("=" * 60)
        self.print_text("\nYou are out of lives! The adventure ends here...")
        self.print_text("Thank you for playing PyQuest!")
        self.print_text("=" * 60)
        
        # Play game over sound
        self.audio.play_sound_effect('death.mp3')
        
        # Close the game after 5 seconds
        self.root.after(5000, self._close_game)
    
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
