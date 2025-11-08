"""
Create a pixel art grassy plain with sky background PNG
"""
from PIL import Image, ImageDraw
import numpy as np
import random

def create_grassy_background():
    """Create a pixel art grassy plain with sky background"""
    # Create a wider canvas for background use (landscape format)
    width = 64
    height = 32
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
    
    # Nature details
    FLOWER_RED = [255, 69, 0, 255]       # Wild flowers
    FLOWER_YELLOW = [255, 255, 0, 255]   # Dandelions
    FLOWER_WHITE = [255, 255, 255, 255]  # Small white flowers
    
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
    
    # CLOUDS (scattered across sky)
    cloud_positions = [
        # Cloud 1 (left side)
        [(3, 8), (3, 9), (3, 10), (3, 11),
         (4, 7), (4, 8), (4, 9), (4, 10), (4, 11), (4, 12),
         (5, 8), (5, 9), (5, 10), (5, 11)],
        
        # Cloud 2 (center-right)
        [(5, 35), (5, 36), (5, 37),
         (6, 34), (6, 35), (6, 36), (6, 37), (6, 38),
         (7, 35), (7, 36), (7, 37)],
        
        # Cloud 3 (far right)
        [(2, 50), (2, 51), (2, 52),
         (3, 49), (3, 50), (3, 51), (3, 52), (3, 53),
         (4, 50), (4, 51), (4, 52)],
    ]
    
    for cloud in cloud_positions:
        for cloud_y, cloud_x in cloud:
            if 0 <= cloud_y < height and 0 <= cloud_x < width:
                canvas[cloud_y][cloud_x] = CLOUD_WHITE
    
    # Cloud shading (bottom edges)
    cloud_shadow_positions = [
        (5, 9), (5, 10),  # Cloud 1
        (7, 35), (7, 36),  # Cloud 2
        (4, 51), (4, 52),  # Cloud 3
    ]
    
    for shadow_y, shadow_x in cloud_shadow_positions:
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
    # Small flowers scattered in the grass
    flower_positions = [
        (grass_start_y + 3, 12, FLOWER_RED),
        (grass_start_y + 5, 28, FLOWER_YELLOW),
        (grass_start_y + 2, 45, FLOWER_WHITE),
        (grass_start_y + 6, 8, FLOWER_YELLOW),
        (grass_start_y + 4, 38, FLOWER_RED),
        (grass_start_y + 7, 55, FLOWER_WHITE),
    ]
    
    for flower_y, flower_x, flower_color in flower_positions:
        if 0 <= flower_y < height and 0 <= flower_x < width:
            canvas[flower_y][flower_x] = flower_color
    
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
    
    # Scale up 8x with nearest neighbor (pixel perfect)
    scale = 8
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