#!/usr/bin/env python3
"""
Wizard's Hat Generator
Creates a 32x32 pixel art wizard's hat in Minecraft style, scaled to 256x256
Matches the art style of create_steel_plate_mail.py
"""

import numpy as np
from PIL import Image

def create_wizard_hat():
    # Canvas setup
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Wizard hat color palette (mystical blue and purple tones)
    DARK_BLUE = np.array([20, 30, 80, 255], dtype=np.uint8)       # Dark hat shadows
    BLUE = np.array([40, 60, 120, 255], dtype=np.uint8)          # Base hat color
    LIGHT_BLUE = np.array([80, 100, 160, 255], dtype=np.uint8)   # Hat highlights
    BRIGHT_BLUE = np.array([120, 140, 200, 255], dtype=np.uint8) # Bright hat shine
    GOLD_STAR = np.array([200, 150, 50, 255], dtype=np.uint8)    # Golden stars/trim
    DEEP_SHADOW = np.array([10, 15, 40, 255], dtype=np.uint8)    # Deep fabric shadows
    SILVER_MOON = np.array([180, 180, 200, 255], dtype=np.uint8) # Silver moon/details
    PURPLE_MAGIC = np.array([80, 40, 120, 255], dtype=np.uint8)  # Purple magical accents
    
    # Transparent background
    canvas[:, :] = [0, 0, 0, 0]
    
    # WIZARD HAT MAIN STRUCTURE (classic pointed cone)
    
    # Hat tip (very top point)
    hat_tip = [(3, 16)]
    
    # Upper cone (narrow tapering)
    upper_cone = {
        4: [15, 16, 17],           # Just below tip
        5: [14, 15, 16, 17, 18],   # Expanding
        6: [13, 14, 15, 16, 17, 18, 19],  # Wider
        7: [12, 13, 14, 15, 16, 17, 18, 19, 20],  # Even wider
    }
    
    # Middle cone (main body)
    middle_cone = {
        8: list(range(11, 22)),    # Main cone body
        9: list(range(10, 23)),    # Expanding cone
        10: list(range(9, 24)),    # Wider cone
        11: list(range(8, 25)),    # Even wider
        12: list(range(7, 26)),    # Maximum cone width
        13: list(range(7, 26)),    # Maintaining width
        14: list(range(6, 27)),    # Slight expansion
        15: list(range(6, 27)),    # Pre-brim area
    }
    
    # Hat brim (wide circular base)
    brim = {
        16: list(range(4, 29)),    # Upper brim
        17: list(range(3, 30)),    # Main brim width
        18: list(range(3, 30)),    # Brim thickness
        19: list(range(4, 29)),    # Brim taper
        20: list(range(5, 28)),    # Brim edge
    }
    
    # Fill hat tip
    for y, x in hat_tip:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = BLUE
    
    # Fill upper cone
    for y, x_coords in upper_cone.items():
        for x in x_coords:
            if 0 <= x < size and 0 <= y < size:
                canvas[y][x] = BLUE
    
    # Fill middle cone
    for y, x_coords in middle_cone.items():
        for x in x_coords:
            if 0 <= x < size and 0 <= y < size:
                canvas[y][x] = BLUE
    
    # Fill brim
    for y, x_coords in brim.items():
        for x in x_coords:
            if 0 <= x < size and 0 <= y < size:
                canvas[y][x] = BLUE
    
    # HAT FABRIC FOLDS AND CREASES
    
    # Vertical creases down the cone
    cone_creases = [
        # Major fold lines
        (range(4, 16), 12),   # Left major crease
        (range(4, 16), 16),   # Center line
        (range(4, 16), 20),   # Right major crease
        
        # Minor fold lines
        (range(6, 14), 10),   # Left minor crease
        (range(6, 14), 22),   # Right minor crease
        (range(8, 12), 14),   # Left-center crease
        (range(8, 12), 18),   # Right-center crease
    ]
    
    for coord in cone_creases:
        if isinstance(coord[0], range):  # Vertical crease
            y_range, x = coord
            for y in y_range:
                if 0 <= x < size and 0 <= y < size:
                    canvas[y][x] = DARK_BLUE
    
    # BRIM DETAILS AND STRUCTURE
    
    # Brim edge definition
    brim_edges = [
        (16, 4), (16, 28),     # Brim top corners
        (17, 3), (17, 29),     # Brim side edges
        (18, 3), (18, 29),     # Brim thickness
        (19, 4), (19, 28),     # Brim taper
        (20, 5), (20, 27),     # Brim bottom
    ]
    
    for y, x in brim_edges:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = DARK_BLUE
    
    # Brim underside shadow
    brim_shadow = [
        (18, range(6, 27)),    # Underside shadow line
        (19, range(7, 26)),    # Shadow taper
    ]
    
    for coord in brim_shadow:
        if isinstance(coord[1], range):  # Horizontal shadow
            y, x_range = coord
            for x in x_range:
                if 0 <= x < size and 0 <= y < size:
                    canvas[y][x] = DEEP_SHADOW
    
    # MAGICAL CELESTIAL DECORATIONS
    
    # Golden stars scattered on hat
    golden_stars = [
        # Large stars
        (6, 15), (6, 17),      # Upper stars
        (8, 13), (8, 19),      # Mid-upper stars
        (10, 11), (10, 21),    # Mid stars
        (12, 9), (12, 23),     # Lower stars
        (14, 14), (14, 18),    # Near-brim stars
        
        # Small star accents
        (7, 16),               # Center star
        (9, 15), (9, 17),      # Twin stars
        (11, 13), (11, 19),    # Side stars
        (13, 12), (13, 20),    # Lower twin stars
    ]
    
    for y, x in golden_stars:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = GOLD_STAR
    
    # Silver moons (crescent shapes)
    silver_moons = [
        # Crescent moons
        (5, 14), (5, 18),      # Upper crescents
        (9, 12), (9, 20),      # Mid crescents
        (13, 10), (13, 22),    # Lower crescents
        
        # Moon accents
        (7, 15), (7, 17),      # Small moons
        (11, 14), (11, 18),    # Twin moons
    ]
    
    for y, x in silver_moons:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = SILVER_MOON
    
    # MAGICAL HIGHLIGHTS AND SHIMMER
    
    # Hat fabric highlights (light catching)
    fabric_highlights = [
        # Cone highlights
        (4, 16),               # Tip highlight
        (5, 15), (5, 17),      # Upper highlights
        (7, 13), (7, 19),      # Mid-upper highlights
        (9, 11), (9, 21),      # Mid highlights
        (11, 9), (11, 23),     # Lower highlights
        (13, 8), (13, 24),     # Near-brim highlights
        
        # Brim highlights
        (16, 6), (16, 26),     # Brim edge highlights
        (17, 5), (17, 27),     # Brim side highlights
    ]
    
    for y, x in fabric_highlights:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = LIGHT_BLUE
    
    # Magical shimmer effects
    magic_shimmer = [
        (4, 16),               # Tip magic
        (6, 16),               # Upper shimmer
        (8, 14), (8, 18),      # Mid shimmer
        (10, 12), (10, 20),    # Lower shimmer
        (12, 16),              # Central shimmer
    ]
    
    for y, x in magic_shimmer:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = BRIGHT_BLUE
    
    # DEEP SHADOWS AND FABRIC DEPTH
    
    # Deep creases and shadows
    deep_shadows = [
        # Under major folds
        (5, 12), (5, 20),      # Upper shadows
        (7, 11), (7, 21),      # Mid shadows
        (9, 10), (9, 22),      # Lower shadows
        (11, 8), (11, 24),     # Bottom shadows
        
        # Brim underside
        (17, 7), (17, 25),     # Brim edge shadows
        (18, 8), (18, 24),     # Brim depth
        
        # Fabric depth
        (8, 16),               # Central deep shadow
        (10, 16),              # Lower central shadow
    ]
    
    for y, x in deep_shadows:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = DEEP_SHADOW
    
    # PURPLE MAGICAL ACCENTS
    
    # Purple mystical energy
    purple_accents = [
        # Magical aura around decorations
        (6, 14), (6, 18),      # Around upper stars
        (8, 12), (8, 20),      # Around mid decorations
        (10, 10), (10, 22),    # Around lower decorations
        (12, 15), (12, 17),    # Central magic
        
        # Hat band magical energy
        (15, 12), (15, 20),    # Brim magic
    ]
    
    for y, x in purple_accents:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = PURPLE_MAGIC
    
    # GOLDEN TRIM AND DETAILS
    
    # Golden hat band (around brim connection)
    golden_band = [
        (15, 7), (15, 8), (15, 9), (15, 10), (15, 11),     # Left band
        (15, 21), (15, 22), (15, 23), (15, 24), (15, 25),  # Right band
        (15, 12), (15, 13), (15, 19), (15, 20),            # Band segments
    ]
    
    # Golden brim trim
    brim_trim = [
        (16, 5), (16, 27),     # Brim corner trim
        (17, 4), (17, 28),     # Brim edge trim
        (20, 6), (20, 26),     # Bottom brim trim
    ]
    
    # Apply golden details
    for y, x in golden_band + brim_trim:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = GOLD_STAR
    
    # HAT TIP SPECIAL EFFECT
    
    # Magical energy at tip
    tip_magic = [
        (3, 15), (3, 17),      # Tip glow
        (2, 16),               # Peak energy
    ]
    
    for y, x in tip_magic:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = BRIGHT_BLUE
    
    # Convert to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up using nearest neighbor for crisp pixels
    scale = 8
    img_scaled = img.resize((size * scale, size * scale), Image.NEAREST)
    
    # Save image
    output_path = 'wizard_hat.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {size * scale}x{size * scale} pixels")
    print(f"   Style: Minecraft-style pixel art wizard's hat")
    print(f"   Materials: Mystical blue fabric, golden trim, celestial decorations")
    print(f"   Details: Pointed cone, wide brim, fabric creases, star patterns")
    print(f"   Features: 3D depth, magical shimmer, celestial symbols")
    print(f"   Magic: Golden stars, silver moons, purple energy, tip glow")
    print(f"   Quality: Classic arcane headwear with enchanted decorations")

if __name__ == '__main__':
    create_wizard_hat()