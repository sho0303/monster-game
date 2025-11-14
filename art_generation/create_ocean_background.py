"""
Create a pixel art ocean biome background PNG
"""
from PIL import Image, ImageDraw
import numpy as np
import random
import math

def create_ocean_background():
    """Create a pixel art ocean landscape with waves on bottom half and sky with sun on top half"""
    # Create a wider canvas for background use (landscape format)
    width = 128
    height = 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette
    # Sky colors
    SKY_LIGHT_BLUE = [135, 206, 250, 255]   # Light sky blue
    SKY_BLUE = [100, 149, 237, 255]         # Cornflower blue
    SKY_HORIZON = [176, 196, 222, 255]      # Light steel blue near horizon
    
    # Sun colors
    SUN_YELLOW = [255, 223, 0, 255]         # Bright yellow sun
    SUN_ORANGE = [255, 200, 0, 255]         # Orange sun glow
    SUN_LIGHT = [255, 255, 200, 255]        # Light yellow glow
    
    # Cloud colors
    CLOUD_WHITE = [248, 248, 255, 255]      # White clouds
    CLOUD_GRAY = [220, 220, 228, 255]       # Light gray cloud shading
    CLOUD_SHADOW = [192, 192, 200, 255]     # Cloud shadow
    
    # Ocean colors
    OCEAN_DARK = [0, 68, 119, 255]          # Dark ocean
    OCEAN_MEDIUM = [0, 105, 148, 255]       # Medium ocean
    OCEAN_LIGHT = [0, 134, 179, 255]        # Light ocean
    OCEAN_SURFACE = [64, 164, 223, 255]     # Surface shimmer
    
    # Wave colors
    WAVE_WHITE = [255, 255, 255, 255]       # White foam
    WAVE_FOAM = [230, 245, 255, 255]        # Light foam
    WAVE_CREST = [200, 230, 255, 255]       # Wave crest
    
    # DRAW SKY (top half - lines 0 to 31)
    sky_height = height // 2  # Top 32 pixels
    # DRAW SKY (top half - lines 0 to 31)
    sky_height = height // 2  # Top 32 pixels
    
    # Create sky gradient from lighter at top to horizon color at bottom
    for y in range(sky_height):
        gradient_ratio = y / sky_height
        
        for x in range(width):
            if gradient_ratio < 0.5:
                # Upper sky - light blue
                canvas[y][x] = SKY_LIGHT_BLUE
            elif gradient_ratio < 0.8:
                # Middle sky
                canvas[y][x] = SKY_BLUE
            else:
                # Near horizon - lighter
                canvas[y][x] = SKY_HORIZON
    
    # DRAW SUN (positioned in upper left quadrant)
    sun_center_x = 25
    sun_center_y = 12
    sun_radius = 8
    
    # Draw sun with glow effect
    for y in range(max(0, sun_center_y - sun_radius - 3), min(sky_height, sun_center_y + sun_radius + 3)):
        for x in range(max(0, sun_center_x - sun_radius - 3), min(width, sun_center_x + sun_radius + 3)):
            distance = math.sqrt((x - sun_center_x)**2 + (y - sun_center_y)**2)
            
            if distance <= sun_radius - 2:
                # Sun core
                canvas[y][x] = SUN_YELLOW
            elif distance <= sun_radius:
                # Sun edge
                canvas[y][x] = SUN_ORANGE
            elif distance <= sun_radius + 2:
                # Sun glow
                canvas[y][x] = SUN_LIGHT
    
    # DRAW CLOUDS (scattered across sky)
    cloud_data = [
        # (x, y, width, height)
        (60, 8, 20, 8),
        (95, 14, 16, 6),
        (40, 22, 18, 7),
        (110, 5, 14, 5),
    ]
    
    for cloud_x, cloud_y, cloud_w, cloud_h in cloud_data:
        # Draw fluffy cloud shape
        for dy in range(cloud_h):
            for dx in range(cloud_w):
                x = cloud_x + dx
                y = cloud_y + dy
                
                if 0 <= x < width and 0 <= y < sky_height:
                    # Create rounded cloud edges
                    is_edge = (dy == 0 and (dx < 3 or dx >= cloud_w - 3)) or \
                             (dy >= cloud_h - 1 and (dx < 2 or dx >= cloud_w - 2)) or \
                             (dx == 0 and dy < 2) or \
                             (dx >= cloud_w - 1 and dy < 2)
                    
                    is_bottom = dy >= cloud_h - 2
                    
                    if not is_edge:
                        if is_bottom:
                            # Cloud shadow at bottom
                            canvas[y][x] = CLOUD_SHADOW
                        elif dy < 2 or dx < 3:
                            # Cloud highlight at top
                            canvas[y][x] = CLOUD_WHITE
                        else:
                            # Cloud body
                            canvas[y][x] = CLOUD_GRAY
    
    # DRAW OCEAN (bottom half - lines 32 to 63)
    ocean_start = sky_height
    
    # Create ocean with depth gradient
    for y in range(ocean_start, height):
        depth_ratio = (y - ocean_start) / (height - ocean_start)
        
        for x in range(width):
            # Base ocean color based on depth
            if depth_ratio < 0.2:
                base_color = OCEAN_SURFACE
            elif depth_ratio < 0.5:
                base_color = OCEAN_LIGHT
            elif depth_ratio < 0.75:
                base_color = OCEAN_MEDIUM
            else:
                base_color = OCEAN_DARK
            
            canvas[y][x] = base_color
    
    # DRAW WAVES (multiple wave layers for depth)
    # Wave layer 1 - large distant waves
    for x in range(width):
        wave_height = int(3 * math.sin(x * 0.1) + 2)
        wave_y = ocean_start + 2 + wave_height
        
        if 0 <= wave_y < height:
            # Wave crest
            canvas[wave_y][x] = WAVE_CREST
            if wave_height > 2 and wave_y + 1 < height:
                canvas[wave_y + 1][x] = OCEAN_LIGHT
    
    # Wave layer 2 - medium waves
    for x in range(width):
        wave_height = int(2 * math.sin(x * 0.2 + 1.5) + 1)
        wave_y = ocean_start + 8 + wave_height
        
        if 0 <= wave_y < height:
            # White foam on peaks
            if int(x * 0.2) % 3 == 0:
                canvas[wave_y][x] = WAVE_FOAM
            else:
                canvas[wave_y][x] = WAVE_CREST
    
    # Wave layer 3 - close foreground waves with foam
    for x in range(width):
        wave_height = int(4 * math.sin(x * 0.15 + 3) + 2)
        wave_y = ocean_start + 18 + wave_height
        
        if 0 <= wave_y < height:
            # Large wave with white foam
            if wave_height >= 4:
                canvas[wave_y][x] = WAVE_WHITE
                if wave_y + 1 < height:
                    canvas[wave_y + 1][x] = WAVE_FOAM
            else:
                canvas[wave_y][x] = WAVE_FOAM
    
    # Add some scattered wave foam details
    foam_positions = [
        (15, ocean_start + 12), (35, ocean_start + 15), (55, ocean_start + 10),
        (75, ocean_start + 14), (95, ocean_start + 11), (110, ocean_start + 16),
        (25, ocean_start + 22), (68, ocean_start + 24), (100, ocean_start + 20),
    ]
    
    for foam_x, foam_y in foam_positions:
        if 0 <= foam_x < width and 0 <= foam_y < height:
            # Small foam patches (2-3 pixels)
            canvas[foam_y][foam_x] = WAVE_WHITE
            if foam_x + 1 < width:
                canvas[foam_y][foam_x + 1] = WAVE_FOAM
            if foam_y + 1 < height and foam_x < width:
                canvas[foam_y + 1][foam_x] = WAVE_FOAM
    
    return canvas

def save_ocean_background():
    """Generate and save the ocean background"""
    print("Creating ocean biome background...")
    
    # Create the ocean landscape
    ocean_canvas = create_ocean_background()
    
    # Convert to PIL Image
    ocean_img = Image.fromarray(ocean_canvas, 'RGBA')
    
    # Scale up for better visibility (4x scale for doubled base resolution)
    scale_factor = 4
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