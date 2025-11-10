#!/usr/bin/env python3
"""
Victory Fireworks Animation Generator - Creates 4 frames of fireworks celebration
Pixel art style matching the merman king art generation approach
Frame sequence shows fireworks exploding in celebration of game victory
"""

import numpy as np
from PIL import Image
import os

def create_fireworks_frame_1():
    """Create first fireworks frame - initial launch"""
    # Create a 64x64 canvas for more space for fireworks
    size = 64
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette for fireworks
    BLACK = [0, 0, 0, 255]
    WHITE = [255, 255, 255, 255]
    SPARK_RED = [255, 100, 100, 255]
    SPARK_ORANGE = [255, 165, 0, 255]
    SPARK_YELLOW = [255, 255, 100, 255]
    SPARK_GOLD = [255, 215, 0, 255]
    SPARK_GREEN = [100, 255, 100, 255]
    SPARK_BLUE = [100, 150, 255, 255]
    SPARK_PURPLE = [200, 100, 255, 255]
    SPARK_PINK = [255, 150, 200, 255]
    TRAIL_WHITE = [255, 255, 255, 180]
    TRAIL_YELLOW = [255, 255, 100, 150]
    NIGHT_SKY = [15, 15, 35, 255]
    
    # Fill background with night sky
    canvas[:, :] = NIGHT_SKY
    
    # Frame 1: Rockets launching upward
    # Left rocket trail
    for y in range(40, 60):
        x = 15
        if y % 2 == 0:  # Dotted trail effect
            canvas[y, x] = TRAIL_YELLOW
            canvas[y, x-1] = TRAIL_WHITE
            canvas[y, x+1] = TRAIL_WHITE
    
    # Right rocket trail  
    for y in range(45, 62):
        x = 48
        if y % 3 == 0:  # Different pattern
            canvas[y, x] = TRAIL_WHITE
            canvas[y, x-1] = TRAIL_YELLOW
            canvas[y, x+1] = TRAIL_YELLOW
    
    # Center rocket trail
    for y in range(50, 64):
        x = 32
        if y % 2 == 1:
            canvas[y, x] = SPARK_GOLD
            canvas[y, x-1] = TRAIL_WHITE
            canvas[y, x+1] = TRAIL_WHITE
    
    # Small sparks at rocket heads
    canvas[38, 15] = SPARK_YELLOW
    canvas[37, 15] = SPARK_ORANGE
    canvas[43, 48] = SPARK_RED
    canvas[42, 48] = SPARK_ORANGE
    canvas[48, 32] = SPARK_GOLD
    canvas[47, 32] = SPARK_YELLOW
    
    return canvas

def create_fireworks_frame_2():
    """Create second fireworks frame - initial explosions"""
    size = 64
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Same color palette
    SPARK_RED = [255, 100, 100, 255]
    SPARK_ORANGE = [255, 165, 0, 255]
    SPARK_YELLOW = [255, 255, 100, 255]
    SPARK_GOLD = [255, 215, 0, 255]
    SPARK_GREEN = [100, 255, 100, 255]
    SPARK_BLUE = [100, 150, 255, 255]
    SPARK_PURPLE = [200, 100, 255, 255]
    SPARK_PINK = [255, 150, 200, 255]
    WHITE = [255, 255, 255, 255]
    NIGHT_SKY = [15, 15, 35, 255]
    
    canvas[:, :] = NIGHT_SKY
    
    # Frame 2: Small explosions beginning
    # Left explosion (red/orange burst)
    center_x, center_y = 15, 25
    explosion_points = [
        (center_y-2, center_x), (center_y+2, center_x), (center_y, center_x-2), (center_y, center_x+2),
        (center_y-1, center_x-1), (center_y-1, center_x+1), (center_y+1, center_x-1), (center_y+1, center_x+1)
    ]
    for i, (y, x) in enumerate(explosion_points):
        if 0 <= y < size and 0 <= x < size:
            color = SPARK_RED if i < 4 else SPARK_ORANGE
            canvas[y, x] = color
    
    # Right explosion (blue/purple burst)
    center_x, center_y = 48, 20
    for i, (y, x) in enumerate(explosion_points):
        y += center_y - 25
        x += center_x - 15
        if 0 <= y < size and 0 <= x < size:
            color = SPARK_BLUE if i < 4 else SPARK_PURPLE
            canvas[y, x] = color
    
    # Center explosion (gold/yellow burst)
    center_x, center_y = 32, 30
    for i, (y, x) in enumerate(explosion_points):
        y += center_y - 25
        x += center_x - 15
        if 0 <= y < size and 0 <= x < size:
            color = SPARK_GOLD if i < 4 else SPARK_YELLOW
            canvas[y, x] = color
    
    # Add center bright spots
    canvas[25, 15] = WHITE
    canvas[20, 48] = WHITE  
    canvas[30, 32] = WHITE
    
    return canvas

