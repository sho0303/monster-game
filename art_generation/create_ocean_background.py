"""
Create a pixel art ocean biome background PNG
"""
from PIL import Image, ImageDraw
import numpy as np
import random

def create_ocean_background():
    """Create a pixel art ocean landscape with waves and underwater elements"""
    # Create a wider canvas for background use (landscape format)
    width = 64
    height = 32
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Ocean color palette (blue, aqua, and sea tones)
    # Sky colors - ocean sky
    SKY_LIGHT_BLUE = [135, 206, 235, 255]   # Light blue sky
    SKY_BLUE = [70, 130, 180, 255]          # Steel blue
    CLOUD_WHITE = [248, 248, 255, 255]      # White clouds
    CLOUD_GRAY = [192, 192, 192, 255]       # Gray cloud shading
    
    # Water colors - various shades for depth
    WATER_SURFACE = [0, 191, 255, 255]      # Bright surface water
    WATER_LIGHT = [30, 144, 255, 255]       # Light blue water
    WATER_MEDIUM = [0, 100, 200, 255]       # Medium blue water
    WATER_DEEP = [0, 50, 150, 255]          # Deep blue water
    WATER_DARK = [0, 30, 100, 255]          # Very deep water
    
    # Wave colors
    WAVE_WHITE = [255, 255, 255, 255]       # Wave foam
    WAVE_LIGHT = [240, 248, 255, 255]       # Light wave foam
    
    # Underwater elements
    CORAL_PINK = [255, 127, 80, 255]        # Coral reefs
    CORAL_ORANGE = [255, 69, 0, 255]        # Orange coral
    SEAWEED_GREEN = [46, 125, 50, 255]      # Dark seaweed
    SEAWEED_LIGHT = [76, 175, 80, 255]      # Light seaweed
    
    # Sand and seafloor
    SAND_LIGHT = [238, 203, 173, 255]       # Light sand
    SAND_MEDIUM = [205, 133, 63, 255]       # Medium sand
    SHELL_WHITE = [255, 228, 196, 255]      # Shells and pearls
    
    # Special ocean elements
    BUBBLE_BLUE = [173, 216, 230, 255]      # Water bubbles
    STARFISH_ORANGE = [255, 99, 71, 255]    # Starfish
    
    # SKY GRADIENT (top 40% of image)
    sky_height = int(height * 0.4)  # Sky takes up top 40%
    
    for y in range(sky_height):
        # Create vertical gradient from light blue at top to steel blue near water
        gradient_ratio = y / sky_height
        
        # Blend between sky colors for ocean atmosphere
        for x in range(width):
            if gradient_ratio < 0.7:
                # Upper sky - light blue
                canvas[y][x] = SKY_LIGHT_BLUE
            else:
                # Lower sky near horizon - darker blue
                canvas[y][x] = SKY_BLUE
    
    # Add some clouds in the sky
    cloud_positions = [(10, 3), (45, 5), (25, 2), (55, 4)]
    for cloud_x, cloud_y in cloud_positions:
        if cloud_y < sky_height and 0 <= cloud_x < width:
            # Small puffy clouds
            for dy in range(-1, 2):
                for dx in range(-2, 3):
                    cy, cx = cloud_y + dy, cloud_x + dx
                    if 0 <= cy < sky_height and 0 <= cx < width:
                        if abs(dx) <= 1 or abs(dy) == 0:  # Cloud shape
                            canvas[cy][cx] = CLOUD_WHITE
    
    # WATER SURFACE AND WAVES (middle section)
    water_start = sky_height
    water_surface_height = 3  # Height of surface wave area
    
    # Create animated-looking waves on the surface
    for y in range(water_start, water_start + water_surface_height):
        wave_intensity = (y - water_start) / water_surface_height
        
        for x in range(width):
            # Create wave pattern using sine-like function
            wave_offset = int(2 * np.sin(x * 0.3) + random.uniform(-0.5, 0.5))
            
            if y == water_start and (x + wave_offset) % 8 < 3:
                # Wave crests with white foam
                canvas[y][x] = WAVE_WHITE
            elif y == water_start + 1 and (x + wave_offset) % 8 < 2:
                # Secondary foam
                canvas[y][x] = WAVE_LIGHT
            else:
                # Regular surface water
                canvas[y][x] = WATER_SURFACE
    
    # UNDERWATER GRADIENT (bottom section)
    water_depth_start = water_start + water_surface_height
    underwater_height = height - water_depth_start
    
    for y in range(water_depth_start, height):
        depth_ratio = (y - water_depth_start) / underwater_height
        
        for x in range(width):
            # Create depth gradient
            if depth_ratio < 0.3:
                canvas[y][x] = WATER_LIGHT
            elif depth_ratio < 0.6:
                canvas[y][x] = WATER_MEDIUM
            elif depth_ratio < 0.8:
                canvas[y][x] = WATER_DEEP
            else:
                canvas[y][x] = WATER_DARK
    
    # Add underwater elements - seaweed
    seaweed_positions = [(8, height-4), (15, height-5), (35, height-6), (50, height-4), (58, height-3)]
    for seaweed_x, seaweed_base_y in seaweed_positions:
        if 0 <= seaweed_x < width:
            # Tall swaying seaweed
            for i in range(4):  # Height of seaweed
                sy = seaweed_base_y - i
                sx = seaweed_x + int(np.sin(i * 0.8) * 1)  # Slight sway
                if 0 <= sy < height and 0 <= sx < width:
                    canvas[sy][sx] = SEAWEED_GREEN
                    # Add some lighter seaweed details
                    if i % 2 == 0 and sx + 1 < width:
                        canvas[sy][sx + 1] = SEAWEED_LIGHT
    
    # Add coral formations on the seafloor
    coral_positions = [(12, height-2), (25, height-3), (40, height-2), (55, height-1)]
    for coral_x, coral_y in coral_positions:
        if 0 <= coral_x < width and 0 <= coral_y < height:
            # Small coral clusters
            canvas[coral_y][coral_x] = CORAL_PINK
            if coral_x + 1 < width:
                canvas[coral_y][coral_x + 1] = CORAL_ORANGE
            if coral_y - 1 >= 0:
                canvas[coral_y - 1][coral_x] = CORAL_PINK
    
    # Add some sandy seafloor patches
    for y in range(height - 2, height):
        for x in range(0, width, 8):
            for dx in range(min(4, width - x)):
                if x + dx < width:
                    canvas[y][x + dx] = SAND_LIGHT
    
    # Add scattered shells and starfish
    detail_positions = [(20, height-1), (45, height-1), (32, height-2)]
    for detail_x, detail_y in detail_positions:
        if 0 <= detail_x < width and 0 <= detail_y < height:
            if detail_x == 32:  # Starfish
                canvas[detail_y][detail_x] = STARFISH_ORANGE
            else:  # Shells
                canvas[detail_y][detail_x] = SHELL_WHITE
    
    # Add some floating bubbles for atmosphere
    bubble_positions = [(18, water_depth_start + 3), (42, water_depth_start + 5), (28, water_depth_start + 7)]
    for bubble_x, bubble_y in bubble_positions:
        if 0 <= bubble_x < width and 0 <= bubble_y < height:
            canvas[bubble_y][bubble_x] = BUBBLE_BLUE
    
    return canvas

def save_ocean_background():
    """Generate and save the ocean background"""
    print("Creating ocean biome background...")
    
    # Create the ocean landscape
    ocean_canvas = create_ocean_background()
    
    # Convert to PIL Image
    ocean_img = Image.fromarray(ocean_canvas, 'RGBA')
    
    # Scale up for better visibility (8x scale)
    scale_factor = 8
    final_width = ocean_canvas.shape[1] * scale_factor
    final_height = ocean_canvas.shape[0] * scale_factor
    
    ocean_img = ocean_img.resize((final_width, final_height), Image.NEAREST)
    
    # Save the image
    output_path = "../art/ocean_background.png"
    ocean_img.save(output_path)
    print(f"Ocean background saved to: {output_path}")
    
    return ocean_img

if __name__ == "__main__":
    save_ocean_background()