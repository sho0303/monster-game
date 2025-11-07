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
        
        # Disable keyboard input in the window (GUI only, no keyboard shortcuts)
        self.root.bind('<Key>', lambda e: 'break')  # Block all keyboard events
        
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
        
        # Create buttons (initially hidden)
        self.btn1 = tk.Button(
            self.button_frame, 
            text="Option 1",
            command=lambda: self.button_clicked(1),
            bg='#4a4a4a',
            fg='#ffffff',
            font=('Arial', 12, 'bold'),
            width=15
        )
        
        self.btn2 = tk.Button(
            self.button_frame,
            text="Option 2", 
            command=lambda: self.button_clicked(2),
            bg='#4a4a4a',
            fg='#ffffff',
            font=('Arial', 12, 'bold'),
            width=15
        )
        
        self.btn3 = tk.Button(
            self.button_frame,
            text="Option 3",
            command=lambda: self.button_clicked(3),
            bg='#4a4a4a',
            fg='#ffffff',
            font=('Arial', 12, 'bold'),
            width=15
        )
        
        self.btn1.pack(side=tk.LEFT, padx=5)
        self.btn2.pack(side=tk.LEFT, padx=5)
        self.btn3.pack(side=tk.LEFT, padx=5)
        
        self.current_action = None
    
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
        """Print text to the text area"""
        self.text_area.config(state=tk.NORMAL)  # Temporarily enable for writing
        self.text_area.insert(tk.END, text + '\n')
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)  # Disable again
        self.root.update()
    
    def clear_text(self):
        """Clear the text area"""
        self.text_area.config(state=tk.NORMAL)  # Temporarily enable for clearing
        self.text_area.delete('1.0', tk.END)
        self.text_area.config(state=tk.DISABLED)  # Disable again
    
    def button_clicked(self, button_num):
        """Handle button clicks"""
        if self.current_action:
            self.current_action(button_num)
    
    def set_buttons(self, labels, action_callback):
        """Set button labels and action"""
        for i, (btn, label) in enumerate(zip([self.btn1, self.btn2, self.btn3], labels)):
            if label:
                btn.config(text=label, state=tk.NORMAL)
            else:
                btn.config(text="", state=tk.DISABLED)
        
        self.current_action = action_callback
    
    def initialize_game(self):
        """Initialize the game"""
        # Start background music that will loop continuously
        self.audio.play_background_music('start.mp3', loop=True, volume=0.4)
        self.show_image('art/pyquest.png')
        self.print_text("=" * 60)
        self.print_text("Welcome to Monster Game!")
        self.print_text("=" * 60)
        
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
                self.print_text(f"  {key}: {value}/{self.game_state.hero['level']*5}")
            elif key == 'item' and value is not None:
                self.print_text(f"  {key}: {value['name']}")
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
