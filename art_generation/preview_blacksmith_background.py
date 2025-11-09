#!/usr/bin/env python3
"""
Preview the generated blacksmith background
"""

from PIL import Image
import os

def preview_blacksmith_background():
    """Display information about the generated blacksmith background"""
    background_path = "art/blacksmith_background.png"
    background_large_path = "art/blacksmith_background_large.png"
    
    if os.path.exists(background_path):
        # Load images
        bg_img = Image.open(background_path)
        
        print("⚒️ BLACKSMITH BACKGROUND GENERATED SUCCESSFULLY! ⚒️")
        print("=" * 60)
        print(f"📁 Regular Background: {background_path}")
        print(f"   📏 Size: {bg_img.size}")
        print(f"   🎨 Mode: {bg_img.mode}")
        
        if os.path.exists(background_large_path):
            bg_large_img = Image.open(background_large_path)
            print(f"\n📁 Large Background: {background_large_path}")
            print(f"   📏 Size: {bg_large_img.size}")
            print(f"   🎨 Mode: {bg_large_img.mode}")
        
        print("\n🎯 VISUAL FEATURES:")
        print("   • Stone brick walls with mortar lines")
        print("   • Active forge with blazing fire")
        print("   • Anvil with hammer and flying sparks")
        print("   • Tool rack with hanging implements")
        print("   • Water barrel for quenching hot metal")
        print("   • Bellows for stoking the forge")
        print("   • Sword rack with blades in various stages")
        print("   • Workbench with precision tools")
        print("   • Coal pile and forge lighting effects")
        print("   • Steam and smoke atmospheric details")
        
        print("\n🎮 INTEGRATION:")
        print("   • Medieval blacksmith atmosphere")
        print("   • Consistent with existing game art style")
        print("   • 512x256 base resolution (64x32 scaled 8x)")
        print("   • Stone and metal color palette")
        print("   • Perfect for enhancement services!")
        
        return bg_img
    else:
        print("❌ Blacksmith background not found. Please run create_blacksmith_background.py first.")
        return None

if __name__ == "__main__":
    preview_blacksmith_background()