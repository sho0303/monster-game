#!/usr/bin/env python3
"""
Mermaid Monster Art Generator - Creates pixel art for the mermaid monster
Creates both regular and attack versions of the mermaid
"""

import numpy as np
from PIL import Image
import os

def create_mermaid_art():
    """Create regular mermaid pixel art"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette for mermaid
    BLACK = [0, 0, 0, 255]
    WHITE = [255, 255, 255, 255]
    SKIN_LIGHT = [255, 220, 177, 255]     # Light skin tone
    SKIN_MEDIUM = [235, 190, 147, 255]    # Medium skin for shading
    HAIR_BLUE = [0, 150, 200, 255]       # Sea-blue hair
    HAIR_DARK = [0, 100, 150, 255]       # Darker hair shading
    TAIL_TEAL = [0, 200, 180, 255]       # Teal mermaid tail
    TAIL_DARK = [0, 150, 130, 255]       # Darker tail shading
    SCALES_LIGHT = [100, 255, 200, 255]  # Light scale highlights
    SHELL_PINK = [255, 182, 193, 255]    # Shell bra color
    SHELL_DARK = [255, 160, 170, 255]    # Shell bra shading
    PEARL_WHITE = [240, 248, 255, 255]   # Pearl accessories
    WATER_BLUE = [173, 216, 230, 255]    # Water effects
    
    # Head and face (upper body)
    for y in range(6, 14):
        for x in range(13, 19):
            # Oval head shape
            if (x-16)**2/9 + (y-10)**2/16 <= 1:
                canvas[y][x] = SKIN_LIGHT
    
    # Hair (flowing sea-blue hair)
    # Main hair mass
    for y in range(4, 16):
        for x in range(11, 21):
            # Hair shape - flowing around head
            if ((x-16)**2 + (y-8)**2 <= 25 and 
                not ((x-16)**2/9 + (y-10)**2/16 <= 1)):  # Exclude face area
                canvas[y][x] = HAIR_BLUE
    
    # Hair strands and flow
    # Left flowing hair
    for i in range(6):
        canvas[10 + i][10 - i//2] = HAIR_BLUE
        canvas[11 + i][9 - i//2] = HAIR_DARK
    
    # Right flowing hair  
    for i in range(6):
        canvas[10 + i][21 + i//2] = HAIR_BLUE
        canvas[11 + i][22 + i//2] = HAIR_DARK
    
    # Hair highlights and depth
    canvas[6][15] = HAIR_DARK
    canvas[6][16] = HAIR_DARK
    canvas[6][17] = HAIR_DARK
    canvas[7][14] = HAIR_DARK
    canvas[7][18] = HAIR_DARK
    
    # Eyes (ocean-blue eyes)
    canvas[9][14] = BLACK      # Left eye
    canvas[9][17] = BLACK      # Right eye
    canvas[8][14] = WATER_BLUE # Eye highlight
    canvas[8][17] = WATER_BLUE # Eye highlight
    
    # Nose (subtle)
    canvas[10][15] = SKIN_MEDIUM
    canvas[10][16] = SKIN_MEDIUM
    
    # Mouth (small smile)
    canvas[11][15] = BLACK
    canvas[11][16] = BLACK
    
    # Neck and shoulders
    for y in range(13, 16):
        for x in range(14, 18):
            canvas[y][x] = SKIN_LIGHT
    
    # Arms (graceful pose)
    # Left arm (reaching out)
    for i in range(4):
        canvas[15 + i][12 - i] = SKIN_LIGHT
        canvas[16 + i][11 - i] = SKIN_LIGHT
    
    # Right arm (by side)
    for i in range(3):
        canvas[15 + i][19] = SKIN_LIGHT
        canvas[16 + i][20] = SKIN_LIGHT
    
    # Shell bra/top
    canvas[14][14] = SHELL_PINK
    canvas[14][15] = SHELL_PINK
    canvas[14][16] = SHELL_PINK
    canvas[14][17] = SHELL_PINK
    canvas[15][14] = SHELL_DARK
    canvas[15][17] = SHELL_DARK
    
    # Pearl necklace
    canvas[13][15] = PEARL_WHITE
    canvas[13][16] = PEARL_WHITE
    
    # Torso transition to tail
    for y in range(16, 20):
        for x in range(14, 18):
            # Gradual transition from skin to scales
            if y < 18:
                canvas[y][x] = SKIN_MEDIUM
            else:
                canvas[y][x] = TAIL_TEAL
    
    # Mermaid tail (lower body)
    # Main tail body
    for y in range(18, 28):
        tail_width = max(2, 6 - (y - 18) // 2)  # Tapers toward the end
        start_x = 16 - tail_width // 2
        end_x = 16 + tail_width // 2
        
        for x in range(start_x, end_x + 1):
            if 0 <= x < size:
                canvas[y][x] = TAIL_TEAL
    
    # Tail fin (at the bottom)
    fin_y = 27
    # Left fin
    for i in range(4):
        canvas[fin_y + i][12 + i] = TAIL_TEAL
        canvas[fin_y + i][13 + i] = TAIL_DARK
    
    # Right fin
    for i in range(4):
        canvas[fin_y + i][19 - i] = TAIL_TEAL
        canvas[fin_y + i][18 - i] = TAIL_DARK
    
    # Scale pattern on tail
    scale_positions = [
        (19, 15), (19, 17), 
        (21, 14), (21, 16), (21, 18),
        (23, 15), (23, 17),
        (25, 14), (25, 16), (25, 18)
    ]
    
    for scale_y, scale_x in scale_positions:
        if 0 <= scale_x < size and 0 <= scale_y < size:
            canvas[scale_y][scale_x] = SCALES_LIGHT
    
    # Tail shading (left side darker)
    for y in range(18, 28):
        if canvas[y][14][3] == 255:  # If there's tail here
            canvas[y][14] = TAIL_DARK
    
    # Water effects around the mermaid (optional bubbles)
    bubble_positions = [(8, 22), (24, 8), (6, 16), (25, 20)]
    for bub_y, bub_x in bubble_positions:
        if 0 <= bub_x < size and 0 <= bub_y < size:
            canvas[bub_y][bub_x] = WATER_BLUE
    
    return canvas

def create_mermaid_attack_art():
    """Create mermaid attack animation pixel art"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Same color palette as regular mermaid
    BLACK = [0, 0, 0, 255]
    WHITE = [255, 255, 255, 255]
    SKIN_LIGHT = [255, 220, 177, 255]
    SKIN_MEDIUM = [235, 190, 147, 255]
    HAIR_BLUE = [0, 150, 200, 255]
    HAIR_DARK = [0, 100, 150, 255]
    TAIL_TEAL = [0, 200, 180, 255]
    TAIL_DARK = [0, 150, 130, 255]
    SCALES_LIGHT = [100, 255, 200, 255]
    SHELL_PINK = [255, 182, 193, 255]
    SHELL_DARK = [255, 160, 170, 255]
    PEARL_WHITE = [240, 248, 255, 255]
    WATER_BLUE = [173, 216, 230, 255]
    
    # Attack effects
    MAGIC_BLUE = [0, 255, 255, 255]      # Bright cyan magic
    MAGIC_WHITE = [240, 255, 255, 255]    # Bright magic highlights
    WAVE_FOAM = [255, 255, 255, 200]     # Semi-transparent wave foam
    
    # Head and face (similar to regular but more dynamic)
    for y in range(5, 13):
        for x in range(12, 18):
            # Oval head shape - slightly tilted for attack pose
            if (x-15)**2/9 + (y-9)**2/16 <= 1:
                canvas[y][x] = SKIN_LIGHT
    
    # Hair (more dynamic, flowing with magic)
    # Main hair mass with movement
    for y in range(3, 15):
        for x in range(10, 20):
            # Hair shape - more scattered for dynamic look
            if ((x-15)**2 + (y-7)**2 <= 30 and 
                not ((x-15)**2/9 + (y-9)**2/16 <= 1)):
                canvas[y][x] = HAIR_BLUE
    
    # Flowing hair strands (more dramatic)
    # Left flowing hair
    for i in range(8):
        if 9 - i//2 >= 0:
            canvas[9 + i][9 - i//2] = HAIR_BLUE
            canvas[10 + i][8 - i//2] = HAIR_DARK
    
    # Right flowing hair  
    for i in range(8):
        canvas[9 + i][20 + i//2] = HAIR_BLUE
        canvas[10 + i][21 + i//2] = HAIR_DARK
    
    # Eyes (glowing with magic power)
    canvas[8][13] = MAGIC_BLUE    # Left eye - glowing
    canvas[8][16] = MAGIC_BLUE    # Right eye - glowing
    canvas[7][13] = MAGIC_WHITE   # Eye glow
    canvas[7][16] = MAGIC_WHITE   # Eye glow
    
    # Mouth (open in attack cry)
    canvas[10][14] = BLACK
    canvas[10][15] = BLACK
    canvas[11][14] = BLACK
    canvas[11][15] = BLACK
    
    # Neck and shoulders
    for y in range(12, 15):
        for x in range(13, 17):
            canvas[y][x] = SKIN_LIGHT
    
    # Arms (raised for casting magic)
    # Left arm (raised up and forward)
    for i in range(5):
        canvas[13 + i][9 - i//2] = SKIN_LIGHT
        canvas[14 + i][8 - i//2] = SKIN_LIGHT
    
    # Right arm (raised and casting)
    for i in range(4):
        canvas[13 + i][21 + i//2] = SKIN_LIGHT
        canvas[14 + i][22 + i//2] = SKIN_LIGHT
    
    # Shell bra/top
    canvas[13][13] = SHELL_PINK
    canvas[13][14] = SHELL_PINK
    canvas[13][15] = SHELL_PINK
    canvas[13][16] = SHELL_PINK
    canvas[14][13] = SHELL_DARK
    canvas[14][16] = SHELL_DARK
    
    # Pearl necklace (glowing)
    canvas[12][14] = PEARL_WHITE
    canvas[12][15] = PEARL_WHITE
    
    # Torso
    for y in range(15, 19):
        for x in range(13, 17):
            if y < 17:
                canvas[y][x] = SKIN_MEDIUM
            else:
                canvas[y][x] = TAIL_TEAL
    
    # Mermaid tail (curved for swimming attack pose)
    # Main tail body (curved)
    for y in range(17, 27):
        tail_width = max(2, 6 - (y - 17) // 2)
        # Curve the tail to the right for dynamic pose
        curve_offset = (y - 17) // 3
        start_x = 15 - tail_width // 2 + curve_offset
        end_x = 15 + tail_width // 2 + curve_offset
        
        for x in range(start_x, end_x + 1):
            if 0 <= x < size:
                canvas[y][x] = TAIL_TEAL
    
    # Tail fin (curved)
    fin_y = 26
    # Curved fin following tail direction
    for i in range(4):
        if fin_y + i < size:
            # Left fin part
            left_x = 14 + i
            if 0 <= left_x < size:
                canvas[fin_y + i][left_x] = TAIL_TEAL
                canvas[fin_y + i][left_x + 1] = TAIL_DARK
            
            # Right fin part
            right_x = 20 + i
            if 0 <= right_x < size:
                canvas[fin_y + i][right_x] = TAIL_TEAL
                canvas[fin_y + i][right_x - 1] = TAIL_DARK
    
    # Scale highlights
    scale_positions = [
        (18, 14), (18, 16), 
        (20, 15), (20, 17),
        (22, 16), (22, 18),
        (24, 17), (24, 19)
    ]
    
    for scale_y, scale_x in scale_positions:
        if 0 <= scale_x < size and 0 <= scale_y < size:
            canvas[scale_y][scale_x] = SCALES_LIGHT
    
    # MAGIC ATTACK EFFECTS
    # Magic orb in left hand
    magic_orb_positions = [
        (16, 6), (17, 6), (16, 7), (17, 7)  # Magic orb
    ]
    for orb_y, orb_x in magic_orb_positions:
        if 0 <= orb_x < size and 0 <= orb_y < size:
            canvas[orb_y][orb_x] = MAGIC_BLUE
    
    # Magic sparkles around orb
    sparkle_positions = [(15, 5), (18, 5), (15, 8), (18, 8), (16, 4), (17, 9)]
    for spark_y, spark_x in sparkle_positions:
        if 0 <= spark_x < size and 0 <= spark_y < size:
            canvas[spark_y][spark_x] = MAGIC_WHITE
    
    # Water magic swirls
    # Curved magic energy flowing from hands
    for i in range(6):
        # Left side magic stream
        magic_x = 5 + i
        magic_y = 15 + i // 2
        if 0 <= magic_x < size and 0 <= magic_y < size:
            canvas[magic_y][magic_x] = MAGIC_BLUE
        
        # Right side magic stream  
        magic_x2 = 26 - i
        magic_y2 = 13 + i // 2
        if 0 <= magic_x2 < size and 0 <= magic_y2 < size:
            canvas[magic_y2][magic_x2] = MAGIC_BLUE
    
    # Water bubbles and foam effects
    bubble_positions = [(4, 20), (28, 10), (2, 12), (30, 18), (6, 25), (26, 22)]
    for bub_y, bub_x in bubble_positions:
        if 0 <= bub_x < size and 0 <= bub_y < size:
            canvas[bub_y][bub_x] = WATER_BLUE
    
    # Add some wave foam effects
    foam_positions = [(20, 2), (22, 3), (24, 4), (10, 28), (12, 29), (14, 30)]
    for foam_y, foam_x in foam_positions:
        if 0 <= foam_x < size and 0 <= foam_y < size:
            canvas[foam_y][foam_x] = WAVE_FOAM
    
    return canvas

def save_mermaid_art():
    """Generate and save both regular and attack mermaid art"""
    print("Creating mermaid monster art...")
    
    # Create regular mermaid
    mermaid_canvas = create_mermaid_art()
    mermaid_img = Image.fromarray(mermaid_canvas, 'RGBA')
    
    # Create attack mermaid
    mermaid_attack_canvas = create_mermaid_attack_art()
    mermaid_attack_img = Image.fromarray(mermaid_attack_canvas, 'RGBA')
    
    # Scale up for consistency with demon (8x scale: 32x32 -> 256x256)
    scale_factor = 8
    final_size = mermaid_canvas.shape[0] * scale_factor
    
    mermaid_img = mermaid_img.resize((final_size, final_size), Image.NEAREST)
    mermaid_attack_img = mermaid_attack_img.resize((final_size, final_size), Image.NEAREST)
    
    # Save the images
    mermaid_path = "../art/mermaid_monster.png"
    mermaid_attack_path = "../art/mermaid_monster_attack.png"
    
    mermaid_img.save(mermaid_path)
    mermaid_attack_img.save(mermaid_attack_path)
    
    print(f"Regular mermaid art saved to: {mermaid_path}")
    print(f"Attack mermaid art saved to: {mermaid_attack_path}")
    
    return mermaid_img, mermaid_attack_img

if __name__ == "__main__":
    save_mermaid_art()