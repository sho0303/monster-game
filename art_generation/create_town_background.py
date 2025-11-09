#!/usr/bin/env python3
"""
Create pixel art town biome background PNG to match game art style
"""
from PIL import Image
import numpy as np
import random
import math

def create_town_background():
    """Create a pixel art medieval town landscape"""
    # Create a pixel art canvas (same dimensions as other biomes)
    width = 64
    height = 32
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Town color palette (medieval fantasy tones)
    # Sky colors - peaceful town sky
    SKY_BLUE = [135, 206, 235, 255]      # Light blue sky
    SKY_LIGHT = [176, 224, 230, 255]     # Lighter blue near horizon
    CLOUD_WHITE = [248, 248, 255, 255]   # White clouds
    CLOUD_GRAY = [192, 192, 192, 255]    # Cloud shading
    
    # Building colors
    STONE_GRAY = [128, 128, 128, 255]    # Stone building walls
    STONE_DARK = [105, 105, 105, 255]    # Stone shading
    STONE_LIGHT = [169, 169, 169, 255]   # Stone highlights
    WOOD_BROWN = [139, 69, 19, 255]      # Wooden beams
    WOOD_LIGHT = [160, 82, 45, 255]      # Light wood
    
    # Roof colors
    ROOF_RED = [178, 34, 34, 255]        # Red clay tiles
    ROOF_DARK = [139, 0, 0, 255]         # Roof shadows
    ROOF_BLUE = [70, 130, 180, 255]      # Blue slate roofs
    THATCH_BROWN = [205, 133, 63, 255]   # Thatched roofs
    
    # Town features
    COBBLE_GRAY = [119, 136, 153, 255]   # Cobblestone streets
    COBBLE_DARK = [105, 105, 105, 255]   # Cobblestone shadows
    FOUNTAIN_BLUE = [0, 191, 255, 255]   # Fountain water
    FOUNTAIN_STONE = [169, 169, 169, 255] # Fountain stone
    
    # Details
    WINDOW_YELLOW = [255, 255, 0, 255]   # Lit windows
    WINDOW_DARK = [139, 69, 19, 255]     # Window frames
    DOOR_BROWN = [101, 67, 33, 255]      # Wooden doors
    SMOKE_GRAY = [211, 211, 211, 255]    # Chimney smoke
    
    # SKY GRADIENT (top 60% of image)
    sky_height = int(height * 0.6)  # Sky takes up top 60%
    
    for y in range(sky_height):
        # Create vertical gradient from light blue at top to lighter blue near horizon
        gradient_ratio = y / sky_height
        
        # Blend between sky colors for peaceful town atmosphere
        r = int(SKY_BLUE[0] + (SKY_LIGHT[0] - SKY_BLUE[0]) * gradient_ratio)
        g = int(SKY_BLUE[1] + (SKY_LIGHT[1] - SKY_BLUE[1]) * gradient_ratio)
        b = int(SKY_BLUE[2] + (SKY_LIGHT[2] - SKY_BLUE[2]) * gradient_ratio)
        
        sky_color = [r, g, b, 255]
        
        # Fill the row with sky gradient
        for x in range(width):
            canvas[y, x] = sky_color
    
    # CLOUDS - peaceful town clouds
    cloud_positions = [
        (12, 3, 8, 3),   # x, y, width, height - fluffy cloud
        (38, 5, 6, 2),   # smaller cloud
        (52, 2, 7, 3),   # wispy cloud
    ]
    
    for cloud_x, cloud_y, cloud_w, cloud_h in cloud_positions:
        for dy in range(cloud_h):
            for dx in range(cloud_w):
                x = cloud_x + dx
                y = cloud_y + dy
                if 0 <= x < width and 0 <= y < sky_height:
                    # Create fluffy cloud texture
                    if random.random() < 0.8:  # 80% cloud density
                        if dy == 0 or dx == 0 or dx == cloud_w-1:
                            canvas[y, x] = CLOUD_GRAY  # Cloud edges
                        else:
                            canvas[y, x] = CLOUD_WHITE  # Cloud center
    
    # GROUND LEVEL - cobblestone streets (bottom 40%)
    ground_start_y = sky_height
    
    # Create base cobblestone layer
    for y in range(ground_start_y, height):
        for x in range(width):
            canvas[y, x] = COBBLE_GRAY
    
    # Add cobblestone pattern
    for y in range(ground_start_y, height):
        for x in range(width):
            if (x + y) % 4 == 0:  # Create cobblestone pattern
                if random.random() < 0.3:
                    canvas[y, x] = COBBLE_DARK
    
    # MEDIEVAL BUILDINGS - create a row of pixel art buildings
    building_specs = [
        # x, y, width, height, wall_color, roof_color, roof_type
        (8, ground_start_y - 12, 6, 8, STONE_GRAY, ROOF_RED, 'peak'),
        (16, ground_start_y - 15, 8, 11, WOOD_BROWN, THATCH_BROWN, 'peak'),
        (26, ground_start_y - 10, 5, 6, STONE_LIGHT, ROOF_BLUE, 'flat'),
        (33, ground_start_y - 14, 7, 10, STONE_GRAY, ROOF_RED, 'peak'),
        (42, ground_start_y - 9, 6, 5, WOOD_LIGHT, THATCH_BROWN, 'peak'),
        (50, ground_start_y - 13, 6, 9, STONE_DARK, ROOF_DARK, 'peak'),
    ]
    
    # First, add building foundations and shadows
    for bld_x, bld_y, bld_w, bld_h, wall_color, roof_color, roof_type in building_specs:
        # Add foundation stones at ground level
        foundation_y = ground_start_y
        for dx in range(bld_w + 2):  # Foundation extends 1 pixel on each side
            x = bld_x - 1 + dx
            if 0 <= x < width and 0 <= foundation_y < height:
                canvas[foundation_y, x] = STONE_DARK  # Dark foundation stones
                # Add foundation depth
                if foundation_y + 1 < height:
                    canvas[foundation_y + 1, x] = COBBLE_DARK
        
        # Add shadow to the right and bottom of buildings
        for dy in range(bld_h + 1):
            # Right shadow
            shadow_x = bld_x + bld_w
            shadow_y = bld_y + dy
            if 0 <= shadow_x < width and 0 <= shadow_y < height:
                if canvas[shadow_y, shadow_x][3] > 0:  # Don't overwrite existing content
                    # Darken existing pixels for shadow effect
                    current = canvas[shadow_y, shadow_x]
                    canvas[shadow_y, shadow_x] = [
                        max(0, int(current[0]) - 40),  # Darken red
                        max(0, int(current[1]) - 40),  # Darken green  
                        max(0, int(current[2]) - 40),  # Darken blue
                        current[3]                     # Keep alpha
                    ]
    
    for bld_x, bld_y, bld_w, bld_h, wall_color, roof_color, roof_type in building_specs:
        # Draw building walls - extend to ground level
        building_bottom = ground_start_y
        actual_height = building_bottom - bld_y + 1
        
        for dy in range(actual_height):
            for dx in range(bld_w):
                x = bld_x + dx
                y = bld_y + dy
                if 0 <= x < width and 0 <= y <= building_bottom:
                    # Add some wall texture
                    if dx == 0 or dy == actual_height - 1:
                        canvas[y, x] = STONE_DARK  # Wall edges darker
                    elif y >= building_bottom - 1:
                        canvas[y, x] = STONE_DARK  # Bottom edge darker (foundation connection)
                    else:
                        canvas[y, x] = wall_color
        
        # Draw roof
        if roof_type == 'peak':
            # Triangular roof
            roof_height = 4
            for dy in range(roof_height):
                roof_width = bld_w - dy
                start_x = bld_x + dy // 2
                for dx in range(roof_width):
                    x = start_x + dx
                    y = bld_y - roof_height + dy
                    if 0 <= x < width and 0 <= y < height:
                        if dy == 0 or dx == 0 or dx == roof_width - 1:
                            canvas[y, x] = ROOF_DARK  # Roof edges
                        else:
                            canvas[y, x] = roof_color
        else:  # flat roof
            for dx in range(bld_w):
                x = bld_x + dx
                y = bld_y - 1
                if 0 <= x < width and 0 <= y < height:
                    canvas[y, x] = roof_color
        
        # Add windows (2x2 pixels each)
        if bld_w >= 4 and bld_h >= 6:
            # Window positions
            win_positions = [(bld_x + 1, bld_y + 2), (bld_x + bld_w - 3, bld_y + 2)]
            if bld_h >= 8:  # Add second floor windows
                win_positions.extend([(bld_x + 1, bld_y + bld_h - 4), (bld_x + bld_w - 3, bld_y + bld_h - 4)])
            
            for win_x, win_y in win_positions:
                if 0 <= win_x + 1 < width and 0 <= win_y + 1 < height:
                    # Window frame
                    canvas[win_y, win_x] = WINDOW_DARK
                    canvas[win_y, win_x + 1] = WINDOW_DARK
                    canvas[win_y + 1, win_x] = WINDOW_DARK
                    canvas[win_y + 1, win_x + 1] = WINDOW_DARK
                    
                    # Window light (chance of being lit)
                    if random.random() < 0.6:
                        if 0 <= win_x < width and 0 <= win_y < height:
                            canvas[win_y, win_x] = WINDOW_YELLOW
        
        # Add door (for some buildings)
        if random.random() < 0.7 and bld_w >= 3:
            door_x = bld_x + bld_w // 2
            door_y = bld_y + bld_h - 3
            if 0 <= door_x < width and 0 <= door_y + 2 < height:
                # Simple door
                canvas[door_y, door_x] = DOOR_BROWN
                canvas[door_y + 1, door_x] = DOOR_BROWN
                canvas[door_y + 2, door_x] = DOOR_BROWN
    
    # TOWN FOUNTAIN - central feature
    fountain_x, fountain_y = width // 2 - 2, ground_start_y + 2
    
    # Fountain base (4x2 pixels)
    for dy in range(2):
        for dx in range(4):
            x = fountain_x + dx
            y = fountain_y + dy
            if 0 <= x < width and 0 <= y < height:
                if dx == 0 or dx == 3 or dy == 0:
                    canvas[y, x] = STONE_DARK  # Fountain edges
                else:
                    canvas[y, x] = FOUNTAIN_STONE
    
    # Fountain water center
    water_x, water_y = fountain_x + 1, fountain_y - 1
    if 0 <= water_x + 1 < width and 0 <= water_y < height:
        canvas[water_y, water_x] = FOUNTAIN_BLUE
        canvas[water_y, water_x + 1] = FOUNTAIN_BLUE
    
    # CHIMNEY SMOKE - add some life to the town
    chimney_positions = [
        (18, ground_start_y - 18),  # From tall building
        (35, ground_start_y - 17),  # From another building
        (52, ground_start_y - 16),  # From third building
    ]
    
    for smoke_x, smoke_y in chimney_positions:
        # Wispy smoke trail
        for i in range(6):
            x = smoke_x + random.randint(-1, 1)
            y = smoke_y - i
            if 0 <= x < width and 0 <= y < height and random.random() < 0.7:
                canvas[y, x] = SMOKE_GRAY
    
    # TOWN DETAILS - market stalls, lamp posts, etc.
    # Simple market stall
    stall_x, stall_y = 4, ground_start_y + 1
    for dx in range(3):
        for dy in range(2):
            x = stall_x + dx
            y = stall_y + dy
            if 0 <= x < width and 0 <= y < height:
                canvas[y, x] = WOOD_LIGHT
    
    # Stall awning
    for dx in range(4):
        x = stall_x - 1 + dx
        y = stall_y - 1
        if 0 <= x < width and 0 <= y < height:
            canvas[y, x] = ROOF_RED
    
    # Lamp posts
    lamp_positions = [12, 28, 45]
    for lamp_x in lamp_positions:
        lamp_y = ground_start_y + 1
        if 0 <= lamp_x < width and 0 <= lamp_y + 2 < height:
            # Lamp post
            canvas[lamp_y, lamp_x] = STONE_DARK
            canvas[lamp_y + 1, lamp_x] = STONE_DARK
            # Lamp light
            if 0 <= lamp_y - 1 < height:
                canvas[lamp_y - 1, lamp_x] = WINDOW_YELLOW
    
    return canvas

