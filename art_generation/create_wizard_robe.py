#!/usr/bin/env python3
"""
Wizard's Robe Generator
Creates a 32x32 pixel art wizard's robe in Minecraft style, scaled to 256x256
Matches the art style of create_steel_plate_mail.py
"""

import numpy as np
from PIL import Image

def create_wizard_robe():
    # Canvas setup
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Wizard robe color palette (mystical purple and blue tones)
    DARK_PURPLE = np.array([40, 20, 80, 255], dtype=np.uint8)      # Dark robe shadows
    PURPLE = np.array([80, 40, 120, 255], dtype=np.uint8)         # Base robe color
    LIGHT_PURPLE = np.array([120, 80, 160, 255], dtype=np.uint8)  # Robe highlights
    BRIGHT_PURPLE = np.array([160, 120, 200, 255], dtype=np.uint8) # Bright robe shine
    GOLD_TRIM = np.array([200, 150, 50, 255], dtype=np.uint8)     # Golden trim/embroidery
    DEEP_SHADOW = np.array([20, 10, 40, 255], dtype=np.uint8)     # Deep fabric shadows
    SILVER_THREAD = np.array([180, 180, 200, 255], dtype=np.uint8) # Silver threading
    MYSTIC_BLUE = np.array([60, 80, 140, 255], dtype=np.uint8)    # Mystical accents
    
    # Transparent background
    canvas[:, :] = [0, 0, 0, 0]
    
    # MAIN WIZARD ROBE STRUCTURE
    robe_shape = {
        # Shoulders and hood area
        5: list(range(14, 19)),   # Hood top
        6: list(range(12, 21)),   # Hood expansion
        7: list(range(10, 23)),   # Hood opening
        8: list(range(9, 24)),    # Shoulder line
        
        # Upper torso (fitted area)
        9: list(range(10, 23)),   # Upper chest
        10: list(range(10, 23)),  # Chest area
        11: list(range(10, 23)),  # Mid chest
        12: list(range(10, 23)),  # Lower chest
        
        # Mid torso (robe body - starting to flow)
        13: list(range(9, 24)),   # Upper robe body
        14: list(range(9, 24)),   # Robe expansion
        15: list(range(8, 25)),   # Flowing robe
        16: list(range(8, 25)),   # Continued flow
        
        # Lower torso (full flowing robe)
        17: list(range(7, 26)),   # Wide robe flow
        18: list(range(7, 26)),   # Maximum width
        19: list(range(6, 27)),   # Flowing hem area
        20: list(range(6, 27)),   # Lower hem
        21: list(range(7, 26)),   # Hem tapering
        22: list(range(8, 25)),   # Robe bottom
        23: list(range(9, 24)),   # Final hem
        
        # Long sleeves (wizard arms)
        9: list(range(6, 10)) + list(range(23, 27)),   # Upper sleeves
        10: list(range(5, 11)) + list(range(22, 28)),  # Mid upper sleeves
        11: list(range(4, 12)) + list(range(21, 29)),  # Lower upper sleeves
        12: list(range(4, 12)) + list(range(21, 29)),  # Elbow area
        13: list(range(5, 11)) + list(range(22, 28)),  # Forearm
        14: list(range(5, 11)) + list(range(22, 28)),  # Lower forearm
        15: list(range(6, 10)) + list(range(23, 27)),  # Wrist area
        16: list(range(6, 10)) + list(range(23, 27)),  # Sleeve ends
    }
    
    # Fill the main robe body with base purple color
    for y, x_coords in robe_shape.items():
        if isinstance(x_coords, list):
            for x in x_coords:
                if 0 <= x < size and 0 <= y < size:
                    canvas[y][x] = PURPLE
    
    # ROBE FABRIC FOLDS AND DRAPING
    
    # Vertical fabric folds (natural draping)
    fabric_folds = [
        # Major vertical folds
        (range(13, 24), 11),  # Left major fold
        (range(13, 24), 16),  # Center fold
        (range(13, 24), 21),  # Right major fold
        
        # Minor fabric creases
        (range(15, 22), 9),   # Left edge fold
        (range(15, 22), 23),  # Right edge fold
        (range(17, 21), 13),  # Left-center fold
        (range(17, 21), 19),  # Right-center fold
    ]
    
    for coord in fabric_folds:
        if isinstance(coord[0], range):  # Vertical fold
            y_range, x = coord
            for y in y_range:
                if 0 <= x < size and 0 <= y < size:
                    canvas[y][x] = DARK_PURPLE
    
    # GOLDEN TRIM AND EMBROIDERY
    
    # Hood trim (golden edging)
    hood_trim = [
        (7, 10), (7, 11), (7, 21), (7, 22),  # Hood opening trim
        (6, 12), (6, 20),                     # Hood side trim
        (5, 14), (5, 18),                     # Hood top trim
    ]
    
    # Sleeve trim (golden cuffs)
    sleeve_trim = [
        # Left sleeve cuff
        (15, 6), (15, 7), (15, 8), (15, 9),
        (16, 6), (16, 7), (16, 8), (16, 9),
        
        # Right sleeve cuff
        (15, 23), (15, 24), (15, 25), (15, 26),
        (16, 23), (16, 24), (16, 25), (16, 26),
    ]
    
    # Robe hem trim (golden bottom border)
    hem_trim = [
        (22, 9), (22, 10), (22, 22), (22, 23),    # Hem corners
        (23, 10), (23, 11), (23, 21), (23, 22),   # Hem edge
    ]
    
    # Central robe embroidery (mystical symbols)
    central_embroidery = [
        # Chest emblem (mystical symbol)
        (10, 15), (10, 16), (10, 17),              # Top line
        (11, 14), (11, 15), (11, 16), (11, 17), (11, 18),  # Symbol body
        (12, 15), (12, 16), (12, 17),              # Bottom line
        
        # Additional decorative elements
        (14, 12), (14, 20),  # Side decorations
        (16, 13), (16, 19),  # Lower decorations
    ]
    
    # Apply all golden trim
    for y, x in hood_trim + sleeve_trim + hem_trim + central_embroidery:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = GOLD_TRIM
    
    # MYSTICAL DETAILS AND HIGHLIGHTS
    
    # Fabric highlights (light catching fabric)
    fabric_highlights = [
        # Shoulder highlights
        (8, 12), (8, 20),     # Shoulder peaks
        (9, 13), (9, 19),     # Upper torso highlights
        
        # Sleeve highlights  
        (10, 7), (10, 25),    # Sleeve peaks
        (12, 8), (12, 24),    # Mid-sleeve highlights
        
        # Robe body highlights
        (14, 10), (14, 22),   # Upper robe highlights
        (17, 8), (17, 24),    # Wide robe highlights
        (20, 12), (20, 20),   # Lower robe highlights
    ]
    
    for y, x in fabric_highlights:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = LIGHT_PURPLE
    
    # Magical shimmer effects
    magic_shimmer = [
        (9, 14), (9, 18),     # Chest shimmer
        (11, 13), (11, 19),   # Mid-chest shimmer
        (15, 11), (15, 21),   # Robe shimmer
        (18, 14), (18, 18),   # Lower shimmer
    ]
    
    for y, x in magic_shimmer:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = BRIGHT_PURPLE
    
    # DEEP SHADOWS AND FABRIC DEPTH
    
    # Deep fabric shadows (under folds)
    deep_shadows = [
        # Under major folds
        (14, 11), (14, 21),   # Under fold shadows
        (16, 16),             # Central deep shadow
        (18, 9), (18, 23),    # Edge shadows
        (20, 13), (20, 19),   # Lower shadows
        
        # Hood interior shadow
        (6, 15), (6, 17),     # Hood depth
        
        # Sleeve interior shadows
        (11, 6), (11, 26),    # Armpit shadows
        (13, 7), (13, 25),    # Sleeve depth
    ]
    
    for y, x in deep_shadows:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = DEEP_SHADOW
    
    # SILVER THREADING AND DETAILS
    
    # Silver mystical threading (magical patterns)
    silver_threading = [
        # Mystical patterns on robe
        (13, 15), (13, 17),   # Upper pattern
        (15, 14), (15, 18),   # Mid pattern
        (17, 15), (17, 17),   # Lower pattern
        
        # Hood silver accents
        (6, 14), (6, 18),     # Hood silver
        
        # Sleeve silver details
        (14, 8), (14, 24),    # Sleeve accents
    ]
    
    for y, x in silver_threading:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = SILVER_THREAD
    
    # MYSTICAL BLUE ACCENTS
    
    # Mystical blue magical energy
    mystical_accents = [
        # Magical aura around emblem
        (10, 14), (10, 18),   # Emblem aura
        (12, 14), (12, 18),   # Lower aura
        
        # Magical energy at sleeve ends
        (16, 7), (16, 25),    # Sleeve magic
        
        # Hem magical glow
        (22, 12), (22, 20),   # Hem magic
    ]
    
    for y, x in mystical_accents:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = MYSTIC_BLUE
    
    # HOOD DETAILS
    
    # Hood shadow and depth
    hood_interior = [
        (6, 15), (6, 16), (6, 17),  # Hood opening shadow
    ]
    
    for y, x in hood_interior:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = DEEP_SHADOW
    
    # Hood highlight edges
    hood_edges = [
        (5, 15), (5, 17),     # Hood top edges
        (7, 12), (7, 20),     # Hood side edges
    ]
    
    for y, x in hood_edges:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = LIGHT_PURPLE
    
    # Convert to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up using nearest neighbor for crisp pixels
    scale = 8
    img_scaled = img.resize((size * scale, size * scale), Image.NEAREST)
    
    # Save image
    output_path = 'wizard_robe.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {size * scale}x{size * scale} pixels")
    print(f"   Style: Minecraft-style pixel art wizard's robe")
    print(f"   Materials: Purple mystical fabric, golden trim, silver threading")
    print(f"   Details: Flowing drapes, fabric folds, hood with opening")
    print(f"   Features: 3D depth, magical shimmer, mystical embroidery")
    print(f"   Magic: Mystical blue accents, enchanted symbols, wizard elegance")
    print(f"   Quality: Luxurious magical robes worthy of an archmage")

if __name__ == '__main__':
    create_wizard_robe()