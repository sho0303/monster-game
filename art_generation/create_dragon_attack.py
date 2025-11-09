#!/usr/bin/env python3
"""
Dragon Open Maw Attack Animation Generator
Creates a menacing dragon with mouth wide open, showing sharp teeth - similar to main dragon but attacking
"""

import numpy as np
from PIL import Image
import os

def create_dragon_maw_attack():
    """Create an epic dragon with open toothy maw - similar to main dragon but in attack pose"""
    # Double the canvas size for epic presence - 64x64 instead of 32x32
    size = 64
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Dragon color palette - identical to main dragon for consistency
    BLACK = [0, 0, 0, 255]
    WHITE = [255, 255, 255, 255]
    
    # Dragon body colors - same as main dragon
    DRAGON_RED = [180, 20, 20, 255]         # Main body (deep crimson red)
    DRAGON_DARK = [120, 15, 15, 255]        # Deep red shadows
    DRAGON_HIGHLIGHT = [220, 60, 60, 255]   # Bright red highlights
    DRAGON_ACCENT = [150, 35, 35, 255]      # Medium red tones
    
    # Eyes - same as main dragon but more intense during attack
    EYE_GREEN = [0, 255, 100, 255]          # Bright green eyes
    EYE_YELLOW = [255, 255, 100, 255]       # Eye highlights
    EYE_INTENSE = [255, 255, 200, 255]      # Intense glow during attack
    PUPIL_BLACK = [0, 0, 0, 255]           # Pupils (dilated for attack)
    
    # Mouth and teeth colors - the new attack feature!
    MOUTH_DARK = [40, 0, 0, 255]           # Inside of mouth (dark red)
    MOUTH_BLACK = [10, 0, 0, 255]          # Deep mouth cavity/throat
    TOOTH_WHITE = [255, 255, 255, 255]     # Sharp white teeth
    TOOTH_IVORY = [240, 240, 220, 255]     # Tooth shading
    TONGUE_RED = [200, 50, 50, 255]        # Dragon tongue
    GUM_DARK = [80, 10, 10, 255]           # Dark gums
    
    # Wing colors - same as main dragon
    WING_MEMBRANE = [100, 30, 30, 255]     # Dark red wing skin
    WING_EDGE = [140, 50, 50, 255]         # Red wing bone structure
    
    # Attack energy effects
    ENERGY_RED = [255, 100, 100, 255]      # Red energy aura
    ENERGY_ORANGE = [255, 150, 0, 255]     # Orange energy crackling
    FIRE_GLOW = [255, 200, 100, 255]       # Fire glow from mouth
    
    print("🔥 Creating dragon with menacing open maw attack...")
    
    # === DRAGON HEAD WITH WIDE OPEN MOUTH ===
    head_center_x, head_center_y = 32, 18
    
    # Main head shape - similar to main dragon but slightly more angular for aggression
    for y in range(8, 30):
        for x in range(18, 46):
            dx = x - head_center_x
            dy = y - head_center_y
            distance = (dx*dx)/144 + (dy*dy)/80
            if distance <= 1:  # Head outline
                if distance < 0.3:  # Inner highlight
                    canvas[y][x] = DRAGON_HIGHLIGHT
                elif distance < 0.7:  # Main body
                    canvas[y][x] = DRAGON_RED
                else:  # Outer shadow
                    canvas[y][x] = DRAGON_DARK
    
    # === WIDE OPEN MOUTH (the main attack feature!) ===
    # Upper jaw
    upper_jaw_points = [
        (20, 28), (21, 30), (22, 32), (23, 34), (24, 36),
        (25, 38), (26, 40), (27, 42), (28, 44)
    ]
    
    for y, x in upper_jaw_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = DRAGON_RED
            # Add thickness to jaw
            if y > 0:
                canvas[y-1][x] = DRAGON_RED
            if y > 1:
                canvas[y-2][x] = DRAGON_DARK
    
    # Lower jaw - wide open
    lower_jaw_points = [
        (28, 28), (29, 30), (30, 32), (31, 34), (32, 36),
        (33, 38), (34, 40), (35, 42), (36, 44)
    ]
    
    for y, x in lower_jaw_points:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = DRAGON_RED
            # Add thickness to jaw
            if y < size - 1:
                canvas[y+1][x] = DRAGON_RED
            if y < size - 2:
                canvas[y+2][x] = DRAGON_DARK
    
    # === MOUTH INTERIOR (dark and menacing) ===
    # Fill the mouth cavity
    for y in range(21, 35):
        for x in range(30, 42):
            # Create mouth cavity shape
            mouth_width = min(x - 28, 44 - x)
            if mouth_width > 0 and 21 <= y <= 34:
                if y < 26:  # Upper mouth
                    canvas[y][x] = MOUTH_DARK
                elif y < 30:  # Mid mouth
                    canvas[y][x] = MOUTH_BLACK
                else:  # Lower mouth/throat
                    canvas[y][x] = MOUTH_BLACK
    
    # === SHARP TEETH (intimidating!) ===
    # Upper teeth (pointing down)
    upper_teeth_positions = [
        (20, 32), (20, 34), (20, 36), (20, 38), (20, 40),  # Top row
        (21, 33), (21, 35), (21, 37), (21, 39),           # Slightly lower
    ]
    
    for y, x in upper_teeth_positions:
        if 0 <= x < size and 0 <= y < size:
            # Sharp triangular teeth
            canvas[y][x] = TOOTH_WHITE
            canvas[y+1][x] = TOOTH_WHITE
            canvas[y+2][x] = TOOTH_IVORY
            canvas[y+3][x] = TOOTH_IVORY
    
    # Lower teeth (pointing up)
    lower_teeth_positions = [
        (34, 32), (34, 34), (34, 36), (34, 38), (34, 40),  # Bottom row
        (33, 33), (33, 35), (33, 37), (33, 39),           # Slightly higher
    ]
    
    for y, x in lower_teeth_positions:
        if 0 <= x < size and 0 <= y < size:
            # Sharp triangular teeth
            canvas[y][x] = TOOTH_WHITE
            canvas[y-1][x] = TOOTH_WHITE
            canvas[y-2][x] = TOOTH_IVORY
            canvas[y-3][x] = TOOTH_IVORY
    
    # === FANGS (extra menacing canine teeth) ===
    # Upper fangs
    canvas[20][34] = TOOTH_WHITE
    canvas[21][34] = TOOTH_WHITE
    canvas[22][34] = TOOTH_WHITE
    canvas[23][34] = TOOTH_IVORY
    canvas[24][34] = TOOTH_IVORY
    
    canvas[20][38] = TOOTH_WHITE
    canvas[21][38] = TOOTH_WHITE
    canvas[22][38] = TOOTH_WHITE
    canvas[23][38] = TOOTH_IVORY
    canvas[24][38] = TOOTH_IVORY
    
    # Lower fangs
    canvas[34][34] = TOOTH_WHITE
    canvas[33][34] = TOOTH_WHITE
    canvas[32][34] = TOOTH_WHITE
    canvas[31][34] = TOOTH_IVORY
    canvas[30][34] = TOOTH_IVORY
    
    canvas[34][38] = TOOTH_WHITE
    canvas[33][38] = TOOTH_WHITE
    canvas[32][38] = TOOTH_WHITE
    canvas[31][38] = TOOTH_IVORY
    canvas[30][38] = TOOTH_IVORY
    
    # === TONGUE ===
    tongue_positions = [
        (28, 35), (29, 36), (30, 36), (31, 35),  # Tongue shape
        (28, 36), (29, 37), (30, 37), (31, 36),
    ]
    
    for y, x in tongue_positions:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = TONGUE_RED
    
    # === INTENSE EYES DURING ATTACK ===
    # Left eye - dilated and intense
    eye_left_x, eye_left_y = 25, 14
    for y in range(10, 18):
        for x in range(21, 29):
            dx = x - eye_left_x
            dy = y - eye_left_y
            if dx*dx + dy*dy <= 16:  # Large circular eye
                canvas[y][x] = EYE_GREEN
    
    # Left eye intense glow
    for y in range(12, 16):
        for x in range(23, 27):
            dx = x - eye_left_x
            dy = y - eye_left_y
            if dx*dx + dy*dy <= 4:
                canvas[y][x] = EYE_INTENSE
    
    # Left pupil - dilated for attack (larger)
    canvas[14][25] = PUPIL_BLACK
    canvas[15][25] = PUPIL_BLACK
    canvas[14][24] = PUPIL_BLACK
    canvas[14][26] = PUPIL_BLACK
    
    # Right eye - dilated and intense
    eye_right_x, eye_right_y = 39, 14
    for y in range(10, 18):
        for x in range(35, 43):
            dx = x - eye_right_x
            dy = y - eye_right_y
            if dx*dx + dy*dy <= 16:  # Large circular eye
                canvas[y][x] = EYE_GREEN
    
    # Right eye intense glow
    for y in range(12, 16):
        for x in range(37, 41):
            dx = x - eye_right_x
            dy = y - eye_right_y
            if dx*dx + dy*dy <= 4:
                canvas[y][x] = EYE_INTENSE
    
    # Right pupil - dilated for attack (larger)
    canvas[14][39] = PUPIL_BLACK
    canvas[15][39] = PUPIL_BLACK
    canvas[14][38] = PUPIL_BLACK
    canvas[14][40] = PUPIL_BLACK
    
    # === BODY (simplified, focus on head/mouth) ===
    body_center_x, body_center_y = 32, 42
    
    # Simplified body showing neck and shoulders
    for y in range(30, 50):
        for x in range(20, 44):
            dx = x - body_center_x
            dy = y - body_center_y
            distance = (dx*dx)/144 + (dy*dy)/64
            if distance <= 1:
                if distance < 0.4:
                    canvas[y][x] = DRAGON_HIGHLIGHT
                elif distance < 0.8:
                    canvas[y][x] = DRAGON_RED
                else:
                    canvas[y][x] = DRAGON_DARK
    
    # === MENACING CLAWS FACING PLAYER ===
    # Claw colors
    CLAW_WHITE = [255, 255, 255, 255]      # Sharp white claws
    CLAW_IVORY = [240, 240, 220, 255]     # Claw shading
    CLAW_BASE = [200, 200, 180, 255]      # Claw base color
    
    # Left side claws (dragon's right arm reaching toward player)
    left_arm_base_x, left_arm_base_y = 18, 38
    
    # Left arm/shoulder
    for y in range(35, 45):
        for x in range(15, 22):
            canvas[y][x] = DRAGON_RED
    
    # Left claws - multiple sharp claws extending toward player
    left_claw_positions = [
        # Claw 1 (top)
        (36, 12), (37, 11), (38, 10), (39, 9),
        # Claw 2 (upper middle) 
        (38, 13), (39, 12), (40, 11), (41, 10),
        # Claw 3 (middle)
        (40, 14), (41, 13), (42, 12), (43, 11),
        # Claw 4 (lower middle)
        (42, 15), (43, 14), (44, 13), (45, 12),
        # Claw 5 (bottom)
        (44, 16), (45, 15), (46, 14), (47, 13),
    ]
    
    for i, (y, x) in enumerate(left_claw_positions):
        if 0 <= x < size and 0 <= y < size:
            claw_num = i // 4  # Which claw (0-4)
            claw_segment = i % 4  # Which segment of the claw (0-3)
            
            if claw_segment == 0:  # Base of claw
                canvas[y][x] = CLAW_BASE
            elif claw_segment == 1:  # Middle
                canvas[y][x] = CLAW_IVORY
            else:  # Tip segments
                canvas[y][x] = CLAW_WHITE
    
    # Right side claws (dragon's left arm reaching toward player)
    right_arm_base_x, right_arm_base_y = 46, 38
    
    # Right arm/shoulder
    for y in range(35, 45):
        for x in range(42, 49):
            canvas[y][x] = DRAGON_RED
    
    # Right claws - multiple sharp claws extending toward player
    right_claw_positions = [
        # Claw 1 (top)
        (36, 52), (37, 53), (38, 54), (39, 55),
        # Claw 2 (upper middle)
        (38, 51), (39, 52), (40, 53), (41, 54),
        # Claw 3 (middle)
        (40, 50), (41, 51), (42, 52), (43, 53),
        # Claw 4 (lower middle)
        (42, 49), (43, 50), (44, 51), (45, 52),
        # Claw 5 (bottom)
        (44, 48), (45, 49), (46, 50), (47, 51),
    ]
    
    for i, (y, x) in enumerate(right_claw_positions):
        if 0 <= x < size and 0 <= y < size:
            claw_num = i // 4  # Which claw (0-4)
            claw_segment = i % 4  # Which segment of the claw (0-3)
            
            if claw_segment == 0:  # Base of claw
                canvas[y][x] = CLAW_BASE
            elif claw_segment == 1:  # Middle
                canvas[y][x] = CLAW_IVORY
            else:  # Tip segments
                canvas[y][x] = CLAW_WHITE
    
    # === CLAW HIGHLIGHTS AND SHADOWS ===
    # Add highlights to make claws look sharp and menacing
    claw_highlight_positions = [
        # Left claw highlights
        (37, 10), (39, 11), (41, 12), (43, 13), (45, 14),
        # Right claw highlights  
        (37, 54), (39, 53), (41, 52), (43, 51), (45, 50),
    ]
    
    for y, x in claw_highlight_positions:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = WHITE  # Bright white highlights on claw tips
    
    # === WINGS (partially visible, spread for attack) ===
    # Left wing tip
    left_wing_points = [
        (25, 10), (22, 15), (19, 20), (16, 25), (13, 30),
        (10, 35), (7, 40), (4, 45)
    ]
    
    for i, (y, x) in enumerate(left_wing_points):
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = WING_EDGE
            # Wing membrane around structure
            for offset_x in range(2):
                for offset_y in range(2):
                    wing_x = x + offset_x
                    wing_y = y + offset_y
                    if 0 <= wing_x < size and 0 <= wing_y < size and canvas[wing_y][wing_x][3] == 0:
                        canvas[wing_y][wing_x] = WING_MEMBRANE
    
    # Right wing tip (mirrored)
    right_wing_points = [
        (25, 54), (22, 49), (19, 44), (16, 39), (13, 34),
        (10, 29), (7, 24), (4, 19)
    ]
    
    for i, (y, x) in enumerate(right_wing_points):
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = WING_EDGE
            # Wing membrane around structure
            for offset_x in range(-1, 1):
                for offset_y in range(2):
                    wing_x = x + offset_x
                    wing_y = y + offset_y
                    if 0 <= wing_x < size and 0 <= wing_y < size and canvas[wing_y][wing_x][3] == 0:
                        canvas[wing_y][wing_x] = WING_MEMBRANE
    
    # === ENERGY EFFECTS AROUND ATTACKING DRAGON ===
    # Energy crackling around the head during attack
    energy_positions = [
        (8, 20), (6, 25), (4, 30), (2, 35),     # Left energy
        (8, 44), (6, 39), (4, 34), (2, 29),     # Right energy
        (15, 46), (20, 48), (25, 50),           # Energy around mouth
        (35, 46), (40, 48), (45, 50),           # More mouth energy
    ]
    
    for y, x in energy_positions:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = ENERGY_RED
    
    # Fire glow effect from the open mouth
    glow_positions = [
        (25, 42), (26, 43), (27, 44), (28, 45),  # Fire glow streaming out
        (29, 46), (30, 47), (31, 48), (32, 49),
    ]
    
    for y, x in glow_positions:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = FIRE_GLOW
    
    print("🔥 Dragon with menacing open maw attack created!")
    return canvas

