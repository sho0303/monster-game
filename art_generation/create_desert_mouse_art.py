#!/usr/bin/env python3
"""
Desert Mouse Monster Art Generator
Creates pixel art for a desert mouse creature
Based on the jerboa/desert mouse with large ears and long tail
"""

import numpy as np
from PIL import Image
import os

def create_desert_mouse_art():
    """Create desert mouse pixel art"""
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette - sandy desert colors
    SAND_TAN = [210, 180, 140, 255]      # Light sandy body
    DARK_TAN = [160, 130, 90, 255]       # Darker fur shading
    CREAM = [245, 222, 179, 255]         # Belly/lighter areas
    BLACK = [0, 0, 0, 255]               # Eyes, nose, whiskers
    PINK = [255, 182, 193, 255]          # Inner ears, nose
    WHITE = [255, 255, 255, 255]         # Eye highlights, teeth
    DARK_BROWN = [101, 67, 33, 255]      # Tail tip, feet details
    
    # Body (round, compact)
    for y in range(14, 24):
        for x in range(10, 22):
            canvas[y][x] = SAND_TAN
    
    # Belly (lighter cream color)
    for y in range(18, 24):
        for x in range(12, 20):
            canvas[y][x] = CREAM
    
    # Back shading (darker)
    for y in range(14, 19):
        for x in range(11, 21):
            canvas[y][x] = DARK_TAN
    
    # Head (large relative to body - cute)
    for y in range(8, 18):
        for x in range(16, 26):
            canvas[y][x] = SAND_TAN
    
    # Cheeks (slightly rounded)
    canvas[15][15] = SAND_TAN
    canvas[16][15] = SAND_TAN
    canvas[15][26] = SAND_TAN
    canvas[16][26] = SAND_TAN
    
    # Snout/nose area
    for y in range(14, 17):
        for x in range(24, 27):
            canvas[y][x] = DARK_TAN
    
    # Pink nose
    canvas[15][26] = PINK
    canvas[16][26] = PINK
    
    # Large ears (characteristic of desert mice)
    # Left ear
    for y in range(4, 12):
        for x in range(14, 18):
            canvas[y][x] = SAND_TAN
    # Inner ear (pink)
    for y in range(6, 11):
        for x in range(15, 17):
            canvas[y][x] = PINK
    
    # Right ear
    for y in range(4, 12):
        for x in range(22, 26):
            canvas[y][x] = SAND_TAN
    # Inner ear (pink)
    for y in range(6, 11):
        for x in range(23, 25):
            canvas[y][x] = PINK
    
    # Large eyes (big and dark for night vision)
    # Left eye
    canvas[11][18] = BLACK
    canvas[11][19] = BLACK
    canvas[12][18] = BLACK
    canvas[12][19] = BLACK
    # Eye highlight
    canvas[11][19] = WHITE
    
    # Right eye
    canvas[11][22] = BLACK
    canvas[11][23] = BLACK
    canvas[12][22] = BLACK
    canvas[12][23] = BLACK
    # Eye highlight
    canvas[11][22] = WHITE
    
    # Whiskers (thin black lines)
    canvas[14][27] = BLACK
    canvas[14][28] = BLACK
    canvas[15][28] = BLACK
    canvas[16][28] = BLACK
    canvas[14][13] = BLACK
    canvas[14][12] = BLACK
    
    # Small teeth
    canvas[17][24] = WHITE
    canvas[17][25] = WHITE
    
    # Long hind legs (powerful for jumping)
    # Back leg (bent, ready to jump)
    for y in range(20, 28):
        canvas[y][9] = DARK_TAN
        canvas[y][10] = DARK_TAN
    
    # Front legs (small)
    for y in range(22, 26):
        canvas[y][18] = DARK_TAN
        canvas[y][19] = DARK_TAN
    
    # Feet/paws (darker)
    canvas[27][9] = DARK_BROWN
    canvas[27][10] = DARK_BROWN
    canvas[25][18] = DARK_BROWN
    canvas[25][19] = DARK_BROWN
    
    # Long tail (thin, with tuft at end)
    # Tail base
    canvas[20][8] = DARK_TAN
    canvas[21][7] = DARK_TAN
    canvas[22][6] = SAND_TAN
    canvas[23][5] = SAND_TAN
    canvas[24][4] = SAND_TAN
    canvas[25][3] = SAND_TAN
    canvas[26][2] = SAND_TAN
    canvas[27][1] = SAND_TAN
    
    # Tail tuft (darker, bushy end)
    canvas[27][0] = DARK_BROWN
    canvas[28][0] = DARK_BROWN
    canvas[28][1] = DARK_BROWN
    canvas[26][0] = DARK_BROWN
    
    return canvas

