#!/usr/bin/env python3
"""Ocean Monster Art Generators - All 4 ocean monsters"""
import numpy as np
from PIL import Image
import os


def create_shark_art():
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    GRAY = [128, 128, 128, 255]
    DARK_GRAY = [80, 80, 80, 255]
    WHITE = [255, 255, 255, 255]
    BLACK = [0, 0, 0, 255]
    BLUE = [70, 130, 180, 100]  # Water
    
    # Body (streamlined shark shape)
    for y in range(12, 20):
        for x in range(6, 26):
            if (x-16)**2//4 + (y-16)**2 <= 16:
                canvas[y][x] = GRAY
    
    # Head (pointed)
    for y in range(14, 18):
        for x in range(22, 28):
            canvas[y][x] = GRAY
    
    # Snout
    canvas[15][28] = DARK_GRAY
    canvas[16][28] = DARK_GRAY
    canvas[15][29] = DARK_GRAY
    
    # Eye (cold, predatory)
    canvas[14][24] = BLACK
    canvas[14][25] = BLACK
    
    # Mouth with teeth
    for x in range(25, 29):
        canvas[17][x] = BLACK
    # Sharp teeth
    canvas[16][26] = WHITE
    canvas[16][27] = WHITE
    canvas[18][26] = WHITE
    canvas[18][27] = WHITE
    
    # Dorsal fin
    for y in range(8, 13):
        canvas[y][14] = DARK_GRAY
        canvas[y][15] = DARK_GRAY
    canvas[7][14] = DARK_GRAY
    
    # Side fins
    canvas[16][10] = GRAY
    canvas[17][9] = GRAY
    canvas[17][8] = DARK_GRAY
    canvas[16][18] = GRAY
    canvas[17][19] = GRAY
    
    # Tail
    for y in range(14, 18):
        canvas[y][4] = GRAY
        canvas[y][5] = GRAY
    canvas[12][3] = DARK_GRAY
    canvas[13][3] = DARK_GRAY
    canvas[18][3] = DARK_GRAY
    canvas[19][3] = DARK_GRAY
    
    # Belly (lighter)
    for y in range(16, 19):
        for x in range(12, 22):
            canvas[y][x] = [160, 160, 160, 255]
    
    # Water effects
    for i in range(5):
        canvas[10+i][20+i] = BLUE
    
    return canvas


def create_shark_attack_art():
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    GRAY = [128, 128, 128, 255]
    DARK_GRAY = [80, 80, 80, 255]
    WHITE = [255, 255, 255, 255]
    BLACK = [0, 0, 0, 255]
    RED = [255, 0, 0, 255]
    SPLASH = [135, 206, 250, 180]
    
    # Body lunging
    for y in range(10, 22):
        for x in range(4, 24):
            if (x-14)**2//4 + (y-16)**2 <= 20:
                canvas[y][x] = GRAY
    
    # Head forward (jaws open)
    for y in range(12, 20):
        for x in range(20, 28):
            canvas[y][x] = GRAY
    
    # JAWS OPEN WIDE
    # Upper jaw
    for x in range(24, 30):
        canvas[12][x] = DARK_GRAY
        canvas[13][x] = BLACK  # Mouth
    # Lower jaw
    for x in range(24, 30):
        canvas[19][x] = DARK_GRAY
        canvas[18][x] = BLACK  # Mouth
    
    # TEETH (menacing)
    for x in range(25, 30, 2):
        canvas[14][x] = WHITE
        canvas[15][x] = WHITE
        canvas[17][x] = WHITE
        canvas[16][x] = WHITE
    
    # Eye (intense)
    canvas[13][22] = BLACK
    canvas[13][23] = RED
    
    # Dorsal fin
    for y in range(6, 11):
        canvas[y][12] = DARK_GRAY
        canvas[y][13] = DARK_GRAY
    
    # Tail thrashing
    for y in range(14, 18):
        canvas[y][2] = GRAY
        canvas[y][3] = GRAY
    canvas[10][1] = DARK_GRAY
    canvas[20][1] = DARK_GRAY
    
    # WATER SPLASH EFFECTS
    for x in range(26, 32):
        canvas[8][x] = SPLASH
        canvas[9][x] = SPLASH
        canvas[22][x] = SPLASH
        canvas[23][x] = SPLASH
    
    # Motion lines
    for i in range(3):
        canvas[14+i][0+i] = [100, 100, 100, 100]
    
    return canvas


