#!/usr/bin/env python3
"""
Golden Plate Mail Armor Generator
Creates a 32x32 pixel art golden plate mail in Minecraft style, scaled to 256x256
Matches the art style of create_wizard_staff.py
"""

import numpy as np
from PIL import Image

def create_gold_plate_mail():
    # Canvas setup
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Gold color palette (golden metallic tones)
    DARK_GOLD = np.array([120, 80, 20, 255], dtype=np.uint8)      # Dark gold shadows
    GOLD = np.array([200, 150, 50, 255], dtype=np.uint8)          # Base gold color
    LIGHT_GOLD = np.array([255, 200, 80, 255], dtype=np.uint8)    # Gold highlights
    BRIGHT_GOLD = np.array([255, 240, 150, 255], dtype=np.uint8)  # Bright gold shine
    BRONZE = np.array([180, 120, 40, 255], dtype=np.uint8)        # Bronze trim/rivets
    BLACK_GOLD = np.array([80, 50, 15, 255], dtype=np.uint8)      # Deep shadows/gaps
    COPPER = np.array([160, 100, 30, 255], dtype=np.uint8)        # Copper details
    
    # Transparent background
    canvas[:, :] = [0, 0, 0, 0]
    
    # MAIN PLATE MAIL BODY STRUCTURE
    plate_mail_shape = {
        # Shoulders and upper chest (wide)
        6: list(range(10, 23)),   # Shoulder line
        7: list(range(9, 24)),    # Upper shoulder plates
        8: list(range(8, 25)),    # Wide shoulder coverage
        
        # Upper torso plates
        9: list(range(8, 25)),    # Upper chest plates
        10: list(range(8, 25)),   # Chest plate continuation
        11: list(range(8, 25)),   # Mid-upper chest
        12: list(range(8, 25)),   # Lower-upper chest
        
        # Mid torso (main body plates)
        13: list(range(9, 24)),   # Main torso start
        14: list(range(9, 24)),   # Mid torso plates
        15: list(range(9, 24)),   # Core body armor
        16: list(range(9, 24)),   # Central plates
        17: list(range(9, 24)),   # Lower mid torso
        18: list(range(9, 24)),   # Continuing plates
        
        # Lower torso (hip protection)
        19: list(range(10, 23)),  # Lower torso narrowing
        20: list(range(10, 23)),  # Hip plate coverage
        21: list(range(11, 22)),  # Lower hip plates
        22: list(range(12, 21)),  # Lowest torso plates
        
        # Arm coverage (sleeves)
        7: list(range(6, 9)) + list(range(24, 27)),      # Shoulder caps
        8: list(range(5, 10)) + list(range(23, 28)),     # Upper arm plates
        9: list(range(5, 10)) + list(range(23, 28)),     # Mid upper arm
        10: list(range(6, 9)) + list(range(24, 27)),     # Lower upper arm
        11: list(range(6, 9)) + list(range(24, 27)),     # Elbow area
        12: list(range(6, 9)) + list(range(24, 27)),     # Forearm start
        13: list(range(7, 9)) + list(range(24, 26)),     # Mid forearm
        14: list(range(7, 9)) + list(range(24, 26)),     # Lower forearm
        15: list(range(7, 9)) + list(range(24, 26)),     # Wrist area
    }
    
    # Fill the main plate mail body with base gold color
    for y, x_coords in plate_mail_shape.items():
        if isinstance(x_coords, list):
            for x in x_coords:
                if 0 <= x < size and 0 <= y < size:
                    canvas[y][x] = GOLD
    
    # INDIVIDUAL ARMOR PLATES (overlapping plate segments)
    
    # Chest plates (horizontal overlapping segments)
    chest_plates = [
        # Upper chest plate segments
        [(9, range(10, 23)), (10, range(9, 24))],   # Top chest plate
        [(11, range(10, 23)), (12, range(9, 24))],  # Second chest plate
        [(13, range(10, 23)), (14, range(9, 24))],  # Third chest plate
        [(15, range(10, 23)), (16, range(9, 24))],  # Fourth chest plate
        [(17, range(10, 23)), (18, range(9, 24))],  # Lower chest plate
    ]
    
    # Apply plate overlaps with light gold
    for plate_group in chest_plates:
        for y, x_range in plate_group:
            for x in x_range:
                if 0 <= x < size and 0 <= y < size:
                    canvas[y][x] = LIGHT_GOLD
    
    # PLATE BORDERS AND RIVETS
    
    # Horizontal plate separation lines (dark gold)
    plate_borders = [
        # Main horizontal separations
        (10, range(9, 24)),   # First separation
        (12, range(9, 24)),   # Second separation  
        (14, range(9, 24)),   # Third separation
        (16, range(9, 24)),   # Fourth separation
        (18, range(9, 24)),   # Fifth separation
        
        # Vertical plate separations
        (range(9, 19), 11),   # Left vertical line
        (range(9, 19), 16),   # Center vertical line
        (range(9, 19), 21),   # Right vertical line
    ]
    
    for coord in plate_borders:
        if isinstance(coord[0], range):  # Vertical line
            y_range, x = coord
            for y in y_range:
                if 0 <= x < size and 0 <= y < size:
                    canvas[y][x] = DARK_GOLD
        else:  # Horizontal line
            y, x_range = coord
            for x in x_range:
                if 0 <= x < size and 0 <= y < size:
                    canvas[y][x] = DARK_GOLD
    
    # ARMOR RIVETS AND DETAILS
    
    # Rivets at plate intersections (bronze dots)
    rivets = [
        # Corner rivets on each plate
        (9, 10), (9, 16), (9, 22),    # Top row rivets
        (11, 9), (11, 16), (11, 23),  # Second row
        (13, 10), (13, 16), (13, 22), # Third row  
        (15, 9), (15, 16), (15, 23),  # Fourth row
        (17, 10), (17, 16), (17, 22), # Fifth row
        (19, 11), (19, 16), (19, 21), # Lower rivets
        
        # Shoulder rivets
        (7, 8), (7, 24), (8, 6), (8, 26),
        
        # Arm plate rivets
        (10, 7), (10, 25), (12, 7), (12, 25), (14, 7), (14, 25)
    ]
    
    for y, x in rivets:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = BRONZE
    
    # METALLIC HIGHLIGHTS AND SHADING
    
    # Bright highlights (catching light)
    highlights = [
        # Top edge highlights
        (8, 12), (8, 16), (8, 20),    # Shoulder highlights
        (9, 11), (9, 17), (9, 21),    # Chest highlights
        (10, 13), (10, 19),           # Upper torso highlights
        (13, 12), (13, 18),           # Mid torso highlights
        (15, 14), (15, 18),           # Lower highlights
        
        # Plate edge highlights
        (9, 9), (11, 9), (13, 9), (15, 9), (17, 9),      # Left edge
        (9, 23), (11, 23), (13, 23), (15, 23), (17, 23), # Right edge
    ]
    
    for y, x in highlights:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = BRIGHT_GOLD
    
    # Deep shadows and gaps between plates
    shadows = [
        # Gaps between major plates
        (10, 10), (10, 22),  # Under first plate
        (12, 10), (12, 22),  # Under second plate
        (14, 10), (14, 22),  # Under third plate
        (16, 10), (16, 22),  # Under fourth plate
        (18, 10), (18, 22),  # Under fifth plate
        
        # Armpit shadows
        (9, 8), (9, 24), (10, 8), (10, 24),
        
        # Underside shadows
        (19, 12), (19, 20), (20, 13), (20, 19),
    ]
    
    for y, x in shadows:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = BLACK_GOLD
    
    # CHAIN MAIL UNDERNEATH (visible gaps)
    
    # Chain mail pattern in gaps between plates
    chain_mail_spots = [
        # Between chest plates (small chain links visible)
        (11, 12), (11, 20),  # Chain between plates
        (13, 11), (13, 21),  # More chain links
        (15, 13), (15, 19),  # Additional chain
        (17, 12), (17, 20),  # Lower chain links
        
        # Shoulder joint chain mail
        (8, 9), (8, 23), (9, 9), (9, 23),
        
        # Arm joint chain mail
        (11, 8), (11, 24), (13, 8), (13, 24),
    ]
    
    for y, x in chain_mail_spots:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = COPPER
    
    # DECORATIVE ELEMENTS
    
    # Central chest emblem/heraldic design
    emblem = [
        (10, 15), (10, 16), (10, 17),  # Top of emblem
        (11, 14), (11, 15), (11, 16), (11, 17), (11, 18),  # Emblem body
        (12, 15), (12, 16), (12, 17),  # Bottom of emblem
    ]
    
    for y, x in emblem:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = BRONZE
    
    # SHOULDER PAULDRONS (additional armor pieces)
    
    # Left shoulder pauldron
    left_pauldron = [
        (6, 11), (6, 12),     # Top edge
        (7, 10), (7, 11), (7, 12), (7, 13),  # Main pauldron
        (8, 10), (8, 11), (8, 12), (8, 13),  # Lower pauldron
    ]
    
    # Right shoulder pauldron  
    right_pauldron = [
        (6, 20), (6, 21),     # Top edge
        (7, 19), (7, 20), (7, 21), (7, 22),  # Main pauldron
        (8, 19), (8, 20), (8, 21), (8, 22),  # Lower pauldron
    ]
    
    for y, x in left_pauldron + right_pauldron:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = LIGHT_GOLD
    
    # Pauldron highlights
    pauldron_highlights = [(6, 11), (6, 20), (7, 11), (7, 21)]
    for y, x in pauldron_highlights:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = BRIGHT_GOLD
    
    # Convert to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up using nearest neighbor for crisp pixels
    scale = 8
    img_scaled = img.resize((size * scale, size * scale), Image.NEAREST)
    
    # Save image
    output_path = 'gold_plate_mail.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {size * scale}x{size * scale} pixels")
    print(f"   Style: Minecraft-style pixel art golden plate mail")
    print(f"   Materials: Gold plates, copper chain mail, bronze rivets")
    print(f"   Details: Overlapping plates, golden shading, pauldrons")
    print(f"   Features: 3D depth, realistic armor segments, heraldic emblem")
    print(f"   Protection: Full torso coverage with articulated joints")
    print(f"   Quality: Luxurious golden plate armor with chain backing")

if __name__ == '__main__':
    create_gold_plate_mail()