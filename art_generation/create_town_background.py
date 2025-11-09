#!/usr/bin/env python3
"""
Create pixel art town biome background PNG to match game art style
"""
from PIL import Image
import numpy as np
import random
import math

def create_town_background():
    """Create a pixel art fantasy wooden village landscape"""
    # Create a pixel art canvas (same dimensions as other biomes)
    width = 64
    height = 32
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Town color palette (fantasy wooden village tones)
    # Sky colors - peaceful village sky
    SKY_BLUE = [135, 206, 235, 255]      # Light blue sky
    SKY_LIGHT = [176, 224, 230, 255]     # Lighter blue near horizon
    CLOUD_WHITE = [248, 248, 255, 255]   # White clouds
    CLOUD_GRAY = [192, 192, 192, 255]    # Cloud shading
    
    # Building colors - primarily wooden
    WOOD_BROWN = [139, 69, 19, 255]      # Main wooden walls (dark brown)
    WOOD_LIGHT = [160, 82, 45, 255]      # Light wood planks
    WOOD_MEDIUM = [120, 60, 30, 255]     # Medium wood tone
    WOOD_DARK = [101, 67, 33, 255]       # Dark wood accents
    LOG_BROWN = [83, 53, 10, 255]        # Log cabin wood
    PLASTER_CREAM = [245, 245, 220, 255] # Cream plaster (Tudor style)
    
    # Roof colors - natural materials
    THATCH_BROWN = [205, 133, 63, 255]   # Thatched roofs (main)
    THATCH_DARK = [160, 100, 50, 255]    # Thatch shadows
    THATCH_GOLD = [218, 165, 32, 255]    # Golden thatch
    WOOD_SHINGLE = [139, 90, 43, 255]    # Wooden shingles
    MOSS_GREEN = [107, 142, 35, 255]     # Mossy roof patches
    
    # Village features
    DIRT_BROWN = [160, 82, 45, 255]      # Dirt roads
    DIRT_DARK = [139, 69, 19, 255]       # Dirt shadows/ruts
    GRAVEL_DARK = [105, 105, 105, 255]   # Dark grey gravel
    GRAVEL_MEDIUM = [128, 128, 128, 255] # Medium grey gravel
    GRAVEL_LIGHT = [169, 169, 169, 255]  # Light grey gravel accents
    WELL_STONE = [169, 169, 169, 255]    # Well stones
    WELL_WATER = [0, 191, 255, 255]      # Well water
    
    # Details
    WINDOW_YELLOW = [255, 255, 0, 255]   # Lit windows
    WINDOW_DARK = [139, 69, 19, 255]     # Window frames
    DOOR_BLACK = [0, 0, 0, 255]          # Black doors
    DOOR_BROWN = [101, 67, 33, 255]      # Brown door frames
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
    
    # GROUND LEVEL - dirt roads (bottom 40%)
    ground_start_y = sky_height
    
    # Create base dirt road layer
    for y in range(ground_start_y, height):
        for x in range(width):
            canvas[y, x] = DIRT_BROWN
    
    # Add dirt road texture and wagon ruts
    for y in range(ground_start_y, height):
        for x in range(width):
            if (x + y) % 5 == 0:  # Create dirt texture pattern
                if random.random() < 0.4:
                    canvas[y, x] = DIRT_DARK
            # Add wagon ruts (parallel lines)
            if x == width // 3 or x == (2 * width) // 3:
                if random.random() < 0.6:
                    canvas[y, x] = DIRT_DARK
    
    # Add horizontal main gravel road running through the village
    main_road_y = ground_start_y + 2  # Road positioned 2 pixels below ground start
    road_width = 3  # 3-pixel wide road
    
    for y in range(main_road_y, min(main_road_y + road_width, height)):
        for x in range(width):
            # Create gravel road surface with varied stone colors
            rand_val = random.random()
            if rand_val < 0.5:
                canvas[y, x] = GRAVEL_DARK    # Dark grey gravel (main surface)
            elif rand_val < 0.8:
                canvas[y, x] = GRAVEL_MEDIUM  # Medium grey gravel
            else:
                canvas[y, x] = GRAVEL_LIGHT   # Light grey gravel accents
            
            # Add wheel ruts along the road (slightly darker gravel)
            if x % 8 == 2 or x % 8 == 6:  # Parallel wheel tracks
                if random.random() < 0.7:
                    canvas[y, x] = [85, 85, 85, 255]  # Very dark grey for wheel ruts
    
    # SMALL VILLAGE HOUSES - 3 cozy houses with proper proportions
    building_specs = [
        # x, y, width, height, wall_color, roof_color, roof_type
        (8, ground_start_y - 5, 7, 4, WOOD_BROWN, THATCH_BROWN, 'peak'),       # Left cottage (smaller)
        (25, ground_start_y - 7, 10, 5, LOG_BROWN, THATCH_GOLD, 'peak'),       # Center house (largest)
        (45, ground_start_y - 6, 8, 4, WOOD_LIGHT, THATCH_DARK, 'peak'),       # Right cottage
    ]
    
    # First, add building foundations and shadows
    for bld_x, bld_y, bld_w, bld_h, wall_color, roof_color, roof_type in building_specs:
        # Add wooden foundation logs at ground level
        foundation_y = ground_start_y
        for dx in range(bld_w + 2):  # Foundation extends 1 pixel on each side
            x = bld_x - 1 + dx
            if 0 <= x < width and 0 <= foundation_y < height:
                canvas[foundation_y, x] = WOOD_DARK  # Dark wooden foundation
                # Add foundation depth in dirt
                if foundation_y + 1 < height:
                    canvas[foundation_y + 1, x] = DIRT_DARK
        
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
                    # Add wood plank texture
                    if dx == 0 or dy == actual_height - 1:
                        canvas[y, x] = WOOD_DARK  # Wall edges darker (wood trim)
                    elif y >= building_bottom - 1:
                        canvas[y, x] = WOOD_DARK  # Bottom edge darker (foundation connection)
                    elif wall_color == PLASTER_CREAM:
                        # Tudor-style with wood beams
                        if dx % 3 == 0 or dy % 4 == 0:
                            canvas[y, x] = WOOD_BROWN  # Wood beam pattern
                        else:
                            canvas[y, x] = wall_color  # Plaster fill
                    else:
                        canvas[y, x] = wall_color
        
        # Draw roof
        if roof_type == 'peak':
            # Classic V-shaped triangular roof
            roof_height = 3
            center_x = bld_x + bld_w // 2
            
            for dy in range(roof_height):
                # Create V-shape by drawing from center outward
                width_at_level = dy + 1
                for side_offset in range(width_at_level):
                    y = bld_y - roof_height + dy
                    
                    # Left side of V
                    x_left = center_x - side_offset
                    if 0 <= x_left < width and 0 <= y < height:
                        if side_offset == width_at_level - 1 or dy == 0:
                            canvas[y, x_left] = THATCH_DARK  # V-shape edges darker
                        else:
                            # Add moss patches on some roofs  
                            if roof_color == THATCH_BROWN and random.random() < 0.1:
                                canvas[y, x_left] = MOSS_GREEN
                            else:
                                canvas[y, x_left] = roof_color
                    
                    # Right side of V (avoid double-drawing center pixel)
                    if side_offset > 0:
                        x_right = center_x + side_offset
                        if 0 <= x_right < width and 0 <= y < height:
                            if side_offset == width_at_level - 1 or dy == 0:
                                canvas[y, x_right] = THATCH_DARK  # V-shape edges darker
                            else:
                                # Add moss patches on some roofs
                                if roof_color == THATCH_BROWN and random.random() < 0.1:
                                    canvas[y, x_right] = MOSS_GREEN
                                else:
                                    canvas[y, x_right] = roof_color
        else:  # flat roof (shouldn't happen with wooden buildings, but keep for safety)
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
        
        # Add door (for all buildings since we only have 2)
        if bld_w >= 3:
            door_x = bld_x + bld_w // 2
            door_y = bld_y + bld_h - 3
            if 0 <= door_x < width and 0 <= door_y + 2 < height:
                # Black door with brown frame
                canvas[door_y, door_x] = DOOR_BLACK     # Top of door
                canvas[door_y + 1, door_x] = DOOR_BLACK # Middle of door  
                canvas[door_y + 2, door_x] = DOOR_BLACK # Bottom of door
                
                # Brown door frame
                if door_x - 1 >= 0:
                    canvas[door_y, door_x - 1] = DOOR_BROWN     # Left frame
                    canvas[door_y + 1, door_x - 1] = DOOR_BROWN
                    canvas[door_y + 2, door_x - 1] = DOOR_BROWN
                if door_x + 1 < width:
                    canvas[door_y, door_x + 1] = DOOR_BROWN     # Right frame
                    canvas[door_y + 1, door_x + 1] = DOOR_BROWN
                    canvas[door_y + 2, door_x + 1] = DOOR_BROWN
    
    # VILLAGE WELL - central feature
    well_x, well_y = width // 2 - 2, ground_start_y + 2
    
    # Well base (4x2 pixels) - stone construction
    for dy in range(2):
        for dx in range(4):
            x = well_x + dx
            y = well_y + dy
            if 0 <= x < width and 0 <= y < height:
                if dx == 0 or dx == 3 or dy == 0:
                    canvas[y, x] = WOOD_DARK  # Well edges (wooden frame)
                else:
                    canvas[y, x] = WELL_STONE
    
    # Well water center
    water_x, water_y = well_x + 1, well_y - 1
    if 0 <= water_x + 1 < width and 0 <= water_y < height:
        canvas[water_y, water_x] = WELL_WATER
        canvas[water_y, water_x + 1] = WELL_WATER
    
    # Well roof/covering (simple wooden roof)
    for dx in range(6):
        x = well_x - 1 + dx
        y = well_y - 2
        if 0 <= x < width and 0 <= y < height:
            canvas[y, x] = WOOD_SHINGLE
    
    # Well posts
    post_positions = [well_x - 1, well_x + 4]
    for post_x in post_positions:
        for post_dy in range(3):
            y = well_y - 2 + post_dy
            if 0 <= post_x < width and 0 <= y < height:
                canvas[y, post_x] = WOOD_BROWN
    
    # CHIMNEY SMOKE - add some life to the village houses
    chimney_positions = [
        (19, ground_start_y - 10),  # From left cottage chimney
        (40, ground_start_y - 11),  # From right house chimney
    ]
    
    for smoke_x, smoke_y in chimney_positions:
        # Small wispy smoke trail from cozy houses
        for i in range(4):  # Shorter smoke trails for smaller houses
            x = smoke_x + random.randint(-1, 1)
            y = smoke_y - i
            if 0 <= x < width and 0 <= y < height and random.random() < 0.8:
                canvas[y, x] = SMOKE_GRAY
    
    # VILLAGE DETAILS - market stalls, wooden posts, etc.
    # Simple wooden market stall
    stall_x, stall_y = 4, ground_start_y + 1
    for dx in range(3):
        for dy in range(2):
            x = stall_x + dx
            y = stall_y + dy
            if 0 <= x < width and 0 <= y < height:
                canvas[y, x] = WOOD_LIGHT
    
    # Stall canvas awning (natural colors)
    for dx in range(4):
        x = stall_x - 1 + dx
        y = stall_y - 1
        if 0 <= x < width and 0 <= y < height:
            canvas[y, x] = PLASTER_CREAM  # Canvas awning
    
    # Wooden fence posts / hitching posts
    post_positions = [12, 28, 45]
    for post_x in post_positions:
        post_y = ground_start_y + 1
        if 0 <= post_x < width and 0 <= post_y + 2 < height:
            # Wooden fence post
            canvas[post_y, post_x] = WOOD_DARK
            canvas[post_y + 1, post_x] = WOOD_DARK
            # Lantern hanging from post (rustic lighting)
            if 0 <= post_y - 1 < height:
                canvas[post_y - 1, post_x] = WINDOW_YELLOW
    
    return canvas