def create_fireworks_frame_3():
    """Create third fireworks frame - full explosion"""
    size = 64
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    SPARK_RED = [255, 100, 100, 255]
    SPARK_ORANGE = [255, 165, 0, 255]
    SPARK_YELLOW = [255, 255, 100, 255]
    SPARK_GOLD = [255, 215, 0, 255]
    SPARK_GREEN = [100, 255, 100, 255]
    SPARK_BLUE = [100, 150, 255, 255]
    SPARK_PURPLE = [200, 100, 255, 255]
    SPARK_PINK = [255, 150, 200, 255]
    WHITE = [255, 255, 255, 255]
    NIGHT_SKY = [15, 15, 35, 255]
    
    canvas[:, :] = NIGHT_SKY
    
    # Frame 3: Maximum explosion - large bursts
    # Large left explosion (red/orange starburst)
    center_x, center_y = 15, 25
    # Create radiating lines
    for angle in range(0, 360, 45):  # 8 directions
        for distance in range(1, 8):
            import math
            x = center_x + int(distance * math.cos(math.radians(angle)))
            y = center_y + int(distance * math.sin(math.radians(angle)))
            if 0 <= y < size and 0 <= x < size:
                if distance <= 3:
                    canvas[y, x] = SPARK_RED
                elif distance <= 5:
                    canvas[y, x] = SPARK_ORANGE
                else:
                    canvas[y, x] = SPARK_YELLOW
    
    # Large right explosion (blue/purple starburst)
    center_x, center_y = 48, 20
    for angle in range(22, 360+22, 45):  # Offset pattern
        for distance in range(1, 7):
            x = center_x + int(distance * math.cos(math.radians(angle)))
            y = center_y + int(distance * math.sin(math.radians(angle)))
            if 0 <= y < size and 0 <= x < size:
                if distance <= 2:
                    canvas[y, x] = WHITE
                elif distance <= 4:
                    canvas[y, x] = SPARK_BLUE
                else:
                    canvas[y, x] = SPARK_PURPLE
    
    # Center explosion (gold/green burst)
    center_x, center_y = 32, 15
    for angle in range(0, 360, 30):  # 12 directions
        for distance in range(1, 6):
            x = center_x + int(distance * math.cos(math.radians(angle)))
            y = center_y + int(distance * math.sin(math.radians(angle)))
            if 0 <= y < size and 0 <= x < size:
                if distance <= 2:
                    canvas[y, x] = SPARK_GOLD
                else:
                    canvas[y, x] = SPARK_GREEN
    
    # Add new launching rockets for next wave
    for y in range(50, 60):
        if y % 3 == 0:
            canvas[y, 25] = SPARK_PINK
            canvas[y, 40] = SPARK_GREEN
    
    return canvas

