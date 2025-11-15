"""
Zombie Monster Creator
Creates pixel art for a horrifying zombie - decaying flesh, hunched posture, tattered clothes.
Inspired by classic undead creatures with rotting skin and shambling movement.

Resolution: 64x64 pixels (scaled 4x to 256x256)
Style: Pixel art with detailed decay and horror elements
Palette: Gray/purple rotting flesh, tattered blue jeans, dark shadows
"""

from PIL import Image
import numpy as np


def create_zombie_default():
    """Create the default shambling zombie pose."""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette - inspired by the zombie image
    FLESH_GRAY = [140, 130, 140, 255]       # Gray rotting flesh
    FLESH_PURPLE = [130, 110, 130, 255]     # Purple decay
    FLESH_DARK = [100, 90, 100, 255]        # Dark rotting areas
    FLESH_LIGHT = [160, 150, 155, 255]      # Lighter flesh
    DECAY_GREEN = [120, 130, 100, 255]      # Greenish decay
    DECAY_BROWN = [100, 80, 70, 255]        # Brown decay patches
    BONE_WHITE = [200, 195, 190, 255]       # Exposed bone
    BONE_YELLOW = [180, 175, 150, 255]      # Yellowed bone
    JEANS_BLUE = [80, 100, 140, 255]        # Tattered jeans
    JEANS_DARK = [60, 75, 105, 255]         # Dark jean areas
    JEANS_LIGHT = [100, 120, 160, 255]      # Light jean areas
    EYE_YELLOW = [200, 190, 100, 255]       # Yellowed eyes
    EYE_DARK = [40, 35, 30, 255]            # Dark eye socket
    TEETH_YELLOW = [190, 180, 140, 255]     # Yellowed teeth
    TEETH_WHITE = [210, 205, 195, 255]      # White teeth
    BLOOD_RED = [120, 40, 40, 255]          # Dark blood stains
    BLOOD_DARK = [80, 30, 30, 255]          # Dried blood
    SHADOW_BLACK = [30, 25, 30, 255]        # Deep shadows
    
    center_x = 32
    base_y = 61
    
    # === LEGS (hunched stance, wearing tattered jeans) ===
    # Left leg
    for ly in range(20):
        leg_width = 4 - ly // 12
        for lx in range(-leg_width, leg_width + 1):
            leg_x = center_x - 6 + lx
            leg_y = base_y - ly
            if 0 <= leg_x < width and 0 <= leg_y < height:
                # Jeans with tears
                if ly > 15 and lx == 0:
                    canvas[leg_y][leg_x] = FLESH_DARK  # Tear showing flesh
                elif lx < 0:
                    canvas[leg_y][leg_x] = JEANS_DARK
                else:
                    canvas[leg_y][leg_x] = JEANS_BLUE
    
    # Right leg
    for ly in range(18):
        leg_width = 4 - ly // 12
        for lx in range(-leg_width, leg_width + 1):
            leg_x = center_x + 6 + lx
            leg_y = base_y - ly
            if 0 <= leg_x < width and 0 <= leg_y < height:
                # Jeans with tears
                if ly > 12 and abs(lx) == 1:
                    canvas[leg_y][leg_x] = FLESH_GRAY  # Tear showing flesh
                elif lx < 0:
                    canvas[leg_y][leg_x] = JEANS_BLUE
                else:
                    canvas[leg_y][leg_x] = JEANS_LIGHT
    
    # Feet (bare, decayed)
    for foot_offset in [-6, 6]:
        for fy in range(3):
            for fx in range(-4, 5):
                foot_x = center_x + foot_offset + fx
                foot_y = base_y + fy
                if 0 <= foot_x < width and 0 <= foot_y < height:
                    if fy > 1:
                        canvas[foot_y][foot_x] = FLESH_DARK
                    elif abs(fx) < 2:
                        canvas[foot_y][foot_x] = FLESH_GRAY
                    else:
                        canvas[foot_y][foot_x] = DECAY_BROWN
    
    # Toes with decay
    for foot_offset in [-6, 6]:
        for toe in range(3):
            toe_x = center_x + foot_offset + (toe - 1) * 2
            toe_y = base_y + 3
            if 0 <= toe_x < width and 0 <= toe_y < height:
                canvas[toe_y][toe_x] = FLESH_DARK
    
    # === TORSO (muscular but decayed, bare chest) ===
    torso_y = base_y - 20
    for ty in range(16):
        torso_width = 10 - ty // 8
        for tx in range(-torso_width, torso_width + 1):
            torso_x = center_x + tx
            torso_ypos = torso_y - ty
            if 0 <= torso_x < width and 0 <= torso_ypos < height:
                # Chest muscles with decay patches
                if ty > 8 and abs(tx) < 4 and (ty + tx) % 5 == 0:
                    canvas[torso_ypos][torso_x] = DECAY_GREEN  # Decay patches
                elif ty > 6 and abs(tx) < 3 and ty % 3 == 0:
                    canvas[torso_ypos][torso_x] = FLESH_PURPLE  # Purple rot
                elif ty > 10 and tx == 0:
                    canvas[torso_ypos][torso_x] = FLESH_DARK  # Center line (abs)
                elif tx < -6:
                    canvas[torso_ypos][torso_x] = FLESH_DARK  # Shadow
                elif tx < -2:
                    canvas[torso_ypos][torso_x] = FLESH_GRAY
                elif tx < 2:
                    canvas[torso_ypos][torso_x] = FLESH_LIGHT
                elif tx < 6:
                    canvas[torso_ypos][torso_x] = FLESH_GRAY
                else:
                    canvas[torso_ypos][torso_x] = FLESH_PURPLE
    
    # Ribs (exposed/showing through)
    rib_y = torso_y - 8
    for rib in range(4):
        for rx in range(-6, 7):
            rib_x = center_x + rx
            rib_ypos = rib_y - rib * 2
            if 0 <= rib_x < width and 0 <= rib_ypos < height and abs(rx) > 1:
                if rx % 2 == 0:
                    canvas[rib_ypos][rib_x] = BONE_YELLOW
    
    # Blood stains on torso
    for blood_spot in [(0, -10), (-3, -12), (4, -8)]:
        for by in range(3):
            for bx in range(-2, 3):
                if abs(bx) + abs(by) < 3:
                    blood_x = center_x + blood_spot[0] + bx
                    blood_y = torso_y + blood_spot[1] + by
                    if 0 <= blood_x < width and 0 <= blood_y < height:
                        canvas[blood_y][blood_x] = BLOOD_RED if by < 2 else BLOOD_DARK
    
    # === ARMS (long, reaching, decayed) ===
    arm_y = torso_y - 14
    
    # Left arm (hanging forward)
    for ay in range(18):
        arm_width = 3 - ay // 10
        arm_forward = ay // 3
        for ax in range(-arm_width, arm_width + 1):
            arm_x = center_x - 10 - arm_forward + ax
            arm_ypos = arm_y + ay
            if 0 <= arm_x < width and 0 <= arm_ypos < height:
                # Decay on arm
                if ay > 8 and ax == 0:
                    canvas[arm_ypos][arm_x] = DECAY_BROWN
                elif ax < 0:
                    canvas[arm_ypos][arm_x] = FLESH_GRAY
                else:
                    canvas[arm_ypos][arm_x] = FLESH_LIGHT
    
    # Right arm (hanging to side)
    for ay in range(16):
        arm_width = 3 - ay // 10
        for ax in range(-arm_width, arm_width + 1):
            arm_x = center_x + 10 + ax
            arm_ypos = arm_y + ay
            if 0 <= arm_x < width and 0 <= arm_ypos < height:
                # More decay on right arm
                if ay > 10 and abs(ax) == 1:
                    canvas[arm_ypos][arm_x] = DECAY_GREEN
                elif ax < 0:
                    canvas[arm_ypos][arm_x] = FLESH_PURPLE
                else:
                    canvas[arm_ypos][arm_x] = FLESH_GRAY
    
    # === HANDS (reaching, clawed) ===
    # Left hand
    left_hand_x = center_x - 16
    left_hand_y = arm_y + 18
    for hy in range(5):
        for hx in range(-3, 4):
            hand_x = left_hand_x + hx
            hand_y = left_hand_y + hy
            if 0 <= hand_x < width and 0 <= hand_y < height and abs(hx) + hy < 6:
                canvas[hand_y][hand_x] = FLESH_DARK if hy > 3 else FLESH_GRAY
    
    # Left fingers (clawed)
    for finger in range(4):
        for fy in range(4):
            finger_x = left_hand_x + (finger - 1.5) * 2
            finger_y = left_hand_y + 5 + fy
            if 0 <= finger_x < width and 0 <= finger_y < height:
                canvas[int(finger_y)][int(finger_x)] = FLESH_DARK if fy > 2 else DECAY_BROWN
    
    # Right hand
    right_hand_x = center_x + 10
    right_hand_y = arm_y + 16
    for hy in range(5):
        for hx in range(-3, 4):
            hand_x = right_hand_x + hx
            hand_y = right_hand_y + hy
            if 0 <= hand_x < width and 0 <= hand_y < height and abs(hx) + hy < 6:
                canvas[hand_y][hand_x] = FLESH_PURPLE if hy > 3 else FLESH_GRAY
    
    # Right fingers
    for finger in range(4):
        for fy in range(3):
            finger_x = right_hand_x + (finger - 1.5) * 2
            finger_y = right_hand_y + 5 + fy
            if 0 <= finger_x < width and 0 <= finger_y < height:
                canvas[int(finger_y)][int(finger_x)] = DECAY_BROWN
    
    # === SHOULDERS (broad, muscular but rotting) ===
    shoulder_y = torso_y - 16
    for sy in range(4):
        for sx in range(-12, 13):
            shoulder_x = center_x + sx
            shoulder_ypos = shoulder_y - sy
            if 0 <= shoulder_x < width and 0 <= shoulder_ypos < height:
                if abs(sx) > 10:
                    canvas[shoulder_ypos][shoulder_x] = FLESH_DARK
                elif abs(sx) > 6:
                    canvas[shoulder_ypos][shoulder_x] = FLESH_GRAY
                else:
                    canvas[shoulder_ypos][shoulder_x] = FLESH_LIGHT
    
    # === NECK (thick, decayed) ===
    neck_y = shoulder_y - 4
    for ny in range(4):
        neck_width = 4 - ny // 2
        for nx in range(-neck_width, neck_width + 1):
            neck_x = center_x + nx
            neck_ypos = neck_y - ny
            if 0 <= neck_x < width and 0 <= neck_ypos < height:
                canvas[neck_ypos][neck_x] = FLESH_GRAY if abs(nx) < 2 else FLESH_PURPLE
    
    # === HEAD (bald, skull-like, horrifying) ===
    head_y = neck_y - 6
    
    # Skull shape
    for hy in range(12):
        head_width = 7 - hy // 4
        for hx in range(-head_width, head_width + 1):
            if abs(hx) * 1.2 + abs(hy - 6) * 0.8 < 8:
                head_x = center_x + hx
                head_ypos = head_y - hy
                if 0 <= head_x < width and 0 <= head_ypos < height:
                    # Skull texture with decay
                    if hy < 4 and abs(hx) < 2:
                        canvas[head_ypos][head_x] = FLESH_LIGHT  # Forehead
                    elif hy > 8:
                        canvas[head_ypos][head_x] = FLESH_GRAY  # Jaw
                    elif hx < -4:
                        canvas[head_ypos][head_x] = FLESH_DARK  # Shadow
                    elif hx < 0:
                        canvas[head_ypos][head_x] = FLESH_GRAY
                    elif hx < 4:
                        canvas[head_ypos][head_x] = FLESH_LIGHT
                    else:
                        canvas[head_ypos][head_x] = FLESH_PURPLE
    
    # Decay patches on head
    for decay_spot in [(-3, -8), (4, -6), (0, -2)]:
        for dy in range(2):
            for dx in range(-2, 2):
                decay_x = center_x + decay_spot[0] + dx
                decay_y = head_y + decay_spot[1] + dy
                if 0 <= decay_x < width and 0 <= decay_y < height:
                    canvas[decay_y][decay_x] = DECAY_GREEN if (dx + dy) % 2 == 0 else DECAY_BROWN
    
    # === EYES (sunken, yellowish) ===
    eye_y = head_y - 4
    for eye_offset in [-3, 3]:
        # Eye socket (dark, sunken)
        for ey in range(-2, 3):
            for ex in range(-2, 3):
                if abs(ex) + abs(ey) < 3:
                    eye_x = center_x + eye_offset + ex
                    eye_ypos = eye_y + ey
                    if 0 <= eye_x < width and 0 <= eye_ypos < height:
                        canvas[eye_ypos][eye_x] = EYE_DARK
        
        # Eye (small, yellow glow)
        for ey in range(-1, 2):
            eye_x = center_x + eye_offset
            eye_ypos = eye_y + ey
            if 0 <= eye_x < width and 0 <= eye_ypos < height:
                canvas[eye_ypos][eye_x] = EYE_YELLOW
    
    # === NOSE (decayed, showing bone) ===
    nose_y = head_y
    for ny in range(2):
        for nx in range(-1, 2):
            nose_x = center_x + nx
            nose_ypos = nose_y + ny
            if 0 <= nose_x < width and 0 <= nose_ypos < height:
                if abs(nx) == 1:
                    canvas[nose_ypos][nose_x] = SHADOW_BLACK  # Nostril holes
                else:
                    canvas[nose_ypos][nose_x] = BONE_WHITE  # Bone showing
    
    # === MOUTH (open, showing teeth, horror) ===
    mouth_y = head_y + 3
    for my in range(5):
        mouth_width = 4 - my // 2
        for mx in range(-mouth_width, mouth_width + 1):
            mouth_x = center_x + mx
            mouth_ypos = mouth_y + my
            if 0 <= mouth_x < width and 0 <= mouth_ypos < height:
                if my < 2:
                    # Upper jaw with teeth
                    if abs(mx) % 2 == 1 and abs(mx) < 4:
                        canvas[mouth_ypos][mouth_x] = TEETH_WHITE
                    else:
                        canvas[mouth_ypos][mouth_x] = SHADOW_BLACK
                elif my == 2:
                    # Mouth opening
                    canvas[mouth_ypos][mouth_x] = SHADOW_BLACK
                else:
                    # Lower jaw with teeth
                    if abs(mx) % 2 == 0 and abs(mx) < 4:
                        canvas[mouth_ypos][mouth_x] = TEETH_YELLOW
                    else:
                        canvas[mouth_ypos][mouth_x] = FLESH_DARK
    
    # Exposed teeth (prominent)
    for tooth_x in [-3, -1, 1, 3]:
        tooth_pos = center_x + tooth_x
        tooth_y = mouth_y + 1
        if 0 <= tooth_pos < width and 0 <= tooth_y < height:
            canvas[tooth_y][tooth_pos] = TEETH_WHITE
    
    # Blood around mouth
    for by in range(2):
        for bx in range(-4, 5):
            if abs(bx) > 2:
                blood_x = center_x + bx
                blood_y = mouth_y + 5 + by
                if 0 <= blood_x < width and 0 <= blood_y < height:
                    canvas[blood_y][blood_x] = BLOOD_DARK
    
    return canvas


