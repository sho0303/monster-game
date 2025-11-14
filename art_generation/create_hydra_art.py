#!/usr/bin/env python3
"""
Hydra Monster Art Generator - Creates pixel art for the multi-headed hydra
Inspired by mythological multi-headed dragon with serpentine necks
Creates both regular and attack versions of the hydra
Base resolution: 64x64, scaled to 256x256 (4x)
"""

import numpy as np
from PIL import Image
import os
import math

def create_hydra_art():
    """Create regular hydra pixel art at 64x64 resolution"""
    # Create a 64x64 canvas
    size = 64
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette for hydra (golden/tan dragon)
    BLACK = [0, 0, 0, 255]
    WHITE = [255, 255, 255, 255]
    
    # Scale colors (golden/tan)
    SCALE_GOLD = [200, 170, 100, 255]
    SCALE_LIGHT = [230, 200, 130, 255]
    SCALE_DARK = [150, 120, 70, 255]
    SCALE_SHADOW = [100, 80, 50, 255]
    
    # Belly/underbelly (lighter tan)
    BELLY_LIGHT = [240, 210, 160, 255]
    BELLY_MID = [220, 190, 140, 255]
    BELLY_SHADOW = [180, 150, 100, 255]
    
    # Eye colors
    EYE_YELLOW = [255, 230, 0, 255]
    EYE_ORANGE = [255, 150, 0, 255]
    EYE_RED = [200, 50, 0, 255]
    
    # Teeth/claws
    TOOTH_WHITE = [240, 240, 230, 255]
    TOOTH_SHADOW = [180, 180, 170, 255]
    
    # Spine/horn colors
    HORN_TAN = [180, 150, 90, 255]
    HORN_LIGHT = [210, 180, 120, 255]
    HORN_DARK = [130, 100, 60, 255]
    
    # Draw main body (quadruped dragon body)
    body_center_x, body_center_y = 32, 45
    
    # Main torso (large oval)
    for y in range(38, 54):
        for x in range(20, 44):
            # Oval body shape
            if ((x - body_center_x) ** 2 / 144 + (y - body_center_y) ** 2 / 64) <= 1:
                canvas[y, x] = SCALE_GOLD
                # Add shading
                if x >= body_center_x + 6 or y >= body_center_y + 4:
                    canvas[y, x] = SCALE_SHADOW
                elif x >= body_center_x + 3 or y >= body_center_y + 2:
                    canvas[y, x] = SCALE_DARK
                # Highlights
                if x <= body_center_x - 4 and y <= body_center_y - 2:
                    canvas[y, x] = SCALE_LIGHT
    
    # Belly scales (lighter underside)
    for y in range(44, 52):
        for x in range(26, 38):
            if canvas[y, x][0] > 0:
                canvas[y, x] = BELLY_MID
                if y >= 48:
                    canvas[y, x] = BELLY_SHADOW
                elif y <= 46:
                    canvas[y, x] = BELLY_LIGHT
    
    # Four legs (sturdy dragon legs)
    # Front left leg
    front_left = [
        (54, 24), (55, 24), (56, 24),
        (54, 25), (55, 25), (56, 25),
        (57, 25), (58, 25), (59, 25),
        (60, 25), (60, 24), (60, 26)
    ]
    for y, x in front_left:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = SCALE_DARK
            if x == 25:
                canvas[y, x] = SCALE_LIGHT
    
    # Front right leg
    front_right = [
        (54, 38), (55, 38), (56, 38),
        (54, 39), (55, 39), (56, 39),
        (57, 38), (58, 38), (59, 38),
        (60, 38), (60, 37), (60, 39)
    ]
    for y, x in front_right:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = SCALE_DARK
    
    # Back left leg
    back_left = [
        (54, 28), (55, 28), (56, 28),
        (54, 29), (55, 29), (56, 29),
        (57, 29), (58, 29), (59, 29),
        (60, 29), (60, 28), (60, 30)
    ]
    for y, x in back_left:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = SCALE_GOLD
            if y >= 58:
                canvas[y, x] = SCALE_SHADOW
    
    # Back right leg
    back_right = [
        (54, 34), (55, 34), (56, 34),
        (54, 35), (55, 35), (56, 35),
        (57, 34), (58, 34), (59, 34),
        (60, 34), (60, 33), (60, 35)
    ]
    for y, x in back_right:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = SCALE_GOLD
            if y >= 58:
                canvas[y, x] = SCALE_SHADOW
    
    # Tail (thick, powerful tail)
    tail_points = [
        (48, 16), (49, 16), (50, 16),
        (48, 17), (49, 17), (50, 17), (51, 17),
        (50, 18), (51, 18), (52, 18),
        (52, 19), (53, 19), (54, 19),
        (54, 20), (55, 20), (56, 20),
        (56, 21), (57, 21), (58, 21),
        (58, 22), (59, 22), (60, 22)
    ]
    for y, x in tail_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = SCALE_DARK
            if x <= 17:
                canvas[y, x] = SCALE_GOLD
    
    # Tail spikes
    tail_spikes = [(48, 15), (50, 15), (52, 17), (54, 18), (56, 19), (58, 20)]
    for y, x in tail_spikes:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = HORN_TAN
            if y > 0:
                canvas[y-1, x] = HORN_LIGHT
    
    # Helper function to draw a dragon head with neck
    def draw_head(base_y, base_x, neck_points, head_direction='up'):
        # Draw neck (serpentine)
        for i, (ny, nx) in enumerate(neck_points):
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    py, px = ny + dy, nx + dx
                    if 0 <= px < size and 0 <= py < size:
                        if abs(dy) <= 1 and abs(dx) <= 1:
                            canvas[py, px] = SCALE_GOLD
                        else:
                            canvas[py, px] = SCALE_DARK
        
        # Draw head at end of neck
        head_y, head_x = neck_points[-1]
        
        # Head shape (dragon skull)
        for y in range(head_y - 4, head_y + 4):
            for x in range(head_x - 3, head_x + 4):
                if 0 <= x < size and 0 <= y < size:
                    # Oval head
                    if ((x - head_x) ** 2 / 9 + (y - head_y) ** 2 / 16) <= 1:
                        canvas[y, x] = SCALE_LIGHT
                        if y >= head_y + 1:
                            canvas[y, x] = SCALE_GOLD
                        if y >= head_y + 2:
                            canvas[y, x] = SCALE_DARK
        
        # Snout (elongated)
        snout_y, snout_x = head_y + 3, head_x
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                sy, sx = snout_y + dy, snout_x + dx
                if 0 <= sx < size and 0 <= sy < size:
                    if abs(dy) <= 1:
                        canvas[sy, sx] = SCALE_DARK
        
        # Eye (fierce yellow/orange)
        eye_y, eye_x = head_y - 1, head_x + 1 if head_direction == 'right' else head_x - 1
        if 0 <= eye_x < size and 0 <= eye_y < size:
            canvas[eye_y, eye_x] = EYE_YELLOW
            canvas[eye_y, eye_x + 1 if head_direction == 'right' else eye_x - 1] = EYE_ORANGE
            if eye_y - 1 >= 0:
                canvas[eye_y - 1, eye_x] = EYE_RED
        
        # Teeth (sharp fangs)
        teeth = [(snout_y, snout_x - 1), (snout_y, snout_x + 1), (snout_y + 1, snout_x)]
        for ty, tx in teeth:
            if 0 <= tx < size and 0 <= ty < size:
                canvas[ty, tx] = TOOTH_WHITE
        
        # Horns/spikes on head
        horn_points = [(head_y - 4, head_x), (head_y - 3, head_x - 1), (head_y - 3, head_x + 1)]
        for hy, hx in horn_points:
            if 0 <= hx < size and 0 <= hy < size:
                canvas[hy, hx] = HORN_TAN
                if hy - 1 >= 0:
                    canvas[hy - 1, hx] = HORN_LIGHT
    
    # Draw three heads (classic hydra)
    
    # Center head (tallest)
    center_neck = [
        (38, 32), (35, 32), (32, 32), (29, 32), (26, 32), (23, 32), (20, 32), (17, 32)
    ]
    draw_head(38, 32, center_neck, 'up')
    
    # Left head
    left_neck = [
        (40, 28), (38, 26), (36, 24), (34, 22), (32, 20), (30, 18), (28, 17), (26, 16)
    ]
    draw_head(40, 28, left_neck, 'left')
    
    # Right head
    right_neck = [
        (40, 36), (38, 38), (36, 40), (34, 42), (32, 44), (30, 46), (28, 47), (26, 48)
    ]
    draw_head(40, 36, right_neck, 'right')
    
    # Add spine ridges on body
    spine_points = [(40, 32), (42, 32), (44, 32), (46, 32), (48, 31), (50, 30)]
    for sy, sx in spine_points:
        if 0 <= sx < size and 0 <= sy < size:
            canvas[sy, sx] = HORN_TAN
            canvas[sy - 1, sx] = HORN_LIGHT
            if sy + 1 < size:
                canvas[sy + 1, sx] = HORN_DARK
    
    # Add scale texture details
    for y in range(40, 52, 3):
        for x in range(22, 42, 3):
            if 0 <= x < size and 0 <= y < size:
                if canvas[y, x][0] in [SCALE_GOLD[0], SCALE_DARK[0]]:
                    canvas[y, x] = SCALE_LIGHT
    
    return canvas

