#!/usr/bin/env python3
"""
Magic Shinobi Jacket Generator
Creates a 32x32 pixel art magical shinobi jacket in Minecraft style, scaled to 256x256
Matches the art style of create_steel_plate_mail.py
"""

import numpy as np
from PIL import Image

def create_magic_shinobi_jacket():
    # Canvas setup
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Magic shinobi jacket color palette (dark stealth colors with magical accents)
    DARK_NAVY = np.array([20, 25, 40, 255], dtype=np.uint8)       # Deep navy fabric
    NAVY = np.array([35, 45, 70, 255], dtype=np.uint8)           # Base jacket color
    LIGHT_NAVY = np.array([55, 70, 100, 255], dtype=np.uint8)    # Jacket highlights
    GRAY_BLUE = np.array([70, 80, 110, 255], dtype=np.uint8)     # Light fabric highlights
    PURPLE_MAGIC = np.array([90, 50, 140, 255], dtype=np.uint8)  # Magical purple energy
    SILVER_TRIM = np.array([160, 165, 170, 255], dtype=np.uint8) # Silver details/trim
    GOLD_ACCENT = np.array([180, 140, 60, 255], dtype=np.uint8)  # Golden clan symbols
    SHADOW_BLACK = np.array([12, 15, 25, 255], dtype=np.uint8)   # Deepest shadows
    
    # Transparent background
    canvas[:, :] = [0, 0, 0, 0]
    
    # SHINOBI JACKET MAIN STRUCTURE
    jacket_shape = {
        # Collar and neck area
        6: list(range(14, 19)),    # Collar top
        7: list(range(12, 21)),    # Collar opening
        8: list(range(11, 22)),    # Neck area
        
        # Shoulders and upper torso
        9: list(range(9, 24)),     # Shoulder line
        10: list(range(8, 25)),    # Upper chest
        11: list(range(7, 26)),    # Wide shoulders
        12: list(range(7, 26)),    # Chest area
        
        # Mid torso (jacket body)
        13: list(range(8, 25)),    # Upper jacket body
        14: list(range(8, 25)),    # Mid jacket body
        15: list(range(8, 25)),    # Jacket continuation
        16: list(range(8, 25)),    # Lower jacket body
        17: list(range(8, 25)),    # Jacket lower section
        18: list(range(8, 25)),    # Pre-hem area
        
        # Lower jacket (hip area)
        19: list(range(9, 24)),    # Lower jacket
        20: list(range(9, 24)),    # Hip area
        21: list(range(10, 23)),   # Jacket bottom
        22: list(range(11, 22)),   # Jacket hem
        
        # Long sleeves (shinobi arms)
        9: list(range(4, 9)) + list(range(24, 29)),     # Upper sleeves
        10: list(range(3, 10)) + list(range(23, 30)),   # Mid upper sleeves
        11: list(range(2, 11)) + list(range(22, 31)),   # Wide sleeves
        12: list(range(2, 11)) + list(range(22, 31)),   # Sleeve body
        13: list(range(3, 10)) + list(range(23, 30)),   # Sleeve taper
        14: list(range(3, 10)) + list(range(23, 30)),   # Mid sleeves
        15: list(range(4, 9)) + list(range(24, 29)),    # Lower sleeves
        16: list(range(4, 9)) + list(range(24, 29)),    # Sleeve ends
        17: list(range(5, 8)) + list(range(25, 28)),    # Wrist area
    }
    
    # Fill the main jacket body with base navy color
    for y, x_coords in jacket_shape.items():
        if isinstance(x_coords, list):
            for x in x_coords:
                if 0 <= x < size and 0 <= y < size:
                    canvas[y][x] = NAVY
    
    # JACKET FRONT OPENING AND PANELS
    
    # Front opening (traditional wrap style)
    front_opening = [
        # Left front panel edge
        (range(8, 22), 15),    # Left panel border
        
        # Right front panel edge
        (range(8, 22), 17),    # Right panel border
        
        # Front opening seam
        (range(9, 21), 16),    # Center opening line
    ]
    
    for coord in front_opening:
        if isinstance(coord[0], range):  # Vertical lines
            y_range, x = coord
            for y in y_range:
                if 0 <= x < size and 0 <= y < size:
                    canvas[y][x] = DARK_NAVY
    
    # SHINOBI CLAN SYMBOLS AND EMBLEMS
    
    # Left chest clan symbol
    left_clan_symbol = [
        (10, 12), (10, 13),    # Symbol top
        (11, 11), (11, 12), (11, 13), (11, 14),  # Symbol body
        (12, 12), (12, 13),    # Symbol bottom
    ]
    
    # Right chest clan symbol
    right_clan_symbol = [
        (10, 19), (10, 20),    # Symbol top
        (11, 18), (11, 19), (11, 20), (11, 21),  # Symbol body
        (12, 19), (12, 20),    # Symbol bottom
    ]
    
    # Apply clan symbols with gold accents
    for y, x in left_clan_symbol + right_clan_symbol:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = GOLD_ACCENT
    
    # MAGICAL ENHANCEMENTS AND RUNES
    
    # Protective ward symbols
    ward_symbols = [
        # Upper torso wards
        (9, 11), (9, 21),      # Shoulder wards
        (13, 10), (13, 22),    # Side protection wards
        (16, 12), (16, 20),    # Lower protection wards
        
        # Sleeve ward symbols
        (10, 6), (10, 26),     # Upper sleeve wards
        (12, 5), (12, 27),     # Mid sleeve wards
        (14, 6), (14, 26),     # Lower sleeve wards
    ]
    
    # Apply ward symbols with purple magic
    for y, x in ward_symbols:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = PURPLE_MAGIC
    
    # FABRIC DETAILS AND STITCHING
    
    # Shoulder seams and construction
    shoulder_seams = [
        # Shoulder construction lines
        (9, range(9, 24)),     # Main shoulder seam
        (11, range(7, 26)),    # Shoulder panel seam
        
        # Sleeve attachment seams
        (range(10, 17), 8),    # Left sleeve seam
        (range(10, 17), 24),   # Right sleeve seam
    ]
    
    for coord in shoulder_seams:
        if isinstance(coord[0], range):  # Vertical seam
            y_range, x = coord
            for y in y_range:
                if 0 <= x < size and 0 <= y < size:
                    canvas[y][x] = DARK_NAVY
        elif isinstance(coord[1], range):  # Horizontal seam
            y, x_range = coord
            for x in x_range:
                if 0 <= x < size and 0 <= y < size:
                    canvas[y][x] = DARK_NAVY
    
    # COLLAR AND NECKLINE DETAILS
    
    # Collar construction
    collar_details = [
        # Collar edges
        (6, 14), (6, 18),      # Collar points
        (7, 13), (7, 19),      # Collar sides
        (8, 12), (8, 20),      # Collar base
        
        # Neck opening trim
        (7, 15), (7, 17),      # Neck trim
        (8, 16),               # Center neck
    ]
    
    for y, x in collar_details:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = SILVER_TRIM
    
    # SLEEVE CUFFS AND DETAILS
    
    # Left sleeve cuff
    left_cuff = [
        (16, 5), (16, 6), (16, 7),     # Cuff band
        (17, 5), (17, 6), (17, 7),     # Cuff thickness
    ]
    
    # Right sleeve cuff
    right_cuff = [
        (16, 25), (16, 26), (16, 27),  # Cuff band
        (17, 25), (17, 26), (17, 27),  # Cuff thickness
    ]
    
    # Apply cuffs with silver trim
    for y, x in left_cuff + right_cuff:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = SILVER_TRIM
    
    # FABRIC HIGHLIGHTS AND TEXTURE
    
    # Main fabric highlights
    fabric_highlights = [
        # Chest highlights
        (10, 14), (10, 18),    # Upper chest
        (12, 13), (12, 19),    # Mid chest
        (14, 14), (14, 18),    # Lower chest
        
        # Shoulder highlights
        (9, 12), (9, 20),      # Shoulder peaks
        (11, 10), (11, 22),    # Shoulder edges
        
        # Sleeve highlights
        (10, 7), (10, 25),     # Upper sleeve highlights
        (12, 6), (12, 26),     # Mid sleeve highlights
        (14, 7), (14, 25),     # Lower sleeve highlights
        
        # Back panel highlights
        (16, 11), (16, 21),    # Lower highlights
    ]
    
    for y, x in fabric_highlights:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = LIGHT_NAVY
    
    # Bright fabric reflections
    bright_highlights = [
        (10, 15), (10, 17),    # Chest bright spots
        (11, 16),              # Center bright spot
        (13, 11), (13, 21),    # Side bright spots
    ]
    
    for y, x in bright_highlights:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = GRAY_BLUE
    
    # HIDDEN POCKETS AND UTILITY FEATURES
    
    # Hidden pocket seams (subtle lines)
    hidden_pockets = [
        # Chest pockets (barely visible)
        (14, 11), (14, 12),    # Left chest pocket
        (14, 20), (14, 21),    # Right chest pocket
        
        # Side utility pockets
        (17, 9), (17, 23),     # Side pocket openings
        
        # Inner sleeve pockets
        (13, 4), (13, 28),     # Sleeve pocket hints
    ]
    
    for y, x in hidden_pockets:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = DARK_NAVY
    
    # MAGICAL STEALTH ENHANCEMENTS
    
    # Stealth magic threading
    stealth_magic = [
        # Magic threads in fabric
        (15, 10), (15, 22),    # Lower magic threads
        (18, 12), (18, 20),    # Hem magic threads
        
        # Sleeve stealth enhancement
        (15, 5), (15, 27),     # Sleeve stealth magic
        
        # Collar stealth magic
        (7, 14), (7, 18),      # Collar magic enhancement
    ]
    
    for y, x in stealth_magic:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = PURPLE_MAGIC
    
    # DEEP SHADOWS AND FABRIC DEPTH
    
    # Deep fabric shadows
    deep_shadows = [
        # Under collar shadows
        (8, 13), (8, 19),      # Collar shadows
        
        # Armpit shadows
        (11, 8), (11, 24),     # Underarm shadows
        (12, 7), (12, 25),     # Deep arm shadows
        
        # Front panel shadows
        (15, 15), (15, 17),    # Panel depth shadows
        
        # Hem shadows
        (21, 11), (21, 21),    # Bottom shadows
        
        # Sleeve depth shadows
        (13, 4), (13, 28),     # Sleeve interior shadows
        (16, 4), (16, 28),     # Cuff shadows
    ]
    
    for y, x in deep_shadows:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = SHADOW_BLACK
    
    # MYSTICAL AURA AND ENERGY
    
    # Subtle magical aura around jacket
    magical_aura = [
        # Outer jacket aura
        (8, 10), (8, 22),      # Upper aura
        (13, 7), (13, 25),     # Side aura
        (19, 8), (19, 24),     # Lower aura
        
        # Sleeve magical energy
        (9, 3), (9, 29),       # Sleeve tip aura
        (15, 3), (15, 29),     # Lower sleeve aura
    ]
    
    for y, x in magical_aura:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = PURPLE_MAGIC
    
    # SILVER THREADING AND DECORATIVE ELEMENTS
    
    # Decorative silver threading
    silver_threading = [
        # Decorative patterns
        (12, 14), (12, 18),    # Chest decorations
        (16, 13), (16, 19),    # Lower decorations
        
        # Functional silver elements
        (18, 11), (18, 21),    # Hem reinforcement
        (9, 16),               # Collar center
        
        # Sleeve decorative threading
        (11, 5), (11, 27),     # Sleeve decoration
        (15, 6), (15, 26),     # Cuff decoration
    ]
    
    for y, x in silver_threading:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = SILVER_TRIM
    
    # Convert to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up using nearest neighbor for crisp pixels
    scale = 8
    img_scaled = img.resize((size * scale, size * scale), Image.NEAREST)
    
    # Save image
    output_path = 'magic_shinobi_jacket.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {size * scale}x{size * scale} pixels")
    print(f"   Style: Minecraft-style pixel art magical shinobi jacket")
    print(f"   Materials: Navy stealth fabric, silver trim, magical threading")
    print(f"   Details: Traditional wrap front, clan symbols, hidden pockets")
    print(f"   Features: 3D depth, magical aura, stealth enhancements")
    print(f"   Magic: Purple ward symbols, gold clan emblems, silver threading")
    print(f"   Quality: Legendary ninja garment with mystical stealth properties")

if __name__ == '__main__':
    create_magic_shinobi_jacket()