def main():
    """Create and save the town background"""
    print("🏘️ Creating pixel art town biome background...")
    
    # Create the town landscape
    town_data = create_town_background()
    
    # Convert to PIL Image
    town_img = Image.fromarray(town_data, 'RGBA')
    
    # Scale up for final output (8x scaling for pixel art effect)
    scale_factor = 8
    final_width = town_data.shape[1] * scale_factor
    final_height = town_data.shape[0] * scale_factor
    
    # Use NEAREST neighbor to maintain crisp pixel art edges
    town_scaled = town_img.resize((final_width, final_height), Image.Resampling.NEAREST)
    
    # Save the town background
    output_path = "../art/town_background.png"
    town_scaled.save(output_path)
    print(f"✅ Town background saved to: {output_path}")
    
    # Also create a larger version for higher resolution displays
    large_width = final_width * 2
    large_height = final_height * 2
    town_large = town_img.resize((large_width, large_height), Image.Resampling.NEAREST)
    output_path_large = "../art/town_background_large.png"
    town_large.save(output_path_large)
    print(f"✅ Large town background saved to: {output_path_large}")
    
    print("🏘️ Town biome background creation complete!")
    print("\n🎨 Town features created:")
    print("   - Peaceful blue sky with fluffy clouds")
    print("   - Medieval buildings with varied architecture")
    print("   - Cobblestone streets with texture")
    print("   - Central town fountain")
    print("   - Lit windows and wooden doors")
    print("   - Chimney smoke for atmosphere")
    print("   - Market stalls and lamp posts")
    print("   - Pixel art style matching other biomes")
    print(f"   - Final size: {final_width}x{final_height} pixels")

if __name__ == "__main__":
    main()