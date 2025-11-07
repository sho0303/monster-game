"""
Comprehensive showcase of all three character attack animations
Shows Ninja, Magician, and Warrior attack animations side by side
"""
import tkinter as tk
from PIL import Image, ImageTk

def create_all_characters_showcase():
    """Create a window showing all three character attack animations"""
    
    root = tk.Tk()
    root.title("⚔️🧙🥷 Complete Character Attack Animation Showcase")
    root.geometry("900x600")
    root.configure(bg='#2d2d2d')
    
    # Title
    title_label = tk.Label(
        root, 
        text="⚔️ Complete Character Attack Animations ⚔️",
        font=('Arial', 18, 'bold'),
        fg='white',
        bg='#2d2d2d'
    )
    title_label.pack(pady=15)
    
    subtitle_label = tk.Label(
        root,
        text="🥷 Ninja • 🧙‍♂️ Magician • ⚔️ Warrior",
        font=('Arial', 14),
        fg='#ffaa00',
        bg='#2d2d2d'
    )
    subtitle_label.pack(pady=5)
    
    # Create frame for all character images
    characters_frame = tk.Frame(root, bg='#2d2d2d')
    characters_frame.pack(expand=True, fill='both', padx=20, pady=10)
    
    try:
        characters = [
            {
                'name': '🥷 Ninja Attack',
                'file': 'ninja_attack.png',
                'features': [
                    '• Lightning-fast kunai strike',
                    '• Motion blur and speed lines', 
                    '• Stealth energy effects',
                    '• Dynamic lunge position'
                ]
            },
            {
                'name': '🧙‍♂️ Magician Spell',
                'file': 'magician_attack.png',
                'features': [
                    '• Massive energy orb casting',
                    '• Crystal explosion effects',
                    '• Lightning magic crackling',
                    '• Mystical aura and sparks'
                ]
            },
            {
                'name': '⚔️ Warrior Strike',
                'file': 'warrior_attack.png',
                'features': [
                    '• Powerful sword slash',
                    '• Impact sparks and energy',
                    '• Battle stance and shield',
                    '• Armor gleaming effects'
                ]
            }
        ]
        
        for i, char in enumerate(characters):
            # Create frame for each character
            char_frame = tk.Frame(characters_frame, bg='#404040', relief='raised', bd=3)
            char_frame.pack(side=tk.LEFT, expand=True, padx=10, pady=10, fill='both')
            
            # Character name
            name_label = tk.Label(
                char_frame, 
                text=char['name'], 
                font=('Arial', 12, 'bold'), 
                fg='white', 
                bg='#404040'
            )
            name_label.pack(pady=8)
            
            # Load and display character image
            img = Image.open(f"art/{char['file']}")
            img = img.resize((150, 150), Image.NEAREST)
            photo = ImageTk.PhotoImage(img)
            
            img_label = tk.Label(char_frame, image=photo, bg='#404040')
            img_label.pack(pady=8)
            img_label.image = photo  # Keep reference
            
            # Features list
            features_text = "\\n".join(char['features'])
            features_label = tk.Label(
                char_frame,
                text=features_text,
                font=('Arial', 8),
                fg='#cccccc',
                bg='#404040',
                justify='left'
            )
            features_label.pack(pady=8)
        
        # Combat integration info
        integration_frame = tk.Frame(root, bg='#2d2d2d')
        integration_frame.pack(pady=15, padx=20)
        
        tk.Label(
            integration_frame,
            text="🎮 Combat Integration Examples:",
            font=('Arial', 12, 'bold'),
            fg='#ffaa00',
            bg='#2d2d2d'
        ).pack()
        
        integration_examples = [
            "if hero['class'] == 'Ninja' and hero_attacks:",
            "    gui.show_image('art/ninja_attack.png')",
            "elif hero['class'] == 'Magician' and hero_casts_spell:",
            "    gui.show_image('art/magician_attack.png')", 
            "elif hero['class'] == 'Warrior' and hero_sword_strike:",
            "    gui.show_image('art/warrior_attack.png')"
        ]
        
        code_text = "\\n".join(integration_examples)
        code_label = tk.Label(
            integration_frame,
            text=code_text,
            font=('Courier', 9),
            fg='#90EE90',
            bg='#1a1a1a',
            justify='left',
            padx=10,
            pady=10
        )
        code_label.pack(pady=10)
        
        # Usage scenarios
        scenarios_frame = tk.Frame(root, bg='#2d2d2d')
        scenarios_frame.pack(pady=10, padx=20)
        
        scenarios_text = (
            "💡 Perfect for: Combat animations • Class-specific abilities • Critical hits • "
            "Skill demonstrations • Boss battles • Character showcases • Menu animations"
        )
        
        scenarios_label = tk.Label(
            scenarios_frame,
            text=scenarios_text,
            font=('Arial', 10, 'italic'),
            fg='#aaaaaa',
            bg='#2d2d2d',
            wraplength=850,
            justify='center'
        )
        scenarios_label.pack()
        
        print("✅ Complete Character Attack Animation Showcase launched!")
        print("   Displaying all three character classes with attack animations:")
        print("   🥷 Ninja - Stealth and speed-based attacks")
        print("   🧙‍♂️ Magician - Magical spells and energy effects")
        print("   ⚔️ Warrior - Sword combat and battle prowess")
        print("   Close the window when done")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error loading character images: {e}")
        print("   Make sure all attack animation files exist in the art/ directory")
        root.destroy()

if __name__ == '__main__':
    create_all_characters_showcase()