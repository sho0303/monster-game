from PIL import Image, ImageDraw
import random

def create_dungeon_background(width=512, height=256, scale_factor=8):
    """Create a pixel art dungeon background for monster encounters"""
    
    # Create base image at lower resolution for pixel art effect
    base_width = width // scale_factor
    base_height = height // scale_factor
    img = Image.new('RGB', (base_width, base_height), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Dark dungeon color palette
    colors = {
        'wall_dark': (30, 30, 40),           # Very dark stone
        'wall': (45, 45, 55),                # Dark stone wall
        'wall_light': (60, 60, 70),          # Lighter stone
        'floor_dark': (25, 20, 15),          # Dark stone floor
        'floor': (35, 30, 25),               # Stone floor
        'floor_light': (45, 40, 35),         # Lighter floor stones
        'torch_flame': (255, 180, 50),       # Bright torch flame
        'torch_flame_core': (255, 220, 100), # Torch flame center
        'torch_wood': (80, 50, 30),          # Torch handle
        'torch_metal': (60, 60, 60),         # Metal torch bracket
        'shadow': (15, 10, 10),              # Deep shadows
        'moss': (20, 40, 20),                # Dark moss/slime
        'crack': (20, 20, 25),               # Cracks in stone
        'cobweb': (80, 80, 80),              # Spider webs
        'bone': (200, 190, 180),             # Old bones
        'chain': (70, 70, 70),               # Metal chains
        'water_puddle': (30, 35, 45),        # Dark water reflection
        'glow': (100, 80, 50),               # Ambient torch glow
    }
    
    # Fill background with dark wall
    draw.rectangle([0, 0, base_width, base_height], fill=colors['wall_dark'])
    
    # Create stone wall texture with blocks
    block_size = 4
    for y in range(0, base_height - 16, block_size):  # Leave bottom for floor
        for x in range(0, base_width, block_size):
            # Alternate block shades for texture
            if (x // block_size + y // block_size) % 3 == 0:
                block_color = colors['wall_light']
            elif (x // block_size + y // block_size) % 3 == 1:
                block_color = colors['wall']
            else:
                block_color = colors['wall_dark']
            
            draw.rectangle([x, y, x + block_size - 1, y + block_size - 1], fill=block_color)
            
            # Add random cracks and weathering
            if random.random() < 0.15:
                crack_x = x + random.randint(0, block_size - 1)
                crack_y = y + random.randint(0, block_size - 1)
                draw.point((crack_x, crack_y), fill=colors['crack'])
    
    # Create stone floor
    floor_start_y = base_height - 16
    for y in range(floor_start_y, base_height):
        for x in range(0, base_width, 6):
            # Floor stone pattern
            stone_color = colors['floor'] if (x // 6 + y) % 2 == 0 else colors['floor_light']
            draw.rectangle([x, y, x + 5, y], fill=stone_color)
            
            # Add darker mortar lines
            if x % 12 == 0:
                draw.line([x, y, x, y], fill=colors['floor_dark'])
    
    # Add some floor shadows and puddles
    for i in range(5):
        puddle_x = random.randint(5, base_width - 10)
        puddle_y = floor_start_y + random.randint(2, 10)
        puddle_size = random.randint(2, 4)
        draw.ellipse([puddle_x, puddle_y, puddle_x + puddle_size, puddle_y + 2], 
                    fill=colors['water_puddle'])
    
    # Create torches on walls
    torch_positions = [
        (8, 12),   # Left torch
        (base_width - 12, 10),  # Right torch
    ]
    
    for torch_x, torch_y in torch_positions:
        # Torch bracket (metal mounting)
        draw.rectangle([torch_x - 1, torch_y + 2, torch_x + 1, torch_y + 6], fill=colors['torch_metal'])
        
        # Torch handle
        draw.rectangle([torch_x, torch_y, torch_x, torch_y + 8], fill=colors['torch_wood'])
        
        # Torch flame (layered for effect)
        flame_colors = [colors['torch_flame'], colors['torch_flame_core']]
        for i, flame_color in enumerate(flame_colors):
            flame_size = 2 - i
            draw.ellipse([torch_x - flame_size, torch_y - 3, 
                         torch_x + flame_size, torch_y + 1], fill=flame_color)
        
        # Torch glow effect on surrounding walls
        glow_radius = 6
        for gx in range(torch_x - glow_radius, torch_x + glow_radius + 1):
            for gy in range(torch_y - glow_radius, torch_y + glow_radius + 1):
                if (0 <= gx < base_width and 0 <= gy < base_height and 
                    (gx - torch_x) ** 2 + (gy - torch_y) ** 2 <= glow_radius ** 2):
                    # Subtle glow effect
                    if random.random() < 0.3:
                        draw.point((gx, gy), fill=colors['glow'])
    
    # Add atmospheric details
    # Cobwebs in corners
    web_corners = [(2, 3), (base_width - 4, 2), (1, base_height - 20)]
    for web_x, web_y in web_corners:
        # Simple cobweb pattern
        draw.line([web_x, web_y, web_x + 3, web_y + 2], fill=colors['cobweb'])
        draw.line([web_x + 1, web_y, web_x + 2, web_y + 3], fill=colors['cobweb'])
        draw.point((web_x + 2, web_y + 1), fill=colors['cobweb'])
    
    # Hanging chains
    chain_positions = [(base_width // 4, 4), (3 * base_width // 4, 6)]
    for chain_x, chain_y in chain_positions:
        # Vertical chain
        for i in range(8):
            if i % 2 == 0:
                draw.point((chain_x, chain_y + i), fill=colors['chain'])
        # Chain links (simple representation)
        draw.rectangle([chain_x - 1, chain_y, chain_x + 1, chain_y + 1], fill=colors['chain'])
    
    # Scattered bones and debris on floor
    debris_positions = [
        (15, floor_start_y + 5),
        (base_width - 20, floor_start_y + 8),
        (base_width // 2, floor_start_y + 12),
    ]
    
    for debris_x, debris_y in debris_positions:
        # Bone fragments
        draw.line([debris_x, debris_y, debris_x + 3, debris_y], fill=colors['bone'])
        draw.point((debris_x + 1, debris_y - 1), fill=colors['bone'])
        
        # Small rocks/debris
        debris_size = random.randint(1, 2)
        draw.rectangle([debris_x + 5, debris_y + 1, 
                       debris_x + 5 + debris_size, debris_y + 1 + debris_size], 
                      fill=colors['floor_dark'])
    
    # Add moss/slime patches on walls
    moss_patches = [
        (3, 18, 4, 3),
        (base_width - 8, 20, 3, 4),
        (base_width // 2 - 2, 25, 3, 2),
    ]
    
    for moss_x, moss_y, moss_w, moss_h in moss_patches:
        for mx in range(moss_x, moss_x + moss_w):
            for my in range(moss_y, moss_y + moss_h):
                if random.random() < 0.7:  # Irregular moss pattern
                    draw.point((mx, my), fill=colors['moss'])
    
    # Add cracks in walls
    crack_lines = [
        [(10, 8), (12, 15)],
        [(base_width - 15, 5), (base_width - 13, 12)],
        [(base_width // 2, 20), (base_width // 2 + 2, 28)],
    ]
    
    for crack_start, crack_end in crack_lines:
        draw.line([crack_start[0], crack_start[1], crack_end[0], crack_end[1]], 
                 fill=colors['crack'])
        # Add some branching cracks
        mid_x = (crack_start[0] + crack_end[0]) // 2
        mid_y = (crack_start[1] + crack_end[1]) // 2
        draw.line([mid_x, mid_y, mid_x + 1, mid_y + 2], fill=colors['crack'])
    
    # Add depth shadows in corners and edges
    shadow_areas = [
        (0, 0, 3, base_height),  # Left edge shadow
        (base_width - 3, 0, 3, base_height),  # Right edge shadow
        (0, 0, base_width, 3),  # Top shadow
    ]
    
    for shadow_x, shadow_y, shadow_w, shadow_h in shadow_areas:
        for sx in range(shadow_x, min(shadow_x + shadow_w, base_width)):
            for sy in range(shadow_y, min(shadow_y + shadow_h, base_height)):
                if random.random() < 0.4:  # Irregular shadow
                    draw.point((sx, sy), fill=colors['shadow'])
    
    # Scale up the image for final output
    img_scaled = img.resize((width, height), Image.Resampling.NEAREST)
    
    return img_scaled

def main():
    """Create and save the dungeon background"""
    print("Creating dungeon background...")
    
    # Create the background image
    dungeon_bg = create_dungeon_background(512, 256, 8)
    
    # Save the image
    output_path = "../art/dungeon_background.png"
    dungeon_bg.save(output_path)
    print(f"Dungeon background saved to: {output_path}")
    
    # Also create a larger version for high-res displays
    dungeon_bg_large = create_dungeon_background(1024, 512, 8)
    output_path_large = "../art/dungeon_background_large.png"
    dungeon_bg_large.save(output_path_large)
    print(f"Large dungeon background saved to: {output_path_large}")
    
    print("Dungeon background creation complete!")
    print("\nFeatures created:")
    print("- Dark stone block walls with weathering")
    print("- Ancient stone floor with mortar lines")
    print("- Flickering wall torches with glow effects")
    print("- Atmospheric cobwebs and hanging chains")
    print("- Scattered bones and debris")
    print("- Moss/slime patches on damp walls")
    print("- Realistic cracks and damage")
    print("- Dark water puddles")
    print("- Deep shadows for ominous atmosphere")

if __name__ == "__main__":
    main()