def create_hydra_attack_art():
    """Create attack version of hydra pixel art at 64x64 resolution"""
    # Create a 64x64 canvas
    size = 64
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Enhanced color palette for attack mode
    BLACK = [0, 0, 0, 255]
    WHITE = [255, 255, 255, 255]
    
    # Scale colors (more vibrant)
    SCALE_GOLD = [220, 180, 110, 255]
    SCALE_LIGHT = [250, 220, 150, 255]
    SCALE_DARK = [170, 130, 80, 255]
    SCALE_SHADOW = [110, 90, 60, 255]
    
    # Belly colors
    BELLY_LIGHT = [250, 220, 170, 255]
    BELLY_MID = [230, 200, 150, 255]
    BELLY_SHADOW = [190, 160, 110, 255]
    
    # Eye colors (glowing with rage)
    EYE_RED = [255, 0, 0, 255]
    EYE_ORANGE = [255, 100, 0, 255]
    EYE_GLOW = [255, 200, 0, 255]
    
    # Fire/energy colors
    FIRE_WHITE = [255, 255, 240, 255]
    FIRE_YELLOW = [255, 220, 0, 255]
    FIRE_ORANGE = [255, 140, 0, 255]
    FIRE_RED = [255, 60, 0, 255]
    FIRE_DARK = [200, 40, 0, 255]
    
    # Teeth colors
    TOOTH_WHITE = [255, 255, 245, 255]
    TOOTH_SHADOW = [200, 200, 190, 255]
    
    # Horn colors
    HORN_TAN = [200, 160, 100, 255]
    HORN_LIGHT = [230, 190, 130, 255]
    HORN_DARK = [150, 110, 70, 255]
    
    # Draw main body (more aggressive stance)
    body_center_x, body_center_y = 32, 46
    
    for y in range(38, 56):
        for x in range(18, 46):
            if ((x - body_center_x) ** 2 / 196 + (y - body_center_y) ** 2 / 81) <= 1:
                canvas[y, x] = SCALE_GOLD
                if x >= body_center_x + 8 or y >= body_center_y + 5:
                    canvas[y, x] = SCALE_SHADOW
                elif x >= body_center_x + 4 or y >= body_center_y + 3:
                    canvas[y, x] = SCALE_DARK
                if x <= body_center_x - 5 and y <= body_center_y - 3:
                    canvas[y, x] = SCALE_LIGHT
    
    # Belly
    for y in range(45, 54):
        for x in range(24, 40):
            if canvas[y, x][0] > 0:
                canvas[y, x] = BELLY_MID
                if y >= 50:
                    canvas[y, x] = BELLY_SHADOW
                elif y <= 47:
                    canvas[y, x] = BELLY_LIGHT
    
    # Legs (in attacking stance)
    # Front legs
    front_left = [
        (56, 22), (57, 22), (58, 22), (59, 22),
        (56, 23), (57, 23), (58, 23), (59, 23),
        (60, 22), (60, 23), (60, 24),
        (61, 23), (61, 24)
    ]
    for y, x in front_left:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = SCALE_DARK
    
    front_right = [
        (56, 40), (57, 40), (58, 40), (59, 40),
        (56, 41), (57, 41), (58, 41), (59, 41),
        (60, 40), (60, 41), (60, 42),
        (61, 41), (61, 42)
    ]
    for y, x in front_right:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = SCALE_DARK
    
    # Back legs
    back_left = [
        (56, 26), (57, 26), (58, 26), (59, 26),
        (56, 27), (57, 27), (58, 27), (59, 27),
        (60, 26), (60, 27), (61, 27)
    ]
    for y, x in back_left:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = SCALE_GOLD
            if y >= 59:
                canvas[y, x] = SCALE_SHADOW
    
    back_right = [
        (56, 36), (57, 36), (58, 36), (59, 36),
        (56, 37), (57, 37), (58, 37), (59, 37),
        (60, 36), (60, 37), (61, 37)
    ]
    for y, x in back_right:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = SCALE_GOLD
            if y >= 59:
                canvas[y, x] = SCALE_SHADOW
    
    # Claws (sharp and visible)
    claw_positions = [(61, 22), (61, 40), (61, 26), (61, 36)]
    for cy, cx in claw_positions:
        if 0 <= cx < size and 0 <= cy < size:
            canvas[cy, cx] = TOOTH_WHITE
            if cy + 1 < size:
                canvas[cy + 1, cx] = TOOTH_SHADOW
    
    # Tail (thrashing)
    tail_points = [
        (48, 14), (49, 14), (50, 14),
        (48, 15), (49, 15), (50, 15), (51, 15),
        (50, 16), (51, 16), (52, 16),
        (52, 17), (53, 17), (54, 17),
        (54, 18), (55, 18), (56, 18),
        (56, 19), (57, 19), (58, 19),
        (58, 20), (59, 20), (60, 20), (61, 20)
    ]
    for y, x in tail_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = SCALE_DARK
    
    # Tail spikes (more prominent)
    tail_spikes = [(47, 14), (48, 13), (50, 14), (52, 15), (54, 16), (56, 17), (58, 18)]
    for y, x in tail_spikes:
        if 0 <= x < size and 0 <= y < size:
            canvas[y, x] = HORN_TAN
            if y > 0:
                canvas[y-1, x] = HORN_LIGHT
    
    # Helper function to draw attacking head with fire breath
    def draw_attack_head(base_y, base_x, neck_points, breath_direction='down'):
        # Draw neck
        for i, (ny, nx) in enumerate(neck_points):
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    py, px = ny + dy, nx + dx
                    if 0 <= px < size and 0 <= py < size:
                        if abs(dy) <= 1 and abs(dx) <= 1:
                            canvas[py, px] = SCALE_GOLD
                        else:
                            canvas[py, px] = SCALE_DARK
        
        # Head
        head_y, head_x = neck_points[-1]
        
        for y in range(head_y - 4, head_y + 5):
            for x in range(head_x - 3, head_x + 4):
                if 0 <= x < size and 0 <= y < size:
                    if ((x - head_x) ** 2 / 9 + (y - head_y) ** 2 / 16) <= 1:
                        canvas[y, x] = SCALE_LIGHT
                        if y >= head_y + 1:
                            canvas[y, x] = SCALE_GOLD
                        if y >= head_y + 3:
                            canvas[y, x] = SCALE_DARK
        
        # Mouth opened wide
        mouth_y, mouth_x = head_y + 4, head_x
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                my, mx = mouth_y + dy, mouth_x + dx
                if 0 <= mx < size and 0 <= my < size:
                    if abs(dy) <= 1 and abs(dx) <= 1:
                        canvas[my, mx] = BLACK  # Open mouth
        
        # Eyes (glowing red)
        eye_y, eye_x = head_y, head_x + 1
        if 0 <= eye_x < size and 0 <= eye_y < size:
            canvas[eye_y, eye_x] = EYE_RED
            canvas[eye_y - 1, eye_x] = EYE_GLOW
        
        eye_x2 = head_x - 1
        if 0 <= eye_x2 < size and 0 <= eye_y < size:
            canvas[eye_y, eye_x2] = EYE_RED
            canvas[eye_y - 1, eye_x2] = EYE_GLOW
        
        # Sharp teeth
        teeth = [
            (mouth_y - 1, mouth_x - 2), (mouth_y - 1, mouth_x - 1),
            (mouth_y - 1, mouth_x + 1), (mouth_y - 1, mouth_x + 2),
            (mouth_y + 2, mouth_x - 1), (mouth_y + 2, mouth_x + 1)
        ]
        for ty, tx in teeth:
            if 0 <= tx < size and 0 <= ty < size:
                canvas[ty, tx] = TOOTH_WHITE
        
        # Fire breath streaming from mouth
        fire_start_y, fire_start_x = mouth_y + 2, mouth_x
        
        # Create fire cone effect
        for i in range(8):
            for spread in range(-i, i+1):
                fy = fire_start_y + i + 2
                fx = fire_start_x + spread
                if 0 <= fx < size and 0 <= fy < size:
                    # Fire gradient
                    if i <= 2:
                        canvas[fy, fx] = FIRE_WHITE
                    elif i <= 4:
                        if abs(spread) <= 1:
                            canvas[fy, fx] = FIRE_YELLOW
                        else:
                            canvas[fy, fx] = FIRE_ORANGE
                    elif i <= 6:
                        if abs(spread) <= 2:
                            canvas[fy, fx] = FIRE_ORANGE
                        else:
                            canvas[fy, fx] = FIRE_RED
                    else:
                        if abs(spread) <= 3:
                            canvas[fy, fx] = FIRE_RED
                        else:
                            canvas[fy, fx] = FIRE_DARK
        
        # Horns (more aggressive)
        horn_points = [
            (head_y - 4, head_x), (head_y - 4, head_x - 1), (head_y - 4, head_x + 1),
            (head_y - 3, head_x - 2), (head_y - 3, head_x + 2)
        ]
        for hy, hx in horn_points:
            if 0 <= hx < size and 0 <= hy < size:
                canvas[hy, hx] = HORN_TAN
                if hy - 1 >= 0:
                    canvas[hy - 1, hx] = HORN_LIGHT
    
    # Draw three heads in attack positions (all breathing fire)
    
    # Center head (forward attack)
    center_neck = [
        (38, 32), (34, 32), (30, 32), (26, 32), (22, 32), (18, 32), (14, 32)
    ]
    draw_attack_head(38, 32, center_neck, 'down')
    
    # Left head (angled attack)
    left_neck = [
        (40, 26), (38, 24), (35, 22), (32, 20), (29, 18), (26, 17), (23, 16)
    ]
    draw_attack_head(40, 26, left_neck, 'left')
    
    # Right head (angled attack)
    right_neck = [
        (40, 38), (38, 40), (35, 42), (32, 44), (29, 46), (26, 47), (23, 48)
    ]
    draw_attack_head(40, 38, right_neck, 'right')
    
    # Enhanced spine ridges (standing up in aggression)
    spine_points = [(39, 32), (41, 32), (43, 32), (45, 32), (47, 31), (49, 30), (51, 29)]
    for sy, sx in spine_points:
        if 0 <= sx < size and 0 <= sy < size:
            canvas[sy, sx] = HORN_TAN
            canvas[sy - 1, sx] = HORN_LIGHT
            if sy - 2 >= 0:
                canvas[sy - 2, sx] = HORN_LIGHT
            if sy + 1 < size:
                canvas[sy + 1, sx] = HORN_DARK
    
    # Add scale texture
    for y in range(40, 54, 3):
        for x in range(20, 44, 3):
            if 0 <= x < size and 0 <= y < size:
                if canvas[y, x][0] in [SCALE_GOLD[0], SCALE_DARK[0]]:
                    canvas[y, x] = SCALE_LIGHT
    
    # Add fire embers around the scene
    ember_positions = [
        (30, 10), (32, 8), (28, 12), (34, 11),
        (30, 54), (32, 56), (28, 52), (34, 53),
        (40, 50), (42, 48), (38, 52)
    ]
    for ey, ex in ember_positions:
        if 0 <= ex < size and 0 <= ey < size:
            if canvas[ey, ex][3] == 0:
                canvas[ey, ex] = FIRE_ORANGE
    
    return canvas

