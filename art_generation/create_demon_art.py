#!/usr/bin/env python3
"""
Demon Monster Art Generator - Creates pixel art for the demon monster
Creates both regular and attack versions of the demon
"""

import numpy as np
from PIL import Image
import os

def create_demon_art():
    """Create regular demon pixel art"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette for demon
    BLACK = [0, 0, 0, 255]
    WHITE = [255, 255, 255, 255]
    RED = [220, 20, 20, 255]
    DARK_RED = [139, 0, 0, 255]
    FLAME_RED = [255, 69, 0, 255]
    FLAME_ORANGE = [255, 140, 0, 255]
    FLAME_YELLOW = [255, 215, 0, 255]
    DARK_SKIN = [101, 67, 33, 255]
    HORN = [64, 64, 64, 255]
    GRAY = [128, 128, 128, 255]
    
    # Head (dark skin)
    for y in range(8, 16):
        for x in range(12, 20):
            if (x-16)**2 + (y-12)**2 <= 16:  # Circular head
                canvas[y][x] = DARK_SKIN
    
    # Horns (curved upward)
    # Left horn
    canvas[6][13] = HORN
    canvas[5][13] = HORN
    canvas[4][12] = HORN
    canvas[3][11] = HORN
    # Right horn  
    canvas[6][18] = HORN
    canvas[5][18] = HORN
    canvas[4][19] = HORN
    canvas[3][20] = HORN
    
    # Eyes (glowing red)
    canvas[10][14] = RED
    canvas[10][17] = RED
    canvas[11][14] = FLAME_RED
    canvas[11][17] = FLAME_RED
    
    # Evil grin (showing fangs)
    canvas[13][14] = BLACK  # Mouth
    canvas[13][15] = BLACK
    canvas[13][16] = BLACK  
    canvas[13][17] = BLACK
    # Fangs
    canvas[14][14] = WHITE
    canvas[14][17] = WHITE
    
    # Body (muscular torso)
    for y in range(16, 26):
        for x in range(10, 22):
            canvas[y][x] = DARK_SKIN
    
    # Muscular definition (darker shading)
    for y in range(18, 24):
        canvas[y][12] = BLACK  # Left muscle line
        canvas[y][19] = BLACK  # Right muscle line
    
    # Arms (powerful)
    # Left arm
    for y in range(18, 24):
        canvas[y][8] = DARK_SKIN
        canvas[y][9] = DARK_SKIN
    # Right arm  
    for y in range(18, 24):
        canvas[y][22] = DARK_SKIN
        canvas[y][23] = DARK_SKIN
    
    # Clawed hands
    # Left claws
    canvas[22][6] = GRAY
    canvas[23][6] = GRAY
    canvas[22][7] = GRAY
    canvas[23][7] = GRAY
    # Right claws
    canvas[22][24] = GRAY
    canvas[23][24] = GRAY
    canvas[22][25] = GRAY  
    canvas[23][25] = GRAY
    
    # Legs
    for y in range(26, 30):
        for x in range(12, 16):  # Left leg
            canvas[y][x] = DARK_SKIN
        for x in range(16, 20):  # Right leg
            canvas[y][x] = DARK_SKIN
    
    # Hooves (dark)
    for x in range(12, 16):
        canvas[30][x] = BLACK
        canvas[31][x] = BLACK
    for x in range(16, 20):
        canvas[30][x] = BLACK
        canvas[31][x] = BLACK
    
    # Tail (whipping behind)
    canvas[20][24] = DARK_SKIN
    canvas[19][25] = DARK_SKIN
    canvas[18][26] = DARK_SKIN
    canvas[17][27] = DARK_SKIN
    canvas[16][28] = DARK_SKIN
    # Tail tip (spaded)
    canvas[15][29] = DARK_RED
    canvas[14][29] = DARK_RED
    
    # Flame aura around the demon (subtle glow)
    # Left side flames
    canvas[12][10] = FLAME_YELLOW
    canvas[15][9] = FLAME_ORANGE
    canvas[18][8] = FLAME_RED
    # Right side flames  
    canvas[12][21] = FLAME_YELLOW
    canvas[15][22] = FLAME_ORANGE
    canvas[18][23] = FLAME_RED
    
    return canvas

def create_demon_attack_art():
    """Create demon attack animation pixel art"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette for demon attack
    BLACK = [0, 0, 0, 255]
    WHITE = [255, 255, 255, 255]
    RED = [220, 20, 20, 255]
    DARK_RED = [139, 0, 0, 255]
    FLAME_RED = [255, 69, 0, 255]
    FLAME_ORANGE = [255, 140, 0, 255]
    FLAME_YELLOW = [255, 215, 0, 255]
    DARK_SKIN = [101, 67, 33, 255]
    HORN = [64, 64, 64, 255]
    GRAY = [128, 128, 128, 255]
    
    # Attack effect colors
    FIRE_BLAST = [255, 100, 0, 200]     # Semi-transparent fire
    ENERGY_GLOW = [255, 0, 0, 180]      # Red energy
    HELLFIRE = [255, 69, 0, 220]        # Intense hellfire
    
    # Head (leaning forward in attack pose)
    for y in range(6, 14):
        for x in range(10, 18):
            if (x-14)**2 + (y-10)**2 <= 16:
                canvas[y][x] = DARK_SKIN
    
    # Horns (more prominent in attack)
    # Left horn
    canvas[4][11] = HORN
    canvas[3][11] = HORN
    canvas[2][10] = HORN
    canvas[1][9] = HORN
    # Right horn  
    canvas[4][16] = HORN
    canvas[3][16] = HORN
    canvas[2][17] = HORN
    canvas[1][18] = HORN
    
    # Eyes (blazing with fury)
    canvas[8][12] = FLAME_RED
    canvas[8][15] = FLAME_RED
    canvas[9][12] = FLAME_YELLOW
    canvas[9][15] = FLAME_YELLOW
    
    # Snarling mouth with visible fangs
    canvas[11][12] = BLACK
    canvas[11][13] = BLACK
    canvas[11][14] = BLACK
    canvas[11][15] = BLACK
    # Large fangs
    canvas[12][12] = WHITE
    canvas[12][15] = WHITE
    canvas[13][12] = WHITE
    canvas[13][15] = WHITE
    
    # Body (crouched in attack position)
    for y in range(14, 22):
        for x in range(8, 20):
            canvas[y][x] = DARK_SKIN
    
    # Arms extended forward (attacking)
    # Left arm reaching out
    for y in range(16, 20):
        for x in range(4, 8):
            canvas[y][x] = DARK_SKIN
    # Right arm reaching out
    for y in range(16, 20):
        for x in range(20, 24):
            canvas[y][x] = DARK_SKIN
    
    # Massive claws (enlarged for attack)
    # Left claws
    canvas[18][2] = GRAY
    canvas[19][2] = GRAY
    canvas[18][3] = GRAY
    canvas[19][3] = GRAY
    canvas[20][1] = GRAY
    canvas[20][2] = GRAY
    # Right claws
    canvas[18][28] = GRAY
    canvas[19][28] = GRAY
    canvas[18][29] = GRAY
    canvas[19][29] = GRAY
    canvas[20][29] = GRAY
    canvas[20][30] = GRAY
    
    # Legs (powerful stance)
    for y in range(22, 28):
        for x in range(10, 14):  # Left leg
            canvas[y][x] = DARK_SKIN
        for x in range(14, 18):  # Right leg
            canvas[y][x] = DARK_SKIN
    
    # Hooves
    for x in range(10, 14):
        canvas[28][x] = BLACK
        canvas[29][x] = BLACK
    for x in range(14, 18):
        canvas[28][x] = BLACK
        canvas[29][x] = BLACK
    
    # Tail (lashing violently)
    canvas[18][22] = DARK_SKIN
    canvas[17][24] = DARK_SKIN
    canvas[16][26] = DARK_SKIN
    canvas[15][28] = DARK_SKIN
    canvas[14][30] = DARK_SKIN
    # Tail tip
    canvas[13][31] = DARK_RED
    
    # HELLFIRE ATTACK EFFECTS!
    # Fire breath/energy blast from mouth
    for x in range(16, 24):
        canvas[11][x] = FLAME_YELLOW
        canvas[12][x] = FLAME_ORANGE
        canvas[13][x] = FLAME_RED
    
    # Flame aura (intense during attack)
    # Left side intense flames
    canvas[10][6] = FLAME_YELLOW
    canvas[12][5] = FLAME_ORANGE
    canvas[14][4] = FLAME_RED
    canvas[16][3] = FIRE_BLAST
    # Right side intense flames
    canvas[10][21] = FLAME_YELLOW  
    canvas[12][22] = FLAME_ORANGE
    canvas[14][23] = FLAME_RED
    canvas[16][24] = FIRE_BLAST
    
    # Energy radiating from claws
    canvas[17][1] = ENERGY_GLOW
    canvas[18][0] = HELLFIRE
    canvas[17][30] = ENERGY_GLOW
    canvas[18][31] = HELLFIRE
    
    # Ground fire where hooves touch
    canvas[30][12] = FLAME_RED
    canvas[31][12] = FLAME_ORANGE
    canvas[30][16] = FLAME_RED  
    canvas[31][16] = FLAME_ORANGE
    
    return canvas

