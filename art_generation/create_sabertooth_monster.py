"""
Create SaberTooth Tiger monster sprite and attack animation.
Style: Pixel art inspired by prehistoric saber-toothed cat
Features: Muscular body, long curved fangs, striped fur pattern, powerful stance
"""

import numpy as np
from PIL import Image

# Color palette for SaberTooth Tiger
# Body colors - tan/orange with darker stripes
BODY_LIGHT = (220, 180, 130)      # Light tan fur
BODY_BASE = (190, 145, 90)        # Base tan/orange
BODY_MID = (160, 115, 70)         # Mid tone
BODY_DARK = (130, 90, 50)         # Dark tan
BODY_SHADOW = (100, 70, 40)       # Shadow areas

# Stripe colors
STRIPE_DARK = (80, 50, 30)        # Dark brown stripes
STRIPE_MID = (100, 65, 40)        # Medium stripe
STRIPE_BLACK = (40, 30, 20)       # Near-black stripes

# Chest/belly colors (lighter)
CHEST_LIGHT = (240, 220, 190)     # Light cream
CHEST_BASE = (220, 200, 170)      # Cream
CHEST_MID = (200, 180, 150)       # Mid cream

# Face/head colors
FACE_LIGHT = (210, 170, 120)      # Light face
FACE_BASE = (180, 140, 95)        # Base face
FACE_DARK = (150, 110, 70)        # Dark face areas

# Fang colors (iconic feature)
FANG_WHITE = (255, 255, 245)      # Bright white fangs
FANG_LIGHT = (240, 240, 230)      # Light fang
FANG_SHADOW = (200, 200, 190)     # Fang shadow
FANG_TIP = (220, 220, 210)        # Fang tip

# Eye colors
EYE_WHITE = (255, 255, 255)       # Eye white
EYE_IRIS = (180, 140, 60)         # Amber iris
EYE_PUPIL = (40, 30, 20)          # Dark pupil
EYE_GLOW = (200, 160, 80)         # Amber glow

# Nose and mouth
NOSE_DARK = (60, 40, 30)          # Dark nose
NOSE_PINK = (140, 90, 80)         # Pink nose highlight
MOUTH_DARK = (50, 30, 20)         # Dark mouth/gums

# Claws
CLAW_WHITE = (240, 240, 235)      # White claws
CLAW_SHADOW = (180, 180, 175)     # Claw shadow

# Ears
EAR_OUTER = (170, 130, 85)        # Outer ear
EAR_INNER = (200, 160, 120)       # Inner ear (lighter)

# Leg and paw colors
PAW_BASE = (180, 140, 90)         # Paw base
PAW_PAD = (90, 70, 50)            # Paw pads (darker)

# Tail colors
TAIL_BASE = (180, 140, 90)        # Tail base
TAIL_TIP_DARK = (90, 60, 40)      # Dark tail tip


