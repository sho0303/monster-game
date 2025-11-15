"""
ManBearPig Monster Creator
Creates pixel art for a terrifying hybrid creature - part man, part bear, part pig.
Inspired by the grotesque chimera with red pig head, furry bear body, and humanoid form.

Resolution: 64x64 pixels (scaled 4x to 256x256)
Style: Pixel art with horrific hybrid features
Palette: Red pig skin, dark brown fur, tan/cream body, yellow eyes
"""

from PIL import Image
import numpy as np


def create_manbearpig_default():
    """Create the default aggressive ManBearPig stance."""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette - inspired by the ManBearPig image
    PIG_RED = [180, 50, 60, 255]           # Red pig head
    PIG_DARK = [140, 35, 45, 255]          # Dark red shadows
    PIG_LIGHT = [210, 70, 80, 255]         # Light red highlights
    BODY_TAN = [220, 200, 170, 255]        # Tan body
    BODY_CREAM = [240, 220, 190, 255]      # Cream highlights
    BODY_SHADOW = [180, 160, 130, 255]     # Body shadows
    FUR_BROWN = [50, 35, 25, 255]          # Dark brown fur
    FUR_DARK = [35, 25, 18, 255]           # Very dark fur
    FUR_LIGHT = [70, 50, 35, 255]          # Lighter fur
    EYE_YELLOW = [230, 220, 80, 255]       # Yellow eyes
    EYE_PUPIL = [20, 20, 15, 255]          # Black pupil
    TEETH_WHITE = [240, 235, 230, 255]     # White teeth
    TEETH_YELLOW = [220, 210, 180, 255]    # Yellowed teeth
    SNOUT_PINK = [200, 100, 110, 255]      # Pink snout
    NOSE_DARK = [100, 30, 35, 255]         # Dark nose holes
    HORN_TAN = [200, 180, 150, 255]        # Horn/tusk color
    HORN_DARK = [150, 130, 100, 255]       # Horn shadow
    CLAW_BLACK = [40, 35, 30, 255]         # Black claws
    BLOOD_RED = [140, 20, 20, 255]         # Blood stains
    BLOOD_DARK = [100, 15, 15, 255]        # Dark blood
    
    center_x = 32
    base_y = 61
    
    # === LEGS (thick, muscular, humanoid stance) ===
    # Left leg
    for ly in range(18):
        leg_width = 5 - ly // 10
        for lx in range(-leg_width, leg_width + 1):
            leg_x = center_x - 7 + lx
            leg_y = base_y - ly
            if 0 <= leg_x < width and 0 <= leg_y < height:
                if lx < -2:
                    canvas[leg_y][leg_x] = BODY_SHADOW
                elif lx < 1:
                    canvas[leg_y][leg_x] = BODY_TAN
                else:
                    canvas[leg_y][leg_x] = BODY_CREAM
    
    # Right leg
    for ly in range(18):
        leg_width = 5 - ly // 10
        for lx in range(-leg_width, leg_width + 1):
            leg_x = center_x + 7 + lx
            leg_y = base_y - ly
            if 0 <= leg_x < width and 0 <= leg_y < height:
                if lx < -1:
                    canvas[leg_y][leg_x] = BODY_TAN
                elif lx < 2:
                    canvas[leg_y][leg_x] = BODY_CREAM
                else:
                    canvas[leg_y][leg_x] = BODY_SHADOW
    
    # Feet (large, clawed)
    for foot_offset in [-7, 7]:
        for fy in range(4):
            for fx in range(-5, 6):
                foot_x = center_x + foot_offset + fx
                foot_y = base_y + fy
                if 0 <= foot_x < width and 0 <= foot_y < height:
                    if fy > 2:
                        canvas[foot_y][foot_x] = BODY_SHADOW
                    elif abs(fx) < 3:
                        canvas[foot_y][foot_x] = BODY_TAN
                    else:
                        canvas[foot_y][foot_x] = BODY_CREAM
        
        # Claws
        for claw in range(3):
            claw_x = center_x + foot_offset + (claw - 1) * 3
            claw_y = base_y + 4
            if 0 <= claw_x < width and 0 <= claw_y < height:
                canvas[claw_y][claw_x] = CLAW_BLACK
    
    # === TORSO (muscular, tan/cream body) ===
    torso_y = base_y - 18
    for ty in range(18):
        torso_width = 11 - ty // 8
        for tx in range(-torso_width, torso_width + 1):
            torso_x = center_x + tx
            torso_ypos = torso_y - ty
            if 0 <= torso_x < width and 0 <= torso_ypos < height:
                # Muscular definition
                if ty > 10 and abs(tx) < 4 and tx == 0:
                    canvas[torso_ypos][torso_x] = BODY_SHADOW  # Center line
                elif tx < -7:
                    canvas[torso_ypos][torso_x] = BODY_SHADOW
                elif tx < -2:
                    canvas[torso_ypos][torso_x] = BODY_TAN
                elif tx < 2:
                    canvas[torso_ypos][torso_x] = BODY_CREAM
                elif tx < 7:
                    canvas[torso_ypos][torso_x] = BODY_TAN
                else:
                    canvas[torso_ypos][torso_x] = BODY_SHADOW
    
    # === DARK FUR PATCHES (bear fur on body) ===
    # Left side fur
    fur_y = torso_y - 10
    for fy in range(14):
        fur_width = 8 - fy // 4
        for fx in range(fur_width):
            fur_x = center_x - 11 - fx
            fur_ypos = fur_y - fy
            if 0 <= fur_x < width and 0 <= fur_ypos < height:
                # Shaggy fur texture
                if (fx + fy) % 3 == 0:
                    canvas[fur_ypos][fur_x] = FUR_DARK
                elif fx < 2:
                    canvas[fur_ypos][fur_x] = FUR_BROWN
                else:
                    canvas[fur_ypos][fur_x] = FUR_LIGHT if fy % 2 == 0 else FUR_BROWN
    
    # Right side fur (less coverage)
    for fy in range(10):
        fur_width = 5 - fy // 4
        for fx in range(fur_width):
            fur_x = center_x + 8 + fx
            fur_ypos = fur_y - fy - 2
            if 0 <= fur_x < width and 0 <= fur_ypos < height:
                if (fx + fy) % 3 == 0:
                    canvas[fur_ypos][fur_x] = FUR_DARK
                else:
                    canvas[fur_ypos][fur_x] = FUR_BROWN
    
    # === BLOOD STAINS ON BODY ===
    for blood_spot in [(-5, -12), (3, -15), (0, -20)]:
        for by in range(4):
            for bx in range(-3, 4):
                if abs(bx) + abs(by) < 5:
                    blood_x = center_x + blood_spot[0] + bx
                    blood_y = torso_y + blood_spot[1] + by
                    if 0 <= blood_x < width and 0 <= blood_y < height:
                        canvas[blood_y][blood_x] = BLOOD_RED if by < 2 else BLOOD_DARK
    
    # === ARMS (thick, furry bear arms) ===
    arm_y = torso_y - 16
    
    # Left arm (covered in fur)
    for ay in range(18):
        arm_width = 4 - ay // 10
        for ax in range(-arm_width, arm_width + 1):
            arm_x = center_x - 12 + ax
            arm_ypos = arm_y + ay
            if 0 <= arm_x < width and 0 <= arm_ypos < height:
                # Furry texture
                if (ax + ay) % 3 == 0:
                    canvas[arm_ypos][arm_x] = FUR_DARK
                elif ax < 0:
                    canvas[arm_ypos][arm_x] = FUR_BROWN
                else:
                    canvas[arm_ypos][arm_x] = FUR_LIGHT
    
    # Right arm (partially furry)
    for ay in range(18):
        arm_width = 4 - ay // 10
        for ax in range(-arm_width, arm_width + 1):
            arm_x = center_x + 12 + ax
            arm_ypos = arm_y + ay
            if 0 <= arm_x < width and 0 <= arm_ypos < height:
                # Mixed fur and skin
                if ay > 10 and (ax + ay) % 2 == 0:
                    canvas[arm_ypos][arm_x] = FUR_BROWN
                elif ax < 0:
                    canvas[arm_ypos][arm_x] = BODY_TAN
                else:
                    canvas[arm_ypos][arm_x] = BODY_CREAM
    
    # === HANDS (clawed) ===
    # Left hand (furry paw)
    left_hand_x = center_x - 12
    left_hand_y = arm_y + 18
    for hy in range(6):
        for hx in range(-4, 5):
            hand_x = left_hand_x + hx
            hand_y = left_hand_y + hy
            if 0 <= hand_x < width and 0 <= hand_y < height and abs(hx) + hy < 8:
                if (hx + hy) % 2 == 0:
                    canvas[hand_y][hand_x] = FUR_BROWN
                else:
                    canvas[hand_y][hand_x] = FUR_DARK
    
    # Left claws
    for claw in range(4):
        for cy in range(4):
            claw_x = left_hand_x + (claw - 1.5) * 2
            claw_y = left_hand_y + 6 + cy
            if 0 <= claw_x < width and 0 <= claw_y < height:
                canvas[int(claw_y)][int(claw_x)] = CLAW_BLACK
    
    # Right hand (more human-like but clawed)
    right_hand_x = center_x + 12
    right_hand_y = arm_y + 18
    for hy in range(6):
        for hx in range(-4, 5):
            hand_x = right_hand_x + hx
            hand_y = right_hand_y + hy
            if 0 <= hand_x < width and 0 <= hand_y < height and abs(hx) + hy < 8:
                canvas[hand_y][hand_x] = BODY_TAN if hy < 4 else BODY_SHADOW
    
    # Right claws
    for claw in range(4):
        for cy in range(3):
            claw_x = right_hand_x + (claw - 1.5) * 2
            claw_y = right_hand_y + 6 + cy
            if 0 <= claw_x < width and 0 <= claw_y < height:
                canvas[int(claw_y)][int(claw_x)] = CLAW_BLACK
    
    # === SHOULDERS (broad, muscular) ===
    shoulder_y = torso_y - 18
    for sy in range(5):
        for sx in range(-13, 14):
            shoulder_x = center_x + sx
            shoulder_ypos = shoulder_y - sy
            if 0 <= shoulder_x < width and 0 <= shoulder_ypos < height:
                if abs(sx) > 11:
                    # Fur on shoulders
                    canvas[shoulder_ypos][shoulder_x] = FUR_BROWN if sx < 0 else BODY_SHADOW
                elif abs(sx) > 8:
                    canvas[shoulder_ypos][shoulder_x] = BODY_TAN
                else:
                    canvas[shoulder_ypos][shoulder_x] = BODY_CREAM
    
    # === NECK (thick) ===
    neck_y = shoulder_y - 5
    for ny in range(4):
        neck_width = 5 - ny // 2
        for nx in range(-neck_width, neck_width + 1):
            neck_x = center_x + nx
            neck_ypos = neck_y - ny
            if 0 <= neck_x < width and 0 <= neck_ypos < height:
                canvas[neck_ypos][neck_x] = BODY_TAN if abs(nx) < 3 else BODY_SHADOW
    
    # === PIG HEAD (realistic pig head with proper proportions) ===
    head_y = neck_y - 6
    
    # Head base (elongated pig head shape)
    for hy in range(16):
        # Pig heads are wider in the middle/snout area
        if hy < 6:
            head_width = 6 + hy // 2  # Wider forehead/skull
        elif hy < 12:
            head_width = 8  # Widest at cheeks/snout
        else:
            head_width = 6 - (hy - 12)  # Narrower at jaw
        
        for hx in range(-head_width, head_width + 1):
            head_x = center_x + hx
            head_ypos = head_y - hy
            if 0 <= head_x < width and 0 <= head_ypos < height:
                # Red pig coloring with shading
                if hx < -6:
                    canvas[head_ypos][head_x] = PIG_DARK  # Deep shadow
                elif hx < -3:
                    canvas[head_ypos][head_x] = PIG_RED
                elif hx < 0:
                    canvas[head_ypos][head_x] = PIG_RED if hy % 2 == 0 else PIG_LIGHT
                elif hx < 3:
                    canvas[head_ypos][head_x] = PIG_LIGHT
                elif hx < 6:
                    canvas[head_ypos][head_x] = PIG_RED
                else:
                    canvas[head_ypos][head_x] = PIG_DARK
    
    # === EARS (proper pig ears - triangular, pointing up) ===
    # Left ear
    for ey in range(7):
        ear_width = 3 - ey // 3
        for ex in range(-ear_width, ear_width + 1):
            ear_x = center_x - 7 + ex
            ear_y = head_y - 12 - ey
            if 0 <= ear_x < width and 0 <= ear_y < height:
                if ex < -1:
                    canvas[ear_y][ear_x] = PIG_DARK
                elif ex < 1:
                    canvas[ear_y][ear_x] = PIG_RED
                else:
                    canvas[ear_y][ear_x] = PIG_LIGHT
    
    # Right ear
    for ey in range(7):
        ear_width = 3 - ey // 3
        for ex in range(-ear_width, ear_width + 1):
            ear_x = center_x + 7 + ex
            ear_y = head_y - 12 - ey
            if 0 <= ear_x < width and 0 <= ear_y < height:
                if ex < -1:
                    canvas[ear_y][ear_x] = PIG_RED
                elif ex < 1:
                    canvas[ear_y][ear_x] = PIG_LIGHT
                else:
                    canvas[ear_y][ear_x] = PIG_DARK
    
    # === EYES (small pig eyes, more realistic placement) ===
    eye_y = head_y - 8
    for eye_offset in [-4, 4]:
        # Small beady pig eyes
        for ey in range(-1, 2):
            for ex in range(-1, 2):
                if abs(ex) + abs(ey) < 2:
                    eye_x = center_x + eye_offset + ex
                    eye_ypos = eye_y + ey
                    if 0 <= eye_x < width and 0 <= eye_ypos < height:
                        canvas[eye_ypos][eye_x] = EYE_YELLOW
        
        # Small black pupil
        pupil_x = center_x + eye_offset
        pupil_y = eye_y
        if 0 <= pupil_x < width and 0 <= pupil_y < height:
            canvas[pupil_y][pupil_x] = EYE_PUPIL
    
    # === SNOUT (prominent pig snout - flat front, oval shape) ===
    snout_y = head_y - 2
    
    # Snout base (extends forward)
    for sy in range(8):
        if sy < 3:
            snout_width = 4 + sy  # Wider at front
        else:
            snout_width = 6 - (sy - 3) // 2  # Narrows toward face
        
        for sx in range(-snout_width, snout_width + 1):
            snout_x = center_x + sx
            snout_ypos = snout_y + sy
            if 0 <= snout_x < width and 0 <= snout_ypos < height:
                # Snout is lighter pink/tan
                if sy < 4:
                    # Front of snout (flatter)
                    if abs(sx) < 4:
                        canvas[snout_ypos][snout_x] = SNOUT_PINK
                    else:
                        canvas[snout_ypos][snout_x] = PIG_LIGHT
                else:
                    # Connects to face
                    if abs(sx) < 3:
                        canvas[snout_ypos][snout_x] = SNOUT_PINK
                    else:
                        canvas[snout_ypos][snout_x] = PIG_RED
    
    # Nostrils (large oval nostrils on flat snout front)
    for nostril_offset in [-2, 2]:
        for ny in range(3):
            for nx in range(-2, 2):
                if abs(nx) + ny < 3:
                    nostril_x = center_x + nostril_offset + nx
                    nostril_y = snout_y + 1 + ny
                    if 0 <= nostril_x < width and 0 <= nostril_y < height:
                        canvas[nostril_y][nostril_x] = NOSE_DARK
    
    # === TUSKS (small tusks curving up from lower jaw) ===
    for tusk_offset in [-6, 6]:
        for ty in range(4):
            tusk_x = center_x + tusk_offset + (ty // 2 if tusk_offset < 0 else -ty // 2)
            tusk_y = head_y + 3 - ty
            if 0 <= tusk_x < width and 0 <= tusk_y < height:
                canvas[tusk_y][tusk_x] = HORN_TAN if ty < 3 else HORN_DARK
    
    # === MOUTH (under snout, showing teeth) ===
    mouth_y = head_y + 6
    for my in range(4):
        mouth_width = 5 - my // 2
        for mx in range(-mouth_width, mouth_width + 1):
            mouth_x = center_x + mx
            mouth_ypos = mouth_y + my
            if 0 <= mouth_x < width and 0 <= mouth_ypos < height:
                if my < 1:
                    # Mouth opening
                    canvas[mouth_ypos][mouth_x] = PIG_DARK
                elif my < 2:
                    # Teeth showing
                    if abs(mx) % 2 == 1 and abs(mx) < 5:
                        canvas[mouth_ypos][mouth_x] = TEETH_WHITE
                    else:
                        canvas[mouth_ypos][mouth_x] = PIG_DARK
                else:
                    # Lower jaw
                    if abs(mx) < 4:
                        canvas[mouth_ypos][mouth_x] = PIG_RED if mx % 2 == 0 else TEETH_YELLOW
                    else:
                        canvas[mouth_ypos][mouth_x] = PIG_DARK
    
    return canvas


def create_manbearpig_attack():
    """Create the attacking ManBearPig - lunging forward with rage."""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Same color palette
    PIG_RED = [180, 50, 60, 255]
    PIG_DARK = [140, 35, 45, 255]
    PIG_LIGHT = [210, 70, 80, 255]
    BODY_TAN = [220, 200, 170, 255]
    BODY_CREAM = [240, 220, 190, 255]
    BODY_SHADOW = [180, 160, 130, 255]
    FUR_BROWN = [50, 35, 25, 255]
    FUR_DARK = [35, 25, 18, 255]
    FUR_LIGHT = [70, 50, 35, 255]
    EYE_YELLOW = [230, 220, 80, 255]
    EYE_PUPIL = [20, 20, 15, 255]
    TEETH_WHITE = [240, 235, 230, 255]
    TEETH_YELLOW = [220, 210, 180, 255]
    SNOUT_PINK = [200, 100, 110, 255]
    NOSE_DARK = [100, 30, 35, 255]
    HORN_TAN = [200, 180, 150, 255]
    HORN_DARK = [150, 130, 100, 255]
    CLAW_BLACK = [40, 35, 30, 255]
    BLOOD_RED = [140, 20, 20, 255]
    BLOOD_DARK = [100, 15, 15, 255]
    MOTION_BLUR = [180, 50, 60, 150]
    
    center_x = 32
    base_y = 61
    
    # === LEGS (lunging stance) ===
    # Left leg (forward)
    for ly in range(16):
        leg_width = 5 - ly // 10
        leg_forward = ly // 4
        for lx in range(-leg_width, leg_width + 1):
            leg_x = center_x - 9 - leg_forward + lx
            leg_y = base_y - ly
            if 0 <= leg_x < width and 0 <= leg_y < height:
                if lx < -2:
                    canvas[leg_y][leg_x] = BODY_SHADOW
                elif lx < 1:
                    canvas[leg_y][leg_x] = BODY_TAN
                else:
                    canvas[leg_y][leg_x] = BODY_CREAM
    
    # Right leg (back)
    for ly in range(16):
        leg_width = 5 - ly // 10
        for lx in range(-leg_width, leg_width + 1):
            leg_x = center_x + 8 + lx
            leg_y = base_y - ly
            if 0 <= leg_x < width and 0 <= leg_y < height:
                if lx < -1:
                    canvas[leg_y][leg_x] = BODY_TAN
                elif lx < 2:
                    canvas[leg_y][leg_x] = BODY_CREAM
                else:
                    canvas[leg_y][leg_x] = BODY_SHADOW
    
    # Feet with claws
    for foot_offset, foot_forward in [(-13, -4), (8, 0)]:
        for fy in range(4):
            for fx in range(-5, 6):
                foot_x = center_x + foot_offset + foot_forward + fx
                foot_y = base_y + fy
                if 0 <= foot_x < width and 0 <= foot_y < height:
                    if fy > 2:
                        canvas[foot_y][foot_x] = BODY_SHADOW
                    elif abs(fx) < 3:
                        canvas[foot_y][foot_x] = BODY_TAN
                    else:
                        canvas[foot_y][foot_x] = BODY_CREAM
        
        # Claws
        for claw in range(3):
            claw_x = center_x + foot_offset + foot_forward + (claw - 1) * 3
            claw_y = base_y + 4
            if 0 <= claw_x < width and 0 <= claw_y < height:
                canvas[claw_y][claw_x] = CLAW_BLACK
    
    # === TORSO (leaning forward aggressively) ===
    torso_y = base_y - 16
    for ty in range(18):
        torso_width = 11 - ty // 8
        torso_lean = ty // 4
        for tx in range(-torso_width, torso_width + 1):
            torso_x = center_x + tx - torso_lean
            torso_ypos = torso_y - ty
            if 0 <= torso_x < width and 0 <= torso_ypos < height:
                if ty > 10 and abs(tx) < 4 and tx == 0:
                    canvas[torso_ypos][torso_x] = BODY_SHADOW
                elif tx < -7:
                    canvas[torso_ypos][torso_x] = BODY_SHADOW
                elif tx < -2:
                    canvas[torso_ypos][torso_x] = BODY_TAN
                elif tx < 2:
                    canvas[torso_ypos][torso_x] = BODY_CREAM
                elif tx < 7:
                    canvas[torso_ypos][torso_x] = BODY_TAN
                else:
                    canvas[torso_ypos][torso_x] = BODY_SHADOW
    
    # === FUR PATCHES ===
    fur_y = torso_y - 10
    for fy in range(14):
        fur_width = 8 - fy // 4
        fur_lean = fy // 3
        for fx in range(fur_width):
            fur_x = center_x - 11 - fx - fur_lean
            fur_ypos = fur_y - fy
            if 0 <= fur_x < width and 0 <= fur_ypos < height:
                if (fx + fy) % 3 == 0:
                    canvas[fur_ypos][fur_x] = FUR_DARK
                elif fx < 2:
                    canvas[fur_ypos][fur_x] = FUR_BROWN
                else:
                    canvas[fur_ypos][fur_x] = FUR_LIGHT if fy % 2 == 0 else FUR_BROWN
    
    # Right side fur
    for fy in range(10):
        fur_width = 5 - fy // 4
        for fx in range(fur_width):
            fur_x = center_x + 8 + fx - fy // 3
            fur_ypos = fur_y - fy - 2
            if 0 <= fur_x < width and 0 <= fur_ypos < height:
                if (fx + fy) % 3 == 0:
                    canvas[fur_ypos][fur_x] = FUR_DARK
                else:
                    canvas[fur_ypos][fur_x] = FUR_BROWN
    
    # === BLOOD STAINS (MORE AGGRESSIVE) ===
    for blood_spot in [(-5, -12), (3, -15), (0, -20), (-2, -8)]:
        for by in range(5):
            for bx in range(-3, 4):
                if abs(bx) + abs(by) < 6:
                    blood_x = center_x + blood_spot[0] + bx - 2
                    blood_y = torso_y + blood_spot[1] + by
                    if 0 <= blood_x < width and 0 <= blood_y < height:
                        canvas[blood_y][blood_x] = BLOOD_RED if by < 3 else BLOOD_DARK
    
    # === ARMS (REACHING FORWARD TO ATTACK) ===
    arm_y = torso_y - 14
    
    # Left arm (extended forward, furry)
    for ay in range(20):
        arm_width = 4 - ay // 12
        arm_forward = ay // 2
        for ax in range(-arm_width, arm_width + 1):
            arm_x = center_x - 14 - arm_forward + ax
            arm_ypos = arm_y + ay - 6
            if 0 <= arm_x < width and 0 <= arm_ypos < height:
                if (ax + ay) % 3 == 0:
                    canvas[arm_ypos][arm_x] = FUR_DARK
                elif ax < 0:
                    canvas[arm_ypos][arm_x] = FUR_BROWN
                else:
                    canvas[arm_ypos][arm_x] = FUR_LIGHT
    
    # Right arm (extended forward)
    for ay in range(18):
        arm_width = 4 - ay // 12
        arm_forward = ay // 2
        for ax in range(-arm_width, arm_width + 1):
            arm_x = center_x - 6 - arm_forward + ax
            arm_ypos = arm_y + ay - 4
            if 0 <= arm_x < width and 0 <= arm_ypos < height:
                if ay > 10 and (ax + ay) % 2 == 0:
                    canvas[arm_ypos][arm_x] = FUR_BROWN
                elif ax < 0:
                    canvas[arm_ypos][arm_x] = BODY_TAN
                else:
                    canvas[arm_ypos][arm_x] = BODY_CREAM
    
    # === HANDS (CLAWING) ===
    # Left hand
    left_hand_x = center_x - 24
    left_hand_y = arm_y + 8
    for hy in range(7):
        for hx in range(-4, 5):
            hand_x = left_hand_x + hx
            hand_y = left_hand_y + hy
            if 0 <= hand_x < width and 0 <= hand_y < height and abs(hx) + hy < 9:
                if (hx + hy) % 2 == 0:
                    canvas[hand_y][hand_x] = FUR_BROWN
                else:
                    canvas[hand_y][hand_x] = FUR_DARK
    
    # Left claws (extended)
    for claw in range(4):
        claw_angle = (claw - 1.5) * 0.5
        for cy in range(5):
            claw_x = left_hand_x + (claw - 1.5) * 2 + int(cy * claw_angle)
            claw_y = left_hand_y + 7 + cy
            if 0 <= claw_x < width and 0 <= claw_y < height:
                canvas[int(claw_y)][int(claw_x)] = CLAW_BLACK
    
    # Right hand
    right_hand_x = center_x - 15
    right_hand_y = arm_y + 10
    for hy in range(7):
        for hx in range(-4, 5):
            hand_x = right_hand_x + hx
            hand_y = right_hand_y + hy
            if 0 <= hand_x < width and 0 <= hand_y < height and abs(hx) + hy < 9:
                canvas[hand_y][hand_x] = BODY_TAN if hy < 5 else BODY_SHADOW
    
    # Right claws (extended)
    for claw in range(4):
        claw_angle = (claw - 1.5) * 0.4
        for cy in range(4):
            claw_x = right_hand_x + (claw - 1.5) * 2 + int(cy * claw_angle)
            claw_y = right_hand_y + 7 + cy
            if 0 <= claw_x < width and 0 <= claw_y < height:
                canvas[int(claw_y)][int(claw_x)] = CLAW_BLACK
    
    # === SHOULDERS ===
    shoulder_y = torso_y - 16
    for sy in range(5):
        for sx in range(-13, 14):
            shoulder_x = center_x + sx - 2
            shoulder_ypos = shoulder_y - sy
            if 0 <= shoulder_x < width and 0 <= shoulder_ypos < height:
                if abs(sx) > 11:
                    canvas[shoulder_ypos][shoulder_x] = FUR_BROWN if sx < 0 else BODY_SHADOW
                elif abs(sx) > 8:
                    canvas[shoulder_ypos][shoulder_x] = BODY_TAN
                else:
                    canvas[shoulder_ypos][shoulder_x] = BODY_CREAM
    
    # === NECK ===
    neck_y = shoulder_y - 5
    for ny in range(4):
        neck_width = 5 - ny // 2
        for nx in range(-neck_width, neck_width + 1):
            neck_x = center_x + nx - 2
            neck_ypos = neck_y - ny
            if 0 <= neck_x < width and 0 <= neck_ypos < height:
                canvas[neck_ypos][neck_x] = BODY_TAN if abs(nx) < 3 else BODY_SHADOW
    
    # === PIG HEAD (AGGRESSIVE ROARING - realistic pig head) ===
    head_y = neck_y - 6
    
    # Head base (elongated pig head shape)
    for hy in range(16):
        # Pig heads are wider in the middle/snout area
        if hy < 6:
            head_width = 6 + hy // 2  # Wider forehead/skull
        elif hy < 12:
            head_width = 8  # Widest at cheeks/snout
        else:
            head_width = 6 - (hy - 12)  # Narrower at jaw
        
        for hx in range(-head_width, head_width + 1):
            head_x = center_x + hx - 2
            head_ypos = head_y - hy
            if 0 <= head_x < width and 0 <= head_ypos < height:
                # Red pig coloring with shading
                if hx < -6:
                    canvas[head_ypos][head_x] = PIG_DARK
                elif hx < -3:
                    canvas[head_ypos][head_x] = PIG_RED
                elif hx < 0:
                    canvas[head_ypos][head_x] = PIG_RED if hy % 2 == 0 else PIG_LIGHT
                elif hx < 3:
                    canvas[head_ypos][head_x] = PIG_LIGHT
                elif hx < 6:
                    canvas[head_ypos][head_x] = PIG_RED
                else:
                    canvas[head_ypos][head_x] = PIG_DARK
    
    # === EARS (triangular pig ears) ===
    # Left ear
    for ey in range(7):
        ear_width = 3 - ey // 3
        for ex in range(-ear_width, ear_width + 1):
            ear_x = center_x - 7 + ex - 2
            ear_y = head_y - 12 - ey
            if 0 <= ear_x < width and 0 <= ear_y < height:
                if ex < -1:
                    canvas[ear_y][ear_x] = PIG_DARK
                elif ex < 1:
                    canvas[ear_y][ear_x] = PIG_RED
                else:
                    canvas[ear_y][ear_x] = PIG_LIGHT
    
    # Right ear
    for ey in range(7):
        ear_width = 3 - ey // 3
        for ex in range(-ear_width, ear_width + 1):
            ear_x = center_x + 7 + ex - 2
            ear_y = head_y - 12 - ey
            if 0 <= ear_x < width and 0 <= ear_y < height:
                if ex < -1:
                    canvas[ear_y][ear_x] = PIG_RED
                elif ex < 1:
                    canvas[ear_y][ear_x] = PIG_LIGHT
                else:
                    canvas[ear_y][ear_x] = PIG_DARK
    
    # === EYES (wide, enraged pig eyes) ===
    eye_y = head_y - 8
    for eye_offset in [-4, 4]:
        # Larger eyes for aggressive look
        for ey in range(-2, 3):
            for ex in range(-2, 3):
                if abs(ex) + abs(ey) < 3:
                    eye_x = center_x + eye_offset + ex - 2
                    eye_ypos = eye_y + ey
                    if 0 <= eye_x < width and 0 <= eye_ypos < height:
                        canvas[eye_ypos][eye_x] = EYE_YELLOW
        
        # Dilated pupil
        for py in range(-1, 2):
            pupil_x = center_x + eye_offset - 2
            pupil_y = eye_y + py
            if 0 <= pupil_x < width and 0 <= pupil_y < height:
                canvas[pupil_y][pupil_x] = EYE_PUPIL
    
    # === SNOUT (prominent, extending forward) ===
    snout_y = head_y - 2
    
    # Snout base
    for sy in range(9):
        if sy < 3:
            snout_width = 4 + sy  # Wider at front
        else:
            snout_width = 6 - (sy - 3) // 2  # Narrows toward face
        
        for sx in range(-snout_width, snout_width + 1):
            snout_x = center_x + sx - 2
            snout_ypos = snout_y + sy
            if 0 <= snout_x < width and 0 <= snout_ypos < height:
                if sy < 5:
                    # Front of snout
                    if abs(sx) < 4:
                        canvas[snout_ypos][snout_x] = SNOUT_PINK
                    else:
                        canvas[snout_ypos][snout_x] = PIG_LIGHT
                else:
                    # Connects to face
                    if abs(sx) < 3:
                        canvas[snout_ypos][snout_x] = SNOUT_PINK
                    else:
                        canvas[snout_ypos][snout_x] = PIG_RED
    
    # Nostrils (flared with rage)
    for nostril_offset in [-3, 3]:
        for ny in range(3):
            for nx in range(-2, 2):
                if abs(nx) + ny < 4:
                    nostril_x = center_x + nostril_offset + nx - 2
                    nostril_y = snout_y + 1 + ny
                    if 0 <= nostril_x < width and 0 <= nostril_y < height:
                        canvas[nostril_y][nostril_x] = NOSE_DARK
    
    # === TUSKS (curved upward) ===
    for tusk_offset in [-7, 7]:
        for ty in range(5):
            tusk_x = center_x + tusk_offset + (ty // 2 if tusk_offset < 0 else -ty // 2) - 2
            tusk_y = head_y + 2 - ty
            if 0 <= tusk_x < width and 0 <= tusk_y < height:
                canvas[tusk_y][tusk_x] = HORN_TAN if ty < 4 else HORN_DARK
    
    # === MOUTH (WIDE OPEN ROARING) ===
    mouth_y = head_y + 7
    for my in range(6):
        mouth_width = 6 - my // 3
        for mx in range(-mouth_width, mouth_width + 1):
            mouth_x = center_x + mx - 2
            mouth_ypos = mouth_y + my
            if 0 <= mouth_x < width and 0 <= mouth_ypos < height:
                if my < 1:
                    # Top of mouth opening
                    canvas[mouth_ypos][mouth_x] = PIG_DARK
                elif my < 3:
                    # Upper teeth
                    if abs(mx) % 2 == 1 and abs(mx) < 6:
                        canvas[mouth_ypos][mouth_x] = TEETH_WHITE
                    else:
                        canvas[mouth_ypos][mouth_x] = PIG_DARK
                else:
                    # Lower jaw with teeth
                    if abs(mx) < 5 and mx % 2 == 0:
                        canvas[mouth_ypos][mouth_x] = TEETH_YELLOW
                    else:
                        canvas[mouth_ypos][mouth_x] = PIG_RED
    
    # === MOTION EFFECTS ===
    # Motion blur on claws
    for blur in range(6):
        for by in range(2):
            blur_x = left_hand_x + 8 + blur
            blur_y = left_hand_y + by
            if 0 <= blur_x < width and 0 <= blur_y < height:
                canvas[blur_y][blur_x] = MOTION_BLUR
    
    return canvas


def main():
    print("Creating ManBearPig monster images...")
    
    manbearpig_default = create_manbearpig_default()
    manbearpig_attack = create_manbearpig_attack()
    
    # Convert to PIL and scale up
    scale = 4
    
    # Default pose
    img_default = Image.fromarray(manbearpig_default, 'RGBA')
    img_default_scaled = img_default.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_default_scaled.save('art/manbearpig_monster.png')
    print(f"✓ Saved: art/manbearpig_monster.png ({64 * scale}x{64 * scale})")
    
    # Attack animation
    img_attack = Image.fromarray(manbearpig_attack, 'RGBA')
    img_attack_scaled = img_attack.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_attack_scaled.save('art/manbearpig_monster_attack.png')
    print(f"✓ Saved: art/manbearpig_monster_attack.png ({64 * scale}x{64 * scale})")
    
    print("\n✅ ManBearPig monster creation complete!")
    print("\nFeatures:")
    print("- Default: Aggressive stance with red pig head, tan body, dark furry patches")
    print("- Attack: Lunging forward with extended claws, roaring mouth, blood-stained")
    print("\nStyle: Horrific hybrid creature (man + bear + pig)")
    print("Colors: Red pig skin, dark brown fur, tan/cream body, yellow eyes, blood stains")


if __name__ == '__main__':
    main()
