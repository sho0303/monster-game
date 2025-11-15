"""
Create pixel art ninja hero images
Inspired by cartoon ninja with dark blue outfit, mask, and ninja stars
"""
from PIL import Image
import numpy as np
import random

def create_ninja_default():
    """Create cute cartoon ninja standing with dual swords on back"""
    width = 64
    height = 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette - cartoon ninja theme
    OUTFIT_NAVY = [20, 20, 22, 255]       # Black outfit
    OUTFIT_DARK = [10, 10, 12, 255]       # Darker black
    OUTFIT_LIGHT = [35, 35, 40, 255]      # Light black/dark grey highlights
    
    ACCENT_RED = [180, 70, 60, 255]       # Red/rust accent
    ACCENT_DARK = [140, 50, 45, 255]      # Dark red
    ACCENT_LIGHT = [200, 90, 75, 255]     # Light red
    
    SKIN_LIGHT = [255, 220, 180, 255]     # Light skin
    SKIN_SHADOW = [210, 180, 150, 255]    # Skin shadow
    
    EYE_BLACK = [20, 20, 25, 255]         # Eye black
    EYE_SHINE = [255, 255, 255, 255]      # Eye shine
    
    BOOT_BLACK = [25, 30, 35, 255]        # Black boots
    BOOT_SHADOW = [15, 18, 22, 255]       # Boot shadow
    
    SWORD_YELLOW = [230, 200, 90, 255]    # Yellow/gold sword handle
    SWORD_DARK = [180, 150, 60, 255]      # Dark yellow
    SWORD_BLADE = [200, 210, 220, 255]    # Silver blade
    
    # Position ninja (centered, standing upright)
    center_x = 32
    base_y = 62  # Bottom of feet
    
    
    # === BOOTS (black with red wraps) ===
    # Left boot
    left_foot_x = center_x - 6
    for y in range(base_y - 6, base_y):
        for x in range(left_foot_x - 3, left_foot_x + 3):
            if 0 <= x < width and 0 <= y < height:
                if y < base_y - 3:
                    canvas[y][x] = BOOT_BLACK if x < left_foot_x else BOOT_SHADOW
                else:
                    canvas[y][x] = BOOT_BLACK
    
    # Left boot wraps (red)
    for wrap_y in [base_y - 5, base_y - 3]:
        for x in range(left_foot_x - 3, left_foot_x + 3):
            if 0 <= x < width and 0 <= wrap_y < height:
                canvas[wrap_y][x] = ACCENT_RED
                if wrap_y + 1 < height:
                    canvas[wrap_y + 1][x] = ACCENT_DARK
    
    # Right boot
    right_foot_x = center_x + 6
    for y in range(base_y - 6, base_y):
        for x in range(right_foot_x - 3, right_foot_x + 3):
            if 0 <= x < width and 0 <= y < height:
                if y < base_y - 3:
                    canvas[y][x] = BOOT_BLACK if x < right_foot_x else BOOT_SHADOW
                else:
                    canvas[y][x] = BOOT_BLACK
    
    # Right boot wraps (red)
    for wrap_y in [base_y - 5, base_y - 3]:
        for x in range(right_foot_x - 3, right_foot_x + 3):
            if 0 <= x < width and 0 <= wrap_y < height:
                canvas[wrap_y][x] = ACCENT_RED
                if wrap_y + 1 < height:
                    canvas[wrap_y + 1][x] = ACCENT_DARK
    
    # === LEGS (navy blue pants) ===
    # Left leg
    for y in range(base_y - 22, base_y - 6):
        leg_width = 3 if y < base_y - 12 else 4
        for x in range(left_foot_x - leg_width, left_foot_x + leg_width):
            if 0 <= x < width and 0 <= y < height:
                canvas[y][x] = OUTFIT_NAVY if x < left_foot_x else OUTFIT_DARK
    
    # Right leg
    for y in range(base_y - 22, base_y - 6):
        leg_width = 3 if y < base_y - 12 else 4
        for x in range(right_foot_x - leg_width, right_foot_x + leg_width):
            if 0 <= x < width and 0 <= y < height:
                canvas[y][x] = OUTFIT_NAVY if x < right_foot_x else OUTFIT_DARK
    
    
    # === TORSO (navy with red sash/vest) ===
    torso_y = base_y - 36
    
    # Main body (rounded, cute style) - fill entire torso first
    for dy in range(-14, 15):
        body_width = 11 - abs(dy) // 3
        for dx in range(-body_width, body_width + 1):
            tx = center_x + dx
            ty = torso_y + dy
            if 0 <= tx < width and 0 <= ty < height:
                # Fill with navy blue
                canvas[ty][tx] = OUTFIT_NAVY if abs(dx) > 3 else OUTFIT_LIGHT
    
    # Red vest/sash in center (on top of navy)
    for dy in range(-12, 15):
        for dx in range(-3, 4):
            if abs(dx) <= 2:
                tx = center_x + dx
                ty = torso_y + dy
                if 0 <= tx < width and 0 <= ty < height:
                    if dx == 0:
                        canvas[ty][tx] = ACCENT_DARK
                    else:
                        canvas[ty][tx] = ACCENT_RED if abs(dx) == 1 else ACCENT_LIGHT
    
    # Red belt/sash around waist (higher and narrower like reference)
    belt_y = base_y - 28
    for belt_row in range(3):
        for x in range(center_x - 8, center_x + 9):
            if 0 <= x < width and 0 <= belt_y + belt_row < height:
                if belt_row == 0 or belt_row == 2:
                    canvas[belt_y + belt_row][x] = ACCENT_DARK
                else:
                    canvas[belt_y + belt_row][x] = ACCENT_RED
    
    # Belt knot on side (adjusted to new belt position)
    knot_x = center_x + 7
    knot_y = base_y - 26
    for dy in range(-2, 4):
        for dx in range(-2, 3):
            kx = knot_x + dx
            ky = knot_y + dy
            if 0 <= kx < width and 0 <= ky < height:
                if abs(dx) + abs(dy) < 4:
                    canvas[ky][kx] = ACCENT_RED if dy > 0 else ACCENT_DARK
    
    
    # === ARMS (simple, rounded) ===
    arm_y = torso_y - 8
    
    # Left arm
    left_arm_x = center_x - 10
    for dy in range(0, 14):
        for dx in range(-3, 3):
            ax = left_arm_x + dx
            ay = arm_y + dy
            if 0 <= ax < width and 0 <= ay < height:
                if dy < 8:
                    canvas[ay][ax] = OUTFIT_NAVY if dx < 0 else OUTFIT_DARK
                else:
                    # Red cuff
                    canvas[ay][ax] = ACCENT_RED if dy < 10 else ACCENT_DARK
    
    # Left hand
    hand_y = arm_y + 14
    for dy in range(0, 3):
        for dx in range(-2, 3):
            hx = left_arm_x + dx
            hy = hand_y + dy
            if 0 <= hx < width and 0 <= hy < height:
                canvas[hy][hx] = SKIN_LIGHT if abs(dx) < 2 else SKIN_SHADOW
    
    # Right arm
    right_arm_x = center_x + 10
    for dy in range(0, 14):
        for dx in range(-3, 3):
            ax = right_arm_x + dx
            ay = arm_y + dy
            if 0 <= ax < width and 0 <= ay < height:
                if dy < 8:
                    canvas[ay][ax] = OUTFIT_NAVY if dx > 0 else OUTFIT_DARK
                else:
                    # Red cuff
                    canvas[ay][ax] = ACCENT_RED if dy < 10 else ACCENT_DARK
    
    # Right hand
    for dy in range(0, 3):
        for dx in range(-2, 3):
            hx = right_arm_x + dx
            hy = hand_y + dy
            if 0 <= hx < width and 0 <= hy < height:
                canvas[hy][hx] = SKIN_LIGHT if abs(dx) < 2 else SKIN_SHADOW
    
    # === DUAL SWORDS ON BACK (crossing behind head like reference) ===
    sword_left_x = center_x - 8
    sword_right_x = center_x + 8
    sword_bottom_y = torso_y + 5
    sword_top_y = 8
    
    # Left sword - angled from left shoulder up behind head
    for i in range(45):
        sx = sword_left_x - i // 3
        sy = sword_bottom_y - i
        if 0 <= sx < width and 0 <= sy < height and sy >= sword_top_y:
            # Handle (bottom 10 pixels with stripes)
            if i < 10:
                if i % 3 == 0:
                    canvas[sy][sx] = SWORD_DARK
                    if sx - 1 >= 0:
                        canvas[sy][sx - 1] = SWORD_DARK
                    if sx + 1 < width:
                        canvas[sy][sx + 1] = SWORD_DARK
                else:
                    canvas[sy][sx] = SWORD_YELLOW
                    if sx - 1 >= 0:
                        canvas[sy][sx - 1] = SWORD_YELLOW
                    if sx + 1 < width:
                        canvas[sy][sx + 1] = SWORD_YELLOW
            else:
                # Blade
                canvas[sy][sx] = SWORD_BLADE
                if sx + 1 < width:
                    canvas[sy][sx + 1] = SWORD_BLADE
    
    # Right sword - angled from right shoulder up behind head
    for i in range(45):
        sx = sword_right_x + i // 3
        sy = sword_bottom_y - i
        if 0 <= sx < width and 0 <= sy < height and sy >= sword_top_y:
            # Handle (bottom 10 pixels with stripes)
            if i < 10:
                if i % 3 == 0:
                    canvas[sy][sx] = SWORD_DARK
                    if sx - 1 >= 0:
                        canvas[sy][sx - 1] = SWORD_DARK
                    if sx + 1 < width:
                        canvas[sy][sx + 1] = SWORD_DARK
                else:
                    canvas[sy][sx] = SWORD_YELLOW
                    if sx - 1 >= 0:
                        canvas[sy][sx - 1] = SWORD_YELLOW
                    if sx + 1 < width:
                        canvas[sy][sx + 1] = SWORD_YELLOW
            else:
                # Blade
                canvas[sy][sx] = SWORD_BLADE
                if sx - 1 >= 0:
                    canvas[sy][sx - 1] = SWORD_BLADE
    
    
    # === HEAD (round, cute ninja) ===
    head_y = torso_y - 20
    
    # Round head shape
    for dy in range(-8, 9):
        for dx in range(-8, 9):
            dist = (dx*dx + dy*dy) ** 0.5
            if dist <= 8:
                hx = center_x + dx
                hy = head_y + dy
                if 0 <= hx < width and 0 <= hy < height:
                    # Navy hood/mask
                    if dy < 2:
                        # Upper part of head
                        if dx < -4:
                            canvas[hy][hx] = OUTFIT_DARK
                        elif dx < 0:
                            canvas[hy][hx] = OUTFIT_NAVY
                        elif dx < 4:
                            canvas[hy][hx] = OUTFIT_LIGHT
                        else:
                            canvas[hy][hx] = OUTFIT_NAVY
                    else:
                        # Mask area (lower face)
                        canvas[hy][hx] = OUTFIT_NAVY if abs(dx) < 4 else OUTFIT_DARK
    
    # Eye slit area (better version from attack animation)
    for y in range(head_y - 2, head_y + 3):
        for x in range(center_x - 7, center_x + 8):
            if 0 <= x < width and 0 <= y < height:
                canvas[y][x] = SKIN_LIGHT if abs(x - center_x) < 6 else SKIN_SHADOW
    
    # Eyes (better version from attack animation - simpler, cleaner)
    left_eye_x = center_x - 3
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            if abs(dx) <= 1 and abs(dy) <= 1:
                ex = left_eye_x + dx
                ey = head_y + dy
                if 0 <= ex < width and 0 <= ey < height:
                    canvas[ey][ex] = EYE_BLACK
    
    if 0 <= left_eye_x - 1 < width and 0 <= head_y - 1 < height:
        canvas[head_y - 1][left_eye_x - 1] = SKIN_LIGHT
    
    right_eye_x = center_x + 3
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            if abs(dx) <= 1 and abs(dy) <= 1:
                ex = right_eye_x + dx
                ey = head_y + dy
                if 0 <= ex < width and 0 <= ey < height:
                    canvas[ey][ex] = EYE_BLACK
    
    if 0 <= right_eye_x - 1 < width and 0 <= head_y - 1 < height:
        canvas[head_y - 1][right_eye_x - 1] = SKIN_LIGHT
    
    return canvas


