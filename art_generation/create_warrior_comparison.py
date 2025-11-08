"""
Create a comparison image showing both warrior art versions
"""
from PIL import Image
import os

def create_warrior_comparison():
    """Create side-by-side comparison of original vs realistic warrior"""
    
    # Load both images
    original_path = 'art/Warrior.png'
    realistic_path = 'art/Warrior_realistic.png'
    
    if not os.path.exists(original_path):
        print(f"❌ Original warrior not found at {original_path}")
        print("   Creating original warrior first...")
        import sys
        sys.path.append('art_generation')
        from create_warrior_art import create_warrior
        create_warrior()
    
    if not os.path.exists(realistic_path):
        print(f"❌ Realistic warrior not found at {realistic_path}")
        return
    
    # Load images
    original_img = Image.open(original_path).convert('RGBA')
    realistic_img = Image.open(realistic_path).convert('RGBA')
    
    # Ensure both images are the same size
    size = (256, 256)
    original_img = original_img.resize(size, Image.NEAREST)  # Pixel art should use nearest
    realistic_img = realistic_img.resize(size, Image.LANCZOS)  # Realistic can use smooth scaling
    
    # Create comparison canvas
    comparison_width = size[0] * 2 + 60  # Space between images
    comparison_height = size[1] + 80     # Space for labels
    
    comparison_img = Image.new('RGBA', (comparison_width, comparison_height), (50, 50, 50, 255))
    
    # Paste images side by side
    comparison_img.paste(original_img, (20, 50), original_img)
    comparison_img.paste(realistic_img, (size[0] + 40, 50), realistic_img)
    
    # Add labels (we'll create simple text by drawing rectangles)
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(comparison_img)
    
    try:
        # Try to use a system font
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Draw labels
    draw.text((20 + size[0]//2 - 50, 20), "Original Pixel Art", fill=(255, 255, 255, 255), font=font)
    draw.text((size[0] + 40 + size[0]//2 - 60, 20), "High-Res Realistic", fill=(255, 255, 255, 255), font=font)
    
    # Draw comparison info
    draw.text((20, comparison_height - 25), "32x32 → 256x256 (8x scale)", fill=(200, 200, 200, 255), font=font)
    draw.text((size[0] + 40, comparison_height - 25), "256x256 native resolution", fill=(200, 200, 200, 255), font=font)
    
    # Save comparison
    output_path = 'art/warrior_comparison.png'
    comparison_img.save(output_path, 'PNG')
    
    print(f"✅ Created {output_path}")
    print(f"   Shows: Original warrior (left) vs High-resolution realistic (right)")
    print(f"   Size: {comparison_width}x{comparison_height} pixels")
    print(f"   ")
    print(f"📊 Comparison Details:")
    print(f"   Original: Pixel art style, 32x32 scaled to 256x256")
    print(f"   Realistic: Native 256x256 with gradient shading and detail")
    print(f"   Both: Same overall design - brown hair, red tunic, blue pants")
    print(f"   Enhanced: Detailed armor, realistic sword/shield, battle effects")
    print(f"   Maintains: Same character proportions and pose")

if __name__ == '__main__':
    create_warrior_comparison()