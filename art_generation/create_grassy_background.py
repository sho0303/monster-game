"""
Create a pixel art grassy plain with sky background PNG
"""
from PIL import Image, ImageDraw
import numpy as np
import random

def create_grassy_background():
    """Create a pixel art grassy plain with sky background"""
    # Create a wider canvas for background use (landscape format)
    # Doubled resolution: 128x64 (from 64x32) for more detail
    width = 128
    height = 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette (matching the game's pixel art style)
    # Sky colors
    SKY_BLUE = [135, 206, 235, 255]      # Light blue sky
    LIGHT_SKY = [176, 224, 230, 255]     # Lighter sky near horizon
    CLOUD_WHITE = [248, 248, 255, 255]   # White clouds
    CLOUD_GRAY = [220, 220, 220, 255]    # Cloud shading
    
    # Grass colors
    GRASS_GREEN = [34, 139, 34, 255]     # Main grass color
    DARK_GRASS = [0, 100, 0, 255]        # Grass shading
    LIGHT_GRASS = [124, 252, 0, 255]     # Grass highlights
    YELLOW_GRASS = [154, 205, 50, 255]   # Dried grass patches
    
    # Ground/soil colors
    DIRT_BROWN = [139, 69, 19, 255]      # Soil showing through
    LIGHT_BROWN = [160, 82, 45, 255]     # Lighter soil
    
    # Nature details - Enhanced flower colors
    FLOWER_RED = [220, 20, 60, 255]      # Red flower petals
    FLOWER_RED_DARK = [160, 10, 40, 255] # Red flower shadow
    FLOWER_YELLOW = [255, 215, 0, 255]   # Yellow dandelion
    FLOWER_YELLOW_CENTER = [200, 150, 0, 255]  # Dandelion center
    FLOWER_WHITE = [255, 255, 255, 255]  # White flower petals
    FLOWER_WHITE_SHADOW = [220, 220, 220, 255]  # White flower shadow
    FLOWER_PINK = [255, 182, 193, 255]   # Pink wildflower
    FLOWER_BLUE = [100, 149, 237, 255]   # Blue wildflower
    FLOWER_STEM = [0, 128, 0, 255]       # Flower stem/leaves
    
    # SKY GRADIENT (top 60% of image)
    sky_height = int(height * 0.6)  # Sky takes up top 60%
    
    for y in range(sky_height):
        # Create vertical gradient from darker blue at top to lighter near horizon
        gradient_ratio = y / sky_height
        
        # Blend between sky colors
        r = int(SKY_BLUE[0] + (LIGHT_SKY[0] - SKY_BLUE[0]) * gradient_ratio)
        g = int(SKY_BLUE[1] + (LIGHT_SKY[1] - SKY_BLUE[1]) * gradient_ratio)
        b = int(SKY_BLUE[2] + (LIGHT_SKY[2] - SKY_BLUE[2]) * gradient_ratio)
        
        sky_color = [r, g, b, 255]
        
        for x in range(width):
            canvas[y][x] = sky_color
    
    # CLOUDS (larger, more complex clouds with better shapes)
    # Cloud 1 (large left cloud)
    cloud_1 = [
        # Top layer
        (4, 12), (4, 13), (4, 14), (4, 15), (4, 16),
        (5, 10), (5, 11), (5, 12), (5, 13), (5, 14), (5, 15), (5, 16), (5, 17), (5, 18),
        (6, 9), (6, 10), (6, 11), (6, 12), (6, 13), (6, 14), (6, 15), (6, 16), (6, 17), (6, 18), (6, 19),
        (7, 10), (7, 11), (7, 12), (7, 13), (7, 14), (7, 15), (7, 16), (7, 17), (7, 18),
        (8, 11), (8, 12), (8, 13), (8, 14), (8, 15), (8, 16), (8, 17),
        # Puff on left
        (5, 8), (5, 9),
        (6, 7), (6, 8),
        (7, 8), (7, 9),
        # Puff on right
        (5, 19), (5, 20),
        (6, 20), (6, 21),
        (7, 19), (7, 20),
    ]
    
    # Cloud 2 (medium center cloud)
    cloud_2 = [
        (6, 55), (6, 56), (6, 57), (6, 58),
        (7, 54), (7, 55), (7, 56), (7, 57), (7, 58), (7, 59), (7, 60),
        (8, 53), (8, 54), (8, 55), (8, 56), (8, 57), (8, 58), (8, 59), (8, 60), (8, 61),
        (9, 54), (9, 55), (9, 56), (9, 57), (9, 58), (9, 59), (9, 60),
        (10, 55), (10, 56), (10, 57), (10, 58), (10, 59),
        # Small puff
        (7, 61), (7, 62),
        (8, 62), (8, 63),
    ]
    
    # Cloud 3 (medium-large right cloud)
    cloud_3 = [
        (3, 100), (3, 101), (3, 102), (3, 103),
        (4, 98), (4, 99), (4, 100), (4, 101), (4, 102), (4, 103), (4, 104), (4, 105),
        (5, 97), (5, 98), (5, 99), (5, 100), (5, 101), (5, 102), (5, 103), (5, 104), (5, 105), (5, 106),
        (6, 98), (6, 99), (6, 100), (6, 101), (6, 102), (6, 103), (6, 104), (6, 105),
        (7, 99), (7, 100), (7, 101), (7, 102), (7, 103), (7, 104),
        # Puff on left
        (4, 96), (4, 97),
        (5, 95), (5, 96),
    ]
    
    # Cloud 4 (small cloud)
    cloud_4 = [
        (10, 28), (10, 29), (10, 30),
        (11, 27), (11, 28), (11, 29), (11, 30), (11, 31),
        (12, 28), (12, 29), (12, 30),
    ]
    
    all_clouds = [cloud_1, cloud_2, cloud_3, cloud_4]
    
    for cloud in all_clouds:
        for cloud_y, cloud_x in cloud:
            if 0 <= cloud_y < height and 0 <= cloud_x < width:
                canvas[cloud_y][cloud_x] = CLOUD_WHITE
    
    # Cloud shading (bottom and right edges for depth)
    cloud_shadows = [
        # Cloud 1 shadows
        (8, 12), (8, 13), (8, 14), (8, 15), (8, 16),
        (7, 18), (7, 19),
        (6, 19),
        # Cloud 2 shadows
        (10, 56), (10, 57), (10, 58), (10, 59),
        (9, 60),
        (8, 61),
        # Cloud 3 shadows
        (7, 100), (7, 101), (7, 102), (7, 103), (7, 104),
        (6, 105),
        (5, 106),
        # Cloud 4 shadows
        (12, 29), (12, 30),
        (11, 31),
    ]
    
    for shadow_y, shadow_x in cloud_shadows:
        if 0 <= shadow_y < height and 0 <= shadow_x < width:
            canvas[shadow_y][shadow_x] = CLOUD_GRAY
    
    # HORIZON LINE (transition area)
    horizon_y = sky_height
    
    # GRASS FIELD (bottom 40% of image)
    grass_start_y = sky_height
    
    # Base grass layer
    for y in range(grass_start_y, height):
        for x in range(width):
            # Add some randomness to grass color
            rand = random.random()
            if rand < 0.1:  # 10% chance of dirt showing through
                canvas[y][x] = DIRT_BROWN
            elif rand < 0.2:  # 10% chance of yellow/dried grass
                canvas[y][x] = YELLOW_GRASS
            elif rand < 0.3:  # 10% chance of dark grass
                canvas[y][x] = DARK_GRASS
            else:  # 70% main grass color
                canvas[y][x] = GRASS_GREEN
    
    # GRASS TEXTURE (individual grass blades/tufts)
    # Vertical grass lines for texture
    for x in range(0, width, 3):  # Every 3 pixels
        grass_height = random.randint(2, 5)
        start_y = height - grass_height
        
        for y in range(start_y, height):
            if 0 <= y < height:
                # Alternate between different grass shades
                if (x // 3) % 2 == 0:
                    canvas[y][x] = LIGHT_GRASS
                else:
                    canvas[y][x] = GRASS_GREEN
    
    # SCATTERED DETAILS
    # FLOWERS (detailed multi-pixel flowers with petals and centers)
    
    def draw_flower(canvas, center_y, center_x, flower_type):
        """Draw a detailed flower with petals, center, and stem"""
        if flower_type == 'red':
            petal_color = FLOWER_RED
            petal_shadow = FLOWER_RED_DARK
            center_color = FLOWER_YELLOW_CENTER
        elif flower_type == 'yellow':
            petal_color = FLOWER_YELLOW
            petal_shadow = FLOWER_YELLOW  # Yellow doesn't need dark shadow
            center_color = FLOWER_YELLOW_CENTER
        elif flower_type == 'white':
            petal_color = FLOWER_WHITE
            petal_shadow = FLOWER_WHITE_SHADOW
            center_color = FLOWER_YELLOW_CENTER
        elif flower_type == 'pink':
            petal_color = FLOWER_PINK
            petal_shadow = FLOWER_RED_DARK
            center_color = FLOWER_YELLOW_CENTER
        elif flower_type == 'blue':
            petal_color = FLOWER_BLUE
            petal_shadow = FLOWER_BLUE  # Blue doesn't need dark shadow
            center_color = FLOWER_YELLOW_CENTER
        else:
            return
        
        # Draw stem (2-3 pixels below flower)
        for i in range(1, 4):
            stem_y = center_y + i
            if 0 <= stem_y < height and 0 <= center_x < width:
                canvas[stem_y][center_x] = FLOWER_STEM
        
        # Draw flower center
        if 0 <= center_y < height and 0 <= center_x < width:
            canvas[center_y][center_x] = center_color
        
        # Draw petals (4-petal pattern around center)
        petals = [
            (center_y - 1, center_x, petal_color),      # Top petal
            (center_y, center_x - 1, petal_color),      # Left petal
            (center_y, center_x + 1, petal_color),      # Right petal
            (center_y + 1, center_x, petal_shadow),     # Bottom petal (shadowed)
        ]
        
        # Add corner petals for larger flowers (red, pink, white have 6 petals)
        if flower_type in ['red', 'pink', 'white']:
            petals.extend([
                (center_y - 1, center_x - 1, petal_color),  # Top-left
                (center_y - 1, center_x + 1, petal_color),  # Top-right
            ])
        
        for petal_y, petal_x, color in petals:
            if 0 <= petal_y < height and 0 <= petal_x < width:
                canvas[petal_y][petal_x] = color
    
    # Define flower center positions (y, x, type)
    flower_positions = [
        (grass_start_y + 3, 12, 'red'),      # Red flower left
        (grass_start_y + 5, 28, 'yellow'),   # Yellow flower
        (grass_start_y + 2, 45, 'white'),    # White flower center
        (grass_start_y + 6, 8, 'yellow'),    # Yellow flower far left
        (grass_start_y + 4, 38, 'pink'),     # Pink flower
        (grass_start_y + 7, 55, 'blue'),     # Blue flower right
        (grass_start_y + 3, 75, 'white'),    # White flower far right
        (grass_start_y + 5, 95, 'red'),      # Red flower far right
        (grass_start_y + 6, 110, 'pink'),    # Pink flower edge
    ]
    
    # Draw all flowers
    for flower_y, flower_x, flower_type in flower_positions:
        draw_flower(canvas, flower_y, flower_x, flower_type)
    
    # Grass highlights (sun catching grass tips)
    highlight_positions = [
        (grass_start_y + 1, 5), (grass_start_y + 1, 15), (grass_start_y + 1, 25),
        (grass_start_y + 1, 35), (grass_start_y + 1, 45), (grass_start_y + 1, 55),
        (grass_start_y + 2, 10), (grass_start_y + 2, 20), (grass_start_y + 2, 30),
        (grass_start_y + 2, 40), (grass_start_y + 2, 50), (grass_start_y + 2, 60),
    ]
    
    for hl_y, hl_x in highlight_positions:
        if 0 <= hl_y < height and 0 <= hl_x < width:
            canvas[hl_y][hl_x] = LIGHT_GRASS
    
    # Dirt patches (worn areas in grass)
    dirt_patches = [
        [(grass_start_y + 5, 18), (grass_start_y + 5, 19), (grass_start_y + 6, 18)],
        [(grass_start_y + 4, 42), (grass_start_y + 5, 41), (grass_start_y + 5, 42)],
    ]
    
    for patch in dirt_patches:
        for dirt_y, dirt_x in patch:
            if 0 <= dirt_y < height and 0 <= dirt_x < width:
                canvas[dirt_y][dirt_x] = LIGHT_BROWN
    
    # DEPTH ILLUSION
    # Make grass in back (near horizon) slightly darker/smaller
    for y in range(grass_start_y, grass_start_y + 3):
        for x in range(width):
            if canvas[y][x][1] > 100:  # If it's a green pixel
                # Darken it slightly for depth
                canvas[y][x] = DARK_GRASS
    
    # Convert numpy array to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 4x with nearest neighbor (pixel perfect)
    # 128x64 base * 4 = 512x256 final size
    scale = 4
    img_scaled = img.resize((width * scale, height * scale), Image.NEAREST)
    
    # Save
    output_path = '../art/grassy_background.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {width * scale}x{height * scale} pixels")
    print(f"   Style: Pixel art grassy plain with sky background")
    print(f"   Features: Blue sky gradient, white clouds, green grass field")
    print(f"   Details: Grass texture, scattered flowers, dirt patches")
    print(f"   Atmosphere: Peaceful outdoor adventure setting")
    print(f"   Usage: Perfect for game interface background")

if __name__ == '__main__':
    # Seed random for consistent but varied results
    random.seed(42)
    create_grassy_background()