def save_hydra_art():
    """Generate and save both versions of hydra art"""
    # Create art directory if it doesn't exist
    art_dir = "../art"
    if not os.path.exists(art_dir):
        os.makedirs(art_dir)
    
    # Generate both versions
    hydra_canvas = create_hydra_art()
    hydra_attack_canvas = create_hydra_attack_art()
    
    hydra_img = Image.fromarray(hydra_canvas, 'RGBA')
    hydra_attack_img = Image.fromarray(hydra_attack_canvas, 'RGBA')
    
    # Scale up to 256x256 (4x scale: 64x64 -> 256x256)
    scale_factor = 4
    final_size = (64 * scale_factor, 64 * scale_factor)
    
    # Resize using nearest neighbor to maintain pixel art look
    hydra_img = hydra_img.resize(final_size, Image.Resampling.NEAREST)
    hydra_attack_img = hydra_attack_img.resize(final_size, Image.Resampling.NEAREST)
    
    # Save the images
    hydra_path = os.path.join(art_dir, "hydra_monster.png")
    hydra_attack_path = os.path.join(art_dir, "hydra_monster_attack.png")
    
    hydra_img.save(hydra_path)
    hydra_attack_img.save(hydra_attack_path)
    
    print(f"✅ Regular hydra art saved to: {hydra_path}")
    print(f"✅ Attack hydra art saved to: {hydra_attack_path}")
    print(f"📐 Base resolution: 64x64, Final size: 256x256 (4x scale)")
    print(f"🐉 Style: Pixel art multi-headed dragon with golden scales and serpentine necks")
    
    return hydra_img, hydra_attack_img

if __name__ == "__main__":
    save_hydra_art()