def create_jellyfish_art():
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    PINK = [255, 192, 203, 200]
    BRIGHT_PINK = [255, 105, 180, 220]
    TENTACLE = [255, 182, 193, 180]
    GLOW = [173, 216, 230, 150]
    
    # Bell/head (translucent dome)
    for y in range(8, 16):
        for x in range(12, 20):
            if (x-16)**2 + (y-12)**2*2 <= 20:
                canvas[y][x] = PINK
    
    # Dome top
    for y in range(6, 10):
        for x in range(14, 18):
            canvas[y][x] = BRIGHT_PINK
    
    # Bioluminescent glow
    canvas[10][15] = GLOW
    canvas[10][16] = GLOW
    canvas[11][15] = GLOW
    canvas[11][16] = GLOW
    
    # Multiple tentacles (flowing)
    tentacles = [
        (13, 16), (14, 16), (15, 16),  # Center
        (13, 14), (14, 13), (15, 12),  # Left
        (13, 18), (14, 19), (15, 20),  # Right
    ]
    
    for y_start, x in tentacles:
        for y in range(y_start, min(y_start + 12, 30)):
            canvas[y][x] = TENTACLE
            # Wave pattern
            if (y - y_start) % 3 == 0:
                canvas[y][x-1] = TENTACLE
            elif (y - y_start) % 3 == 1:
                canvas[y][x+1] = TENTACLE
    
    # More tentacles for swarm effect
    for x in range(10, 22, 3):
        for y in range(16, 28):
            if y % 4 != 0:
                canvas[y][x] = TENTACLE
    
    return canvas


def create_jellyfish_attack_art():
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    PINK = [255, 192, 203, 220]
    BRIGHT_PINK = [255, 105, 180, 240]
    TENTACLE = [255, 182, 193, 200]
    ELECTRIC = [0, 255, 255, 255]
    ZAP = [255, 255, 0, 220]
    
    # Bell (pulsing)
    for y in range(6, 14):
        for x in range(10, 22):
            if (x-16)**2 + (y-10)**2*2 <= 30:
                canvas[y][x] = PINK
    
    # Bright center (electric charge)
    for y in range(8, 12):
        for x in range(14, 18):
            canvas[y][x] = BRIGHT_PINK
    
    # ELECTRIC CHARGE
    canvas[9][15] = ELECTRIC
    canvas[9][16] = ELECTRIC
    canvas[10][15] = ELECTRIC
    canvas[10][16] = ELECTRIC
    
    # Electric aura
    canvas[9][14] = ZAP
    canvas[9][17] = ZAP
    canvas[10][14] = ZAP
    canvas[10][17] = ZAP
    
    # Tentacles (extended, electrified)
    for x in range(8, 24, 2):
        for y in range(14, 30):
            canvas[y][x] = TENTACLE
            # Electric pulses
            if y % 5 == 0:
                canvas[y][x] = ELECTRIC
                canvas[y][x+1] = ZAP
    
    # Lightning bolts from tentacles
    for i in range(4):
        canvas[20+i][6+i] = ELECTRIC
        canvas[20+i][25-i] = ELECTRIC
        canvas[24+i][10+i] = ZAP
        canvas[24+i][21-i] = ZAP
    
    return canvas


