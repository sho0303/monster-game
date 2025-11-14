from PIL import Image, ImageDraw
import random
import math

def create_dungeon_background(width=512, height=256, scale_factor=4):
    """Create a pixel art dungeon background with walls on top and stone floor on bottom"""
    
    # Create base image at lower resolution for pixel art effect
    base_width = width // scale_factor
    base_height = height // scale_factor
    img = Image.new('RGB', (base_width, base_height), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Dungeon color palette
    colors = {
        # Wall colors
        'wall_dark': (35, 35, 45),           # Dark stone wall
        'wall_medium': (50, 50, 60),         # Medium stone
        'wall_light': (65, 65, 75),          # Light stone highlights
        'wall_mortar': (25, 25, 30),         # Mortar between stones
        
        # Floor colors
        'floor_dark': (40, 35, 30),          # Dark floor stone
        'floor_medium': (55, 50, 45),        # Medium floor stone
        'floor_light': (70, 65, 60),         # Light floor stone
        'floor_mortar': (30, 25, 20),        # Floor mortar
        
        # Torch colors
        'torch_flame': (255, 180, 50),       # Bright orange flame
        'torch_flame_core': (255, 220, 100), # Yellow flame center
        'torch_glow': (200, 140, 60),        # Ambient glow
        'torch_wood': (70, 45, 25),          # Wooden handle
        'torch_metal': (80, 80, 85),         # Metal bracket
        
        # Chain colors
        'chain_dark': (60, 60, 65),          # Dark chain metal
        'chain_light': (85, 85, 90),         # Light chain highlights
        
        # Skeleton colors
        'bone_white': (220, 215, 205),       # Bone white
        'bone_shadow': (180, 175, 165),      # Bone shadows
        'bone_dark': (140, 135, 125),        # Dark bone crevices
    }
    
    
    # Split canvas: top half = walls, bottom half = floor
    mid_height = base_height // 2
    
    # ===== DRAW TOP HALF - DUNGEON WALLS =====
    
    # Draw stone block walls
    for y in range(0, mid_height):
        for x in range(0, base_width):
            # Create stone block pattern (8x8 blocks)
            block_x = x // 8
            block_y = y // 8
            
            # Mortar lines between blocks
            if x % 8 == 0 or y % 8 == 0:
                draw.point((x, y), fill=colors['wall_mortar'])
            else:
                # Vary stone color for texture
                offset = (block_x * 3 + block_y * 7) % 5
                if offset == 0:
                    draw.point((x, y), fill=colors['wall_light'])
                elif offset < 3:
                    draw.point((x, y), fill=colors['wall_medium'])
                else:
                    draw.point((x, y), fill=colors['wall_dark'])
    
    # Draw wall torches (2 torches)
    torch_positions = [
        (25, 15),  # Left torch
        (base_width - 25, 15),  # Right torch
    ]
    
    for torch_x, torch_y in torch_positions:
        # Metal bracket (smaller)
        draw.rectangle([torch_x - 1, torch_y + 2, torch_x + 1, torch_y + 6], 
                      fill=colors['torch_metal'])
        
        # Wooden handle (shorter)
        draw.rectangle([torch_x, torch_y, torch_x, torch_y + 8], 
                      fill=colors['torch_wood'])
        
        # Flame (smaller, layered)
        # Outer flame
        draw.ellipse([torch_x - 3, torch_y - 5, torch_x + 3, torch_y], 
                    fill=colors['torch_flame'])
        # Inner bright core
        draw.ellipse([torch_x - 1, torch_y - 3, torch_x + 1, torch_y - 1], 
                    fill=colors['torch_flame_core'])
        
        # Glow effect around torch (smaller radius)
        for glow_y in range(torch_y - 7, torch_y + 10):
            for glow_x in range(torch_x - 7, torch_x + 7):
                if 0 <= glow_x < base_width and 0 <= glow_y < mid_height:
                    distance = math.sqrt((glow_x - torch_x)**2 + (glow_y - torch_y)**2)
                    if 4 < distance < 7:
                        if random.random() < 0.15:
                            draw.point((glow_x, glow_y), fill=colors['torch_glow'])
    
    # Draw hanging chains (3 chains)
    chain_positions = [
        (base_width // 4, 5),
        (base_width // 2, 3),
        (3 * base_width // 4, 6),
    ]
    
    for chain_x, chain_y in chain_positions:
        # Chain links going down
        chain_length = 24
        for i in range(chain_length):
            y_pos = chain_y + i
            if y_pos < mid_height:
                # Alternate dark and light for link effect
                if i % 3 == 0:
                    draw.point((chain_x, y_pos), fill=colors['chain_light'])
                    draw.point((chain_x + 1, y_pos), fill=colors['chain_light'])
                else:
                    draw.point((chain_x, y_pos), fill=colors['chain_dark'])
                    draw.point((chain_x + 1, y_pos), fill=colors['chain_dark'])
        
        # Chain anchor at top
        draw.rectangle([chain_x - 1, chain_y - 1, chain_x + 2, chain_y + 1], 
                      fill=colors['chain_light'])
        
        # Wrist shackle at bottom of chain
        shackle_y = chain_y + chain_length
        if shackle_y < mid_height:
            # Shackle metal ring
            draw.ellipse([chain_x - 3, shackle_y, chain_x + 4, shackle_y + 5], 
                        fill=colors['chain_dark'])
            # Inner opening (hollow center)
            draw.ellipse([chain_x - 1, shackle_y + 1, chain_x + 2, shackle_y + 3], 
                        fill=colors['wall_dark'])
            # Shackle highlight
            draw.point((chain_x - 2, shackle_y + 1), fill=colors['chain_light'])
            draw.point((chain_x + 3, shackle_y + 1), fill=colors['chain_light'])
    
    # ===== DRAW BOTTOM HALF - STONE FLOOR =====
    
    # Draw stone floor tiles
    for y in range(mid_height, base_height):
        for x in range(0, base_width):
            # Create larger floor tile pattern (12x6 tiles)
            tile_x = x // 12
            tile_y = (y - mid_height) // 6
            
            # Mortar lines
            if x % 12 == 0 or (y - mid_height) % 6 == 0:
                draw.point((x, y), fill=colors['floor_mortar'])
            else:
                # Vary floor stone color
                offset = (tile_x * 5 + tile_y * 3) % 5
                if offset == 0:
                    draw.point((x, y), fill=colors['floor_light'])
                elif offset < 3:
                    draw.point((x, y), fill=colors['floor_medium'])
                else:
                    draw.point((x, y), fill=colors['floor_dark'])
    
    # Scale up the image for final output
    img_scaled = img.resize((width, height), Image.Resampling.NEAREST)
    
    return img_scaled

def main():
    """Create and save the dungeon background"""
    print("Creating dungeon background...")
    
    # Create the background image (scale factor 4 for doubled base resolution)
    dungeon_bg = create_dungeon_background(512, 256, 4)
    
    # Save the image
    output_path = "../art/dungeon_background.png"
    dungeon_bg.save(output_path)
    print(f"Dungeon background saved to: {output_path}")
    
    # Also create a larger version for high-res displays
    dungeon_bg_large = create_dungeon_background(1024, 512, 4)
    output_path_large = "../art/dungeon_background_large.png"
    dungeon_bg_large.save(output_path_large)
    print(f"Large dungeon background saved to: {output_path_large}")
    
    print("Dungeon background creation complete!")
    print("\nFeatures created:")
    print("- Stone block dungeon walls (top half)")
    print("- Two smaller flickering wall torches with glow effects")
    print("- Three hanging chains with wrist shackles")
    print("- Stone tile floor (bottom half)")

if __name__ == "__main__":
    main()