def create_fireworks_frame_4():
    """Create fourth fireworks frame - finale with multiple explosions"""
    size = 64
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    SPARK_RED = [255, 100, 100, 255]
    SPARK_ORANGE = [255, 165, 0, 255]
    SPARK_YELLOW = [255, 255, 100, 255]
    SPARK_GOLD = [255, 215, 0, 255]
    SPARK_GREEN = [100, 255, 100, 255]
    SPARK_BLUE = [100, 150, 255, 255]
    SPARK_PURPLE = [200, 100, 255, 255]
    SPARK_PINK = [255, 150, 200, 255]
    WHITE = [255, 255, 255, 255]
    NIGHT_SKY = [15, 15, 35, 255]
    
    canvas[:, :] = NIGHT_SKY
    
    # Frame 4: Grand finale - multiple simultaneous explosions
    import math
    
    # Multiple explosion centers
    explosions = [
        (12, 15, SPARK_RED, SPARK_ORANGE),      # Top left
        (45, 18, SPARK_BLUE, SPARK_PURPLE),    # Top right  
        (30, 12, SPARK_GOLD, SPARK_YELLOW),    # Top center
        (20, 35, SPARK_GREEN, SPARK_PINK),     # Mid left
        (42, 40, SPARK_PURPLE, SPARK_BLUE),    # Mid right
        (32, 45, SPARK_PINK, WHITE),           # Bottom center
    ]
    
    for center_x, center_y, color1, color2 in explosions:
        # Create varying sized bursts
        max_distance = 4 + (center_y % 3)  # Varying sizes
        
        for angle in range(0, 360, 20):  # 18 directions
            for distance in range(1, max_distance):
                x = center_x + int(distance * math.cos(math.radians(angle)))
                y = center_y + int(distance * math.sin(math.radians(angle)))
                if 0 <= y < size and 0 <= x < size:
                    if distance <= 2:
                        canvas[y, x] = color1
                    else:
                        canvas[y, x] = color2
        
        # Bright center
        canvas[center_y, center_x] = WHITE
    
    # Add sparkly trailing effects
    for i in range(20):
        x = np.random.randint(5, size-5)
        y = np.random.randint(5, size-5)
        colors = [SPARK_GOLD, SPARK_YELLOW, WHITE, SPARK_PINK]
        canvas[y, x] = colors[i % len(colors)]
    
    return canvas

def main():
    """Create all 4 fireworks animation frames"""
    print("🎆 Creating Victory Fireworks Animation Frames...")
    
    # Create art directory if it doesn't exist
    os.makedirs('art', exist_ok=True)
    
    frames = [
        (create_fireworks_frame_1(), "art/victory_fireworks_1.png", "Rockets launching"),
        (create_fireworks_frame_2(), "art/victory_fireworks_2.png", "Initial explosions"),
        (create_fireworks_frame_3(), "art/victory_fireworks_3.png", "Full explosion"),
        (create_fireworks_frame_4(), "art/victory_fireworks_4.png", "Grand finale")
    ]
    
    scale = 8  # 64x64 -> 512x512 final size
    
    for i, (canvas, filename, description) in enumerate(frames, 1):
        # Convert numpy array to PIL Image
        img = Image.fromarray(canvas, 'RGBA')
        
        # Scale up with nearest neighbor for pixel-perfect scaling
        final_size = canvas.shape[0] * scale
        img_scaled = img.resize((final_size, final_size), Image.NEAREST)
        
        # Save the frame
        img_scaled.save(filename)
        print(f"✅ Frame {i}: {filename} - {description}")
        print(f"   Size: {final_size}x{final_size} pixels")
    
    print(f"\n🎆 Victory Fireworks Animation Complete!")
    print(f"📁 Created 4 frames in art/ directory")
    print(f"🎮 Ready for victory celebration animation!")
    print(f"\n🎯 Animation sequence:")
    print(f"   Frame 1 → Frame 2 → Frame 3 → Frame 4 → Loop")
    print(f"   Rockets → Small bursts → Full explosion → Grand finale")

if __name__ == "__main__":
    main()