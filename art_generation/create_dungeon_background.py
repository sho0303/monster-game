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
        # Metal bracket
        draw.rectangle([torch_x - 2, torch_y + 3, torch_x + 2, torch_y + 10], 
                      fill=colors['torch_metal'])
        
        # Wooden handle
        draw.rectangle([torch_x - 1, torch_y, torch_x + 1, torch_y + 12], 
                      fill=colors['torch_wood'])
        
        # Flame (layered)
        # Outer flame
        draw.ellipse([torch_x - 4, torch_y - 7, torch_x + 4, torch_y + 1], 
                    fill=colors['torch_flame'])
        # Inner bright core
        draw.ellipse([torch_x - 2, torch_y - 5, torch_x + 2, torch_y - 1], 
                    fill=colors['torch_flame_core'])
        
        # Glow effect around torch
        for glow_y in range(torch_y - 10, torch_y + 15):
            for glow_x in range(torch_x - 10, torch_x + 10):
                if 0 <= glow_x < base_width and 0 <= glow_y < mid_height:
                    distance = math.sqrt((glow_x - torch_x)**2 + (glow_y - torch_y)**2)
                    if 5 < distance < 10:
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
        for i in range(20):
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
    
    # Draw skeleton on floor (positioned lower-center)
    skeleton_x = base_width // 2 - 10
    skeleton_y = mid_height + 15
    
    # Skull
    skull_x = skeleton_x + 8
    skull_y = skeleton_y
    # Skull oval
    draw.ellipse([skull_x, skull_y, skull_x + 8, skull_y + 8], 
                fill=colors['bone_white'])
    # Eye sockets
    draw.rectangle([skull_x + 2, skull_y + 2, skull_x + 3, skull_y + 3], 
                  fill=colors['bone_dark'])
    draw.rectangle([skull_x + 5, skull_y + 2, skull_x + 6, skull_y + 3], 
                  fill=colors['bone_dark'])
    # Jaw
    draw.rectangle([skull_x + 2, skull_y + 6, skull_x + 6, skull_y + 7], 
                  fill=colors['bone_shadow'])
    
    # Spine/ribcage
    spine_x = skeleton_x + 10
    spine_y = skeleton_y + 9
    # Vertebrae
    for i in range(8):
        draw.point((spine_x, spine_y + i), fill=colors['bone_white'])
        draw.point((spine_x + 1, spine_y + i), fill=colors['bone_white'])
    
    # Ribs (simplified)
    for i in range(3):
        rib_y = spine_y + 2 + i * 2
        # Left ribs
        draw.line([spine_x - 1, rib_y, spine_x - 3, rib_y + 1], 
                 fill=colors['bone_shadow'])
        # Right ribs
        draw.line([spine_x + 2, rib_y, spine_x + 4, rib_y + 1], 
                 fill=colors['bone_shadow'])
    
    # Left arm bones
    arm_y = spine_y + 2
    draw.line([spine_x - 3, arm_y, spine_x - 8, arm_y + 3], 
             fill=colors['bone_white'])
    # Left hand
    draw.point((spine_x - 8, arm_y + 4), fill=colors['bone_shadow'])
    draw.point((spine_x - 9, arm_y + 4), fill=colors['bone_shadow'])
    
    # Right arm bones
    draw.line([spine_x + 4, arm_y, spine_x + 9, arm_y + 3], 
             fill=colors['bone_white'])
    # Right hand
    draw.point((spine_x + 9, arm_y + 4), fill=colors['bone_shadow'])
    draw.point((spine_x + 10, arm_y + 4), fill=colors['bone_shadow'])
    
    # Pelvis
    pelvis_y = spine_y + 8
    draw.rectangle([spine_x - 2, pelvis_y, spine_x + 3, pelvis_y + 2], 
                  fill=colors['bone_white'])
    
    # Left leg bones
    leg_y = pelvis_y + 3
    draw.line([spine_x - 1, leg_y, spine_x - 3, leg_y + 8], 
             fill=colors['bone_white'])
    # Left foot
    draw.rectangle([spine_x - 5, leg_y + 8, spine_x - 3, leg_y + 9], 
                  fill=colors['bone_shadow'])
    
    # Right leg bones
    draw.line([spine_x + 2, leg_y, spine_x + 4, leg_y + 8], 
             fill=colors['bone_white'])
    # Right foot
    draw.rectangle([spine_x + 4, leg_y + 8, spine_x + 6, leg_y + 9], 
                  fill=colors['bone_shadow'])
    
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
    print("- Two flickering wall torches with glow effects")
    print("- Three hanging chains from ceiling")
    print("- Stone tile floor (bottom half)")
    print("- Complete skeleton lying on floor")

if __name__ == "__main__":
    main()