def create_desert_mouse_attack_art():
    """Create desert mouse attack - aggressive jump/lunge"""
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Same color palette
    SAND_TAN = [210, 180, 140, 255]
    DARK_TAN = [160, 130, 90, 255]
    CREAM = [245, 222, 179, 255]
    BLACK = [0, 0, 0, 255]
    PINK = [255, 182, 193, 255]
    WHITE = [255, 255, 255, 255]
    DARK_BROWN = [101, 67, 33, 255]
    SAND_CLOUD = [210, 180, 140, 150]  # Dust from jumping
    
    # Body (mid-jump, angled forward)
    for y in range(10, 20):
        for x in range(8, 20):
            canvas[y][x] = SAND_TAN
    
    # Belly
    for y in range(14, 20):
        for x in range(10, 18):
            canvas[y][x] = CREAM
    
    # Back (darker)
    for y in range(10, 15):
        for x in range(9, 19):
            canvas[y][x] = DARK_TAN
    
    # Head (lunging forward)
    for y in range(8, 16):
        for x in range(18, 28):
            canvas[y][x] = SAND_TAN
    
    # Aggressive face - mouth open
    for y in range(12, 15):
        for x in range(26, 29):
            canvas[y][x] = DARK_TAN
    
    # Open mouth (showing teeth)
    canvas[13][27] = BLACK
    canvas[13][28] = BLACK
    canvas[14][27] = BLACK
    
    # Sharp teeth
    canvas[12][26] = WHITE
    canvas[12][27] = WHITE
    canvas[14][26] = WHITE
    canvas[14][27] = WHITE
    
    # Pink nose
    canvas[11][27] = PINK
    canvas[11][28] = PINK
    
    # Ears laid back (aggressive)
    # Left ear
    for y in range(6, 10):
        for x in range(16, 19):
            canvas[y][x] = SAND_TAN
    canvas[7][17] = PINK
    
    # Right ear
    for y in range(5, 9):
        for x in range(24, 27):
            canvas[y][x] = SAND_TAN
    canvas[6][25] = PINK
    
    # Angry eyes (narrowed)
    canvas[9][21] = BLACK
    canvas[9][22] = BLACK
    canvas[10][21] = BLACK
    canvas[9][24] = BLACK
    canvas[9][25] = BLACK
    canvas[10][25] = BLACK
    # Highlights
    canvas[9][22] = WHITE
    canvas[9][24] = WHITE
    
    # Extended claws on front paws
    canvas[16][22] = DARK_BROWN
    canvas[17][22] = DARK_BROWN
    canvas[17][23] = DARK_BROWN
    canvas[18][23] = BLACK
    canvas[18][24] = BLACK
    canvas[18][25] = BLACK
    
    # Powerful hind legs extended (jumping)
    for y in range(18, 26):
        canvas[y][6] = DARK_TAN
        canvas[y][7] = DARK_TAN
    
    # Foot pushing off
    canvas[25][5] = DARK_BROWN
    canvas[25][6] = DARK_BROWN
    canvas[25][7] = DARK_BROWN
    
    # Tail whipping (motion blur effect)
    for x in range(0, 8):
        canvas[20][x] = SAND_TAN
        canvas[21][x] = DARK_TAN
    
    # Tail tuft
    canvas[20][0] = DARK_BROWN
    canvas[21][0] = DARK_BROWN
    canvas[21][1] = DARK_BROWN
    
    # Dust cloud from jump
    canvas[26][4] = SAND_CLOUD
    canvas[26][5] = SAND_CLOUD
    canvas[26][6] = SAND_CLOUD
    canvas[27][5] = SAND_CLOUD
    canvas[27][6] = SAND_CLOUD
    canvas[27][7] = SAND_CLOUD
    canvas[28][6] = SAND_CLOUD
    
    return canvas

def save_desert_mouse_art():
    """Generate and save desert mouse art"""
    print("Creating desert mouse monster art...")
    
    # Create normal pose
    mouse_canvas = create_desert_mouse_art()
    mouse_img = Image.fromarray(mouse_canvas, 'RGBA')
    mouse_scaled = mouse_img.resize((256, 256), Image.NEAREST)
    mouse_scaled.save('art/desert_mouse_monster.png')
    print("✓ Saved art/desert_mouse_monster.png")
    
    # Create attack pose
    attack_canvas = create_desert_mouse_attack_art()
    attack_img = Image.fromarray(attack_canvas, 'RGBA')
    attack_scaled = attack_img.resize((256, 256), Image.NEAREST)
    attack_scaled.save('art/desert_mouse_monster_attack.png')
    print("✓ Saved art/desert_mouse_monster_attack.png")
    
    print("\nDesert Mouse Monster Art Complete!")
    print("Features:")
    print("- Large ears (characteristic of desert rodents)")
    print("- Sandy tan coloring for desert camouflage")
    print("- Big eyes for night vision")
    print("- Long powerful hind legs for jumping")
    print("- Long tail with tuft")
    print("- Attack pose shows aggressive jump/lunge")

if __name__ == '__main__':
    save_desert_mouse_art()