def save_images():
    """Generate and save both demon images"""
    # Create art directory if it doesn't exist
    art_dir = "../art"
    if not os.path.exists(art_dir):
        os.makedirs(art_dir)
    
    # Generate and save regular demon
    demon_canvas = create_demon_art()
    demon_img = Image.fromarray(demon_canvas, 'RGBA')
    
    # Scale up 8x for consistency with other monsters (32x32 -> 256x256)
    scale = 8
    size = 32
    demon_img_scaled = demon_img.resize((size * scale, size * scale), Image.NEAREST)
    demon_img_scaled.save(f"{art_dir}/demon_monster.png")
    print(f"✅ Created: {art_dir}/demon_monster.png (256x256)")
    
    # Generate and save demon attack
    demon_attack_canvas = create_demon_attack_art()
    demon_attack_img = Image.fromarray(demon_attack_canvas, 'RGBA')
    
    # Scale up 8x for consistency with other monsters (32x32 -> 256x256)
    demon_attack_img_scaled = demon_attack_img.resize((size * scale, size * scale), Image.NEAREST)
    demon_attack_img_scaled.save(f"{art_dir}/demon_monster_attack.png")
    print(f"✅ Created: {art_dir}/demon_monster_attack.png (256x256)")

if __name__ == "__main__":
    print("🔥 Generating Demon Monster Art...")
    save_images()
    print("🔥 Demon art generation complete!")