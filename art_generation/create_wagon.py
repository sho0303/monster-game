"""
Create a pixel art style covered wagon image for the monster game.
Inspired by old western wagons with a canvas cover.
Matches the blocky style of create_boar_art.py
"""

import numpy as np
from PIL import Image
import os

def create_wagon():
    """Create a blocky pixel art covered wagon"""
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette
    WOOD_BROWN = [101, 67, 33, 255]
    WOOD_DARK = [70, 47, 23, 255]
    CANVAS_TAN = [222, 202, 170, 255]
    CANVAS_SHADOW = [180, 162, 140, 255]
    BLACK = [0, 0, 0, 255]
    GRAY = [100, 100, 100, 255]
    
    # Draw wagon wheels (both wheels identical, bigger)
    # Back wheel - circular outline (wider and taller)
    for y in range(18, 30):
        for x in range(0, 8):
            canvas[y][x] = WOOD_BROWN
    
    # Make it more circular by trimming corners
    canvas[18][0] = [0, 0, 0, 0]
    canvas[18][1] = [0, 0, 0, 0]
    canvas[18][6] = [0, 0, 0, 0]
    canvas[18][7] = [0, 0, 0, 0]
    canvas[19][0] = [0, 0, 0, 0]
    canvas[19][7] = [0, 0, 0, 0]
    canvas[29][0] = [0, 0, 0, 0]
    canvas[29][1] = [0, 0, 0, 0]
    canvas[29][6] = [0, 0, 0, 0]
    canvas[29][7] = [0, 0, 0, 0]
    canvas[28][0] = [0, 0, 0, 0]
    canvas[28][7] = [0, 0, 0, 0]
    
    # Back wheel inner rim
    for y in range(20, 28):
        for x in range(2, 6):
            canvas[y][x] = WOOD_DARK
    
    # Back wheel hub (center)
    canvas[23][3] = GRAY
    canvas[23][4] = GRAY
    canvas[24][3] = GRAY
    canvas[24][4] = GRAY
    
    # Back wheel spokes (4 clear spokes)
    canvas[20][3] = BLACK
    canvas[21][3] = BLACK
    canvas[22][3] = BLACK
    canvas[25][3] = BLACK
    canvas[26][3] = BLACK
    canvas[27][3] = BLACK
    canvas[23][1] = BLACK
    canvas[23][2] = BLACK
    canvas[24][1] = BLACK
    canvas[24][2] = BLACK
    canvas[23][5] = BLACK
    canvas[23][6] = BLACK
    canvas[24][5] = BLACK
    canvas[24][6] = BLACK
    
    # Front wheel - identical to back wheel
    for y in range(18, 30):
        for x in range(22, 30):
            canvas[y][x] = WOOD_BROWN
    
    # Make it more circular
    canvas[18][22] = [0, 0, 0, 0]
    canvas[18][23] = [0, 0, 0, 0]
    canvas[18][28] = [0, 0, 0, 0]
    canvas[18][29] = [0, 0, 0, 0]
    canvas[19][22] = [0, 0, 0, 0]
    canvas[19][29] = [0, 0, 0, 0]
    canvas[29][22] = [0, 0, 0, 0]
    canvas[29][23] = [0, 0, 0, 0]
    canvas[29][28] = [0, 0, 0, 0]
    canvas[29][29] = [0, 0, 0, 0]
    canvas[28][22] = [0, 0, 0, 0]
    canvas[28][29] = [0, 0, 0, 0]
    
    # Front wheel inner rim
    for y in range(20, 28):
        for x in range(24, 28):
            canvas[y][x] = WOOD_DARK
    
    # Front wheel hub
    canvas[23][25] = GRAY
    canvas[23][26] = GRAY
    canvas[24][25] = GRAY
    canvas[24][26] = GRAY
    
    # Front wheel spokes (4 clear spokes)
    canvas[20][25] = BLACK
    canvas[21][25] = BLACK
    canvas[22][25] = BLACK
    canvas[25][25] = BLACK
    canvas[26][25] = BLACK
    canvas[27][25] = BLACK
    canvas[23][23] = BLACK
    canvas[23][24] = BLACK
    canvas[24][23] = BLACK
    canvas[24][24] = BLACK
    canvas[23][27] = BLACK
    canvas[23][28] = BLACK
    canvas[24][27] = BLACK
    canvas[24][28] = BLACK
    
    # Draw wagon bed (rectangular wooden base)
    for y in range(16, 22):
        for x in range(4, 28):
            canvas[y][x] = WOOD_BROWN
    
    # Wood planks detail
    for x in range(8, 26, 4):
        for y in range(16, 22):
            canvas[y][x] = WOOD_DARK
    
    # Draw canvas cover (rounded top)
    # Canvas cover - arch shape
    for y in range(8, 16):
        for x in range(6, 26):
            canvas[y][x] = CANVAS_TAN
    
    # Round the top
    canvas[8][6] = [0, 0, 0, 0]
    canvas[8][7] = [0, 0, 0, 0]
    canvas[8][24] = [0, 0, 0, 0]
    canvas[8][25] = [0, 0, 0, 0]
    canvas[9][6] = [0, 0, 0, 0]
    canvas[9][25] = [0, 0, 0, 0]
    
    # Canvas shadow/folds
    for y in range(10, 16):
        canvas[y][12] = CANVAS_SHADOW
        canvas[y][18] = CANVAS_SHADOW
    
    # Horizontal seams
    for x in range(8, 24):
        canvas[11][x] = CANVAS_SHADOW
        canvas[14][x] = CANVAS_SHADOW
    
    # Draw support hoops (wooden arches visible)
    for x in [10, 15, 20]:
        canvas[10][x] = WOOD_DARK
        canvas[9][x] = WOOD_DARK
        canvas[8][x] = WOOD_DARK
    
    # Axles
    for x in range(4, 6):
        canvas[19][x] = GRAY
    for x in range(24, 27):
        canvas[21][x] = GRAY
    
    # Wagon tongue (pole extending forward)
    for x in range(0, 6):
        canvas[23][x] = WOOD_BROWN
        canvas[24][x] = WOOD_BROWN
    
    # Iron bands on tongue
    canvas[23][1] = BLACK
    canvas[24][1] = BLACK
    canvas[23][3] = BLACK
    canvas[24][3] = BLACK
    
    # Add outline for definition
    # Top outline
    for x in range(10, 22):
        canvas[7][x] = WOOD_DARK
    
    return canvas

def main():
    """Create and save the wagon image"""
    print("Creating blocky pixel art wagon...")
    
    wagon_canvas = create_wagon()
    
    # Convert to PIL Image and scale up (like boar art does)
    wagon_img = Image.fromarray(wagon_canvas, mode='RGBA')
    
    # Scale up by 8x to make it 256x256 (32 * 8 = 256)
    wagon_img = wagon_img.resize((256, 256), Image.NEAREST)
    
    # Save the image
    output_path = 'art/wagon.png'
    wagon_img.save(output_path)
    
    print(f"✅ Created {output_path}")
    print(f"   Base size: 32x32 pixels")
    print(f"   Scaled size: {wagon_img.size[0]}x{wagon_img.size[1]} pixels")
    print(f"   Style: Blocky pixel art covered wagon")
    print(f"   Features: Canvas cover, wooden wheels with spokes, wagon tongue")

if __name__ == '__main__':
    main()