def create_ninja_attack():
    """Create cute ninja attack - pulling one sword from back"""
    width = 64
    height = 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Same color palette as default
    OUTFIT_NAVY = [20, 20, 22, 255]       # Black outfit
    OUTFIT_DARK = [10, 10, 12, 255]       # Darker black
    OUTFIT_LIGHT = [35, 35, 40, 255]      # Light black/dark grey highlights
    
    ACCENT_RED = [180, 70, 60, 255]
    ACCENT_DARK = [140, 50, 45, 255]
    ACCENT_LIGHT = [200, 90, 75, 255]
    
    SKIN_LIGHT = [255, 220, 180, 255]
    SKIN_SHADOW = [210, 180, 150, 255]
    
    EYE_BLACK = [20, 20, 25, 255]
    EYE_SHINE = [255, 255, 255, 255]
    
    BOOT_BLACK = [25, 30, 35, 255]
    BOOT_SHADOW = [15, 18, 22, 255]
    
    SWORD_YELLOW = [230, 200, 90, 255]
    SWORD_DARK = [180, 150, 60, 255]
    SWORD_BLADE = [200, 210, 220, 255]
    
    # Motion effects
    MOTION_BLUR = [150, 170, 200, 120]
    
    center_x = 32
    base_y = 62
    
    
    # === BOOTS (same as default) ===
    left_foot_x = center_x - 6
    for y in range(base_y - 6, base_y):
        for x in range(left_foot_x - 3, left_foot_x + 3):
            if 0 <= x < width and 0 <= y < height:
                if y < base_y - 3:
                    canvas[y][x] = BOOT_BLACK if x < left_foot_x else BOOT_SHADOW
                else:
                    canvas[y][x] = BOOT_BLACK
    
    for wrap_y in [base_y - 5, base_y - 3]:
        for x in range(left_foot_x - 3, left_foot_x + 3):
            if 0 <= x < width and 0 <= wrap_y < height:
                canvas[wrap_y][x] = ACCENT_RED
                if wrap_y + 1 < height:
                    canvas[wrap_y + 1][x] = ACCENT_DARK
    
    right_foot_x = center_x + 6
    for y in range(base_y - 6, base_y):
        for x in range(right_foot_x - 3, right_foot_x + 3):
            if 0 <= x < width and 0 <= y < height:
                if y < base_y - 3:
                    canvas[y][x] = BOOT_BLACK if x < right_foot_x else BOOT_SHADOW
                else:
                    canvas[y][x] = BOOT_BLACK
    
    for wrap_y in [base_y - 5, base_y - 3]:
        for x in range(right_foot_x - 3, right_foot_x + 3):
            if 0 <= x < width and 0 <= wrap_y < height:
                canvas[wrap_y][x] = ACCENT_RED
                if wrap_y + 1 < height:
                    canvas[wrap_y + 1][x] = ACCENT_DARK
    
    # === LEGS (same as default) ===
    for y in range(base_y - 22, base_y - 6):
        leg_width = 3 if y < base_y - 12 else 4
        for x in range(left_foot_x - leg_width, left_foot_x + leg_width):
            if 0 <= x < width and 0 <= y < height:
                canvas[y][x] = OUTFIT_NAVY if x < left_foot_x else OUTFIT_DARK
    
    for y in range(base_y - 22, base_y - 6):
        leg_width = 3 if y < base_y - 12 else 4
        for x in range(right_foot_x - leg_width, right_foot_x + leg_width):
            if 0 <= x < width and 0 <= y < height:
                canvas[y][x] = OUTFIT_NAVY if x < right_foot_x else OUTFIT_DARK
    
    # === TORSO (same as default) ===
    torso_y = base_y - 36
    
    for dy in range(-14, 15):
        body_width = 11 - abs(dy) // 3
        for dx in range(-body_width, body_width + 1):
            tx = center_x + dx
            ty = torso_y + dy
            if 0 <= tx < width and 0 <= ty < height:
                canvas[ty][tx] = OUTFIT_NAVY if abs(dx) > 3 else OUTFIT_LIGHT
    
    for dy in range(-12, 15):
        for dx in range(-3, 4):
            if abs(dx) <= 2:
                tx = center_x + dx
                ty = torso_y + dy
                if 0 <= tx < width and 0 <= ty < height:
                    if dx == 0:
                        canvas[ty][tx] = ACCENT_DARK
                    else:
                        canvas[ty][tx] = ACCENT_RED if abs(dx) == 1 else ACCENT_LIGHT
    
    # Red belt/sash around waist (higher and narrower like reference)
    belt_y = base_y - 28
    for belt_row in range(3):
        for x in range(center_x - 8, center_x + 9):
            if 0 <= x < width and 0 <= belt_y + belt_row < height:
                if belt_row == 0 or belt_row == 2:
                    canvas[belt_y + belt_row][x] = ACCENT_DARK
                else:
                    canvas[belt_y + belt_row][x] = ACCENT_RED
    
    # Belt knot on side (adjusted to new belt position)
    knot_x = center_x + 7
    knot_y = base_y - 26
    for dy in range(-2, 4):
        for dx in range(-2, 3):
            kx = knot_x + dx
            ky = knot_y + dy
            if 0 <= kx < width and 0 <= ky < height:
                if abs(dx) + abs(dy) < 4:
                    canvas[ky][kx] = ACCENT_RED if dy > 0 else ACCENT_DARK
    
    # === LEFT ARM (normal, at side) ===
    arm_y = torso_y - 8
    left_arm_x = center_x - 10
    for dy in range(0, 14):
        for dx in range(-3, 3):
            ax = left_arm_x + dx
            ay = arm_y + dy
            if 0 <= ax < width and 0 <= ay < height:
                if dy < 8:
                    canvas[ay][ax] = OUTFIT_NAVY if dx < 0 else OUTFIT_DARK
                else:
                    canvas[ay][ax] = ACCENT_RED if dy < 10 else ACCENT_DARK
    
    hand_y = arm_y + 14
    for dy in range(0, 3):
        for dx in range(-2, 3):
            hx = left_arm_x + dx
            hy = hand_y + dy
            if 0 <= hx < width and 0 <= hy < height:
                canvas[hy][hx] = SKIN_LIGHT if abs(dx) < 2 else SKIN_SHADOW
    
    # === RIGHT ARM (extended down and out, holding sword) ===
    right_arm_x = center_x + 10
    # Arm extending down and outward
    for i in range(16):
        ax = right_arm_x + i // 3
        ay = arm_y + i
        for dx in range(-3, 3):
            px = ax + dx
            if 0 <= px < width and 0 <= ay < height:
                canvas[ay][px] = OUTFIT_NAVY if dx > 0 else OUTFIT_DARK
    
    # Hand
    hand_x = right_arm_x + 5
    hand_y = arm_y + 16
    for dy in range(-3, 3):
        for dx in range(-2, 3):
            hx = hand_x + dx
            hy = hand_y + dy
            if 0 <= hx < width and 0 <= hy < height:
                canvas[hy][hx] = SKIN_LIGHT if abs(dx) < 2 and abs(dy) < 2 else SKIN_SHADOW
    
    # === SWORD (held down and out, diagonal) ===
    sword_handle_x = hand_x
    sword_handle_y = hand_y
    
    # Handle (striped)
    for i in range(8):
        hx = sword_handle_x + i // 2
        hy = sword_handle_y + i
        if 0 <= hx < width and 0 <= hy < height:
            if i % 3 == 0:
                canvas[hy][hx] = SWORD_DARK
                if hx - 1 >= 0:
                    canvas[hy][hx - 1] = SWORD_DARK
                if hx + 1 < width:
                    canvas[hy][hx + 1] = SWORD_DARK
            else:
                canvas[hy][hx] = SWORD_YELLOW
                if hx - 1 >= 0:
                    canvas[hy][hx - 1] = SWORD_YELLOW
                if hx + 1 < width:
                    canvas[hy][hx + 1] = SWORD_YELLOW
    
    # Blade (extending down and out)
    for i in range(15):
        bx = sword_handle_x + (i + 8) // 2
        by = sword_handle_y + i + 8
        if 0 <= bx < width and 0 <= by < height:
            canvas[by][bx] = SWORD_BLADE
    
    # Motion blur (adjusted for downward motion)
    for i in range(8):
        mx = hand_x - i
        my = hand_y - i * 2
        if 0 <= mx < width and 0 <= my < height:
            canvas[my][mx] = MOTION_BLUR
    
    # === ONE SWORD ON BACK (left sword - crossed pattern) ===
    # Left sword angled from left shoulder up behind head
    sword_left_x = center_x - 8
    sword_bottom_y = torso_y + 5
    sword_top_y = 8
    
    for i in range(45):
        sx = sword_left_x - i // 3
        sy = sword_bottom_y - i
        if 0 <= sx < width and 0 <= sy < height and sy >= sword_top_y:
            # Handle (bottom 10 pixels with stripes)
            if i < 10:
                if i % 3 == 0:
                    canvas[sy][sx] = SWORD_DARK
                    if sx - 1 >= 0:
                        canvas[sy][sx - 1] = SWORD_DARK
                    if sx + 1 < width:
                        canvas[sy][sx + 1] = SWORD_DARK
                else:
                    canvas[sy][sx] = SWORD_YELLOW
                    if sx - 1 >= 0:
                        canvas[sy][sx - 1] = SWORD_YELLOW
                    if sx + 1 < width:
                        canvas[sy][sx + 1] = SWORD_YELLOW
            else:
                # Blade
                canvas[sy][sx] = SWORD_BLADE
                if sx + 1 < width:
                    canvas[sy][sx + 1] = SWORD_BLADE
    
    # === HEAD (same as default - cute cartoon) ===
    head_y = torso_y - 20
    
    for dy in range(-8, 9):
        for dx in range(-8, 9):
            dist = (dx * dx + dy * dy) ** 0.5
            if dist <= 8:
                hx = center_x + dx
                hy = head_y + dy
                if 0 <= hx < width and 0 <= hy < height:
                    if dx < -1:
                        canvas[hy][hx] = OUTFIT_DARK
                    elif dx < 1:
                        canvas[hy][hx] = OUTFIT_NAVY
                    else:
                        canvas[hy][hx] = OUTFIT_LIGHT
    
    for y in range(head_y - 2, head_y + 3):
        for x in range(center_x - 7, center_x + 8):
            if 0 <= x < width and 0 <= y < height:
                canvas[y][x] = SKIN_LIGHT if abs(x - center_x) < 6 else SKIN_SHADOW
    
    left_eye_x = center_x - 3
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            if abs(dx) <= 1 and abs(dy) <= 1:
                ex = left_eye_x + dx
                ey = head_y + dy
                if 0 <= ex < width and 0 <= ey < height:
                    canvas[ey][ex] = EYE_BLACK
    
    if 0 <= left_eye_x - 1 < width and 0 <= head_y - 1 < height:
        canvas[head_y - 1][left_eye_x - 1] = SKIN_LIGHT
    
    right_eye_x = center_x + 3
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            if abs(dx) <= 1 and abs(dy) <= 1:
                ex = right_eye_x + dx
                ey = head_y + dy
                if 0 <= ex < width and 0 <= ey < height:
                    canvas[ey][ex] = EYE_BLACK
    
    if 0 <= right_eye_x - 1 < width and 0 <= head_y - 1 < height:
        canvas[head_y - 1][right_eye_x - 1] = SKIN_LIGHT

    
    return canvas


