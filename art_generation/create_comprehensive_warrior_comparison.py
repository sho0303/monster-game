"""
Create a comprehensive comparison image showing all warrior art versions
Original vs 256x256 realistic vs 128x128 realistic
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_comprehensive_warrior_comparison():
    """Create side-by-side comparison of all warrior art versions"""
    
    # Define paths
    original_path = 'art/Warrior.png'
    realistic_256_path = 'art/Warrior_realistic.png'
    realistic_128_path = 'art/Warrior_realistic_128.png'
    
    # Check if all files exist
    files_status = {}
    for name, path in [("Original", original_path), ("256x256 Realistic", realistic_256_path), ("128x128 Realistic", realistic_128_path)]:
        files_status[name] = os.path.exists(path)
        print(f"{name}: {'✅' if files_status[name] else '❌'} {path}")
    
    if not files_status["128x128 Realistic"]:
        print("❌ 128x128 realistic warrior not found!")
        return
    
    # Load images and ensure consistent display size
    display_size = (160, 160)  # Consistent display size for comparison
    images = {}
    
    if files_status["Original"]:
        images["Original"] = Image.open(original_path).convert('RGBA').resize(display_size, Image.NEAREST)
    
    if files_status["256x256 Realistic"]:
        images["256x256 Realistic"] = Image.open(realistic_256_path).convert('RGBA').resize(display_size, Image.LANCZOS)
    
    if files_status["128x128 Realistic"]:
        images["128x128 Realistic"] = Image.open(realistic_128_path).convert('RGBA').resize(display_size, Image.LANCZOS)
    
    # Create comprehensive comparison canvas
    num_images = len(images)
    spacing = 20
    label_height = 60
    
    comparison_width = num_images * display_size[0] + (num_images + 1) * spacing
    comparison_height = display_size[1] + label_height * 2
    
    comparison_img = Image.new('RGBA', (comparison_width, comparison_height), (40, 40, 40, 255))
    draw = ImageDraw.Draw(comparison_img)
    
    try:
        # Try to use a system font
        title_font = ImageFont.truetype("arial.ttf", 14)
        detail_font = ImageFont.truetype("arial.ttf", 10)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        detail_font = ImageFont.load_default()
    
    # Place images and labels
    x_offset = spacing
    for i, (name, img) in enumerate(images.items()):
        # Paste image
        comparison_img.paste(img, (x_offset, label_height), img)
        
        # Draw title
        title_x = x_offset + display_size[0] // 2 - len(name) * 4
        draw.text((title_x, 20), name, fill=(255, 255, 255, 255), font=title_font)
        
        # Draw details
        if name == "Original":
            details = ["32x32 → 160x160", "Pixel Art Style", "Sharp Pixels"]
        elif name == "256x256 Realistic":
            details = ["Native 256x256", "Photorealistic", "High Detail"]
        elif name == "128x128 Realistic":
            details = ["Native 128x128", "Photorealistic", "Optimized Detail"]
        else:
            details = ["Unknown", "", ""]
        
        detail_y = display_size[1] + label_height + 5
        for j, detail in enumerate(details):
            detail_x = x_offset + display_size[0] // 2 - len(detail) * 3
            draw.text((detail_x, detail_y + j * 12), detail, fill=(200, 200, 200, 255), font=detail_font)
        
        x_offset += display_size[0] + spacing
    
    # Add comparison title
    title = "Warrior Art Comparison - All Versions"
    title_x = comparison_width // 2 - len(title) * 6
    draw.text((title_x, 5), title, fill=(255, 215, 0, 255), font=title_font)
    
    # Save comprehensive comparison
    output_path = 'art/warrior_comprehensive_comparison.png'
    comparison_img.save(output_path, 'PNG')
    
    print(f"✅ Created {output_path}")
    print(f"   Shows: All available warrior art versions")
    print(f"   Size: {comparison_width}x{comparison_height} pixels")
    print(f"   ")
    print(f"📊 Version Comparison:")
    print(f"   Original: 32x32 pixel art scaled up")
    print(f"   256x256: High-resolution photorealistic")  
    print(f"   128x128: Optimized photorealistic (smaller file)")
    print(f"   ")
    print(f"💡 Usage Recommendations:")
    print(f"   • Original: Retro/pixel art aesthetic")
    print(f"   • 256x256: Maximum visual quality")
    print(f"   • 128x128: Balance of quality and performance")

if __name__ == '__main__':
    create_comprehensive_warrior_comparison()