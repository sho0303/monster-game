#!/usr/bin/env python3
"""
Kraken Monster Art Generator - Creates pixel art for the legendary kraken sea monster
Inspired by massive octopus-like creatures with tentacles and ancient power
Creates both regular and attack versions of the kraken
Base resolution: 64x64, scaled to 256x256 (4x)
"""

import numpy as np
from PIL import Image
import os

def create_kraken_art():
    """Create regular kraken pixel art at 64x64 resolution"""
    # Create a 64x64 canvas (doubled from 32x32)
    size = 64
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette for kraken (deep sea monster)
    BLACK = [0, 0, 0, 255]
    WHITE = [255, 255, 255, 255]
    BODY_DARK = [40, 20, 60, 255]         # Dark purple main body
    BODY_MID = [50, 25, 70, 255]          # Mid-tone body
    BODY_SHADOW = [20, 10, 30, 255]       # Darker body shading
    TENTACLE_PURPLE = [60, 30, 80, 255]   # Purple tentacles
    TENTACLE_MID = [50, 25, 65, 255]      # Mid tentacle tone
    TENTACLE_DARK = [35, 15, 45, 255]     # Dark tentacle shading
    SUCKER_PINK = [200, 120, 140, 255]    # Pink sucker cups
    SUCKER_LIGHT = [220, 140, 160, 255]   # Light sucker highlight
    SUCKER_DARK = [150, 80, 100, 255]     # Dark sucker shading
    EYE_RED = [200, 50, 50, 255]          # Menacing red eyes
    EYE_GLOW = [255, 100, 100, 255]       # Eye glow
    EYE_DARK = [120, 30, 30, 255]         # Eye shadow
    BEAK_YELLOW = [220, 200, 120, 255]    # Yellowish beak
    BEAK_LIGHT = [240, 220, 140, 255]     # Beak highlight
    BEAK_DARK = [180, 160, 80, 255]       # Beak shading
    WATER_BLUE = [0, 80, 120, 255]        # Deep water
    WATER_FOAM = [180, 220, 240, 255]     # Water foam
    BARNACLE = [160, 140, 120, 255]       # Ancient barnacles
    BARNACLE_DARK = [120, 100, 80, 255]   # Barnacle shadow
    
    # Main body (bulbous head/mantle) - larger and more detailed
    for y in range(12, 38):
        for x in range(20, 44):
            # Create oval shape for the mantle
            center_x, center_y = 32, 25
            if ((x - center_x) ** 2 / 144 + (y - center_y) ** 2 / 196) <= 1:
                # Base color
                canvas[y, x] = BODY_DARK
                # Add shading layers for depth
                if x >= center_x + 4:
                    canvas[y, x] = BODY_SHADOW
                elif x >= center_x + 2:
                    canvas[y, x] = BODY_MID
                if y >= center_y + 6:
                    canvas[y, x] = BODY_SHADOW
                elif y >= center_y + 3:
                    if canvas[y, x][0] == BODY_DARK[0]:
                        canvas[y, x] = BODY_MID
    
    # Eyes (large and menacing) - more detailed
    # Left eye
    for y in range(18, 28):
        for x in range(24, 32):
            eye_center_x, eye_center_y = 28, 23
            distance = ((x - eye_center_x) ** 2 + (y - eye_center_y) ** 2)
            if distance <= 16:  # Eye white/red area
                canvas[y, x] = EYE_RED
                # Eye highlight
                if distance <= 4 and x <= eye_center_x and y <= eye_center_y:
                    canvas[y, x] = EYE_GLOW
                # Pupil
                if distance <= 6 and x >= eye_center_x and y >= eye_center_y:
                    canvas[y, x] = BLACK
                # Eye shadow
                if x >= eye_center_x + 2 or y >= eye_center_y + 2:
                    if canvas[y, x][0] == EYE_RED[0]:
                        canvas[y, x] = EYE_DARK
    
    # Right eye
    for y in range(18, 28):
        for x in range(32, 40):
            eye_center_x, eye_center_y = 36, 23
            distance = ((x - eye_center_x) ** 2 + (y - eye_center_y) ** 2)
            if distance <= 16:
                canvas[y, x] = EYE_RED
                if distance <= 4 and x >= eye_center_x and y <= eye_center_y:
                    canvas[y, x] = EYE_GLOW
                if distance <= 6 and x <= eye_center_x and y >= eye_center_y:
                    canvas[y, x] = BLACK
                if x <= eye_center_x - 2 or y >= eye_center_y + 2:
                    if canvas[y, x][0] == EYE_RED[0]:
                        canvas[y, x] = EYE_DARK
    
    # Beak/mouth (sharp and dangerous) - more detailed
    beak_center_x, beak_center_y = 32, 30
    for y in range(28, 34):
        for x in range(29, 35):
            if abs(x - beak_center_x) + abs(y - beak_center_y) <= 4:
                canvas[y, x] = BEAK_YELLOW
                # Add highlights and shadows
                if x <= beak_center_x and y <= beak_center_y:
                    canvas[y, x] = BEAK_LIGHT
                elif x >= beak_center_x + 1 or y >= beak_center_y + 1:
                    canvas[y, x] = BEAK_DARK
    
    # Helper function to draw thick tentacle with suckers
    def draw_tentacle(points, thickness=3, sucker_spacing=6):
        for i, (y, x) in enumerate(points):
            for dy in range(-thickness//2, thickness//2 + 1):
                for dx in range(-thickness//2, thickness//2 + 1):
                    ny, nx = y + dy, x + dx
                    if 0 <= nx < size and 0 <= ny < size:
                        # Base tentacle color
                        canvas[ny, nx] = TENTACLE_PURPLE
                        # Add shading on edges
                        if abs(dy) == thickness//2 or abs(dx) == thickness//2:
                            canvas[ny, nx] = TENTACLE_DARK
                        elif abs(dy) <= 1 and abs(dx) <= 1:
                            canvas[ny, nx] = TENTACLE_MID
                        
                        # Add suckers at intervals
                        if i % sucker_spacing == 0 and abs(dy) <= 1 and abs(dx) <= 1:
                            if dy == 0 and dx == 0:
                                canvas[ny, nx] = SUCKER_LIGHT
                            else:
                                canvas[ny, nx] = SUCKER_PINK
    
    # Tentacle 1 (top-left)
    # Tentacle 1 (top-left, curving upward)
    tentacle_1 = [(36, 16), (38, 14), (40, 12), (42, 10), (44, 8), (46, 6), (48, 4), (50, 2)]
    draw_tentacle(tentacle_1, thickness=4)
    
    # Tentacle 2 (top-right, curving upward)
    tentacle_2 = [(36, 48), (38, 50), (40, 52), (42, 54), (44, 56), (46, 58), (48, 60), (50, 62)]
    draw_tentacle(tentacle_2, thickness=4)
    
    # Tentacle 3 (left side, extending outward)
    tentacle_3 = [(32, 12), (34, 10), (36, 8), (38, 6), (40, 4), (42, 2), (44, 1)]
    draw_tentacle(tentacle_3, thickness=4)
    
    # Tentacle 4 (right side, extending outward)
    tentacle_4 = [(32, 52), (34, 54), (36, 56), (38, 58), (40, 60), (42, 62), (44, 63)]
    draw_tentacle(tentacle_4, thickness=4)
    
    # Tentacle 5 (bottom-left, curving downward)
    tentacle_5 = [(40, 20), (42, 18), (44, 16), (46, 14), (48, 12), (50, 10), (52, 8), (54, 6)]
    draw_tentacle(tentacle_5, thickness=4)
    
    # Tentacle 6 (bottom-right, curving downward)
    tentacle_6 = [(40, 44), (42, 46), (44, 48), (46, 50), (48, 52), (50, 54), (52, 56), (54, 58)]
    draw_tentacle(tentacle_6, thickness=4)
    
    # Tentacle 7 (bottom center-left)
    tentacle_7 = [(40, 28), (44, 26), (48, 24), (52, 22), (56, 20), (60, 18), (62, 16)]
    draw_tentacle(tentacle_7, thickness=4)
    
    # Tentacle 8 (bottom center-right)
    tentacle_8 = [(40, 36), (44, 38), (48, 40), (52, 42), (56, 44), (60, 46), (62, 48)]
    draw_tentacle(tentacle_8, thickness=4)
    
    # Ancient barnacles on the body (showing age and power)
    barnacle_clusters = [
        (20, 28), (20, 29), (21, 28),
        (24, 36), (24, 37), (25, 36),
        (28, 24), (28, 25), (29, 24),
        (32, 38), (32, 39), (33, 38),
        (36, 26), (36, 27), (37, 26)
    ]
    for y, x in barnacle_clusters:
        if 0 <= x < size and 0 <= y < size:
            if canvas[y, x][3] == 0 or canvas[y, x][0] in [BODY_DARK[0], BODY_MID[0]]:
                canvas[y, x] = BARNACLE
                # Add shadow to barnacles
                if y + 1 < size:
                    if canvas[y+1, x][0] in [BODY_DARK[0], BODY_MID[0]]:
                        canvas[y+1, x] = BARNACLE_DARK
    
    # Water effects around the creature (splash and foam)
    water_splash_points = [
        (10, 16), (10, 48), (8, 24), (8, 40),
        (54, 12), (54, 52), (56, 8), (56, 56),
        (58, 4), (58, 60), (60, 0), (60, 63),
        (11, 18), (11, 46), (9, 22), (9, 42)
    ]
    for y, x in water_splash_points:
        if 0 <= x < size and 0 <= y < size:
            if canvas[y, x][3] == 0:  # Only draw on empty spaces
                canvas[y, x] = WATER_FOAM
    
    return canvas

def create_kraken_attack_art():
    """Create attack version of kraken pixel art at 64x64 resolution"""
    # Create a 64x64 canvas
    size = 64
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Enhanced color palette for attack mode
    BLACK = [0, 0, 0, 255]
    WHITE = [255, 255, 255, 255]
    BODY_DARK = [40, 20, 60, 255]
    BODY_MID = [50, 25, 70, 255]
    BODY_SHADOW = [20, 10, 30, 255]
    TENTACLE_PURPLE = [80, 40, 100, 255]    # Darker, more aggressive
    TENTACLE_MID = [65, 30, 80, 255]
    TENTACLE_DARK = [45, 20, 55, 255]
    SUCKER_PINK = [220, 140, 160, 255]      # Brighter, more visible
    SUCKER_LIGHT = [240, 160, 180, 255]
    SUCKER_DARK = [170, 100, 120, 255]
    EYE_RED = [255, 0, 0, 255]              # Brighter, more menacing
    EYE_GLOW = [255, 150, 150, 255]         # Glowing with rage
    EYE_DARK = [150, 0, 0, 255]
    BEAK_YELLOW = [240, 220, 140, 255]
    BEAK_LIGHT = [255, 240, 160, 255]
    BEAK_DARK = [200, 180, 100, 255]
    WHIRLPOOL = [0, 60, 100, 255]           # Dark swirling water
    FOAM_VIOLENT = [255, 255, 255, 255]     # Violent white foam
    LIGHTNING = [255, 255, 200, 255]        # Electric effects
    VENOM = [100, 255, 100, 255]            # Toxic green
    VENOM_DARK = [60, 180, 60, 255]
    
    # Main body (more aggressive posture, slightly larger)
    for y in range(10, 36):
        for x in range(18, 46):
            center_x, center_y = 32, 23
            if ((x - center_x) ** 2 / 196 + (y - center_y) ** 2 / 256) <= 1:
                canvas[y, x] = BODY_DARK
                if x >= center_x + 6:
                    canvas[y, x] = BODY_SHADOW
                elif x >= center_x + 3:
                    canvas[y, x] = BODY_MID
                if y >= center_y + 8:
                    canvas[y, x] = BODY_SHADOW
                elif y >= center_y + 4:
                    if canvas[y, x][0] == BODY_DARK[0]:
                        canvas[y, x] = BODY_MID
    
    # Eyes (glowing with fury) - larger and more intense
    # Left eye
    for y in range(16, 28):
        for x in range(22, 33):
            eye_center_x, eye_center_y = 27, 22
            distance = ((x - eye_center_x) ** 2 + (y - eye_center_y) ** 2)
            if distance <= 25:  # Larger eye
                canvas[y, x] = EYE_RED
                # Intense glow
                if distance <= 9 and x <= eye_center_x and y <= eye_center_y:
                    canvas[y, x] = EYE_GLOW
                # Larger pupil
                if distance <= 12 and x >= eye_center_x and y >= eye_center_y:
                    canvas[y, x] = BLACK
                # Eye shadow
                if x >= eye_center_x + 3 or y >= eye_center_y + 3:
                    if canvas[y, x][0] == EYE_RED[0]:
                        canvas[y, x] = EYE_DARK
    
    # Right eye
    for y in range(16, 28):
        for x in range(31, 42):
            eye_center_x, eye_center_y = 37, 22
            distance = ((x - eye_center_x) ** 2 + (y - eye_center_y) ** 2)
            if distance <= 25:
                canvas[y, x] = EYE_RED
                if distance <= 9 and x >= eye_center_x and y <= eye_center_y:
                    canvas[y, x] = EYE_GLOW
                if distance <= 12 and x <= eye_center_x and y >= eye_center_y:
                    canvas[y, x] = BLACK
                if x <= eye_center_x - 3 or y >= eye_center_y + 3:
                    if canvas[y, x][0] == EYE_RED[0]:
                        canvas[y, x] = EYE_DARK
    
    # Beak (opened wide for attack) - larger and more detailed
    beak_center_x, beak_center_y = 32, 28
    for y in range(25, 33):
        for x in range(27, 37):
            if abs(x - beak_center_x) + abs(y - beak_center_y) <= 6:
                canvas[y, x] = BEAK_YELLOW
                if x <= beak_center_x - 1 and y <= beak_center_y:
                    canvas[y, x] = BEAK_LIGHT
                elif x >= beak_center_x + 2 or y >= beak_center_y + 2:
                    canvas[y, x] = BEAK_DARK
    
    # Venom dripping from beak - more detailed
    venom_drips = [
        (33, 30), (34, 31), (35, 32), (36, 31),
        (33, 34), (34, 33), (35, 32), (36, 33),
        (37, 32), (38, 33), (39, 32)
    ]
    for y, x in venom_drips:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = VENOM
            if y < size - 1:
                canvas[y+1, x] = VENOM_DARK
    
    # Helper function for attack tentacles - thicker and more aggressive
    def draw_attack_tentacle(points, thickness=5, add_lightning=False):
        for i, (y, x) in enumerate(points):
            for dy in range(-thickness//2, thickness//2 + 1):
                for dx in range(-thickness//2, thickness//2 + 1):
                    ny, nx = y + dy, x + dx
                    if 0 <= nx < size and 0 <= ny < size:
                        canvas[ny, nx] = TENTACLE_PURPLE
                        if abs(dy) == thickness//2 or abs(dx) == thickness//2:
                            canvas[ny, nx] = TENTACLE_DARK
                        elif abs(dy) <= 2 and abs(dx) <= 2:
                            canvas[ny, nx] = TENTACLE_MID
                        
                        # Glowing suckers in attack mode
                        if i % 4 == 0 and abs(dy) <= 1 and abs(dx) <= 1:
                            if dy == 0 and dx == 0:
                                canvas[ny, nx] = SUCKER_LIGHT
                            else:
                                canvas[ny, nx] = SUCKER_PINK
                        
                        # Add lightning effect
                        if add_lightning and i % 6 == 0 and dy == 0 and dx == 0:
                            canvas[ny, nx] = LIGHTNING
    
    # Aggressive striking tentacles (raised for attack)
    # Tentacle 1 (striking upward left)
    strike_1 = [(36, 12), (34, 10), (32, 8), (30, 6), (28, 4), (26, 2), (24, 0)]
    draw_attack_tentacle(strike_1, thickness=5, add_lightning=True)
    
    # Tentacle 2 (striking upward right)
    strike_2 = [(36, 52), (34, 54), (32, 56), (30, 58), (28, 60), (26, 62), (24, 63)]
    draw_attack_tentacle(strike_2, thickness=5, add_lightning=True)
    
    # Tentacle 3 (grasping left)
    grasp_1 = [(30, 14), (32, 12), (34, 10), (36, 8), (38, 6), (40, 4), (42, 2), (44, 0)]
    draw_attack_tentacle(grasp_1, thickness=5)
    
    # Tentacle 4 (grasping right)
    grasp_2 = [(30, 50), (32, 52), (34, 54), (36, 56), (38, 58), (40, 60), (42, 62), (44, 63)]
    draw_attack_tentacle(grasp_2, thickness=5)
    
    # Whirlpool tentacles (bottom, creating vortex)
    whirl_1 = [(38, 24), (42, 22), (46, 20), (50, 18), (54, 16), (58, 14), (62, 12)]
    draw_attack_tentacle(whirl_1, thickness=5)
    
    whirl_2 = [(38, 40), (42, 42), (46, 44), (50, 46), (54, 48), (58, 50), (62, 52)]
    draw_attack_tentacle(whirl_2, thickness=5)
    
    whirl_3 = [(40, 32), (44, 32), (48, 32), (52, 32), (56, 32), (60, 32), (62, 32)]
    draw_attack_tentacle(whirl_3, thickness=5)
    
    whirl_4 = [(40, 28), (44, 30), (48, 28), (52, 26), (56, 24), (60, 22), (62, 20)]
    draw_attack_tentacle(whirl_4, thickness=5)
    
    # Whirlpool effect (showing the kraken's power) - larger and more detailed
    whirlpool_center = (52, 32)
    for radius in range(2, 12, 2):
        for angle in range(0, 360, 20):
            x = int(whirlpool_center[1] + radius * np.cos(np.radians(angle)))
            y = int(whirlpool_center[0] + radius * np.sin(np.radians(angle)))
            if 0 <= x < size and 0 <= y < size:
                if canvas[y, x][3] == 0 or canvas[y, x][0] in [TENTACLE_PURPLE[0], TENTACLE_MID[0]]:
                    if radius % 4 == 0:
                        canvas[y, x] = WHIRLPOOL
                    else:
                        canvas[y, x] = FOAM_VIOLENT
    
    # Lightning crackling around the creature (ancient power) - more extensive
    lightning_strikes = [
        (4, 16), (6, 20), (2, 24), (8, 28),
        (4, 40), (6, 44), (2, 48), (8, 52),
        (0, 32), (2, 36), (4, 30), (6, 34),
        (5, 18), (7, 22), (3, 26), (9, 30),
        (5, 42), (7, 46), (3, 50), (9, 54)
    ]
    for y, x in lightning_strikes:
        if 0 <= x < size and 0 <= y < size:
            if canvas[y, x][3] == 0:
                canvas[y, x] = LIGHTNING
                # Add lightning branches
                if x + 1 < size and canvas[y, x+1][3] == 0:
                    canvas[y, x+1] = LIGHTNING
    
    # Violent water eruption - more dramatic
    eruption_areas = [
        (0, 8), (0, 56), (2, 4), (2, 60),
        (4, 0), (4, 62), (6, 2), (6, 58),
        (62, 4), (62, 60), (60, 0), (60, 62),
        (58, 2), (58, 58), (56, 6), (56, 54),
        (1, 10), (1, 54), (3, 6), (3, 58),
        (5, 2), (5, 60), (7, 4), (7, 56)
    ]
    for y, x in eruption_areas:
        if 0 <= x < size and 0 <= y < size:
            if canvas[y, x][3] == 0:
                canvas[y, x] = FOAM_VIOLENT
    
    return canvas

def save_kraken_art():
    """Generate and save both versions of kraken art"""
    # Create art directory if it doesn't exist
    art_dir = "../art"
    if not os.path.exists(art_dir):
        os.makedirs(art_dir)
    
    # Generate both versions
    kraken_canvas = create_kraken_art()
    kraken_attack_canvas = create_kraken_attack_art()
    
    kraken_img = Image.fromarray(kraken_canvas, 'RGBA')
    kraken_attack_img = Image.fromarray(kraken_attack_canvas, 'RGBA')
    
    # Scale up to 256x256 (4x scale: 64x64 -> 256x256)
    scale_factor = 4
    final_size = (64 * scale_factor, 64 * scale_factor)
    
    # Resize using nearest neighbor to maintain pixel art look
    kraken_img = kraken_img.resize(final_size, Image.Resampling.NEAREST)
    kraken_attack_img = kraken_attack_img.resize(final_size, Image.Resampling.NEAREST)
    
    # Save the images
    kraken_path = os.path.join(art_dir, "kraken_monster.png")
    kraken_attack_path = os.path.join(art_dir, "kraken_monster_attack.png")
    
    kraken_img.save(kraken_path)
    kraken_attack_img.save(kraken_attack_path)
    
    print(f"✅ Regular kraken art saved to: {kraken_path}")
    print(f"✅ Attack kraken art saved to: {kraken_attack_path}")
    print(f"📐 Base resolution: 64x64, Final size: 256x256 (4x scale)")
    
    return kraken_img, kraken_attack_img

if __name__ == "__main__":
    save_kraken_art()