def main():
    """Create and save the town background"""
    print("🏘️ Creating pixel art fantasy wooden village background...")
    
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
    output_path = "art/town_background.png"
    town_scaled.save(output_path)
    print(f"✅ Town background saved to: {output_path}")
    
    # Also create a larger version for higher resolution displays
    large_width = final_width * 2
    large_height = final_height * 2
    town_large = town_img.resize((large_width, large_height), Image.Resampling.NEAREST)
    output_path_large = "art/town_background_large.png"
    town_large.save(output_path_large)
    print(f"✅ Large town background saved to: {output_path_large}")
    
    print("🏘️ Small fantasy village background creation complete!")
    print("\n🎨 Cozy village features created:")
    print("   - Peaceful blue sky with fluffy clouds")
    print("   - 3 small wooden houses with varied designs")
    print("   - Classic V-shaped thatched roofs with natural colors")
    print("   - Horizontal main gravel road through village")
    print("   - Vertical dirt paths with wagon ruts")
    print("   - Central village well with wooden cover")
    print("   - Black doors with brown wooden frames")
    print("   - Lit cottage windows and cozy atmosphere")
    print("   - Gentle chimney smoke from hearths")
    print("   - Small market stall and wooden fence posts")
    print("   - Natural village scale and atmosphere")
    print("   - Pixel art style matching other biomes")
    print(f"   - Final size: {final_width}x{final_height} pixels")

if __name__ == "__main__":
    main()