def create_zombie_attack():
    """Create the attacking zombie - lunging with arms reaching forward."""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Same color palette
    FLESH_GRAY = [140, 130, 140, 255]
    FLESH_PURPLE = [130, 110, 130, 255]
    FLESH_DARK = [100, 90, 100, 255]
    FLESH_LIGHT = [160, 150, 155, 255]
    DECAY_GREEN = [120, 130, 100, 255]
    DECAY_BROWN = [100, 80, 70, 255]
    BONE_WHITE = [200, 195, 190, 255]
    BONE_YELLOW = [180, 175, 150, 255]
    JEANS_BLUE = [80, 100, 140, 255]
    JEANS_DARK = [60, 75, 105, 255]
    JEANS_LIGHT = [100, 120, 160, 255]
    EYE_YELLOW = [200, 190, 100, 255]
    EYE_DARK = [40, 35, 30, 255]
    TEETH_YELLOW = [190, 180, 140, 255]
    TEETH_WHITE = [210, 205, 195, 255]
    BLOOD_RED = [120, 40, 40, 255]
    BLOOD_DARK = [80, 30, 30, 255]
    SHADOW_BLACK = [30, 25, 30, 255]
    MOTION_BLUR = [140, 130, 140, 150]
    
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
                if ly > 14 and lx == 0:
                    canvas[leg_y][leg_x] = FLESH_DARK
                elif lx < 0:
                    canvas[leg_y][leg_x] = JEANS_DARK
                else:
                    canvas[leg_y][leg_x] = JEANS_BLUE
    
    # Right leg (back)
    for ly in range(16):
        leg_width = 4 - ly // 12
        for lx in range(-leg_width, leg_width + 1):
            leg_x = center_x + 7 + lx
            leg_y = base_y - ly
            if 0 <= leg_x < width and 0 <= leg_y < height:
                if ly > 10 and abs(lx) == 1:
                    canvas[leg_y][leg_x] = FLESH_GRAY
                elif lx < 0:
                    canvas[leg_y][leg_x] = JEANS_BLUE
                else:
                    canvas[leg_y][leg_x] = JEANS_LIGHT
    
    # Feet
    for foot_offset, foot_forward in [(-12, -4), (7, 0)]:
        for fy in range(3):
            for fx in range(-4, 5):
                foot_x = center_x + foot_offset + foot_forward + fx
                foot_y = base_y + fy
                if 0 <= foot_x < width and 0 <= foot_y < height:
                    if fy > 1:
                        canvas[foot_y][foot_x] = FLESH_DARK
                    elif abs(fx) < 2:
                        canvas[foot_y][foot_x] = FLESH_GRAY
                    else:
                        canvas[foot_y][foot_x] = DECAY_BROWN
    
    # === TORSO (leaning forward aggressively) ===
    torso_y = base_y - 18
    for ty in range(16):
        torso_width = 10 - ty // 8
        torso_lean = ty // 4
        for tx in range(-torso_width, torso_width + 1):
            torso_x = center_x + tx - torso_lean
            torso_ypos = torso_y - ty
            if 0 <= torso_x < width and 0 <= torso_ypos < height:
                if ty > 8 and abs(tx) < 4 and (ty + tx) % 5 == 0:
                    canvas[torso_ypos][torso_x] = DECAY_GREEN
                elif ty > 6 and abs(tx) < 3 and ty % 3 == 0:
                    canvas[torso_ypos][torso_x] = FLESH_PURPLE
                elif ty > 10 and tx == 0:
                    canvas[torso_ypos][torso_x] = FLESH_DARK
                elif tx < -6:
                    canvas[torso_ypos][torso_x] = FLESH_DARK
                elif tx < -2:
                    canvas[torso_ypos][torso_x] = FLESH_GRAY
                elif tx < 2:
                    canvas[torso_ypos][torso_x] = FLESH_LIGHT
                elif tx < 6:
                    canvas[torso_ypos][torso_x] = FLESH_GRAY
                else:
                    canvas[torso_ypos][torso_x] = FLESH_PURPLE
    
    # Ribs showing
    rib_y = torso_y - 8
    for rib in range(4):
        for rx in range(-6, 7):
            rib_x = center_x + rx - 2
            rib_ypos = rib_y - rib * 2
            if 0 <= rib_x < width and 0 <= rib_ypos < height and abs(rx) > 1:
                if rx % 2 == 0:
                    canvas[rib_ypos][rib_x] = BONE_YELLOW
    
    # Blood stains
    for blood_spot in [(0, -10), (-3, -12), (4, -8)]:
        for by in range(3):
            for bx in range(-2, 3):
                if abs(bx) + abs(by) < 3:
                    blood_x = center_x + blood_spot[0] + bx - 2
                    blood_y = torso_y + blood_spot[1] + by
                    if 0 <= blood_x < width and 0 <= blood_y < height:
                        canvas[blood_y][blood_x] = BLOOD_RED if by < 2 else BLOOD_DARK
    
    # === ARMS (REACHING FORWARD - attacking pose) ===
    arm_y = torso_y - 14
    
    # Left arm (extended forward aggressively)
    for ay in range(20):
        arm_width = 3 - ay // 12
        arm_forward = ay // 2
        for ax in range(-arm_width, arm_width + 1):
            arm_x = center_x - 12 - arm_forward + ax
            arm_ypos = arm_y + ay - 5
            if 0 <= arm_x < width and 0 <= arm_ypos < height:
                if ay > 10 and ax == 0:
                    canvas[arm_ypos][arm_x] = DECAY_BROWN
                elif ax < 0:
                    canvas[arm_ypos][arm_x] = FLESH_GRAY
                else:
                    canvas[arm_ypos][arm_x] = FLESH_LIGHT
    
    # Right arm (extended forward)
    for ay in range(18):
        arm_width = 3 - ay // 12
        arm_forward = ay // 2
        for ax in range(-arm_width, arm_width + 1):
            arm_x = center_x - 6 - arm_forward + ax
            arm_ypos = arm_y + ay - 3
            if 0 <= arm_x < width and 0 <= arm_ypos < height:
                if ay > 12 and abs(ax) == 1:
                    canvas[arm_ypos][arm_x] = DECAY_GREEN
                elif ax < 0:
                    canvas[arm_ypos][arm_x] = FLESH_PURPLE
                else:
                    canvas[arm_ypos][arm_x] = FLESH_GRAY
    
    # === HANDS (CLAWING, reaching for victim) ===
    # Left hand
    left_hand_x = center_x - 22
    left_hand_y = arm_y + 10
    for hy in range(6):
        for hx in range(-3, 4):
            hand_x = left_hand_x + hx
            hand_y = left_hand_y + hy
            if 0 <= hand_x < width and 0 <= hand_y < height and abs(hx) + hy < 7:
                canvas[hand_y][hand_x] = FLESH_DARK if hy > 4 else FLESH_GRAY
    
    # Left fingers (clawed, spread)
    for finger in range(5):
        finger_angle = (finger - 2) * 0.5
        for fy in range(5):
            finger_x = left_hand_x + (finger - 2) * 2 + int(fy * finger_angle)
            finger_y = left_hand_y + 6 + fy
            if 0 <= finger_x < width and 0 <= finger_y < height:
                canvas[finger_y][finger_x] = FLESH_DARK if fy > 3 else DECAY_BROWN
    
    # Right hand
    right_hand_x = center_x - 15
    right_hand_y = arm_y + 12
    for hy in range(6):
        for hx in range(-3, 4):
            hand_x = right_hand_x + hx
            hand_y = right_hand_y + hy
            if 0 <= hand_x < width and 0 <= hand_y < height and abs(hx) + hy < 7:
                canvas[hand_y][hand_x] = FLESH_PURPLE if hy > 4 else FLESH_GRAY
    
    # Right fingers (clawed)
    for finger in range(5):
        finger_angle = (finger - 2) * 0.4
        for fy in range(4):
            finger_x = right_hand_x + (finger - 2) * 2 + int(fy * finger_angle)
            finger_y = right_hand_y + 6 + fy
            if 0 <= finger_x < width and 0 <= finger_y < height:
                canvas[finger_y][finger_x] = DECAY_BROWN
    
    # === SHOULDERS ===
    shoulder_y = torso_y - 16
    for sy in range(4):
        for sx in range(-12, 13):
            shoulder_x = center_x + sx - 2
            shoulder_ypos = shoulder_y - sy
            if 0 <= shoulder_x < width and 0 <= shoulder_ypos < height:
                if abs(sx) > 10:
                    canvas[shoulder_ypos][shoulder_x] = FLESH_DARK
                elif abs(sx) > 6:
                    canvas[shoulder_ypos][shoulder_x] = FLESH_GRAY
                else:
                    canvas[shoulder_ypos][shoulder_x] = FLESH_LIGHT
    
    # === NECK ===
    neck_y = shoulder_y - 4
    for ny in range(4):
        neck_width = 4 - ny // 2
        for nx in range(-neck_width, neck_width + 1):
            neck_x = center_x + nx - 2
            neck_ypos = neck_y - ny
            if 0 <= neck_x < width and 0 <= neck_ypos < height:
                canvas[neck_ypos][neck_x] = FLESH_GRAY if abs(nx) < 2 else FLESH_PURPLE
    
    # === HEAD (AGGRESSIVE, forward) ===
    head_y = neck_y - 6
    
    # Skull
    for hy in range(12):
        head_width = 7 - hy // 4
        for hx in range(-head_width, head_width + 1):
            if abs(hx) * 1.2 + abs(hy - 6) * 0.8 < 8:
                head_x = center_x + hx - 2
                head_ypos = head_y - hy
                if 0 <= head_x < width and 0 <= head_ypos < height:
                    if hy < 4 and abs(hx) < 2:
                        canvas[head_ypos][head_x] = FLESH_LIGHT
                    elif hy > 8:
                        canvas[head_ypos][head_x] = FLESH_GRAY
                    elif hx < -4:
                        canvas[head_ypos][head_x] = FLESH_DARK
                    elif hx < 0:
                        canvas[head_ypos][head_x] = FLESH_GRAY
                    elif hx < 4:
                        canvas[head_ypos][head_x] = FLESH_LIGHT
                    else:
                        canvas[head_ypos][head_x] = FLESH_PURPLE
    
    # Decay patches
    for decay_spot in [(-3, -8), (4, -6), (0, -2)]:
        for dy in range(2):
            for dx in range(-2, 2):
                decay_x = center_x + decay_spot[0] + dx - 2
                decay_y = head_y + decay_spot[1] + dy
                if 0 <= decay_x < width and 0 <= decay_y < height:
                    canvas[decay_y][decay_x] = DECAY_GREEN if (dx + dy) % 2 == 0 else DECAY_BROWN
    
    # === EYES (WIDE, HUNGRY) ===
    eye_y = head_y - 4
    for eye_offset in [-3, 3]:
        # Eye socket
        for ey in range(-3, 4):
            for ex in range(-2, 3):
                if abs(ex) + abs(ey) < 4:
                    eye_x = center_x + eye_offset + ex - 2
                    eye_ypos = eye_y + ey
                    if 0 <= eye_x < width and 0 <= eye_ypos < height:
                        canvas[eye_ypos][eye_x] = EYE_DARK
        
        # Eye (glowing yellow)
        for ey in range(-2, 3):
            for ex in range(-1, 2):
                if abs(ex) + abs(ey) < 3:
                    eye_x = center_x + eye_offset + ex - 2
                    eye_ypos = eye_y + ey
                    if 0 <= eye_x < width and 0 <= eye_ypos < height:
                        canvas[eye_ypos][eye_x] = EYE_YELLOW
    
    # === NOSE (decayed) ===
    nose_y = head_y
    for ny in range(2):
        for nx in range(-1, 2):
            nose_x = center_x + nx - 2
            nose_ypos = nose_y + ny
            if 0 <= nose_x < width and 0 <= nose_ypos < height:
                if abs(nx) == 1:
                    canvas[nose_ypos][nose_x] = SHADOW_BLACK
                else:
                    canvas[nose_ypos][nose_x] = BONE_WHITE
    
    # === MOUTH (WIDE OPEN - ROARING/BITING) ===
    mouth_y = head_y + 3
    for my in range(7):
        mouth_width = 5 - my // 3
        for mx in range(-mouth_width, mouth_width + 1):
            mouth_x = center_x + mx - 2
            mouth_ypos = mouth_y + my
            if 0 <= mouth_x < width and 0 <= mouth_ypos < height:
                if my < 2:
                    # Upper teeth
                    if abs(mx) % 2 == 1 and abs(mx) < 5:
                        canvas[mouth_ypos][mouth_x] = TEETH_WHITE
                    else:
                        canvas[mouth_ypos][mouth_x] = SHADOW_BLACK
                elif my < 4:
                    # Mouth cavity
                    canvas[mouth_ypos][mouth_x] = SHADOW_BLACK
                else:
                    # Lower teeth
                    if abs(mx) % 2 == 0 and abs(mx) < 5:
                        canvas[mouth_ypos][mouth_x] = TEETH_YELLOW
                    else:
                        canvas[mouth_ypos][mouth_x] = FLESH_DARK
    
    # Prominent fangs
    for tooth_x in [-4, -2, 2, 4]:
        tooth_pos = center_x + tooth_x - 2
        tooth_y = mouth_y + 1
        if 0 <= tooth_pos < width and 0 <= tooth_y < height:
            canvas[tooth_y][tooth_pos] = TEETH_WHITE
        
        tooth_y = mouth_y + 5
        if 0 <= tooth_pos < width and 0 <= tooth_y < height:
            canvas[tooth_y][tooth_pos] = TEETH_YELLOW
    
    # Blood dripping
    for by in range(3):
        for bx in range(-5, 6):
            if abs(bx) > 2:
                blood_x = center_x + bx - 2
                blood_y = mouth_y + 7 + by
                if 0 <= blood_x < width and 0 <= blood_y < height:
                    canvas[blood_y][blood_x] = BLOOD_DARK if by > 1 else BLOOD_RED
    
    # === MOTION EFFECTS (lunging forward) ===
    # Motion blur on arms
    for blur in range(8):
        for by in range(3):
            blur_x = left_hand_x + 10 + blur
            blur_y = left_hand_y + by
            if 0 <= blur_x < width and 0 <= blur_y < height:
                canvas[blur_y][blur_x] = MOTION_BLUR
    
    return canvas


def main():
    print("Creating zombie monster images...")
    
    zombie_default = create_zombie_default()
    zombie_attack = create_zombie_attack()
    
    # Convert to PIL and scale up
    scale = 4
    
    # Default pose
    img_default = Image.fromarray(zombie_default, 'RGBA')
    img_default_scaled = img_default.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_default_scaled.save('art/zombie_monster.png')
    print(f"✓ Saved: art/zombie_monster.png ({64 * scale}x{64 * scale})")
    
    # Attack animation
    img_attack = Image.fromarray(zombie_attack, 'RGBA')
    img_attack_scaled = img_attack.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_attack_scaled.save('art/zombie_monster_attack.png')
    print(f"✓ Saved: art/zombie_monster_attack.png ({64 * scale}x{64 * scale})")
    
    print("\n✅ Zombie monster creation complete!")
    print("\nFeatures:")
    print("- Default: Shambling zombie with decayed flesh, hunched posture, tattered jeans")
    print("- Attack: Lunging forward with arms reaching, mouth open wide, aggressive stance")
    print("\nStyle: Classic undead horror zombie")
    print("Colors: Gray/purple rotting flesh, decay patches, blood stains, tattered blue jeans")


if __name__ == '__main__':
    main()
