#!/usr/bin/env python3
"""
Create pixel art town biome background PNG to match game art style
"""
from PIL import Image, ImageDraw
import numpy as np
import random

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
    
    # Mountains/hills in the background
    mountain_points = []
    for x in range(0, width + 50, 50):
        y = height // 3 + 30 + int(20 * np.sin(x * 0.02)) + np.random.randint(-15, 15)
        mountain_points.extend([x, y])
    mountain_points.extend([width, height, 0, height])
    draw.polygon(mountain_points, fill='#1a2f1a')  # Dark green mountains
    
    # Town buildings - create a row of medieval-style buildings
    building_colors = ['#8B4513', '#654321', '#A0522D', '#D2691E', '#CD853F']  # Brown tones
    roof_colors = ['#800000', '#8B0000', '#A52A2A', '#B22222']  # Red roof tones
    
    # Buildings from left to right
    building_positions = [
        (50, height - 250, 120, 180),   # Building 1 (x, y, width, height)
        (180, height - 300, 140, 230),  # Building 2 (taller)
        (330, height - 220, 100, 150),  # Building 3
        (440, height - 280, 130, 210),  # Building 4
        (580, height - 240, 110, 170),  # Building 5
        (700, height - 200, 90, 130),   # Building 6
    ]
    
    for i, (x, y, w, h) in enumerate(building_positions):
        # Building body
        building_color = building_colors[i % len(building_colors)]
        draw.rectangle([x, y, x + w, y + h], fill=building_color, outline='#2F1B14', width=2)
        
        # Roof (triangular)
        roof_color = roof_colors[i % len(roof_colors)]
        roof_points = [x - 5, y, x + w//2, y - 30, x + w + 5, y]
        draw.polygon(roof_points, fill=roof_color, outline='#4A0000')
        
        # Windows (2x2 grid for most buildings)
        window_w, window_h = 15, 20
        for row in range(2):
            for col in range(2):
                win_x = x + 20 + col * 35
                win_y = y + 30 + row * 40
                if win_x + window_w < x + w - 10:  # Keep windows within building
                    # Window frame
                    draw.rectangle([win_x, win_y, win_x + window_w, win_y + window_h], 
                                 fill='#FFD700', outline='#8B4513', width=2)
                    # Window cross
                    draw.line([win_x + window_w//2, win_y, win_x + window_w//2, win_y + window_h], 
                            fill='#8B4513', width=2)
                    draw.line([win_x, win_y + window_h//2, win_x + window_w, win_y + window_h//2], 
                            fill='#8B4513', width=2)
        
        # Door (only on some buildings)
        if i % 2 == 0:  # Every other building gets a door
            door_w, door_h = 25, 50
            door_x = x + w//2 - door_w//2
            door_y = y + h - door_h
            draw.rectangle([door_x, door_y, door_x + door_w, door_y + door_h], 
                         fill='#654321', outline='#2F1B14', width=2)
            # Door handle
            draw.ellipse([door_x + door_w - 8, door_y + door_h//2 - 3, 
                         door_x + door_w - 2, door_y + door_h//2 + 3], fill='#FFD700')
    
    # Town square / road
    road_y = height - 70
    draw.rectangle([0, road_y, width, height], fill='#8B7D6B')  # Dirt road color
    
    # Add some cobblestones pattern to the road
    for x in range(0, width, 30):
        for y in range(road_y, height, 20):
            if (x + y) % 60 == 0:  # Create pattern
                stone_x, stone_y = x + np.random.randint(-5, 5), y + np.random.randint(-3, 3)
                draw.ellipse([stone_x, stone_y, stone_x + 8, stone_y + 6], 
                           fill='#A0A0A0', outline='#696969')
    
    # Add some market stalls/decorations
    # Market stall 1
    stall_x, stall_y = 250, height - 140
    draw.rectangle([stall_x, stall_y, stall_x + 60, stall_y + 40], fill='#DEB887')
    # Stall awning
    draw.polygon([stall_x - 5, stall_y, stall_x + 30, stall_y - 15, stall_x + 65, stall_y], 
                fill='#FF6347')
    
    # Market stall 2
    stall_x2, stall_y2 = 500, height - 130
    draw.rectangle([stall_x2, stall_y2, stall_x2 + 50, stall_y2 + 35], fill='#D2B48C')
    draw.polygon([stall_x2 - 5, stall_y2, stall_x2 + 25, stall_y2 - 12, stall_x2 + 55, stall_y2], 
                fill='#32CD32')
    
    # Add some fantasy elements
    # Street lamps
    lamp_positions = [150, 350, 550, 750]
    for lamp_x in lamp_positions:
        lamp_y = height - 120
        # Lamp post
        draw.rectangle([lamp_x, lamp_y, lamp_x + 6, lamp_y + 50], fill='#2F4F2F')
        # Lamp light
        draw.ellipse([lamp_x - 8, lamp_y - 15, lamp_x + 14, lamp_y + 5], 
                    fill='#FFFF99', outline='#FFD700', width=2)
        # Light glow effect
        draw.ellipse([lamp_x - 12, lamp_y - 19, lamp_x + 18, lamp_y + 9], 
                    fill='#FFFF99')
    
    # Trees (sparse, to show it's a town square)
    tree_positions = [(80, height - 160), (650, height - 180)]
    for tree_x, tree_y in tree_positions:
        # Tree trunk
        draw.rectangle([tree_x, tree_y, tree_x + 12, tree_y + 40], fill='#8B4513')
        # Tree leaves (circular)
        draw.ellipse([tree_x - 15, tree_y - 25, tree_x + 27, tree_y + 15], 
                    fill='#228B22', outline='#006400', width=2)
    
    # Add a fountain in the center
    fountain_x, fountain_y = width//2 - 30, height - 180
    # Fountain base
    draw.ellipse([fountain_x, fountain_y, fountain_x + 60, fountain_y + 30], 
                fill='#708090', outline='#2F4F4F', width=3)
    # Fountain center
    draw.ellipse([fountain_x + 20, fountain_y - 10, fountain_x + 40, fountain_y + 10], 
                fill='#87CEEB', outline='#4682B4', width=2)
    # Water sparkles
    for i in range(5):
        spark_x = fountain_x + 25 + np.random.randint(-8, 8)
        spark_y = fountain_y + np.random.randint(-5, 5)
        draw.ellipse([spark_x, spark_y, spark_x + 3, spark_y + 3], fill='#E6E6FA')
    
    return img

def main():
    print("🏘️ Creating fantasy town background...")
    
    # Create the town background
    town_bg = create_town_background()
    
    # Save the image
    output_path = 'art/town_background.png'
    
    # Ensure art directory exists
    os.makedirs('art', exist_ok=True)
    
    town_bg.save(output_path, 'PNG')
    print(f"✅ Town background saved as {output_path}")
    print("📐 Size: 800x600 pixels")
    print("🎨 Features: Medieval buildings, market stalls, fountain, street lamps")
    
    # Also create a smaller preview
    preview = town_bg.resize((400, 300), Image.Resampling.LANCZOS)
    preview.save('art/town_background_preview.png', 'PNG')
    print("🔍 Preview saved as art/town_background_preview.png")

if __name__ == '__main__':
    main()