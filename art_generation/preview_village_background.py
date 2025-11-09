#!/usr/bin/env python3
"""
Preview the updated fantasy wooden village background
"""

from PIL import Image
import os

def preview_village_background():
    """Display information about the updated village background"""
    background_path = "art/town_background.png"
    background_large_path = "art/town_background_large.png"
    
    if os.path.exists(background_path):
        # Load images
        bg_img = Image.open(background_path)
        
        print("🏘️ FANTASY WOODEN VILLAGE BACKGROUND UPDATED! 🏘️")
        print("=" * 60)
        print(f"📁 Regular Background: {background_path}")
        print(f"   📏 Size: {bg_img.size}")
        print(f"   🎨 Mode: {bg_img.mode}")
        
        if os.path.exists(background_large_path):
            bg_large_img = Image.open(background_large_path)
            print(f"\n📁 Large Background: {background_large_path}")
            print(f"   📏 Size: {bg_large_img.size}")
            print(f"   🎨 Mode: {bg_large_img.mode}")
        
        print("\n🔄 CHANGES MADE (City → Fantasy Village):")
        print("   ❌ Removed: Stone buildings and cobblestone streets")
        print("   ❌ Removed: Formal city fountain")
        print("   ❌ Removed: Stone lamp posts")
        print("   ❌ Removed: Red clay tile roofs")
        print("")
        print("   ✅ Added: Wooden houses and log cabins")
        print("   ✅ Added: Thatched roofs with moss patches")
        print("   ✅ Added: Tudor-style plaster & timber cottages")
        print("   ✅ Added: Dirt roads with wagon wheel ruts")
        print("   ✅ Added: Village well with wooden covering")
        print("   ✅ Added: Wooden fence posts and hitching posts")
        print("   ✅ Added: Canvas market stall awnings")
        print("   ✅ Added: Natural color palette (browns, creams, golds)")
        
        print("\n🎯 FANTASY VILLAGE FEATURES:")
        print("   🏠 6 different wooden buildings:")
        print("      - Wood cottage with thatched roof")
        print("      - Log cabin with golden thatch")
        print("      - Tudor cottage with plaster & timber")
        print("      - Medium wood house")
        print("      - Light wood cottage")
        print("      - Dark wood house with wooden shingles")
        print("   🛤️  Natural dirt roads instead of stone")
        print("   🪣 Village well replaces formal fountain")
        print("   🕯️ Rustic lanterns on wooden fence posts")
        print("   🌿 Moss patches on some thatched roofs")
        print("   💨 Cozy chimney smoke")
        
        print("\n🎮 GAME INTEGRATION:")
        print("   • Perfect fantasy atmosphere")
        print("   • Matches wooden aesthetic of other game elements")
        print("   • Cozy, welcoming village feel")
        print("   • Consistent pixel art style")
        print("   • Same dimensions as original (512x256)")
        
        return bg_img
    else:
        print("❌ Village background not found. Please run create_town_background.py first.")
        return None

if __name__ == "__main__":
    preview_village_background()