def create_sabertooth_default(width=64, height=64):
    """Create default SaberTooth Tiger pose - sideways profile filling the frame."""
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Position - head on left, body extending right, filling frame
    head_x = 12
    head_y = 18
    body_start_x = 20
    body_end_x = 52
    body_y = 26
    
    # HEAD - facing left with profile view
    # Head segments (vertical slices from front to back)
    head_profile = [
        # Muzzle/nose area (front of head)
        (head_x, head_y + 6, 4, FACE_BASE),      # Nose tip
        (head_x + 1, head_y + 5, 6, FACE_LIGHT),  # Upper muzzle
        (head_x + 2, head_y + 5, 6, FACE_BASE),
        (head_x + 3, head_y + 4, 7, FACE_BASE),   # Cheek area
        (head_x + 4, head_y + 3, 8, FACE_BASE),
        (head_x + 5, head_y + 2, 9, FACE_BASE),   # Widest part of head
        (head_x + 6, head_y + 2, 9, FACE_DARK),
        (head_x + 7, head_y + 1, 10, BODY_BASE),  # Back of head/neck
        (head_x + 8, head_y + 1, 10, BODY_MID),
    ]
    
    for hx, hy, h_height, color in head_profile:
        for dy in range(h_height):
            py = hy + dy
            if 0 <= hx < width and 0 <= py < height:
                canvas[py][hx] = (*color, 255)
    for hx, hy, h_height, color in head_profile:
        for dy in range(h_height):
            py = hy + dy
            if 0 <= hx < width and 0 <= py < height:
                canvas[py][hx] = (*color, 255)
    
    # Ear (small rounded triangle on top of head)
    ear_x = head_x + 5
    ear_y = head_y + 1
    ear_points = [(0, 0), (-1, 1), (0, 1), (1, 1), (-1, 2), (0, 2), (1, 2)]
    for dx, dy in ear_points:
        px, py = ear_x + dx, ear_y + dy
        if 0 <= px < width and 0 <= py < height:
            canvas[py][px] = (*EAR_OUTER, 255)
    # Inner ear
    canvas[ear_y + 1][ear_x] = (*EAR_INNER, 255)
    
    # Eye (single eye visible in profile)
    eye_x = head_x + 4
    eye_y = head_y + 4
    # Eye shape
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            px, py = eye_x + dx, eye_y + dy
            if 0 <= px < width and 0 <= py < height:
                canvas[py][px] = (*EYE_IRIS, 255)
    # Pupil
    canvas[eye_y][eye_x] = (*EYE_PUPIL, 255)
    # Highlight
    canvas[eye_y - 1][eye_x - 1] = (*EYE_GLOW, 255)
    
    # Nose (dark tip at front of muzzle)
    nose_x = head_x
    nose_y = head_y + 7
    for dy in range(2):
        for dx in range(2):
            px, py = nose_x + dx, nose_y + dy
            if 0 <= px < width and 0 <= py < height:
                canvas[py][px] = (*NOSE_DARK, 255)
    canvas[nose_y][nose_x] = (*NOSE_PINK, 255)
    
    # ICONIC FANGS - long curved sabers hanging down from upper jaw
    # Two fangs visible in profile
    fang_positions = [(head_x + 2, head_y + 8), (head_x + 4, head_y + 8)]
    for fang_x, fang_y in fang_positions:
        # Each fang is 9 segments long, curving down and slightly forward
        fang_curve = [(0, 0), (0, 1), (-1, 2), (-1, 3), (-1, 4), (-1, 5), (-2, 6), (-2, 7), (-2, 8)]
        
        for i, (dx, dy) in enumerate(fang_curve):
            px, py = fang_x + dx, fang_y + dy
            # Fangs are 2 pixels wide at base, taper to 1 at tip
            if i < 3:
                for wx in range(2):
                    fang_px = px + wx
                    if 0 <= fang_px < width and 0 <= py < height:
                        if i == 0:
                            canvas[py][fang_px] = (*FANG_SHADOW, 255)
                        else:
                            canvas[py][fang_px] = (*FANG_WHITE, 255)
            else:
                if 0 <= px < width and 0 <= py < height:
                    if i >= len(fang_curve) - 2:
                        canvas[py][px] = (*FANG_TIP, 255)
                    else:
                        canvas[py][px] = (*FANG_WHITE, 255)
    
    # Mouth line (slight opening)
    for mx in range(head_x + 1, head_x + 5):
        my = head_y + 8
        if 0 <= mx < width and 0 <= my < height:
            canvas[my][mx] = (*MOUTH_DARK, 255)
    
    # BODY - long horizontal body from head to tail
    # Body segments (top to bottom profile, repeated across body length)
    for bx in range(body_start_x, body_end_x):
        # Calculate body height at this x position (slight curve)
        progress = (bx - body_start_x) / (body_end_x - body_start_x)
        
        # Neck to shoulder (gets taller)
        if progress < 0.2:
            body_height = int(10 + progress * 30)
            color_top = BODY_DARK
            color_mid = BODY_BASE
            color_bottom = CHEST_BASE
        # Shoulder/chest (tallest)
        elif progress < 0.5:
            body_height = 16
            color_top = BODY_BASE
            color_mid = BODY_MID
            color_bottom = CHEST_LIGHT
        # Mid body
        elif progress < 0.8:
            body_height = 15
            color_top = BODY_BASE
            color_mid = BODY_BASE
            color_bottom = CHEST_BASE
        # Hindquarters (slightly shorter)
        else:
            body_height = int(15 - (progress - 0.8) * 20)
            color_top = BODY_DARK
            color_mid = BODY_BASE
            color_bottom = CHEST_BASE
        
        # Draw vertical column for this x position
        body_top = body_y - body_height // 2
        body_bottom = body_top + body_height
        
        for by in range(body_top, body_bottom):
            if 0 <= bx < width and 0 <= by < height:
                # Top third (back)
                if by < body_top + body_height // 3:
                    canvas[by][bx] = (*color_top, 255)
                # Middle third
                elif by < body_top + 2 * body_height // 3:
                    canvas[by][bx] = (*color_mid, 255)
                # Bottom third (belly)
                else:
                    canvas[by][bx] = (*color_bottom, 255)
    
    # Add dark stripes across body (vertical bands)
    stripe_x_positions = [25, 30, 35, 40, 45]
    for stripe_x in stripe_x_positions:
        if 0 <= stripe_x < width:
            for sy in range(body_y - 6, body_y + 2):
                if 0 <= sy < height:
                    canvas[sy][stripe_x] = (*STRIPE_DARK, 255)
                    # Add darker center
                    if stripe_x + 1 < width:
                        canvas[sy][stripe_x + 1] = (*STRIPE_BLACK, 255)
    
    # LEGS - four legs visible in sideways view
    # Front left leg (foreground)
    front_left_leg = [(24, body_y + 8), (24, body_y + 14), (23, body_y + 20), (23, body_y + 25)]
    # Front right leg (background, partially hidden)
    front_right_leg = [(28, body_y + 8), (28, body_y + 14), (27, body_y + 20), (27, body_y + 25)]
    # Back left leg (foreground)
    back_left_leg = [(42, body_y + 8), (42, body_y + 14), (41, body_y + 20), (41, body_y + 25)]
    # Back right leg (background, partially hidden)
    back_right_leg = [(46, body_y + 8), (46, body_y + 14), (45, body_y + 20), (45, body_y + 25)]
    
    all_legs = [back_right_leg, front_right_leg, back_left_leg, front_left_leg]
    
    for leg_idx, leg in enumerate(all_legs):
        is_foreground = leg_idx >= 2
        for i, (lx, ly) in enumerate(leg):
            # Leg thickness
            thickness = 3 if is_foreground else 2
            if i == len(leg) - 1:  # Paw
                thickness = 4 if is_foreground else 3
            
            for dy in range(-thickness // 2, thickness // 2 + 1):
                for dx in range(-1, 2):
                    px, py = lx + dx, ly + dy
                    if 0 <= px < width and 0 <= py < height:
                        if i == 0:  # Top of leg
                            canvas[py][px] = (*BODY_DARK, 255)
                        elif i == len(leg) - 1:  # Paw
                            canvas[py][px] = (*PAW_BASE, 255)
                            # Add paw pads
                            if dx == 0 and dy == 0:
                                canvas[py][px] = (*PAW_PAD, 255)
                        else:  # Mid leg
                            canvas[py][px] = (*BODY_MID, 255)
    
    # Add claws to foreground legs
    for leg in [front_left_leg, back_left_leg]:
        paw_x, paw_y = leg[-1]
        for i in range(3):
            cx = paw_x - 1 + i
            cy = paw_y + 2
            if 0 <= cx < width and 0 <= cy < height:
                canvas[cy][cx] = (*CLAW_WHITE, 255)
                if cy + 1 < height:
                    canvas[cy + 1][cx] = (*CLAW_SHADOW, 255)
    
    # TAIL - curved tail extending from back
    tail_start_x = body_end_x - 2
    tail_start_y = body_y
    tail_curve = [
        (tail_start_x, tail_start_y),
        (tail_start_x + 2, tail_start_y - 2),
        (tail_start_x + 4, tail_start_y - 3),
        (tail_start_x + 6, tail_start_y - 2),
        (tail_start_x + 8, tail_start_y),
        (tail_start_x + 9, tail_start_y + 2),
        (tail_start_x + 10, tail_start_y + 4),
    ]
    
    for i, (tx, ty) in enumerate(tail_curve):
        thickness = 4 if i < 2 else 3 if i < 4 else 2
        for dy in range(-thickness // 2, thickness // 2 + 1):
            for dx in range(-1, 2):
                px, py = tx + dx, ty + dy
                if 0 <= px < width and 0 <= py < height:
                    color = TAIL_TIP_DARK if i >= len(tail_curve) - 2 else TAIL_BASE
                    canvas[py][px] = (*color, 255)
    
    return canvas


def create_sabertooth_attack(width=64, height=64):
    """Create attacking SaberTooth Tiger - lunging sideways with open jaws, filling frame."""
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Position - lunging forward (to the left), filling frame
    head_x = 8
    head_y = 16
    body_start_x = 18
    body_end_x = 54
    body_y = 25
    
    # HEAD - facing left with JAWS WIDE OPEN
    # Upper jaw/head
    upper_head_profile = [
        (head_x, head_y + 4, 4, FACE_BASE),      # Front of muzzle
        (head_x + 1, head_y + 3, 5, FACE_LIGHT),
        (head_x + 2, head_y + 3, 5, FACE_BASE),
        (head_x + 3, head_y + 2, 6, FACE_BASE),   # Cheek
        (head_x + 4, head_y + 1, 7, FACE_BASE),
        (head_x + 5, head_y, 8, FACE_BASE),       # Top of head
        (head_x + 6, head_y, 8, FACE_DARK),
        (head_x + 7, head_y, 9, BODY_BASE),       # Back of head
        (head_x + 8, head_y + 1, 9, BODY_MID),
    ]
    
    for hx, hy, h_height, color in upper_head_profile:
        for dy in range(h_height):
            py = hy + dy
            if 0 <= hx < width and 0 <= py < height:
                canvas[py][hx] = (*color, 255)
    
    # Lower jaw (dropped open)
    lower_jaw_y = head_y + 12
    lower_jaw_profile = [
        (head_x, lower_jaw_y, 3, FACE_DARK),
        (head_x + 1, lower_jaw_y, 4, FACE_BASE),
        (head_x + 2, lower_jaw_y + 1, 4, FACE_BASE),
        (head_x + 3, lower_jaw_y + 1, 3, FACE_DARK),
    ]
    
    for hx, hy, h_height, color in lower_jaw_profile:
        for dy in range(h_height):
            py = hy + dy
            if 0 <= hx < width and 0 <= py < height:
                canvas[py][hx] = (*color, 255)
    
    # Open mouth cavity (dark)
    for my in range(head_y + 7, lower_jaw_y):
        for mx in range(head_x, head_x + 5):
            if 0 <= mx < width and 0 <= my < height:
                canvas[my][mx] = (*MOUTH_DARK, 255)
    
    # Ear (flattened back)
    ear_x = head_x + 6
    ear_y = head_y
    for dy in range(3):
        for dx in range(-1, 2):
            px, py = ear_x + dx, ear_y + dy
            if 0 <= px < width and 0 <= py < height:
                canvas[py][px] = (*EAR_OUTER, 255)
    
    # Eye (fierce and wide)
    eye_x = head_x + 4
    eye_y = head_y + 3
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            px, py = eye_x + dx, eye_y + dy
            if 0 <= px < width and 0 <= py < height:
                canvas[py][px] = (*EYE_IRIS, 255)
    # Dilated pupil
    for dy in range(-1, 1):
        for dx in range(-1, 1):
            px, py = eye_x + dx, eye_y + dy
            if 0 <= px < width and 0 <= py < height:
                canvas[py][px] = (*EYE_PUPIL, 255)
    # Bright glow
    canvas[eye_y - 1][eye_x - 1] = (*EYE_GLOW, 255)
    canvas[eye_y - 1][eye_x] = (*EYE_GLOW, 255)
    
    # Nose
    nose_x = head_x
    nose_y = head_y + 5
    for dy in range(2):
        for dx in range(2):
            px, py = nose_x + dx, nose_y + dy
            if 0 <= px < width and 0 <= py < height:
                canvas[py][px] = (*NOSE_DARK, 255)
    
    # EXTENDED FANGS - longer in attack, hanging from upper jaw
    fang_positions = [(head_x + 2, head_y + 7), (head_x + 4, head_y + 7)]
    for fang_x, fang_y in fang_positions:
        # Attack fangs are 11 segments (very long)
        fang_curve = [(0, 0), (0, 1), (-1, 2), (-1, 3), (-1, 4), (-2, 5), (-2, 6), (-2, 7), (-3, 8), (-3, 9), (-3, 10)]
        
        for i, (dx, dy) in enumerate(fang_curve):
            px, py = fang_x + dx, fang_y + dy
            # Fangs wider at base
            if i < 4:
                for wx in range(2):
                    fang_px = px + wx
                    if 0 <= fang_px < width and 0 <= py < height:
                        if i == 0:
                            canvas[py][fang_px] = (*FANG_SHADOW, 255)
                        else:
                            canvas[py][fang_px] = (*FANG_WHITE, 255)
            else:
                if 0 <= px < width and 0 <= py < height:
                    if i >= len(fang_curve) - 2:
                        canvas[py][px] = (*FANG_TIP, 255)
                    else:
                        canvas[py][px] = (*FANG_WHITE, 255)
    
    # Lower fangs (smaller)
    lower_fang_x = head_x + 2
    lower_fang_y = lower_jaw_y
    for dy in range(4):
        px, py = lower_fang_x, lower_fang_y - dy
        if 0 <= px < width and 0 <= py < height:
            canvas[py][px] = (*FANG_LIGHT, 255)
    # Lower fangs (smaller)
    lower_fang_x = head_x + 2
    lower_fang_y = lower_jaw_y
    for dy in range(4):
        px, py = lower_fang_x, lower_fang_y - dy
        if 0 <= px < width and 0 <= py < height:
            canvas[py][px] = (*FANG_LIGHT, 255)
    
    # BODY - lunging forward, stretched horizontally
    for bx in range(body_start_x, body_end_x):
        progress = (bx - body_start_x) / (body_end_x - body_start_x)
        
        # Body tapers from neck to hindquarters
        if progress < 0.15:
            body_height = int(9 + progress * 40)
            color_top = BODY_DARK
            color_mid = BODY_BASE
            color_bottom = CHEST_BASE
        elif progress < 0.45:
            body_height = 16
            color_top = BODY_BASE
            color_mid = BODY_MID
            color_bottom = CHEST_LIGHT
        elif progress < 0.75:
            body_height = 15
            color_top = BODY_BASE
            color_mid = BODY_BASE
            color_bottom = CHEST_BASE
        else:
            body_height = int(15 - (progress - 0.75) * 24)
            color_top = BODY_DARK
            color_mid = BODY_BASE
            color_bottom = CHEST_BASE
        
        body_top = body_y - body_height // 2
        body_bottom = body_top + body_height
        
        for by in range(body_top, body_bottom):
            if 0 <= bx < width and 0 <= by < height:
                if by < body_top + body_height // 3:
                    canvas[by][bx] = (*color_top, 255)
                elif by < body_top + 2 * body_height // 3:
                    canvas[by][bx] = (*color_mid, 255)
                else:
                    canvas[by][bx] = (*color_bottom, 255)
    
    # Stripes (more prominent in attack)
    stripe_x_positions = [24, 29, 34, 39, 44, 49]
    for stripe_x in stripe_x_positions:
        if 0 <= stripe_x < width:
            for sy in range(body_y - 6, body_y + 3):
                if 0 <= sy < height:
                    canvas[sy][stripe_x] = (*STRIPE_DARK, 255)
                    if stripe_x + 1 < width:
                        canvas[sy][stripe_x + 1] = (*STRIPE_BLACK, 255)
    
    # LEGS - stretched out in lunge
    # Front legs reaching forward
    front_left_leg = [(20, body_y + 7), (18, body_y + 13), (16, body_y + 19), (14, body_y + 24)]
    front_right_leg = [(24, body_y + 7), (22, body_y + 13), (20, body_y + 19), (18, body_y + 24)]
    # Back legs pushing
    back_left_leg = [(44, body_y + 7), (45, body_y + 13), (45, body_y + 19), (45, body_y + 25)]
    back_right_leg = [(48, body_y + 7), (49, body_y + 13), (49, body_y + 19), (49, body_y + 25)]
    
    all_legs = [back_right_leg, front_right_leg, back_left_leg, front_left_leg]
    
    for leg_idx, leg in enumerate(all_legs):
        is_foreground = leg_idx >= 2
        for i, (lx, ly) in enumerate(leg):
            thickness = 3 if is_foreground else 2
            if i == len(leg) - 1:
                thickness = 4 if is_foreground else 3
            
            for dy in range(-thickness // 2, thickness // 2 + 1):
                for dx in range(-1, 2):
                    px, py = lx + dx, ly + dy
                    if 0 <= px < width and 0 <= py < height:
                        if i == 0:
                            canvas[py][px] = (*BODY_DARK, 255)
                        elif i == len(leg) - 1:
                            canvas[py][px] = (*PAW_BASE, 255)
                            if dx == 0 and dy == 0:
                                canvas[py][px] = (*PAW_PAD, 255)
                        else:
                            canvas[py][px] = (*BODY_MID, 255)
    
    # Extended claws (attacking)
    for leg in [front_left_leg, back_left_leg]:
        paw_x, paw_y = leg[-1]
        for i in range(4):
            cx = paw_x - 2 + i
            cy = paw_y + 2 + (i % 2)
            if 0 <= cx < width and 0 <= cy < height:
                canvas[cy][cx] = (*CLAW_WHITE, 255)
                if cy + 1 < height:
                    canvas[cy + 1][cx] = (*CLAW_SHADOW, 255)
    
    # TAIL - lashing upward
    tail_start_x = body_end_x - 2
    tail_start_y = body_y + 2
    tail_curve = [
        (tail_start_x, tail_start_y),
        (tail_start_x + 1, tail_start_y - 2),
        (tail_start_x + 2, tail_start_y - 5),
        (tail_start_x + 3, tail_start_y - 7),
        (tail_start_x + 4, tail_start_y - 8),
        (tail_start_x + 5, tail_start_y - 7),
    ]
    
    for i, (tx, ty) in enumerate(tail_curve):
        thickness = 4 if i < 2 else 3 if i < 4 else 2
        for dy in range(-thickness // 2, thickness // 2 + 1):
            for dx in range(-1, 2):
                px, py = tx + dx, ty + dy
                if 0 <= px < width and 0 <= py < height:
                    color = TAIL_TIP_DARK if i >= len(tail_curve) - 2 else TAIL_BASE
                    canvas[py][px] = (*color, 255)
    
    # Motion blur trailing behind
    for bx in range(body_end_x, min(body_end_x + 8, width)):
        for by in range(body_y - 4, body_y + 4):
            if 0 <= bx < width and 0 <= by < height:
                canvas[by][bx] = (*BODY_MID, 80)
    
    return canvas


def main():
    print("Creating SaberTooth Tiger monster images...")
    
    # Create both poses
    default_sprite = create_sabertooth_default()
    attack_sprite = create_sabertooth_attack()
    
    # Convert to PIL Images
    default_img = Image.fromarray(default_sprite, mode='RGBA')
    attack_img = Image.fromarray(attack_sprite, mode='RGBA')
    
    # Scale up 4x using nearest neighbor (pixel art style)
    scale = 4
    default_scaled = default_img.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    attack_scaled = attack_img.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    
    # Save images
    default_path = 'art/sabertooth_monster.png'
    attack_path = 'art/sabertooth_monster_attack.png'
    
    default_scaled.save(default_path)
    attack_scaled.save(attack_path)
    
    print(f"✓ Saved: {default_path} ({64*scale}x{64*scale})")
    print(f"✓ Saved: {attack_path} ({64*scale}x{64*scale})")
    print("✅ SaberTooth Tiger monster creation complete!")
    print("\nFeatures:")
    print("- Default: Powerful standing pose with iconic long curved fangs visible")
    print("- Attack: Lunging forward with jaws wide open, extended fangs, fierce eyes")
    print("- Style: Pixel art with tan/orange fur, dark stripes, muscular build")
    print("- Colors: Tan body with brown stripes, cream chest, white fangs, amber eyes")


if __name__ == '__main__':
    main()
