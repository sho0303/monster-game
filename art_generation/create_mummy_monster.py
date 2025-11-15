"""
Mummy Monster Creator
Creates pixel art for an ancient mummy - wrapped in bandages with glowing yellow eyes.
Inspired by classic Egyptian mummies with tattered wrappings and shambling movement.

Resolution: 64x64 pixels (scaled 4x to 256x256)
Style: Pixel art with detailed bandage wrapping patterns
Palette: Tan/beige bandages, yellow glowing eyes, shadow browns
"""

from PIL import Image
import numpy as np


def create_mummy_default():
    """Create the default shambling mummy pose."""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette - inspired by the mummy image
    BANDAGE_TAN = [180, 165, 130, 255]      # Main bandage color
    BANDAGE_LIGHT = [200, 185, 150, 255]    # Light bandage highlights
    BANDAGE_DARK = [140, 125, 95, 255]      # Dark bandage shadows
    BANDAGE_SHADOW = [110, 95, 70, 255]     # Deep shadows in wrappings
    BANDAGE_DIRTY = [160, 145, 110, 255]    # Dirty/aged bandages
    EYE_YELLOW = [240, 220, 80, 255]        # Glowing yellow eyes
    EYE_ORANGE = [220, 180, 60, 255]        # Orange eye glow
    EYE_DARK = [30, 25, 20, 255]            # Eye socket darkness
    WRAP_LINE_DARK = [100, 85, 60, 255]     # Bandage wrap lines
    WRAP_LINE_LIGHT = [190, 175, 140, 255]  # Light wrap lines
    
    center_x = 32
    base_y = 61
    
    # === LEGS (wrapped in bandages, shambling stance) ===
    # Left leg
    for ly in range(20):
        leg_width = 4 - ly // 12
        for lx in range(-leg_width, leg_width + 1):
            leg_x = center_x - 6 + lx
            leg_y = base_y - ly
            if 0 <= leg_x < width and 0 <= leg_y < height:
                # Bandage wrapping with shadows
                if lx < -2:
                    canvas[leg_y][leg_x] = BANDAGE_SHADOW
                elif lx < 0:
                    canvas[leg_y][leg_x] = BANDAGE_DARK
                elif lx < 2:
                    canvas[leg_y][leg_x] = BANDAGE_TAN
                else:
                    canvas[leg_y][leg_x] = BANDAGE_LIGHT
    
    # Right leg
    for ly in range(20):
        leg_width = 4 - ly // 12
        for lx in range(-leg_width, leg_width + 1):
            leg_x = center_x + 6 + lx
            leg_y = base_y - ly
            if 0 <= leg_x < width and 0 <= leg_y < height:
                if lx < -1:
                    canvas[leg_y][leg_x] = BANDAGE_DARK
                elif lx < 1:
                    canvas[leg_y][leg_x] = BANDAGE_TAN
                elif lx < 3:
                    canvas[leg_y][leg_x] = BANDAGE_LIGHT
                else:
                    canvas[leg_y][leg_x] = BANDAGE_DARK
    
    # Horizontal wrap lines on legs
    for wrap_y in [base_y - 5, base_y - 10, base_y - 15]:
        for wx in range(-10, 11):
            if abs(wx) < 10:
                wrap_x = center_x + wx
                if 0 <= wrap_x < width and 0 <= wrap_y < height:
                    canvas[wrap_y][wrap_x] = WRAP_LINE_DARK
    
    # Feet (wrapped)
    for foot_offset in [-6, 6]:
        for fy in range(3):
            for fx in range(-4, 5):
                foot_x = center_x + foot_offset + fx
                foot_y = base_y + fy
                if 0 <= foot_x < width and 0 <= foot_y < height:
                    if fy > 1:
                        canvas[foot_y][foot_x] = BANDAGE_SHADOW
                    elif abs(fx) < 2:
                        canvas[foot_y][foot_x] = BANDAGE_TAN
                    else:
                        canvas[foot_y][foot_x] = BANDAGE_DARK
    
    # === TORSO (cylindrical, wrapped in bandages) ===
    torso_y = base_y - 20
    for ty in range(18):
        torso_width = 10 - ty // 10
        for tx in range(-torso_width, torso_width + 1):
            torso_x = center_x + tx
            torso_ypos = torso_y - ty
            if 0 <= torso_x < width and 0 <= torso_ypos < height:
                # Layered bandage wrapping
                if tx < -7:
                    canvas[torso_ypos][torso_x] = BANDAGE_SHADOW
                elif tx < -3:
                    canvas[torso_ypos][torso_x] = BANDAGE_DARK
                elif tx < -1:
                    canvas[torso_ypos][torso_x] = BANDAGE_DIRTY
                elif tx < 1:
                    canvas[torso_ypos][torso_x] = BANDAGE_TAN
                elif tx < 3:
                    canvas[torso_ypos][torso_x] = BANDAGE_LIGHT
                elif tx < 7:
                    canvas[torso_ypos][torso_x] = BANDAGE_TAN
                else:
                    canvas[torso_ypos][torso_x] = BANDAGE_DARK
    
    # Horizontal wrap lines on torso
    for wrap_y_offset in [2, 6, 10, 14]:
        wrap_y = torso_y - wrap_y_offset
        for wx in range(-9, 10):
            wrap_x = center_x + wx
            if 0 <= wrap_x < width and 0 <= wrap_y < height:
                if abs(wx) < 9:
                    canvas[wrap_y][wrap_x] = WRAP_LINE_DARK if wx % 2 == 0 else BANDAGE_SHADOW
    
    # Vertical wrap lines (loose bandages)
    for vx_offset in [-4, 0, 4]:
        for vy in range(18):
            v_x = center_x + vx_offset
            v_y = torso_y - vy
            if 0 <= v_x < width and 0 <= v_y < height:
                if vy % 3 == 0:
                    canvas[v_y][v_x] = WRAP_LINE_LIGHT
    
    # === ARMS (wrapped, hanging/reaching) ===
    arm_y = torso_y - 16
    
    # Left arm (hanging forward)
    for ay in range(18):
        arm_width = 3 - ay // 12
        for ax in range(-arm_width, arm_width + 1):
            arm_x = center_x - 11 + ax
            arm_ypos = arm_y + ay
            if 0 <= arm_x < width and 0 <= arm_ypos < height:
                if ax < -1:
                    canvas[arm_ypos][arm_x] = BANDAGE_DARK
                elif ax < 1:
                    canvas[arm_ypos][arm_x] = BANDAGE_TAN
                else:
                    canvas[arm_ypos][arm_x] = BANDAGE_LIGHT
    
    # Left arm wrap lines
    for wrap_ay in [3, 7, 11, 15]:
        for wx in range(-3, 4):
            arm_wrap_x = center_x - 11 + wx
            arm_wrap_y = arm_y + wrap_ay
            if 0 <= arm_wrap_x < width and 0 <= arm_wrap_y < height and abs(wx) < 3:
                canvas[arm_wrap_y][arm_wrap_x] = WRAP_LINE_DARK
    
    # Right arm (hanging at side)
    for ay in range(18):
        arm_width = 3 - ay // 12
        for ax in range(-arm_width, arm_width + 1):
            arm_x = center_x + 11 + ax
            arm_ypos = arm_y + ay
            if 0 <= arm_x < width and 0 <= arm_ypos < height:
                if ax < -1:
                    canvas[arm_ypos][arm_x] = BANDAGE_LIGHT
                elif ax < 1:
                    canvas[arm_ypos][arm_x] = BANDAGE_TAN
                else:
                    canvas[arm_ypos][arm_x] = BANDAGE_DARK
    
    # Right arm wrap lines
    for wrap_ay in [3, 7, 11, 15]:
        for wx in range(-3, 4):
            arm_wrap_x = center_x + 11 + wx
            arm_wrap_y = arm_y + wrap_ay
            if 0 <= arm_wrap_x < width and 0 <= arm_wrap_y < height and abs(wx) < 3:
                canvas[arm_wrap_y][arm_wrap_x] = WRAP_LINE_DARK
    
    # === HANDS (wrapped, with finger definition) ===
    # Left hand
    left_hand_x = center_x - 11
    left_hand_y = arm_y + 18
    for hy in range(5):
        for hx in range(-3, 4):
            hand_x = left_hand_x + hx
            hand_y = left_hand_y + hy
            if 0 <= hand_x < width and 0 <= hand_y < height and abs(hx) + hy < 7:
                canvas[hand_y][hand_x] = BANDAGE_TAN if abs(hx) < 2 else BANDAGE_DARK
    
    # Left fingers (wrapped)
    for finger in range(3):
        for fy in range(3):
            finger_x = left_hand_x + (finger - 1) * 2
            finger_y = left_hand_y + 5 + fy
            if 0 <= finger_x < width and 0 <= finger_y < height:
                canvas[finger_y][finger_x] = BANDAGE_DIRTY if fy > 1 else BANDAGE_TAN
    
    # Right hand
    right_hand_x = center_x + 11
    right_hand_y = arm_y + 18
    for hy in range(5):
        for hx in range(-3, 4):
            hand_x = right_hand_x + hx
            hand_y = right_hand_y + hy
            if 0 <= hand_x < width and 0 <= hand_y < height and abs(hx) + hy < 7:
                canvas[hand_y][hand_x] = BANDAGE_LIGHT if abs(hx) < 2 else BANDAGE_DARK
    
    # Right fingers
    for finger in range(3):
        for fy in range(3):
            finger_x = right_hand_x + (finger - 1) * 2
            finger_y = right_hand_y + 5 + fy
            if 0 <= finger_x < width and 0 <= finger_y < height:
                canvas[finger_y][finger_x] = BANDAGE_TAN if fy < 2 else BANDAGE_DIRTY
    
    # === SHOULDERS (wrapped, broad) ===
    shoulder_y = torso_y - 18
    for sy in range(4):
        for sx in range(-12, 13):
            shoulder_x = center_x + sx
            shoulder_ypos = shoulder_y - sy
            if 0 <= shoulder_x < width and 0 <= shoulder_ypos < height:
                if abs(sx) > 10:
                    canvas[shoulder_ypos][shoulder_x] = BANDAGE_SHADOW
                elif abs(sx) > 6:
                    canvas[shoulder_ypos][shoulder_x] = BANDAGE_DARK
                elif abs(sx) < 3:
                    canvas[shoulder_ypos][shoulder_x] = BANDAGE_TAN
                else:
                    canvas[shoulder_ypos][shoulder_x] = BANDAGE_LIGHT
    
    # === NECK (wrapped) ===
    neck_y = shoulder_y - 4
    for ny in range(4):
        neck_width = 4 - ny // 2
        for nx in range(-neck_width, neck_width + 1):
            neck_x = center_x + nx
            neck_ypos = neck_y - ny
            if 0 <= neck_x < width and 0 <= neck_ypos < height:
                canvas[neck_ypos][neck_x] = BANDAGE_TAN if abs(nx) < 2 else BANDAGE_DARK
    
    # Neck wrap line
    neck_wrap_y = neck_y - 2
    for wx in range(-4, 5):
        wrap_x = center_x + wx
        if 0 <= wrap_x < width and 0 <= neck_wrap_y < height:
            canvas[neck_wrap_y][wrap_x] = WRAP_LINE_DARK
    
    # === HEAD (round, wrapped completely) ===
    head_y = neck_y - 6
    
    # Head shape
    for hy in range(12):
        head_width = 7 - abs(hy - 6) // 3
        for hx in range(-head_width, head_width + 1):
            if abs(hx) * 1.2 + abs(hy - 6) * 0.9 < 8:
                head_x = center_x + hx
                head_ypos = head_y - hy
                if 0 <= head_x < width and 0 <= head_ypos < height:
                    # Wrapped head with shading
                    if hx < -5:
                        canvas[head_ypos][head_x] = BANDAGE_SHADOW
                    elif hx < -2:
                        canvas[head_ypos][head_x] = BANDAGE_DARK
                    elif hx < 0:
                        canvas[head_ypos][head_x] = BANDAGE_DIRTY
                    elif hx < 2:
                        canvas[head_ypos][head_x] = BANDAGE_TAN
                    elif hx < 5:
                        canvas[head_ypos][head_x] = BANDAGE_LIGHT
                    else:
                        canvas[head_ypos][head_x] = BANDAGE_DARK
    
    # Horizontal wrap lines on head
    for wrap_hy in [-2, -5, -8]:
        wrap_y = head_y + wrap_hy
        for wx in range(-6, 7):
            wrap_x = center_x + wx
            if 0 <= wrap_x < width and 0 <= wrap_y < height and abs(wx) < 6:
                canvas[wrap_y][wrap_x] = WRAP_LINE_DARK
    
    # Vertical/diagonal wrap on head
    for vhy in range(-10, 2):
        v_y = head_y + vhy
        v_x = center_x - 3 + vhy // 3
        if 0 <= v_x < width and 0 <= v_y < height:
            canvas[v_y][v_x] = WRAP_LINE_LIGHT
    
    # === EYES (glowing yellow through bandages) ===
    eye_y = head_y - 4
    for eye_offset in [-3, 3]:
        # Eye socket shadow
        for ey in range(-2, 3):
            for ex in range(-2, 3):
                if abs(ex) + abs(ey) < 3:
                    eye_x = center_x + eye_offset + ex
                    eye_ypos = eye_y + ey
                    if 0 <= eye_x < width and 0 <= eye_ypos < height:
                        canvas[eye_ypos][eye_x] = EYE_DARK
        
        # Glowing yellow eye
        for ey in range(-2, 3):
            for ex in range(-1, 2):
                if abs(ex) + abs(ey) < 2:
                    eye_x = center_x + eye_offset + ex
                    eye_ypos = eye_y + ey
                    if 0 <= eye_x < width and 0 <= eye_ypos < height:
                        canvas[eye_ypos][eye_x] = EYE_YELLOW
        
        # Bright center
        bright_x = center_x + eye_offset
        bright_y = eye_y
        if 0 <= bright_x < width and 0 <= bright_y < height:
            canvas[bright_y][bright_x] = EYE_YELLOW
            # Glow effect around eye
            for gy in range(-1, 2):
                for gx in range(-1, 2):
                    if abs(gx) + abs(gy) == 1:
                        glow_x = bright_x + gx
                        glow_y = bright_y + gy
                        if 0 <= glow_x < width and 0 <= glow_y < height:
                            canvas[glow_y][glow_x] = EYE_ORANGE
    
    # === LOOSE BANDAGE STRIPS (dangling) ===
    # Left side loose strip
    for strip_y in range(8):
        strip_x = center_x - 8
        strip_ypos = torso_y - 6 + strip_y
        if 0 <= strip_x < width and 0 <= strip_ypos < height:
            canvas[strip_ypos][strip_x] = BANDAGE_DIRTY if strip_y % 2 == 0 else BANDAGE_DARK
    
    # Right side loose strip
    for strip_y in range(6):
        strip_x = center_x + 9
        strip_ypos = shoulder_y + 2 + strip_y
        if 0 <= strip_x < width and 0 <= strip_ypos < height:
            canvas[strip_ypos][strip_x] = BANDAGE_LIGHT if strip_y % 2 == 0 else BANDAGE_DARK
    
    return canvas


