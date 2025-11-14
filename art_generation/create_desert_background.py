"""
Create a pixel art desert biome background PNG
"""
from PIL import Image, ImageDraw
import numpy as np
import random

def create_desert_background():
    """Create a pixel art desert landscape with dunes and cacti"""
    # Create a wider canvas for background use (landscape format)
    width = 128
    height = 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Desert color palette (warm, sandy tones)
    # Sky colors - warmer desert sky
    SKY_ORANGE = [255, 165, 0, 255]      # Orange desert sky
    SKY_YELLOW = [255, 215, 0, 255]      # Golden sky near horizon
    LIGHT_ORANGE = [255, 228, 181, 255]  # Light orange/peach
    CLOUD_WHITE = [248, 248, 255, 255]   # White clouds
    CLOUD_SAND = [238, 203, 173, 255]    # Sandy cloud shading
    
    # Sand colors - various shades for depth
    SAND_LIGHT = [238, 203, 173, 255]    # Light sand dunes
    SAND_MEDIUM = [205, 133, 63, 255]    # Medium sand
    SAND_DARK = [160, 82, 45, 255]       # Dark sand shadows
    SAND_GOLD = [255, 215, 0, 255]       # Golden sand highlights
    
    # Rock/stone colors
    ROCK_GRAY = [105, 105, 105, 255]     # Desert rocks
    ROCK_BROWN = [139, 69, 19, 255]      # Red rock formations
    ROCK_LIGHT = [169, 169, 169, 255]    # Light stone
    
    # Cactus and desert plant colors
    CACTUS_GREEN = [107, 142, 35, 255]   # Cactus body
    CACTUS_DARK = [85, 107, 47, 255]     # Cactus shading
    CACTUS_SPINE = [255, 255, 255, 255]  # Cactus spines
    
    # Desert details
    BONE_WHITE = [255, 228, 196, 255]    # Desert bones/skulls
    CRYSTAL_BLUE = [0, 191, 255, 255]    # Rare desert crystals
    
    # SKY GRADIENT (top 60% of image)
    sky_height = int(height * 0.6)  # Sky takes up top 60%
    
    for y in range(sky_height):
        # Create vertical gradient from orange at top to golden near horizon
        gradient_ratio = y / sky_height
        
        # Blend between sky colors for desert atmosphere
        r = int(SKY_ORANGE[0] + (SKY_YELLOW[0] - SKY_ORANGE[0]) * gradient_ratio)
        g = int(SKY_ORANGE[1] + (SKY_YELLOW[1] - SKY_ORANGE[1]) * gradient_ratio)
        b = int(SKY_ORANGE[2] + (SKY_YELLOW[2] - SKY_ORANGE[2]) * gradient_ratio)
        
        sky_color = [r, g, b, 255]
        
        # Fill the row with sky gradient
        for x in range(width):
            canvas[y, x] = sky_color
    
    # CLOUDS - sparse desert clouds (scaled for doubled resolution)
    cloud_positions = [
        (20, 10, 12, 6),   # x, y, width, height - small cloud
        (90, 16, 16, 4),   # larger wispy cloud
        (50, 6, 8, 4),     # tiny cloud
    ]
    
    for cloud_x, cloud_y, cloud_w, cloud_h in cloud_positions:
        for dy in range(cloud_h):
            for dx in range(cloud_w):
                x = cloud_x + dx
                y = cloud_y + dy
                if 0 <= x < width and 0 <= y < sky_height:
                    # Create fluffy cloud texture
                    if random.random() < 0.7:  # 70% cloud density for wispy look
                        if dy == 0 or dx == 0 or dx == cloud_w-1:
                            canvas[y, x] = CLOUD_SAND  # Sandy cloud edges
                        else:
                            canvas[y, x] = CLOUD_WHITE  # White cloud center
    
    # DESERT GROUND - create rolling sand dunes (bottom 40%)
    ground_start_y = sky_height
    
    # Create base sand layer
    for y in range(ground_start_y, height):
        for x in range(width):
            canvas[y, x] = SAND_MEDIUM
    
    # Create sand dune undulations using sine waves
    import math
    
    # Multiple dune layers for depth (amplitudes doubled for resolution)
    dune_layers = [
        (0.1, 6, SAND_LIGHT),    # frequency, amplitude, color - background dunes
        (0.15, 4, SAND_GOLD),    # mid-ground dunes
        (0.2, 8, SAND_DARK),     # foreground dune shadows
    ]
    
    for frequency, amplitude, sand_color in dune_layers:
        for x in range(width):
            # Calculate dune height using sine wave
            dune_offset = int(amplitude * math.sin(frequency * x * math.pi))
            dune_y = ground_start_y + 2 + dune_offset
            
            # Draw dune at calculated position
            for y in range(max(ground_start_y, dune_y), min(height, dune_y + 3)):
                if 0 <= y < height:
                    # Add some randomness for natural texture
                    if random.random() < 0.8:
                        canvas[y, x] = sand_color
    
    # DESERT VEGETATION - sparse cacti and desert plants (scaled for doubled resolution)
    cactus_positions = [
        (30, ground_start_y + 10, 'tall'),    # x, y, type
        (70, ground_start_y + 6, 'short'),
        (100, ground_start_y + 12, 'tall'),
        (16, ground_start_y + 8, 'short'),
    ]
    
    for cactus_x, cactus_y, cactus_type in cactus_positions:
        if cactus_type == 'tall':
            # Tall saguaro-style cactus (doubled height)
            cactus_height = 16
            # Main trunk
            for dy in range(cactus_height):
                y = min(cactus_y + dy, height - 1)
                if 0 <= cactus_x < width and 0 <= y < height:
                    canvas[y, cactus_x] = CACTUS_GREEN
                    # Add shading
                    if cactus_x + 1 < width:
                        canvas[y, cactus_x + 1] = CACTUS_DARK
            
            # Cactus arms (doubled size)
            arm_y = cactus_y + 6
            if 0 <= arm_y < height:
                # Left arm (larger)
                for dx in range(-4, 0):
                    x = cactus_x + dx
                    if 0 <= x < width:
                        canvas[arm_y, x] = CACTUS_GREEN
                        canvas[arm_y + 1, x] = CACTUS_GREEN
                        canvas[arm_y + 2, x] = CACTUS_GREEN
                
                # Right arm (larger)
                for dx in range(2, 6):
                    x = cactus_x + dx
                    if 0 <= x < width:
                        canvas[arm_y + 2, x] = CACTUS_GREEN
                        canvas[arm_y + 3, x] = CACTUS_GREEN
                        canvas[arm_y + 4, x] = CACTUS_GREEN
        
        elif cactus_type == 'short':
            # Small barrel cactus (doubled size)
            for dy in range(6):
                for dx in range(4):
                    x = cactus_x + dx
                    y = cactus_y + dy
                    if 0 <= x < width and 0 <= y < height:
                        if dx == 0 or dy == 0:
                            canvas[y, x] = CACTUS_GREEN
                        else:
                            canvas[y, x] = CACTUS_DARK
    
    # DESERT ROCKS - scattered rock formations (scaled for doubled resolution)
    rock_positions = [
        (44, ground_start_y + 4, 6, 4),   # x, y, width, height
        (84, ground_start_y + 8, 4, 6),
        (116, ground_start_y + 2, 8, 4),
        (10, ground_start_y + 6, 4, 4),
    ]
    
    for rock_x, rock_y, rock_w, rock_h in rock_positions:
        for dy in range(rock_h):
            for dx in range(rock_w):
                x = rock_x + dx
                y = rock_y + dy
                if 0 <= x < width and 0 <= y < height:
                    if dx == 0 or dy == rock_h - 1:
                        canvas[y, x] = ROCK_BROWN  # Rock shadows
                    else:
                        canvas[y, x] = ROCK_GRAY   # Rock highlights
    
    # DESERT DETAILS - bones, crystals, small details (scaled for doubled resolution)
    detail_positions = [
        (56, ground_start_y + 14, 'bone'),
        (36, ground_start_y + 4, 'crystal'),
        (96, ground_start_y + 16, 'bone'),
        (120, ground_start_y + 10, 'crystal'),
        (20, ground_start_y + 18, 'bone'),
    ]
    
    for detail_x, detail_y, detail_type in detail_positions:
        if detail_type == 'bone' and 0 <= detail_x < width and 0 <= detail_y < height:
            # Small skull or bone (doubled size for better detail)
            canvas[detail_y, detail_x] = BONE_WHITE
            if detail_x + 1 < width:
                canvas[detail_y, detail_x + 1] = BONE_WHITE
            if detail_y + 1 < height:
                canvas[detail_y + 1, detail_x] = BONE_WHITE
            if detail_x + 1 < width and detail_y + 1 < height:
                canvas[detail_y + 1, detail_x + 1] = BONE_WHITE
        elif detail_type == 'crystal' and 0 <= detail_x < width and 0 <= detail_y < height:
            # Rare desert crystal (doubled size)
            canvas[detail_y, detail_x] = CRYSTAL_BLUE
            if detail_y - 1 >= 0:
                canvas[detail_y - 1, detail_x] = CRYSTAL_BLUE
    
    # HEAT SHIMMER EFFECT - add some distortion to simulate desert heat
    # Randomly lighten some sand pixels to create heat shimmer
    for y in range(ground_start_y, height):
        for x in range(width):
            if random.random() < 0.05:  # 5% chance for shimmer effect
                # Lighten the pixel slightly
                current = canvas[y, x]
                if current[0] < 240:  # Don't lighten already bright pixels
                    canvas[y, x] = [
                        min(255, current[0] + 20),
                        min(255, current[1] + 15),
                        min(255, current[2] + 10),
                        255
                    ]
    
    return canvas