def main():
    """Create the dragon open maw attack animation"""
    print("🔥 Creating Dragon Open Maw Attack Animation...")
    
    # Create the dragon attack
    attack_data = create_dragon_maw_attack()
    
    # Convert to PIL Image
    attack_img = Image.fromarray(attack_data, 'RGBA')
    
    # Scale up 8x for final display (64x64 -> 512x512)
    scale_factor = 8
    final_width = attack_data.shape[1] * scale_factor
    final_height = attack_data.shape[0] * scale_factor
    
    attack_scaled = attack_img.resize((final_width, final_height), Image.Resampling.NEAREST)
    
    # Save the dragon attack animation
    output_path = "art/dragon_endboss_attack.png"
    attack_scaled.save(output_path)
    print(f"✅ Dragon Open Maw Attack saved to: {output_path}")
    
    print("🔥 Dragon Open Maw Attack Animation complete!")
    print("\n⚡ Menacing open maw attack features:")
    print("   - Massive 64x64 base resolution (double standard size)")
    print("   - Scaled to 512x512 final size for maximum impact")
    print("   - Same elegant design as main dragon but in attack pose")
    print("   - Wide open mouth showing menacing interior")
    print("   - Sharp white teeth and prominent fangs")
    print("   - Dark mouth cavity and red tongue")
    print("   - Intensely glowing eyes with dilated pupils")
    print("   - Partially spread wings in aggressive stance")
    print("   - Energy crackling around the attacking dragon")
    print("   - Fire glow effect streaming from open mouth")
    print("   - Perfect intimidating attack animation!")

if __name__ == "__main__":
    main()