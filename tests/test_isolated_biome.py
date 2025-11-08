#!/usr/bin/env python3
"""
Isolate the exact issue with ocean biome setting
"""

import tkinter as tk
from gui_main import GameGUI
from game_state import initialize_game_state

def test_isolated_biome_setting():
    """Test the exact biome setting logic in isolation"""
    
    print("🔬 Isolated Ocean Biome Test 🔬")
    print("=" * 40)
    
    # Create minimal GUI
    root = tk.Tk()
    root.withdraw()
    
    try:
        gui = GameGUI(root)
        gui.game_state = initialize_game_state()
        
        # Test the exact biome setting logic with detailed tracing
        print("📋 Testing set_biome_background('ocean') step by step:")
        
        biome_name = 'ocean'
        print(f"   Input biome_name: '{biome_name}' (type: {type(biome_name)})")
        
        # Check if current_biome exists
        has_current_biome = hasattr(gui, 'current_biome')
        print(f"   hasattr(gui, 'current_biome'): {has_current_biome}")
        if has_current_biome:
            print(f"   gui.current_biome before: '{gui.current_biome}'")
        
        # Test biome_configs lookup
        biome_configs = {
            'grassland': {'background': 'art/grassy_background.png', 'fallback_color': '#4a7c59'},
            'desert': {'background': 'art/desert_background.png', 'fallback_color': '#daa520'},
            'dungeon': {'background': 'art/dungeon_background.png', 'fallback_color': '#2d1f1a'},
            'ocean': {'background': 'art/ocean_background.png', 'fallback_color': '#0077be'}
        }
        
        print(f"   biome_configs keys: {list(biome_configs.keys())}")
        
        is_in_configs = biome_name in biome_configs
        print(f"   '{biome_name}' in biome_configs: {is_in_configs}")
        
        if is_in_configs:
            config = biome_configs[biome_name]
            print(f"   Selected config: {config}")
            
            # Manually set current_biome (simulate what should happen)
            print(f"   Setting gui.current_biome = '{biome_name}'...")
            gui.current_biome = biome_name
            print(f"   gui.current_biome after manual set: '{gui.current_biome}'")
            
            # Test set_background_image call
            print(f"   Testing set_background_image('{config['background']}', '{config['fallback_color']}')")
            
            try:
                # Create a version of set_background_image that reports what it's doing
                background_path = config['background']
                fallback_color = config['fallback_color']
                
                print(f"     Loading image: {background_path}")
                from PIL import Image, ImageTk
                
                # Check file exists
                import os
                if not os.path.exists(background_path):
                    print(f"     ❌ FILE MISSING: {background_path}")
                    return
                else:
                    print(f"     ✅ File exists: {background_path}")
                
                # Try to load image
                bg_img = Image.open(background_path)
                print(f"     ✅ Image loaded: {bg_img.size}")
                
                # Try to resize
                canvas_width, canvas_height = 800, 400
                bg_img_resized = bg_img.resize((canvas_width, canvas_height), Image.Resampling.NEAREST)
                print(f"     ✅ Image resized: {bg_img_resized.size}")
                
                # Try to create PhotoImage
                bg_photo = ImageTk.PhotoImage(bg_img_resized)
                print(f"     ✅ PhotoImage created")
                
                # Try canvas operations
                gui.image_canvas.delete("all")
                gui.image_canvas.create_image(0, 0, image=bg_photo, anchor='nw', tags="background")
                print(f"     ✅ Canvas updated")
                
                # Store reference to prevent garbage collection
                gui.bg_photo = bg_photo
                
                print(f"     ✅ set_background_image completed successfully")
                
            except Exception as e:
                print(f"     ❌ set_background_image failed: {e}")
                import traceback
                traceback.print_exc()
        
        print(f"\n🔎 Final state check:")
        print(f"   gui.current_biome: '{gui.current_biome}'")
        
        # Now test the actual method
        print(f"\n🧪 Testing actual set_biome_background method:")
        print(f"   Before: gui.current_biome = '{gui.current_biome}'")
        
        gui.set_biome_background('ocean')
        
        print(f"   After:  gui.current_biome = '{gui.current_biome}'")
        
        if gui.current_biome == 'ocean':
            print(f"   ✅ SUCCESS: Ocean biome properly set!")
        else:
            print(f"   ❌ FAILED: Expected 'ocean', got '{gui.current_biome}'")
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        try:
            root.destroy()
        except:
            pass

if __name__ == "__main__":
    test_isolated_biome_setting()