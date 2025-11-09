#!/usr/bin/env python3
"""
Compare the old and new town background art styles
"""

import sys
import os
import tkinter as tk
from PIL import Image, ImageTk

def compare_town_backgrounds():
    """Show side-by-side comparison of old vs new town backgrounds"""
    
    print("🎨 Comparing Town Background Art Styles")
    print("=" * 60)
    
    # Create comparison window
    root = tk.Tk()
    root.title("Town Background Comparison - Old vs New")
    root.geometry("1200x400")
    root.configure(bg='#1a1a1a')
    
    try:
        # Load images
        new_bg_path = "art/town_background.png"
        old_bg_path = None
        
        # Check if old background exists
        if os.path.exists("art/town_background_old.png"):
            old_bg_path = "art/town_background_old.png"
        
        if not os.path.exists(new_bg_path):
            print("❌ New town background not found!")
            return
        
        # Load new background
        new_img = Image.open(new_bg_path)
        print(f"✅ New background loaded: {new_img.size[0]}x{new_img.size[1]} pixels")
        
        # Resize for display
        display_width, display_height = 500, 300
        new_display = new_img.resize((display_width, display_height), Image.Resampling.NEAREST)
        new_photo = ImageTk.PhotoImage(new_display)
        
        # Create labels
        title_label = tk.Label(root, text="🎨 Town Background Art Style Comparison", 
                              font=('Arial', 16, 'bold'), fg='white', bg='#1a1a1a')
        title_label.pack(pady=10)
        
        # Frame for images
        image_frame = tk.Frame(root, bg='#1a1a1a')
        image_frame.pack(expand=True, fill='both')
        
        if old_bg_path and os.path.exists(old_bg_path):
            # Load old background
            old_img = Image.open(old_bg_path)
            print(f"✅ Old background loaded: {old_img.size[0]}x{old_img.size[1]} pixels")
            old_display = old_img.resize((display_width, display_height))
            old_photo = ImageTk.PhotoImage(old_display)
            
            # Old background panel
            old_frame = tk.Frame(image_frame, bg='#1a1a1a')
            old_frame.pack(side='left', padx=10, expand=True, fill='both')
            
            old_title = tk.Label(old_frame, text="OLD: Large Canvas Art Style", 
                                font=('Arial', 12, 'bold'), fg='#ff6666', bg='#1a1a1a')
            old_title.pack(pady=5)
            
            old_label = tk.Label(old_frame, image=old_photo, bg='#1a1a1a')
            old_label.pack()
            
            old_info = tk.Label(old_frame, 
                              text=f"Size: {old_img.size[0]}x{old_img.size[1]}\nStyle: Detailed artwork\nMethod: PIL drawing", 
                              font=('Arial', 10), fg='#cccccc', bg='#1a1a1a')
            old_info.pack(pady=5)
        else:
            # No old background found
            old_frame = tk.Frame(image_frame, bg='#1a1a1a')
            old_frame.pack(side='left', padx=10, expand=True, fill='both')
            
            no_old_label = tk.Label(old_frame, text="OLD BACKGROUND\nNOT FOUND", 
                                  font=('Arial', 14, 'bold'), fg='#666666', bg='#1a1a1a')
            no_old_label.pack(expand=True)
        
        # New background panel
        new_frame = tk.Frame(image_frame, bg='#1a1a1a')
        new_frame.pack(side='right', padx=10, expand=True, fill='both')
        
        new_title = tk.Label(new_frame, text="NEW: Pixel Art Style", 
                            font=('Arial', 12, 'bold'), fg='#66ff66', bg='#1a1a1a')
        new_title.pack(pady=5)
        
        new_label = tk.Label(new_frame, image=new_photo, bg='#1a1a1a')
        new_label.pack()
        
        new_info = tk.Label(new_frame, 
                          text=f"Size: {new_img.size[0]}x{new_img.size[1]}\nStyle: Pixel art\nMethod: Numpy array + 8x scaling", 
                          font=('Arial', 10), fg='#cccccc', bg='#1a1a1a')
        new_info.pack(pady=5)
        
        # Comparison info
        comparison_text = """
🎯 KEY IMPROVEMENTS:
• Matches desert biome pixel art style
• Crisp 8x upscaled pixel art
• Consistent with game's visual theme
• Smaller base canvas (64x32) for authentic retro feel
• Uses numpy arrays like other biomes
        """
        
        info_label = tk.Label(root, text=comparison_text, 
                            font=('Arial', 10), fg='#ffdd00', bg='#1a1a1a', justify='left')
        info_label.pack(pady=10)
        
        # Keep references to prevent garbage collection
        root.new_photo = new_photo
        if old_bg_path and os.path.exists(old_bg_path):
            root.old_photo = old_photo
        
        print("✅ Comparison window created")
        print("🖼️ Showing visual comparison...")
        
        # Show window
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error creating comparison: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            root.quit()
        except:
            pass

def analyze_art_styles():
    """Analyze the technical differences between art styles"""
    
    print("\n🔍 TECHNICAL ANALYSIS")
    print("=" * 60)
    
    new_bg_path = "art/town_background.png"
    
    if os.path.exists(new_bg_path):
        new_img = Image.open(new_bg_path)
        
        print("🆕 NEW PIXEL ART STYLE:")
        print(f"   📐 Dimensions: {new_img.size[0]}x{new_img.size[1]} pixels")
        print(f"   🎨 Mode: {new_img.mode}")
        print(f"   📁 File size: {os.path.getsize(new_bg_path)} bytes")
        print("   🎯 Method: 64x32 numpy array → 8x nearest neighbor scaling")
        print("   🖼️ Style: Crisp pixel art with defined color palette")
        print("   ⚡ Performance: Optimized for game rendering")
        print("   🎮 Consistency: Matches desert biome art style")
        
        # Check if it matches biome style dimensions
        desert_bg_path = "art/desert_background.png"
        if os.path.exists(desert_bg_path):
            desert_img = Image.open(desert_bg_path)
            if new_img.size == desert_img.size:
                print("   ✅ Dimensions match desert biome perfectly!")
            else:
                print(f"   ⚠️ Size mismatch with desert: {desert_img.size}")
    
    print("\n🎯 STYLE CONSISTENCY CHECK:")
    
    # Check other biome backgrounds for consistency
    biome_backgrounds = [
        ("desert_background.png", "Desert"),
        ("grassy_background.png", "Grassland"), 
        ("dungeon_background.png", "Dungeon"),
        ("ocean_background.png", "Ocean"),
        ("town_background.png", "Town")
    ]
    
    sizes = {}
    for filename, biome_name in biome_backgrounds:
        path = f"art/{filename}"
        if os.path.exists(path):
            img = Image.open(path)
            sizes[biome_name] = img.size
            print(f"   📐 {biome_name}: {img.size[0]}x{img.size[1]}")
        else:
            print(f"   ❌ {biome_name}: Not found")
    
    # Check consistency
    if len(set(sizes.values())) == 1:
        print("   ✅ All biome backgrounds have consistent dimensions!")
    else:
        print("   ⚠️ Inconsistent dimensions detected")
        
    print(f"\n🏘️ TOWN BACKGROUND READY FOR USE!")

if __name__ == '__main__':
    compare_town_backgrounds()
    analyze_art_styles()