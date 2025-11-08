"""
Quick desert biome test - simple console script to verify desert background creation
"""

from PIL import Image
import os

def test_desert_background():
    """Simple test to check if desert background was created correctly"""
    
    # Check if desert background exists
    desert_path = "art/desert_background.png"
    
    if os.path.exists(desert_path):
        print("✅ Desert background found!")
        
        # Load and display info about the image
        try:
            desert_img = Image.open(desert_path)
            print(f"   📏 Dimensions: {desert_img.size[0]} x {desert_img.size[1]} pixels")
            print(f"   🎨 Mode: {desert_img.mode}")
            print(f"   📂 File size: {os.path.getsize(desert_path)} bytes")
            
            # Show a preview of colors by sampling some pixels
            width, height = desert_img.size
            
            # Sample some key areas
            samples = [
                ("Sky (top-left)", (width//4, height//8)),
                ("Sky (top-right)", (3*width//4, height//8)), 
                ("Horizon", (width//2, height//2)),
                ("Ground (bottom-left)", (width//4, 7*height//8)),
                ("Ground (bottom-right)", (3*width//4, 7*height//8)),
            ]
            
            print("\n   🎨 Color samples:")
            for name, (x, y) in samples:
                pixel = desert_img.getpixel((x, y))
                if len(pixel) >= 3:
                    print(f"      {name}: RGB({pixel[0]}, {pixel[1]}, {pixel[2]})")
            
            print("\n🏜️ Desert biome features should include:")
            print("   - Warm orange/golden sky gradient")
            print("   - Sandy dunes with multiple tones")
            print("   - Desert cacti and rock formations")
            print("   - Scattered bones and crystals")
            print("   - Heat shimmer effects")
            
            print(f"\n✨ Desert background ready for use in biome system!")
            
        except Exception as e:
            print(f"❌ Error reading desert background: {e}")
    else:
        print(f"❌ Desert background not found at {desert_path}")
        print("   Run 'python create_desert_background.py' to create it first")

if __name__ == "__main__":
    print("🏜️ Desert Biome Test 🏜️")
    print("=" * 40)
    test_desert_background()