def create_sea_serpent_art():
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    TEAL = [0, 128, 128, 255]
    DARK_TEAL = [0, 100, 100, 255]
    GREEN = [46, 139, 87, 255]
    YELLOW = [255, 255, 0, 255]
    BLACK = [0, 0, 0, 255]
    SCALE = [64, 224, 208, 255]
    
    # Serpentine body (long S-curve)
    coords = [
        (8, 28), (10, 27), (12, 26), (14, 25), (16, 24),
        (17, 23), (18, 22), (18, 21), (17, 20), (16, 19),
        (14, 18), (12, 17), (10, 16), (9, 15), (9, 14),
        (10, 13), (12, 12), (14, 11), (16, 10), (18, 9),
        (20, 8), (22, 7)
    ]
    
    for x, y in coords:
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                canvas[y+dy][x+dx] = TEAL
        # Scales
        if len(coords) % 3 == 0:
            canvas[y][x] = SCALE
    
    # Head (dragon-like)
    for y in range(5, 10):
        for x in range(22, 30):
            canvas[y][x] = DARK_TEAL
    
    # Snout
    for y in range(6, 9):
        canvas[y][29] = GREEN
        canvas[y][30] = GREEN
    
    # Eye (fierce)
    canvas[6][25] = YELLOW
    canvas[7][25] = BLACK
    
    # Fins/spines along back
    for i in range(0, len(coords), 4):
        x, y = coords[i]
        canvas[y-2][x] = GREEN
        canvas[y-3][x] = GREEN
    
    # Tail end
    canvas[29][8] = DARK_TEAL
    canvas[30][7] = TEAL
    
    return canvas


def create_sea_serpent_attack_art():
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    TEAL = [0, 128, 128, 255]
    DARK_TEAL = [0, 100, 100, 255]
    GREEN = [46, 139, 87, 255]
    YELLOW = [255, 255, 0, 255]
    WHITE = [255, 255, 255, 255]
    WATER = [135, 206, 250, 180]
    
    # Body coiled
    coords = [
        (6, 24), (8, 22), (10, 20), (12, 18), (14, 16),
        (16, 14), (17, 12), (16, 10), (14, 8)
    ]
    
    for x, y in coords:
        for dx in range(-1, 3):
            for dy in range(-1, 3):
                if 0 <= y+dy < 32 and 0 <= x+dx < 32:
                    canvas[y+dy][x+dx] = TEAL
    
    # Head striking
    for y in range(6, 12):
        for x in range(16, 26):
            canvas[y][x] = DARK_TEAL
    
    # Jaws open
    for x in range(24, 30):
        canvas[8][x] = [0, 0, 0, 255]
    
    # Fangs
    canvas[7][26] = WHITE
    canvas[7][28] = WHITE
    canvas[9][26] = WHITE
    canvas[9][28] = WHITE
    canvas[10][26] = WHITE
    canvas[10][28] = WHITE
    
    # Eye (furious)
    canvas[7][20] = YELLOW
    canvas[7][21] = YELLOW
    
    # Fins erect
    for y in range(4, 8):
        canvas[y][18] = GREEN
        canvas[y][19] = GREEN
    
    # Water spray
    for x in range(26, 32):
        for y in range(4, 8):
            canvas[y][x] = WATER
    
    return canvas


def create_pirate_ghost_art():
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    GHOST = [220, 220, 255, 180]
    DARK_GHOST = [180, 180, 220, 200]
    EYE = [0, 255, 0, 255]  # Eerie green glow
    BLACK = [0, 0, 0, 150]
    HAT = [50, 50, 50, 200]
    GOLD = [255, 215, 0, 255]
    
    # Pirate hat
    for y in range(4, 8):
        for x in range(10, 22):
            canvas[y][x] = HAT
    canvas[4][16] = GOLD  # Skull emblem
    canvas[5][16] = GOLD
    
    # Hat brim
    for x in range(8, 24):
        canvas[8][x] = BLACK
    
    # Ghostly head
    for y in range(9, 15):
        for x in range(12, 20):
            if (x-16)**2 + (y-12)**2 <= 16:
                canvas[y][x] = GHOST
    
    # Glowing eyes
    canvas[11][14] = EYE
    canvas[11][17] = EYE
    canvas[12][14] = EYE
    canvas[12][17] = EYE
    
    # Eye patch
    canvas[11][17] = BLACK
    canvas[12][17] = BLACK
    for x in range(15, 19):
        canvas[10][x] = BLACK
    
    # Ghostly beard
    for y in range(13, 16):
        for x in range(13, 19):
            canvas[y][x] = DARK_GHOST
    
    # Translucent body
    for y in range(15, 28):
        alpha = max(50, 180 - (y - 15) * 8)
        for x in range(11, 21):
            canvas[y][x] = [GHOST[0], GHOST[1], GHOST[2], alpha]
    
    # Ghostly coat
    for y in range(16, 26):
        canvas[y][10] = DARK_GHOST
        canvas[y][21] = DARK_GHOST
    
    # Ethereal hook hand
    canvas[18][8] = [128, 128, 128, 180]
    canvas[19][7] = [128, 128, 128, 180]
    canvas[20][7] = [128, 128, 128, 180]
    
    # Ghostly sword
    for y in range(18, 24):
        canvas[y][23] = [192, 192, 192, 180]
    canvas[17][23] = [255, 255, 255, 180]  # Tip
    
    return canvas