def create_ninja_death():
    """Create ninja death animation - fallen flat on ground with blood"""
    width = 64
    height = 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette (same as updated default)
    OUTFIT_NAVY = [20, 20, 22, 255]       # Black outfit
    OUTFIT_DARK = [10, 10, 12, 255]       # Darker black
    OUTFIT_LIGHT = [35, 35, 40, 255]      # Light black/dark grey highlights
    
    ACCENT_RED = [180, 70, 60, 255]
    ACCENT_DARK = [140, 50, 45, 255]
    ACCENT_LIGHT = [200, 90, 75, 255]
    
    SKIN_LIGHT = [255, 220, 180, 255]
    SKIN_SHADOW = [200, 170, 140, 255]
    
    EYE_BLACK = [20, 20, 25, 255]
    
    BOOT_BLACK = [25, 30, 35, 255]
    BOOT_SHADOW = [15, 20, 25, 255]
    
    SWORD_YELLOW = [230, 200, 90, 255]
    SWORD_DARK = [180, 150, 60, 255]
    SWORD_BLADE = [200, 210, 220, 255]
    
    # Blood colors
    BLOOD_DARK = [100, 0, 0, 255]
    BLOOD_MID = [140, 20, 20, 255]
    BLOOD_LIGHT = [180, 40, 40, 255]
    
    center_x = 32
    base_y = 50  # Center figure higher to show lying flat
    
    # === BLOOD POOL (underneath ninja) ===
    blood_y = base_y + 8
    for y in range(blood_y - 4, blood_y + 8):
        for x in range(center_x - 18, center_x + 18):
            if 0 <= x < width and 0 <= y < height:
                dx = x - center_x
                dy = y - blood_y
                dist = (dx * dx * 0.3 + dy * dy) ** 0.5
                if dist < 12:
                    if dist < 4:
                        canvas[y][x] = BLOOD_DARK
                    elif dist < 8:
                        canvas[y][x] = BLOOD_MID if (x + y) % 2 == 0 else BLOOD_DARK
                    else:
                        canvas[y][x] = BLOOD_LIGHT if (x + y) % 3 == 0 else BLOOD_MID
    
    # === LEGS (lying flat, extended) ===
    left_leg_x = center_x - 6
    right_leg_x = center_x + 6
    
    # Left leg
    for y in range(base_y + 6, base_y + 20):
        for x in range(left_leg_x - 3, left_leg_x + 3):
            if 0 <= x < width and 0 <= y < height:
                canvas[y][x] = OUTFIT_NAVY if x < left_leg_x else OUTFIT_DARK
    
    # Right leg
    for y in range(base_y + 6, base_y + 20):
        for x in range(right_leg_x - 3, right_leg_x + 3):
            if 0 <= x < width and 0 <= y < height:
                canvas[y][x] = OUTFIT_NAVY if x < right_leg_x else OUTFIT_DARK
    
    # === BOOTS ===
    for foot_x in [left_leg_x, right_leg_x]:
        for y in range(base_y + 20, min(base_y + 26, height)):
            for x in range(foot_x - 3, foot_x + 3):
                if 0 <= x < width and 0 <= y < height:
                    canvas[y][x] = BOOT_BLACK if x < foot_x else BOOT_SHADOW
        
        # Red wrap
        wrap_y = base_y + 22
        for x in range(foot_x - 3, foot_x + 3):
            if 0 <= x < width and 0 <= wrap_y < height:
                canvas[wrap_y][x] = ACCENT_RED
    
    # === TORSO (lying flat on back) ===
    torso_y = base_y - 4
    
    for dy in range(-8, 10):
        body_width = 10 - abs(dy) // 3
        for dx in range(-body_width, body_width + 1):
            tx = center_x + dx
            ty = torso_y + dy
            if 0 <= tx < width and 0 <= ty < height:
                canvas[ty][tx] = OUTFIT_NAVY if abs(dx) > 3 else OUTFIT_LIGHT
    
    # Red vest/sash
    for dy in range(-6, 10):
        for dx in range(-3, 4):
            if abs(dx) <= 2:
                tx = center_x + dx
                ty = torso_y + dy
                if 0 <= tx < width and 0 <= ty < height:
                    if dx == 0:
                        canvas[ty][tx] = ACCENT_DARK
                    else:
                        canvas[ty][tx] = ACCENT_RED if abs(dx) == 1 else ACCENT_LIGHT
    
    # === ARMS (spread out on ground) ===
    arm_y = torso_y
    
    # Left arm extended outward
    left_arm_x = center_x - 10
    for i in range(12):
        ax = left_arm_x - i
        for dy in range(-2, 3):
            ay = arm_y + dy
            if 0 <= ax < width and 0 <= ay < height:
                canvas[ay][ax] = OUTFIT_NAVY if abs(dy) <= 1 else OUTFIT_DARK
        
        # Red cuff near end
        if i > 6:
            for dy in range(-2, 3):
                ay = arm_y + dy
                if 0 <= left_arm_x - i < width and 0 <= ay < height:
                    canvas[ay][left_arm_x - i] = ACCENT_RED
    
    # Left hand
    hand_x = left_arm_x - 12
    for dy in range(-2, 3):
        for dx in range(-2, 2):
            hx = hand_x + dx
            hy = arm_y + dy
            if 0 <= hx < width and 0 <= hy < height:
                canvas[hy][hx] = SKIN_LIGHT if abs(dy) <= 1 else SKIN_SHADOW
    
    # Right arm extended outward
    right_arm_x = center_x + 10
    for i in range(12):
        ax = right_arm_x + i
        for dy in range(-2, 3):
            ay = arm_y + dy
            if 0 <= ax < width and 0 <= ay < height:
                canvas[ay][ax] = OUTFIT_NAVY if abs(dy) <= 1 else OUTFIT_DARK
        
        # Red cuff near end
        if i > 6:
            for dy in range(-2, 3):
                ay = arm_y + dy
                if 0 <= right_arm_x + i < width and 0 <= ay < height:
                    canvas[ay][right_arm_x + i] = ACCENT_RED
    
    # Right hand
    hand_x = right_arm_x + 12
    for dy in range(-2, 3):
        for dx in range(-2, 2):
            hx = hand_x + dx
            hy = arm_y + dy
            if 0 <= hx < width and 0 <= hy < height:
                canvas[hy][hx] = SKIN_LIGHT if abs(dy) <= 1 else SKIN_SHADOW
    
    # === HEAD (lying on side, facing up) ===
    head_y = torso_y - 12
    
    # Round head
    for dy in range(-8, 9):
        for dx in range(-8, 9):
            dist = (dx * dx + dy * dy) ** 0.5
            if dist <= 8:
                hx = center_x + dx
                hy = head_y + dy
                if 0 <= hx < width and 0 <= hy < height:
                    if dx < -1:
                        canvas[hy][hx] = OUTFIT_DARK
                    elif dx < 1:
                        canvas[hy][hx] = OUTFIT_NAVY
                    else:
                        canvas[hy][hx] = OUTFIT_LIGHT
    
    # Eye slit area
    for y in range(head_y - 2, head_y + 3):
        for x in range(center_x - 7, center_x + 8):
            if 0 <= x < width and 0 <= y < height:
                canvas[y][x] = SKIN_LIGHT if abs(x - center_x) < 6 else SKIN_SHADOW
    
    # X eyes (defeated)
    left_eye_x = center_x - 3
    right_eye_x = center_x + 3
    
    for eye_x in [left_eye_x, right_eye_x]:
        # Draw X
        for i in range(-2, 3):
            # Diagonal \
            if 0 <= eye_x + i < width and 0 <= head_y + i < height:
                canvas[head_y + i][eye_x + i] = EYE_BLACK
            # Diagonal /
            if 0 <= eye_x + i < width and 0 <= head_y - i < height:
                canvas[head_y - i][eye_x + i] = EYE_BLACK
    
    # === DROPPED SWORDS (both fallen beside ninja) ===
    # Left sword
    sword_left_x = center_x - 16
    sword_y = base_y + 2
    
    for i in range(10):
        sx = sword_left_x + i
        if 0 <= sx < width and 0 <= sword_y < height:
            if i < 4:
                # Handle
                if i % 2 == 0:
                    canvas[sword_y][sx] = SWORD_DARK
                else:
                    canvas[sword_y][sx] = SWORD_YELLOW
            else:
                # Blade
                canvas[sword_y][sx] = SWORD_BLADE
    
    # Right sword
    sword_right_x = center_x + 6
    for i in range(10):
        sx = sword_right_x + i
        if 0 <= sx < width and 0 <= sword_y < height:
            if i < 4:
                # Handle
                if i % 2 == 0:
                    canvas[sword_y][sx] = SWORD_DARK
                else:
                    canvas[sword_y][sx] = SWORD_YELLOW
            else:
                # Blade
                canvas[sword_y][sx] = SWORD_BLADE
    
    return canvas
    
    return canvas