def main():
    """Create and save the desert background"""
    print("Creating desert biome background...")
    
    # Create the desert landscape
    desert_data = create_desert_background()
    
    # Convert to PIL Image
    desert_img = Image.fromarray(desert_data, 'RGBA')
    
    # Scale up for final output (4x scaling for pixel art effect)
    scale_factor = 4
    final_width = desert_data.shape[1] * scale_factor
    final_height = desert_data.shape[0] * scale_factor
    
    # Use NEAREST neighbor to maintain crisp pixel art edges
    desert_scaled = desert_img.resize((final_width, final_height), Image.Resampling.NEAREST)
    
    # Save the desert background
    output_path = "../art/desert_background.png"
    desert_scaled.save(output_path)
    print(f"Desert background saved to: {output_path}")
    
    # Also create a larger version
    large_width = final_width * 2
    large_height = final_height * 2
    desert_large = desert_img.resize((large_width, large_height), Image.Resampling.NEAREST)
    output_path_large = "../art/desert_background_large.png"
    desert_large.save(output_path_large)
    print(f"Large desert background saved to: {output_path_large}")
    
    print("Desert biome background creation complete!")
    print("\nDesert features created:")
    print("- Warm orange-golden sky gradient")
    print("- Rolling sand dunes with multiple layers")
    print("- Tall saguaro and barrel cacti")
    print("- Desert rock formations")
    print("- Scattered bones and rare crystals")
    print("- Heat shimmer effect on sand")
    print("- Sparse wispy clouds")
    print("- Multiple sand tones for depth")

if __name__ == "__main__":
    main()