def create_mummy_attack():
    """Create the attacking mummy - lunging forward with arms reaching."""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Same color palette
    BANDAGE_TAN = [180, 165, 130, 255]
    BANDAGE_LIGHT = [200, 185, 150, 255]
    BANDAGE_DARK = [140, 125, 95, 255]
    BANDAGE_SHADOW = [110, 95, 70, 255]
    BANDAGE_DIRTY = [160, 145, 110, 255]
    EYE_YELLOW = [240, 220, 80, 255]
    EYE_ORANGE = [220, 180, 60, 255]
    EYE_DARK = [30, 25, 20, 255]
    WRAP_LINE_DARK = [100, 85, 60, 255]
    WRAP_LINE_LIGHT = [190, 175, 140, 255]
    MOTION_BLUR = [180, 165, 130, 120]
    
    center_x = 32
    base_y = 61
    
    # === LEGS (lunging stance) ===
    # Left leg (forward)
    for ly in range(18):
        leg_width = 4 - ly // 12
        leg_forward = ly // 4
        for lx in range(-leg_width, leg_width + 1):
            leg_x = center_x - 8 - leg_forward + lx
            leg_y = base_y - ly
            if 0 <= leg_x < width and 0 <= leg_y < height:
                if lx < -2:
                    canvas[leg_y][leg_x] = BANDAGE_SHADOW
                elif lx < 0:
                    canvas[leg_y][leg_x] = BANDAGE_DARK
                elif lx < 2:
                    canvas[leg_y][leg_x] = BANDAGE_TAN
                else:
                    canvas[leg_y][leg_x] = BANDAGE_LIGHT
    
    # Right leg (back)
    for ly in range(18):
        leg_width = 4 - ly // 12
        for lx in range(-leg_width, leg_width + 1):
            leg_x = center_x + 7 + lx
            leg_y = base_y - ly
            if 0 <= leg_x < width and 0 <= leg_y < height:
                if lx < -1:
                    canvas[leg_y][leg_x] = BANDAGE_DARK
                elif lx < 1:
                    canvas[leg_y][leg_x] = BANDAGE_TAN
                elif lx < 3:
                    canvas[leg_y][leg_x] = BANDAGE_LIGHT
                else:
                    canvas[leg_y][leg_x] = BANDAGE_DARK
    
    # Wrap lines on legs
    for wrap_y in [base_y - 4, base_y - 9, base_y - 14]:
        for wx in range(-14, 12):
            if abs(wx) < 12:
                wrap_x = center_x + wx
                if 0 <= wrap_x < width and 0 <= wrap_y < height:
                    canvas[wrap_y][wrap_x] = WRAP_LINE_DARK
    
    # Feet
    for foot_offset, foot_forward in [(-12, -4), (7, 0)]:
        for fy in range(3):
            for fx in range(-4, 5):
                foot_x = center_x + foot_offset + foot_forward + fx
                foot_y = base_y + fy
                if 0 <= foot_x < width and 0 <= foot_y < height:
                    if fy > 1:
                        canvas[foot_y][foot_x] = BANDAGE_SHADOW
                    elif abs(fx) < 2:
                        canvas[foot_y][foot_x] = BANDAGE_TAN
                    else:
                        canvas[foot_y][foot_x] = BANDAGE_DARK
    
    # === TORSO (leaning forward) ===
    torso_y = base_y - 18
    for ty in range(18):
        torso_width = 10 - ty // 10
        torso_lean = ty // 4
        for tx in range(-torso_width, torso_width + 1):
            torso_x = center_x + tx - torso_lean
            torso_ypos = torso_y - ty
            if 0 <= torso_x < width and 0 <= torso_ypos < height:
                if tx < -7:
                    canvas[torso_ypos][torso_x] = BANDAGE_SHADOW
                elif tx < -3:
                    canvas[torso_ypos][torso_x] = BANDAGE_DARK
                elif tx < -1:
                    canvas[torso_ypos][torso_x] = BANDAGE_DIRTY
                elif tx < 1:
                    canvas[torso_ypos][torso_x] = BANDAGE_TAN
                elif tx < 3:
                    canvas[torso_ypos][torso_x] = BANDAGE_LIGHT
                elif tx < 7:
                    canvas[torso_ypos][torso_x] = BANDAGE_TAN
                else:
                    canvas[torso_ypos][torso_x] = BANDAGE_DARK
    
    # Wrap lines on torso
    for wrap_y_offset in [2, 6, 10, 14]:
        wrap_y = torso_y - wrap_y_offset
        for wx in range(-10, 10):
            wrap_x = center_x + wx - wrap_y_offset // 3
            if 0 <= wrap_x < width and 0 <= wrap_y < height:
                if abs(wx) < 9:
                    canvas[wrap_y][wrap_x] = WRAP_LINE_DARK if wx % 2 == 0 else BANDAGE_SHADOW
    
    # === ARMS (REACHING FORWARD AGGRESSIVELY) ===
    arm_y = torso_y - 16
    
    # Left arm (extended forward)
    for ay in range(20):
        arm_width = 3 - ay // 14
        arm_forward = ay // 2
        for ax in range(-arm_width, arm_width + 1):
            arm_x = center_x - 14 - arm_forward + ax
            arm_ypos = arm_y + ay - 6
            if 0 <= arm_x < width and 0 <= arm_ypos < height:
                if ax < -1:
                    canvas[arm_ypos][arm_x] = BANDAGE_DARK
                elif ax < 1:
                    canvas[arm_ypos][arm_x] = BANDAGE_TAN
                else:
                    canvas[arm_ypos][arm_x] = BANDAGE_LIGHT
    
    # Left arm wrap lines
    for wrap_ay in [2, 6, 10, 14]:
        for wx in range(-3, 4):
            arm_wrap_x = center_x - 14 - wrap_ay // 2 + wx
            arm_wrap_y = arm_y + wrap_ay - 6
            if 0 <= arm_wrap_x < width and 0 <= arm_wrap_y < height and abs(wx) < 3:
                canvas[arm_wrap_y][arm_wrap_x] = WRAP_LINE_DARK
    
    # Right arm (extended forward)
    for ay in range(18):
        arm_width = 3 - ay // 14
        arm_forward = ay // 2
        for ax in range(-arm_width, arm_width + 1):
            arm_x = center_x - 7 - arm_forward + ax
            arm_ypos = arm_y + ay - 4
            if 0 <= arm_x < width and 0 <= arm_ypos < height:
                if ax < -1:
                    canvas[arm_ypos][arm_x] = BANDAGE_LIGHT
                elif ax < 1:
                    canvas[arm_ypos][arm_x] = BANDAGE_TAN
                else:
                    canvas[arm_ypos][arm_x] = BANDAGE_DARK
    
    # Right arm wrap lines
    for wrap_ay in [2, 6, 10, 14]:
        for wx in range(-3, 4):
            arm_wrap_x = center_x - 7 - wrap_ay // 2 + wx
            arm_wrap_y = arm_y + wrap_ay - 4
            if 0 <= arm_wrap_x < width and 0 <= arm_wrap_y < height and abs(wx) < 3:
                canvas[arm_wrap_y][arm_wrap_x] = WRAP_LINE_DARK
    
    # === HANDS (REACHING/GRASPING) ===
    # Left hand
    left_hand_x = center_x - 24
    left_hand_y = arm_y + 8
    for hy in range(6):
        for hx in range(-3, 4):
            hand_x = left_hand_x + hx
            hand_y = left_hand_y + hy
            if 0 <= hand_x < width and 0 <= hand_y < height and abs(hx) + hy < 8:
                canvas[hand_y][hand_x] = BANDAGE_TAN if abs(hx) < 2 else BANDAGE_DARK
    
    # Left fingers (spread/grasping)
    for finger in range(4):
        finger_angle = (finger - 1.5) * 0.5
        for fy in range(4):
            finger_x = left_hand_x + (finger - 1.5) * 2 + int(fy * finger_angle)
            finger_y = left_hand_y + 6 + fy
            if 0 <= finger_x < width and 0 <= finger_y < height:
                canvas[int(finger_y)][int(finger_x)] = BANDAGE_DIRTY if fy > 2 else BANDAGE_TAN
    
    # Right hand
    right_hand_x = center_x - 16
    right_hand_y = arm_y + 10
    for hy in range(6):
        for hx in range(-3, 4):
            hand_x = right_hand_x + hx
            hand_y = right_hand_y + hy
            if 0 <= hand_x < width and 0 <= hand_y < height and abs(hx) + hy < 8:
                canvas[hand_y][hand_x] = BANDAGE_LIGHT if abs(hx) < 2 else BANDAGE_DARK
    
    # Right fingers (spread)
    for finger in range(4):
        finger_angle = (finger - 1.5) * 0.4
        for fy in range(3):
            finger_x = right_hand_x + (finger - 1.5) * 2 + int(fy * finger_angle)
            finger_y = right_hand_y + 6 + fy
            if 0 <= finger_x < width and 0 <= finger_y < height:
                canvas[int(finger_y)][int(finger_x)] = BANDAGE_TAN if fy < 2 else BANDAGE_DIRTY
    
    # === SHOULDERS ===
    shoulder_y = torso_y - 18
    for sy in range(4):
        for sx in range(-12, 13):
            shoulder_x = center_x + sx - 2
            shoulder_ypos = shoulder_y - sy
            if 0 <= shoulder_x < width and 0 <= shoulder_ypos < height:
                if abs(sx) > 10:
                    canvas[shoulder_ypos][shoulder_x] = BANDAGE_SHADOW
                elif abs(sx) > 6:
                    canvas[shoulder_ypos][shoulder_x] = BANDAGE_DARK
                elif abs(sx) < 3:
                    canvas[shoulder_ypos][shoulder_x] = BANDAGE_TAN
                else:
                    canvas[shoulder_ypos][shoulder_x] = BANDAGE_LIGHT
    
    # === NECK ===
    neck_y = shoulder_y - 4
    for ny in range(4):
        neck_width = 4 - ny // 2
        for nx in range(-neck_width, neck_width + 1):
            neck_x = center_x + nx - 2
            neck_ypos = neck_y - ny
            if 0 <= neck_x < width and 0 <= neck_ypos < height:
                canvas[neck_ypos][neck_x] = BANDAGE_TAN if abs(nx) < 2 else BANDAGE_DARK
    
    # Neck wrap
    neck_wrap_y = neck_y - 2
    for wx in range(-4, 5):
        wrap_x = center_x + wx - 2
        if 0 <= wrap_x < width and 0 <= neck_wrap_y < height:
            canvas[neck_wrap_y][wrap_x] = WRAP_LINE_DARK
    
    # === HEAD (tilted forward aggressively) ===
    head_y = neck_y - 6
    
    # Head shape
    for hy in range(12):
        head_width = 7 - abs(hy - 6) // 3
        for hx in range(-head_width, head_width + 1):
            if abs(hx) * 1.2 + abs(hy - 6) * 0.9 < 8:
                head_x = center_x + hx - 2
                head_ypos = head_y - hy
                if 0 <= head_x < width and 0 <= head_ypos < height:
                    if hx < -5:
                        canvas[head_ypos][head_x] = BANDAGE_SHADOW
                    elif hx < -2:
                        canvas[head_ypos][head_x] = BANDAGE_DARK
                    elif hx < 0:
                        canvas[head_ypos][head_x] = BANDAGE_DIRTY
                    elif hx < 2:
                        canvas[head_ypos][head_x] = BANDAGE_TAN
                    elif hx < 5:
                        canvas[head_ypos][head_x] = BANDAGE_LIGHT
                    else:
                        canvas[head_ypos][head_x] = BANDAGE_DARK
    
    # Wrap lines on head
    for wrap_hy in [-2, -5, -8]:
        wrap_y = head_y + wrap_hy
        for wx in range(-6, 7):
            wrap_x = center_x + wx - 2
            if 0 <= wrap_x < width and 0 <= wrap_y < height and abs(wx) < 6:
                canvas[wrap_y][wrap_x] = WRAP_LINE_DARK
    
    # Vertical wrap
    for vhy in range(-10, 2):
        v_y = head_y + vhy
        v_x = center_x - 3 + vhy // 3 - 2
        if 0 <= v_x < width and 0 <= v_y < height:
            canvas[v_y][v_x] = WRAP_LINE_LIGHT
    
    # === EYES (GLOWING BRIGHTER - aggressive) ===
    eye_y = head_y - 4
    for eye_offset in [-3, 3]:
        # Eye socket
        for ey in range(-2, 3):
            for ex in range(-2, 3):
                if abs(ex) + abs(ey) < 3:
                    eye_x = center_x + eye_offset + ex - 2
                    eye_ypos = eye_y + ey
                    if 0 <= eye_x < width and 0 <= eye_ypos < height:
                        canvas[eye_ypos][eye_x] = EYE_DARK
        
        # Glowing eye (larger for aggression)
        for ey in range(-2, 3):
            for ex in range(-2, 3):
                if abs(ex) + abs(ey) < 3:
                    eye_x = center_x + eye_offset + ex - 2
                    eye_ypos = eye_y + ey
                    if 0 <= eye_x < width and 0 <= eye_ypos < height:
                        canvas[eye_ypos][eye_x] = EYE_YELLOW
        
        # Bright center
        bright_x = center_x + eye_offset - 2
        bright_y = eye_y
        if 0 <= bright_x < width and 0 <= bright_y < height:
            canvas[bright_y][bright_x] = EYE_YELLOW
            # Enhanced glow
            for gy in range(-2, 3):
                for gx in range(-2, 3):
                    if abs(gx) + abs(gy) < 3 and not (gx == 0 and gy == 0):
                        glow_x = bright_x + gx
                        glow_y = bright_y + gy
                        if 0 <= glow_x < width and 0 <= glow_y < height:
                            canvas[glow_y][glow_x] = EYE_ORANGE
    
    # === LOOSE BANDAGES (MORE AGGRESSIVE) ===
    # Multiple loose strips flying
    for strip_y in range(10):
        strip_x = center_x - 9 - strip_y // 3
        strip_ypos = torso_y - 4 + strip_y
        if 0 <= strip_x < width and 0 <= strip_ypos < height:
            canvas[strip_ypos][strip_x] = BANDAGE_DIRTY if strip_y % 2 == 0 else BANDAGE_DARK
    
    for strip_y in range(8):
        strip_x = center_x + 10
        strip_ypos = shoulder_y + strip_y
        if 0 <= strip_x < width and 0 <= strip_ypos < height:
            canvas[strip_ypos][strip_x] = BANDAGE_LIGHT if strip_y % 2 == 0 else BANDAGE_DARK
    
    # === MOTION BLUR ON ARMS ===
    for blur in range(6):
        for by in range(2):
            blur_x = left_hand_x + 8 + blur
            blur_y = left_hand_y + by
            if 0 <= blur_x < width and 0 <= blur_y < height:
                canvas[blur_y][blur_x] = MOTION_BLUR
    
    return canvas


def main():
    print("Creating mummy monster images...")
    
    mummy_default = create_mummy_default()
    mummy_attack = create_mummy_attack()
    
    # Convert to PIL and scale up
    scale = 4
    
    # Default pose
    img_default = Image.fromarray(mummy_default, 'RGBA')
    img_default_scaled = img_default.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_default_scaled.save('art/mummy_monster.png')
    print(f"✓ Saved: art/mummy_monster.png ({64 * scale}x{64 * scale})")
    
    # Attack animation
    img_attack = Image.fromarray(mummy_attack, 'RGBA')
    img_attack_scaled = img_attack.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_attack_scaled.save('art/mummy_monster_attack.png')
    print(f"✓ Saved: art/mummy_monster_attack.png ({64 * scale}x{64 * scale})")
    
    print("\n✅ Mummy monster creation complete!")
    print("\nFeatures:")
    print("- Default: Shambling stance with complete bandage wrapping, glowing yellow eyes")
    print("- Attack: Lunging forward with arms reaching, brighter eye glow, loose bandages")
    print("\nStyle: Ancient Egyptian mummy with detailed wrap patterns")
    print("Colors: Tan/beige bandages with shadows, glowing yellow eyes, aged/dirty wrappings")


if __name__ == '__main__':
    main()
