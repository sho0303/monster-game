#!/usr/bin/env python3
"""
Magic Ninja Tabi Generator
Creates a 32x32 pixel art magical ninja tabi in Minecraft style, scaled to 256x256
Matches the art style of create_steel_plate_mail.py
"""

import numpy as np
from PIL import Image

def create_magic_ninja_tabi():
    # Canvas setup
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Magic ninja tabi color palette (dark stealth colors with magical accents)
    DARK_BLACK = np.array([15, 15, 20, 255], dtype=np.uint8)      # Deep black fabric
    BLACK = np.array([30, 30, 35, 255], dtype=np.uint8)          # Base tabi color
    GRAY = np.array([50, 55, 60, 255], dtype=np.uint8)           # Tabi highlights
    LIGHT_GRAY = np.array([80, 85, 90, 255], dtype=np.uint8)     # Fabric highlights
    PURPLE_GLOW = np.array([100, 50, 150, 255], dtype=np.uint8)  # Magical purple glow
    BLUE_MAGIC = np.array([40, 80, 180, 255], dtype=np.uint8)    # Blue magical energy
    SILVER_THREAD = np.array([150, 155, 160, 255], dtype=np.uint8) # Silver stitching
    SHADOW_BLACK = np.array([8, 8, 12, 255], dtype=np.uint8)     # Deepest shadows
    
    # Transparent background
    canvas[:, :] = [0, 0, 0, 0]
    
    # NINJA TABI MAIN STRUCTURE (split-toe design)
    
    # Left foot tabi (positioned on left side)
    left_tabi = {
        # Ankle area
        8: list(range(5, 12)),     # Ankle opening
        9: list(range(4, 13)),     # Upper ankle
        10: list(range(4, 13)),    # Mid ankle
        11: list(range(4, 13)),    # Lower ankle
        
        # Foot main body
        12: list(range(3, 14)),    # Upper foot
        13: list(range(3, 14)),    # Mid-upper foot
        14: list(range(3, 14)),    # Mid foot
        15: list(range(3, 14)),    # Lower foot
        16: list(range(3, 14)),    # Foot body
        17: list(range(3, 14)),    # Lower foot body
        
        # Toe area (split design)
        18: list(range(4, 13)),    # Toe area start
        19: [4, 5, 6, 7] + [10, 11, 12],  # Split toes (big toe + other toes)
        20: [5, 6] + [10, 11],     # Toe tips
        21: [5, 6] + [10, 11],     # Toe ends
    }
    
    # Right foot tabi (positioned on right side)
    right_tabi = {
        # Ankle area
        8: list(range(20, 27)),    # Ankle opening
        9: list(range(19, 28)),    # Upper ankle
        10: list(range(19, 28)),   # Mid ankle
        11: list(range(19, 28)),   # Lower ankle
        
        # Foot main body
        12: list(range(18, 29)),   # Upper foot
        13: list(range(18, 29)),   # Mid-upper foot
        14: list(range(18, 29)),   # Mid foot
        15: list(range(18, 29)),   # Lower foot
        16: list(range(18, 29)),   # Foot body
        17: list(range(18, 29)),   # Lower foot body
        
        # Toe area (split design)
        18: list(range(19, 28)),   # Toe area start
        19: [19, 20, 21] + [24, 25, 26, 27],  # Split toes (big toe + other toes)
        20: [20, 21] + [25, 26],   # Toe tips
        21: [20, 21] + [25, 26],   # Toe ends
    }
    
    # Fill both tabi with base black color
    for y, x_coords in left_tabi.items():
        for x in x_coords:
            if 0 <= x < size and 0 <= y < size:
                canvas[y][x] = BLACK
    
    for y, x_coords in right_tabi.items():
        for x in x_coords:
            if 0 <= x < size and 0 <= y < size:
                canvas[y][x] = BLACK
    
    # FABRIC TEXTURE AND SEAMS
    
    # Left tabi seams and stitching
    left_seams = [
        # Vertical seams
        (range(9, 18), 8),     # Main side seam
        (range(12, 18), 6),    # Inner seam
        
        # Horizontal seams
        (11, range(4, 13)),    # Ankle seam
        (17, range(4, 13)),    # Foot bottom seam
        
        # Toe separation seam
        (18, 8), (18, 9),      # Toe split seam
        (19, 8), (20, 8),      # Continuing split
    ]
    
    # Right tabi seams and stitching
    right_seams = [
        # Vertical seams
        (range(9, 18), 23),    # Main side seam
        (range(12, 18), 25),   # Inner seam
        
        # Horizontal seams
        (11, range(19, 28)),   # Ankle seam
        (17, range(19, 28)),   # Foot bottom seam
        
        # Toe separation seam
        (18, 23), (18, 24),    # Toe split seam
        (19, 23), (20, 23),    # Continuing split
    ]
    
    # Apply seams with dark stitching
    for coord in left_seams + right_seams:
        if isinstance(coord[0], range):  # Vertical seam
            y_range, x = coord
            for y in y_range:
                if 0 <= x < size and 0 <= y < size:
                    canvas[y][x] = DARK_BLACK
        elif isinstance(coord[1], range):  # Horizontal seam
            y, x_range = coord
            for x in x_range:
                if 0 <= x < size and 0 <= y < size:
                    canvas[y][x] = DARK_BLACK
        else:  # Single point seam
            y, x = coord
            if 0 <= x < size and 0 <= y < size:
                canvas[y][x] = DARK_BLACK
    
    # MAGICAL NINJA SYMBOLS AND RUNES
    
    # Left tabi magical symbols
    left_magic_symbols = [
        # Ninja clan symbol (stylized)
        (10, 8), (10, 9),      # Symbol top
        (11, 7), (11, 8), (11, 9), (11, 10),  # Symbol body
        (12, 8), (12, 9),      # Symbol bottom
        
        # Magic runes along foot
        (14, 6), (14, 10),     # Side runes
        (16, 7), (16, 9),      # Lower runes
    ]
    
    # Right tabi magical symbols
    right_magic_symbols = [
        # Ninja clan symbol (stylized)
        (10, 23), (10, 24),    # Symbol top
        (11, 22), (11, 23), (11, 24), (11, 25),  # Symbol body
        (12, 23), (12, 24),    # Symbol bottom
        
        # Magic runes along foot
        (14, 21), (14, 25),    # Side runes
        (16, 22), (16, 24),    # Lower runes
    ]
    
    # Apply magical symbols with purple glow
    for y, x in left_magic_symbols + right_magic_symbols:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = PURPLE_GLOW
    
    # STEALTH ENHANCEMENT DETAILS
    
    # Magical silence padding (sole enhancement)
    left_sole_magic = [
        (18, 5), (18, 7), (18, 9), (18, 11),    # Sole magic points
        (19, 6), (19, 12),                       # Toe magic points
    ]
    
    right_sole_magic = [
        (18, 20), (18, 22), (18, 24), (18, 26), # Sole magic points
        (19, 20), (19, 26),                      # Toe magic points
    ]
    
    # Apply sole magic with blue energy
    for y, x in left_sole_magic + right_sole_magic:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = BLUE_MAGIC
    
    # FABRIC HIGHLIGHTS AND TEXTURE
    
    # Left tabi highlights
    left_highlights = [
        # Ankle highlights
        (9, 5), (9, 11),       # Ankle edges
        (10, 6), (10, 10),     # Upper foot highlights
        
        # Foot body highlights
        (13, 4), (13, 12),     # Side highlights
        (15, 5), (15, 11),     # Mid-foot highlights
        (17, 6), (17, 10),     # Lower highlights
    ]
    
    # Right tabi highlights
    right_highlights = [
        # Ankle highlights
        (9, 20), (9, 26),      # Ankle edges
        (10, 21), (10, 25),    # Upper foot highlights
        
        # Foot body highlights
        (13, 19), (13, 27),    # Side highlights
        (15, 20), (15, 26),    # Mid-foot highlights
        (17, 21), (17, 25),    # Lower highlights
    ]
    
    # Apply fabric highlights
    for y, x in left_highlights + right_highlights:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = GRAY
    
    # Bright fabric highlights (light reflection)
    bright_highlights = [
        # Left tabi bright spots
        (10, 7), (13, 8), (15, 9),
        
        # Right tabi bright spots
        (10, 22), (13, 23), (15, 24),
    ]
    
    for y, x in bright_highlights:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = LIGHT_GRAY
    
    # SILVER STITCHING DETAILS
    
    # Decorative silver stitching
    silver_stitching = [
        # Left tabi silver details
        (9, 7), (9, 9),        # Ankle silver stitching
        (12, 5), (12, 11),     # Side silver stitching
        (16, 6), (16, 8),      # Lower silver stitching
        
        # Right tabi silver details
        (9, 22), (9, 24),      # Ankle silver stitching
        (12, 20), (12, 26),    # Side silver stitching
        (16, 23), (16, 25),    # Lower silver stitching
        
        # Toe reinforcement stitching
        (19, 7), (19, 11),     # Left toe stitching
        (19, 21), (19, 25),    # Right toe stitching
    ]
    
    for y, x in silver_stitching:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = SILVER_THREAD
    
    # DEEP SHADOWS AND DEPTH
    
    # Deep fabric shadows
    deep_shadows = [
        # Left tabi shadows
        (11, 5), (11, 11),     # Ankle shadows
        (14, 4), (14, 12),     # Foot shadows
        (17, 5), (17, 11),     # Bottom shadows
        (19, 9),               # Toe split shadow
        
        # Right tabi shadows
        (11, 20), (11, 26),    # Ankle shadows
        (14, 19), (14, 27),    # Foot shadows
        (17, 20), (17, 26),    # Bottom shadows
        (19, 24),              # Toe split shadow
    ]
    
    for y, x in deep_shadows:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = SHADOW_BLACK
    
    # MAGICAL AURA EFFECTS
    
    # Subtle magical aura around the tabi
    magical_aura = [
        # Left tabi aura
        (8, 6), (8, 10),       # Ankle aura
        (12, 3), (12, 13),     # Side aura
        (18, 4), (18, 12),     # Bottom aura
        
        # Right tabi aura
        (8, 21), (8, 25),      # Ankle aura
        (12, 18), (12, 28),    # Side aura
        (18, 19), (18, 27),    # Bottom aura
    ]
    
    for y, x in magical_aura:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = PURPLE_GLOW
    
    # NINJA STEALTH ENHANCEMENTS
    
    # Magical silence runes (small)
    silence_runes = [
        # Left foot silence magic
        (15, 7), (15, 9),      # Silence symbols
        
        # Right foot silence magic
        (15, 22), (15, 24),    # Silence symbols
    ]
    
    for y, x in silence_runes:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = BLUE_MAGIC
    
    # Convert to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up using nearest neighbor for crisp pixels
    scale = 8
    img_scaled = img.resize((size * scale, size * scale), Image.NEAREST)
    
    # Save image
    output_path = 'magic_ninja_tabi.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {size * scale}x{size * scale} pixels")
    print(f"   Style: Minecraft-style pixel art magical ninja tabi")
    print(f"   Materials: Black stealth fabric, silver stitching, magical threads")
    print(f"   Details: Split-toe design, ninja clan symbols, mystical runes")
    print(f"   Features: 3D depth, magical aura, stealth enhancements")
    print(f"   Magic: Purple glow effects, blue silence magic, silver threading")
    print(f"   Quality: Legendary ninja footwear with magical stealth properties")

if __name__ == '__main__':
    create_magic_ninja_tabi()