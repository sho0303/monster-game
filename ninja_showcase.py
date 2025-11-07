"""
Demo script to showcase the ninja attack animation
Shows both the original and attack versions in the game interface
"""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def create_ninja_showcase():
    """Create a window showing both ninja versions"""
    
    root = tk.Tk()
    root.title("🥷 Ninja Attack Animation Showcase")
    root.geometry("600x400")
    root.configure(bg='#2d2d2d')
    
    # Title
    title_label = tk.Label(
        root, 
        text="🥷 Ninja Character - Original vs Attack Animation",
        font=('Arial', 16, 'bold'),
        fg='white',
        bg='#2d2d2d'
    )
    title_label.pack(pady=10)
    
    # Create frame for images
    image_frame = tk.Frame(root, bg='#2d2d2d')
    image_frame.pack(expand=True, fill='both', padx=20, pady=10)
    
    try:
        # Load original ninja
        original_img = Image.open('art/Ninja.png')
        original_img = original_img.resize((200, 200), Image.NEAREST)
        original_photo = ImageTk.PhotoImage(original_img)
        
        # Load attack ninja
        attack_img = Image.open('art/ninja_attack.png')
        attack_img = attack_img.resize((200, 200), Image.NEAREST)
        attack_photo = ImageTk.PhotoImage(attack_img)
        
        # Original ninja frame
        original_frame = tk.Frame(image_frame, bg='#404040', relief='sunken', bd=2)
        original_frame.pack(side=tk.LEFT, expand=True, padx=10, pady=10)
        
        tk.Label(original_frame, text="Original Ninja", font=('Arial', 12, 'bold'), fg='white', bg='#404040').pack(pady=5)
        original_label = tk.Label(original_frame, image=original_photo, bg='#404040')
        original_label.pack(pady=10)
        
        tk.Label(original_frame, text="• Standing pose\\n• Defensive stance\\n• Ready position", 
                font=('Arial', 9), fg='#cccccc', bg='#404040', justify='left').pack(pady=5)
        
        # Attack ninja frame
        attack_frame = tk.Frame(image_frame, bg='#404040', relief='sunken', bd=2)
        attack_frame.pack(side=tk.RIGHT, expand=True, padx=10, pady=10)
        
        tk.Label(attack_frame, text="Attack Animation", font=('Arial', 12, 'bold'), fg='white', bg='#404040').pack(pady=5)
        attack_label = tk.Label(attack_frame, image=attack_photo, bg='#404040')
        attack_label.pack(pady=10)
        
        tk.Label(attack_frame, text="• Dynamic attack pose\\n• Motion effects\\n• Speed lines & sparkles", 
                font=('Arial', 9), fg='#cccccc', bg='#404040', justify='left').pack(pady=5)
        
        # Keep references to prevent garbage collection
        original_label.image = original_photo
        attack_label.image = attack_photo
        
        # Info text
        info_text = tk.Label(
            root,
            text="The attack animation shows the ninja in mid-strike with motion blur, speed lines, and impact effects!",
            font=('Arial', 10),
            fg='#cccccc',
            bg='#2d2d2d',
            wraplength=550
        )
        info_text.pack(pady=10)
        
        # Usage note
        usage_text = tk.Label(
            root,
            text="💡 Usage: This can be used for combat animations, attack buttons, or character abilities in the game!",
            font=('Arial', 9, 'italic'),
            fg='#aaaaaa',
            bg='#2d2d2d',
            wraplength=550
        )
        usage_text.pack(pady=5)
        
        print("✅ Ninja Attack Animation Showcase launched!")
        print("   View the comparison between original and attack versions")
        print("   Close the window when done")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error loading images: {e}")
        print("   Make sure both Ninja.png and ninja_attack.png exist in the art/ directory")
        root.destroy()

if __name__ == '__main__':
    create_ninja_showcase()