"""
Demo script to showcase the magician attack animation
Shows both the original and attack versions in the game interface
"""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def create_magician_showcase():
    """Create a window showing both magician versions"""
    
    root = tk.Tk()
    root.title("🧙 Magician Attack Animation Showcase")
    root.geometry("700x500")
    root.configure(bg='#2d2d2d')
    
    # Title
    title_label = tk.Label(
        root, 
        text="🧙‍♂️ Magician Character - Original vs Spell-Casting Attack",
        font=('Arial', 16, 'bold'),
        fg='white',
        bg='#2d2d2d'
    )
    title_label.pack(pady=10)
    
    # Create frame for images
    image_frame = tk.Frame(root, bg='#2d2d2d')
    image_frame.pack(expand=True, fill='both', padx=20, pady=10)
    
    try:
        # Load original magician
        original_img = Image.open('art/Magician.png')
        original_img = original_img.resize((200, 200), Image.NEAREST)
        original_photo = ImageTk.PhotoImage(original_img)
        
        # Load attack magician
        attack_img = Image.open('art/magician_attack.png')
        attack_img = attack_img.resize((200, 200), Image.NEAREST)
        attack_photo = ImageTk.PhotoImage(attack_img)
        
        # Original magician frame
        original_frame = tk.Frame(image_frame, bg='#404040', relief='sunken', bd=2)
        original_frame.pack(side=tk.LEFT, expand=True, padx=10, pady=10)
        
        tk.Label(original_frame, text="Original Magician", font=('Arial', 12, 'bold'), fg='white', bg='#404040').pack(pady=5)
        original_label = tk.Label(original_frame, image=original_photo, bg='#404040')
        original_label.pack(pady=10)
        
        original_features = tk.Label(original_frame, 
            text="• Standing pose\\n• Staff at rest\\n• Calm magical aura\\n• Steady magic orb", 
            font=('Arial', 9), fg='#cccccc', bg='#404040', justify='left'
        )
        original_features.pack(pady=5)
        
        # Attack magician frame
        attack_frame = tk.Frame(image_frame, bg='#404040', relief='sunken', bd=2)
        attack_frame.pack(side=tk.RIGHT, expand=True, padx=10, pady=10)
        
        tk.Label(attack_frame, text="Spell-Casting Attack", font=('Arial', 12, 'bold'), fg='white', bg='#404040').pack(pady=5)
        attack_label = tk.Label(attack_frame, image=attack_photo, bg='#404040')
        attack_label.pack(pady=10)
        
        attack_features = tk.Label(attack_frame, 
            text="• Dramatic casting pose\\n• Massive energy spell\\n• Crystal explosion\\n• Lightning effects", 
            font=('Arial', 9), fg='#cccccc', bg='#404040', justify='left'
        )
        attack_features.pack(pady=5)
        
        # Keep references to prevent garbage collection
        original_label.image = original_photo
        attack_label.image = attack_photo
        
        # Feature comparison
        comparison_frame = tk.Frame(root, bg='#2d2d2d')
        comparison_frame.pack(pady=10, padx=20)
        
        tk.Label(comparison_frame, text="✨ Attack Animation Features:", 
                font=('Arial', 12, 'bold'), fg='#ffaa00', bg='#2d2d2d').pack()
        
        features_text = (
            "🔮 Massive Energy Orb - Bright glowing spell with radiating beams\\n"
            "⚡ Lightning Magic - Electric blue energy crackling through robes\\n"
            "💫 Crystal Explosion - Staff tip bursting with magical power\\n"
            "👁️ Glowing Eyes - Channeling mystical energy\\n"
            "🌪️ Flowing Effects - Beard and robes moving with magical wind\\n"
            "✨ Energy Sparks - Multi-colored magical effects\\n"
            "🔥 Ground Magic - Energy crackling at wizard's feet\\n"
            "🌟 Golden Aura - Enhanced trim glowing with spell power"
        )
        
        features_label = tk.Label(
            comparison_frame,
            text=features_text,
            font=('Arial', 9),
            fg='#cccccc',
            bg='#2d2d2d',
            justify='left',
            wraplength=650
        )
        features_label.pack(pady=5)
        
        # Usage note
        usage_text = tk.Label(
            root,
            text="💡 Perfect for: Spell-casting animations, magic attacks, boss battles, and mystical abilities!",
            font=('Arial', 10, 'italic'),
            fg='#aaaaaa',
            bg='#2d2d2d',
            wraplength=650
        )
        usage_text.pack(pady=10)
        
        print("✅ Magician Attack Animation Showcase launched!")
        print("   View the comparison between original and spell-casting attack versions")
        print("   Features dramatic magical effects and energy animations")
        print("   Close the window when done")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error loading images: {e}")
        print("   Make sure both Magician.png and magician_attack.png exist in the art/ directory")
        root.destroy()

if __name__ == '__main__':
    create_magician_showcase()