def main():
    """Create and save all three ninja hero images"""
    print("Creating ninja hero images...")
    
    # Create all three images
    ninja_default = create_ninja_default()
    ninja_attack = create_ninja_attack()
    ninja_death = create_ninja_death()
    
    # Convert to PIL and scale up
    scale = 4
    
    # Default pose
    img_default = Image.fromarray(ninja_default, 'RGBA')
    img_default_scaled = img_default.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_default_scaled.save("../art/ninja_hero.png")
    print("✓ Saved: ninja_hero.png (256x256)")
    
    # Attack animation
    img_attack = Image.fromarray(ninja_attack, 'RGBA')
    img_attack_scaled = img_attack.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_attack_scaled.save("../art/ninja_hero_attack.png")
    print("✓ Saved: ninja_hero_attack.png (256x256)")
    
    # Death animation
    img_death = Image.fromarray(ninja_death, 'RGBA')
    img_death_scaled = img_death.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_death_scaled.save("../art/ninja_hero_death.png")
    print("✓ Saved: ninja_hero_death.png (256x256)")
    
    print("\n✅ Cute cartoon ninja hero creation complete!")
    print("\nFeatures:")
    print("- Default: Cute ninja standing with dual swords on back")
    print("- Attack: Dynamic sword slash with motion blur arc")
    print("- Death: Fallen ninja with blood pool, dropped sword, closed eyes")
    print("\nStyle: Cute cartoon pixel art")
    print("Colors: Navy blue outfit, red/orange accents, yellow striped sword handles, big cute eyes")


if __name__ == "__main__":
    main()