def create_pirate_ghost_attack_art():
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    GHOST = [220, 220, 255, 200]
    DARK_GHOST = [180, 180, 220, 220]
    EYE = [0, 255, 0, 255]
    BLACK = [0, 0, 0, 180]
    HAT = [50, 50, 50, 220]
    SPECTRAL = [100, 255, 100, 150]
    
    # Hat (tilted in action)
    for y in range(6, 10):
        for x in range(8, 20):
            canvas[y][x] = HAT
    
    # Head (menacing)
    for y in range(10, 16):
        for x in range(10, 18):
            canvas[y][x] = GHOST
    
    # Blazing eyes
    canvas[12][12] = EYE
    canvas[12][15] = EYE
    canvas[13][12] = EYE
    canvas[13][15] = EYE
    # Eye trails
    canvas[12][11] = SPECTRAL
    canvas[12][16] = SPECTRAL
    
    # Eye patch
    canvas[12][15] = BLACK
    canvas[13][15] = BLACK
    
    # Body (lunging)
    for y in range(16, 26):
        for x in range(8, 20):
            alpha = max(80, 200 - (y - 16) * 10)
            canvas[y][x] = [GHOST[0], GHOST[1], GHOST[2], alpha]
    
    # Sword slashing
    for i in range(8):
        x = 20 + i
        y = 12 + i
        if x < 32 and y < 32:
            canvas[y][x] = [200, 200, 200, 220]
            canvas[y][x+1] = [255, 255, 255, 180]
    
    # Spectral slash effect
    for i in range(10):
        x = 22 + i
        y = 14 + i
        if x < 32 and y < 32:
            canvas[y][x] = SPECTRAL
    
    # Hook hand extended
    for y in range(18, 22):
        canvas[y][4] = [128, 128, 128, 200]
    canvas[20][2] = [128, 128, 128, 200]
    canvas[21][2] = [128, 128, 128, 200]
    
    return canvas


def save_all_ocean_monsters():
    art_dir = "../art"
    os.makedirs(art_dir, exist_ok=True)
    
    # Shark
    for art_func, name in [
        (create_shark_art, "shark_monster.png"),
        (create_shark_attack_art, "shark_monster_attack.png"),
        (create_jellyfish_art, "jellyfish_monster.png"),
        (create_jellyfish_attack_art, "jellyfish_monster_attack.png"),
        (create_sea_serpent_art, "sea_serpent_monster.png"),
        (create_sea_serpent_attack_art, "sea_serpent_monster_attack.png"),
        (create_pirate_ghost_art, "pirate_ghost_monster.png"),
        (create_pirate_ghost_attack_art, "pirate_ghost_monster_attack.png"),
    ]:
        img = Image.fromarray(art_func(), 'RGBA')
        img = img.resize((256, 256), Image.NEAREST)
        img.save(f"{art_dir}/{name}")
        print(f"✅ Created: {art_dir}/{name}")


if __name__ == "__main__":
    print("🌊 Generating All Ocean Monster Art...")
    save_all_ocean_monsters()
    print("🌊 Complete!")
