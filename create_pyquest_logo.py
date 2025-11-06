"""
Create a PNG logo for PYQUEST game title
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_pyquest_logo():
    """Create a game-style PYQUEST logo"""
    # Create image with transparent background
    width, height = 800, 300
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw background panel (dark with border)
    margin = 20
    draw.rectangle([margin, margin, width-margin, height-margin], 
                   fill=(26, 26, 26, 240), 
                   outline=(255, 215, 0, 255), 
                   width=5)
    
    # Try to use a bold font, fall back to default if not available
    try:
        # Try different font options
        font_options = [
            ("arial.ttf", 100),
            ("arialbd.ttf", 100),
            ("impact.ttf", 100),
            ("C:\\Windows\\Fonts\\impact.ttf", 100),
            ("C:\\Windows\\Fonts\\arialbd.ttf", 100),
        ]
        
        font = None
        for font_path, size in font_options:
            try:
                font = ImageFont.truetype(font_path, size)
                break
            except:
                continue
        
        if font is None:
            # Use default font as last resort
            font = ImageFont.load_default()
            font_size = 80  # Approximate size for default font
    except:
        font = ImageFont.load_default()
        font_size = 80
    
    # Draw text with shadow effect
    text = "PYQUEST"
    
    # Get text bounding box for centering
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center position
    x = (width - text_width) // 2
    y = (height - text_height) // 2 - 10
    
    # Draw shadow (offset)
    shadow_color = (0, 0, 0, 200)
    draw.text((x+4, y+4), text, font=font, fill=shadow_color)
    
    # Draw outline
    outline_color = (139, 69, 19, 255)  # Saddle brown
    for offset_x in [-2, -1, 0, 1, 2]:
        for offset_y in [-2, -1, 0, 1, 2]:
            if offset_x != 0 or offset_y != 0:
                draw.text((x+offset_x, y+offset_y), text, font=font, fill=outline_color)
    
    # Draw main text with gradient effect (simulate with two layers)
    # Top color (gold)
    top_color = (255, 215, 0, 255)  # Gold
    draw.text((x, y), text, font=font, fill=top_color)
    
    # Add subtitle
    try:
        subtitle_font = ImageFont.truetype("arial.ttf", 30)
    except:
        subtitle_font = ImageFont.load_default()
    
    subtitle = "⚔️  Monster Battle Adventure  ⚔️"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = y + text_height + 30
    
    # Subtitle shadow
    draw.text((subtitle_x+2, subtitle_y+2), subtitle, font=subtitle_font, fill=(0, 0, 0, 200))
    # Subtitle text
    draw.text((subtitle_x, subtitle_y), subtitle, font=subtitle_font, fill=(200, 200, 200, 255))
    
    # Add decorative corners
    corner_size = 30
    corner_color = (255, 215, 0, 255)
    # Top-left
    draw.line([margin+5, margin+5, margin+corner_size, margin+5], fill=corner_color, width=3)
    draw.line([margin+5, margin+5, margin+5, margin+corner_size], fill=corner_color, width=3)
    # Top-right
    draw.line([width-margin-5, margin+5, width-margin-corner_size, margin+5], fill=corner_color, width=3)
    draw.line([width-margin-5, margin+5, width-margin-5, margin+corner_size], fill=corner_color, width=3)
    # Bottom-left
    draw.line([margin+5, height-margin-5, margin+corner_size, height-margin-5], fill=corner_color, width=3)
    draw.line([margin+5, height-margin-5, margin+5, height-margin-corner_size], fill=corner_color, width=3)
    # Bottom-right
    draw.line([width-margin-5, height-margin-5, width-margin-corner_size, height-margin-5], fill=corner_color, width=3)
    draw.line([width-margin-5, height-margin-5, width-margin-5, height-margin-corner_size], fill=corner_color, width=3)
    
    # Save image
    output_path = 'ascii_art/pyquest.png'
    img.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {width}x{height} pixels")
    print(f"   Format: PNG with transparency")

if __name__ == '__main__':
    create_pyquest_logo()
