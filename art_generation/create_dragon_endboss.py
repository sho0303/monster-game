#!/usr/bin/env python3
"""
Epic Dragon End Boss Art Generator - Inspired by Toothless
Creates a massive, sleek dragon with cat-like features and elegant design
Double size (64x64) with enhanced detail and epic presence
"""

import numpy as np
from PIL import Image
import os

def create_toothless_inspired_dragon():
    """Create an epic dragon end boss inspired by Toothless's sleek design"""
    # Double the canvas size for epic presence - 64x64 instead of 32x32
    size = 64
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Toothless-inspired color palette - sleek and elegant but menacing
    BLACK = [0, 0, 0, 255]
    WHITE = [255, 255, 255, 255]
    
    # Dragon body colors - sleek red with rich variations
    DRAGON_RED = [180, 20, 20, 255]         # Main body (deep crimson red)
    DRAGON_DARK = [120, 15, 15, 255]        # Deep red shadows
    DRAGON_HIGHLIGHT = [220, 60, 60, 255]   # Bright red highlights
    DRAGON_ACCENT = [150, 35, 35, 255]      # Medium red tones
    
    # Eyes - large, expressive, cat-like (Toothless's signature feature)
    EYE_GREEN = [0, 255, 100, 255]          # Bright green eyes
    EYE_YELLOW = [255, 255, 100, 255]       # Eye highlights
    EYE_DARK = [0, 150, 50, 255]           # Eye shadows
    PUPIL_BLACK = [0, 0, 0, 255]           # Pupils (slit-like)
    
    # Wing colors - red-tinted membrane
    WING_MEMBRANE = [100, 30, 30, 255]     # Dark red wing skin
    WING_EDGE = [140, 50, 50, 255]         # Red wing bone structure
    
    # Details
    CLAW_WHITE = [220, 220, 220, 255]      # Sharp white claws
    NOSTRIL_DARK = [10, 10, 15, 255]       # Dark nostrils
    FIRE_BLUE = [100, 150, 255, 255]       # Plasma blast (like Toothless)
    FIRE_WHITE = [255, 255, 255, 255]      # Plasma core
    FIRE_PURPLE = [150, 100, 255, 255]     # Plasma edges
    
    print("🐉 Creating Toothless-inspired dragon boss...")
    
    # === SLEEK DRAGON HEAD (cat-like, rounded) ===
    head_center_x, head_center_y = 32, 18
    
    # Main head shape - rounded like Toothless
    for y in range(10, 28):
        for x in range(20, 44):
            dx = x - head_center_x
            dy = y - head_center_y
            distance = (dx*dx)/121 + (dy*dy)/64
            if distance <= 1:  # Elliptical head
                if distance < 0.3:  # Inner highlight
                    canvas[y][x] = DRAGON_HIGHLIGHT
                elif distance < 0.7:  # Main body
                    canvas[y][x] = DRAGON_RED
                else:  # Outer shadow
                    canvas[y][x] = DRAGON_DARK
    
    # === LARGE CAT-LIKE EYES (Toothless's most distinctive feature) ===
    # Left eye - large and expressive
    eye_left_x, eye_left_y = 27, 16
    for y in range(12, 20):
        for x in range(23, 31):
            dx = x - eye_left_x
            dy = y - eye_left_y
            if dx*dx + dy*dy <= 16:  # Large circular eye
                canvas[y][x] = EYE_GREEN
    
    # Left eye inner glow
    for y in range(14, 18):
        for x in range(25, 29):
            dx = x - eye_left_x
            dy = y - eye_left_y
            if dx*dx + dy*dy <= 4:
                canvas[y][x] = EYE_YELLOW
    
    # Left pupil - vertical slit (cat-like)
    canvas[15][27] = PUPIL_BLACK
    canvas[16][27] = PUPIL_BLACK
    canvas[17][27] = PUPIL_BLACK
    
    # Right eye - large and expressive
    eye_right_x, eye_right_y = 37, 16
    for y in range(12, 20):
        for x in range(33, 41):
            dx = x - eye_right_x
            dy = y - eye_right_y
            if dx*dx + dy*dy <= 16:  # Large circular eye
                canvas[y][x] = EYE_GREEN
    
    # Right eye inner glow
    for y in range(14, 18):
        for x in range(35, 39):
            dx = x - eye_right_x
            dy = y - eye_right_y
            if dx*dx + dy*dy <= 4:
                canvas[y][x] = EYE_YELLOW
    
    # Right pupil - vertical slit (cat-like)
    canvas[15][37] = PUPIL_BLACK
    canvas[16][37] = PUPIL_BLACK
    canvas[17][37] = PUPIL_BLACK
    
    # === SLEEK MUZZLE ===
    # Extended muzzle - not too long
    for y in range(18, 24):
        for x in range(28, 36):
            canvas[y][x] = DRAGON_RED
    
    # Nostrils
    canvas[20][30] = NOSTRIL_DARK
    canvas[20][33] = NOSTRIL_DARK
    
    # === STREAMLINED BODY ===
    body_center_x, body_center_y = 32, 38
    
    # Main body - sleek and aerodynamic
    for y in range(25, 50):
        for x in range(16, 48):
            dx = x - body_center_x
            dy = y - body_center_y
            distance = (dx*dx)/256 + (dy*dy)/156
            if distance <= 1:
                if distance < 0.2:
                    canvas[y][x] = DRAGON_HIGHLIGHT
                elif distance < 0.8:
                    canvas[y][x] = DRAGON_RED
                else:
                    canvas[y][x] = DRAGON_DARK
    
    # === ELEGANT WINGS (bat-like, like Toothless) ===
    # Left wing
    wing_points_left = [
        # Wing membrane outline
        (20, 15), (18, 20), (16, 25), (14, 30), (12, 35),
        (10, 40), (8, 45), (6, 50), (4, 55),
    ]
    
    # Draw left wing membrane
    for i, (y, x) in enumerate(wing_points_left):
        if 0 <= x < size and 0 <= y < size:
            # Wing membrane
            for offset_x in range(3):
                for offset_y in range(2):
                    wing_x = x + offset_x
                    wing_y = y + offset_y
                    if 0 <= wing_x < size and 0 <= wing_y < size:
                        canvas[wing_y][wing_x] = WING_MEMBRANE
            
            # Wing bones/structure
            canvas[y][x] = WING_EDGE
    
    # Right wing (mirrored)
    wing_points_right = [
        (20, 49), (18, 44), (16, 39), (14, 34), (12, 29),
        (10, 24), (8, 19), (6, 14), (4, 9),
    ]
    
    # Draw right wing membrane
    for i, (y, x) in enumerate(wing_points_right):
        if 0 <= x < size and 0 <= y < size:
            # Wing membrane
            for offset_x in range(-2, 1):
                for offset_y in range(2):
                    wing_x = x + offset_x
                    wing_y = y + offset_y
                    if 0 <= wing_x < size and 0 <= wing_y < size:
                        canvas[wing_y][wing_x] = WING_MEMBRANE
            
            # Wing bones/structure
            canvas[y][x] = WING_EDGE
    
    # === POWERFUL LIMBS ===
    # Left front leg
    for y in range(30, 45):
        for x in range(20, 25):
            canvas[y][x] = DRAGON_RED
    
    # Right front leg
    for y in range(30, 45):
        for x in range(39, 44):
            canvas[y][x] = DRAGON_RED
    
    # Left rear leg
    for y in range(40, 55):
        for x in range(22, 27):
            canvas[y][x] = DRAGON_RED
    
    # Right rear leg
    for y in range(40, 55):
        for x in range(37, 42):
            canvas[y][x] = DRAGON_RED
    
    # === RETRACTABLE CLAWS (like Toothless) ===
    # Left front claws
    claw_positions = [
        (45, 18), (46, 17), (47, 16),  # Claw 1
        (45, 20), (46, 19), (47, 18),  # Claw 2
        (45, 22), (46, 21), (47, 20),  # Claw 3
    ]
    
    for y, x in claw_positions:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = CLAW_WHITE
    
    # Right front claws (mirrored)
    claw_positions_right = [
        (45, 46), (46, 47), (47, 48),  # Claw 1
        (45, 44), (46, 45), (47, 46),  # Claw 2
        (45, 42), (46, 43), (47, 44),  # Claw 3
    ]
    
    for y, x in claw_positions_right:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = CLAW_WHITE
    
    # === SLEEK TAIL ===
    tail_segments = [
        (45, 32), (48, 33), (51, 34), (54, 35), (57, 36), (60, 37)
    ]
    
    for i, (y, x) in enumerate(tail_segments):
        if 0 <= x < size and 0 <= y < size:
            # Tail gets thinner towards the end
            thickness = max(1, 3 - i//2)
            for offset in range(-thickness, thickness + 1):
                tail_y = y + offset
                if 0 <= tail_y < size:
                    canvas[tail_y][x] = DRAGON_RED
    
    # Tail fins (like Toothless's tail fins)
    tail_fin_positions = [
        (43, 60), (44, 61), (45, 62),  # Upper fin
        (47, 60), (48, 61), (49, 62),  # Lower fin
    ]
    
    for y, x in tail_fin_positions:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = WING_MEMBRANE
    
    # === PLASMA BLAST EFFECT (Toothless's signature attack) ===
    # Plasma charging in mouth
    plasma_positions = [
        (21, 32), (22, 33), (23, 34),  # Plasma buildup
        (20, 31), (21, 31), (22, 31),  # Plasma glow
    ]
    
    for y, x in plasma_positions:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = FIRE_BLUE
    
    # Plasma core
    canvas[21][32] = FIRE_WHITE
    
    # Plasma energy around head
    energy_positions = [
        (15, 25), (16, 39), (25, 20), (25, 44),  # Energy crackling
    ]
    
    for y, x in energy_positions:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = FIRE_PURPLE
    
    print("🐉 Toothless-inspired dragon boss created!")
    return canvas

def main():
    """Create the Toothless-inspired dragon end boss art"""
    print("🐉 Creating Toothless-Inspired Dragon End Boss...")
    
    # Create the dragon
    dragon_data = create_toothless_inspired_dragon()
    
    # Convert to PIL Image
    dragon_img = Image.fromarray(dragon_data, 'RGBA')
    
    # Scale up 8x for final display (64x64 -> 512x512)
    scale_factor = 8
    final_width = dragon_data.shape[1] * scale_factor
    final_height = dragon_data.shape[0] * scale_factor
    
    dragon_scaled = dragon_img.resize((final_width, final_height), Image.Resampling.NEAREST)
    
    # Save the final dragon
    output_path = "art/dragon_endboss.png"
    dragon_scaled.save(output_path)
    print(f"✅ Toothless-inspired Dragon Boss saved to: {output_path}")
    
    print("🐉 Epic Dragon End Boss creation complete!")
    print("🔥 Toothless-inspired features created:")
    print("   - Massive 64x64 base resolution (double standard size)")
    print("   - Scaled to 512x512 final size for maximum impact")
    print("   - Sleek crimson red body with rich color variations")
    print("   - Large, expressive cat-like green eyes with slit pupils")
    print("   - Rounded, cat-like head shape")
    print("   - Elegant red-tinted wings with membrane detail")
    print("   - Streamlined, aerodynamic body design")
    print("   - Retractable white claws")
    print("   - Sleek tail with distinctive tail fins")
    print("   - Plasma blast charging effect")
    print("   - Perfect blend of elegance and menace in striking red!")

if __name__ == "__main__":
    main()