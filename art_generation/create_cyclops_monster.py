"""
Cyclops Monster Creator
Creates pixel art for a powerful one-eyed giant with muscular build.
Inspired by the classical cyclops with horns, powerful physique, and tribal appearance.

Resolution: 64x64 pixels (scaled 4x to 256x256)
Style: Pixel art with muscular detail
Palette: Tan/beige skin tones, brown hair/skirt, dark horns
"""

from PIL import Image
import numpy as np


def create_cyclops_default():
    """Create the default standing cyclops pose."""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette - inspired by the reference image
    SKIN_BASE = [210, 180, 140, 255]       # Tan skin
    SKIN_LIGHT = [230, 200, 160, 255]      # Light highlights
    SKIN_DARK = [170, 140, 100, 255]       # Dark shadows
    SKIN_SHADOW = [140, 110, 80, 255]      # Deep shadows
    HORN_LIGHT = [200, 180, 140, 255]      # Horn base
    HORN_DARK = [120, 100, 70, 255]        # Horn shadow
    HAIR_BROWN = [140, 100, 60, 255]       # Brown hair/skirt
    HAIR_DARK = [100, 70, 40, 255]         # Dark hair
    HAIR_LIGHT = [180, 130, 80, 255]       # Light hair strands
    EYE_WHITE = [240, 240, 240, 255]       # Eye white
    EYE_IRIS = [100, 80, 60, 255]          # Brown iris
    EYE_PUPIL = [20, 20, 20, 255]          # Black pupil
    MOUTH_DARK = [80, 50, 40, 255]         # Mouth interior
    TEETH_WHITE = [240, 230, 220, 255]     # Teeth/tusks
    
    center_x = 32
    base_y = 58
    
    # === LEGS ===
    # Left leg
    for ly in range(18):
        leg_width = 5 - ly // 8
        for lx in range(-leg_width, leg_width + 1):
            leg_x = center_x - 6 + lx
            leg_y = base_y - ly
            if 0 <= leg_x < width and 0 <= leg_y < height:
                if lx < 0:
                    canvas[leg_y][leg_x] = SKIN_BASE if abs(lx) < 2 else SKIN_SHADOW
                else:
                    canvas[leg_y][leg_x] = SKIN_LIGHT if lx < 2 else SKIN_BASE
    
    # Right leg
    for ly in range(18):
        leg_width = 5 - ly // 8
        for lx in range(-leg_width, leg_width + 1):
            leg_x = center_x + 6 + lx
            leg_y = base_y - ly
            if 0 <= leg_x < width and 0 <= leg_y < height:
                if lx < 0:
                    canvas[leg_y][leg_x] = SKIN_SHADOW
                else:
                    canvas[leg_y][leg_x] = SKIN_LIGHT if lx < 2 else SKIN_BASE
    
    # Feet
    for foot_offset in [-6, 6]:
        for fy in range(3):
            for fx in range(-3, 4):
                foot_x = center_x + foot_offset + fx
                foot_y = base_y + fy
                if 0 <= foot_x < width and 0 <= foot_y < height:
                    canvas[foot_y][foot_x] = SKIN_DARK if abs(fx) < 2 else SKIN_SHADOW
    
    # === GRASS SKIRT ===
    skirt_y = base_y - 18
    for sy in range(10):
        skirt_width = 12 - sy // 2
        for sx in range(-skirt_width, skirt_width + 1):
            skirt_x = center_x + sx
            skirt_ypos = skirt_y - sy
            if 0 <= skirt_x < width and 0 <= skirt_ypos < height:
                # Vertical strands
                if (sx + sy) % 3 == 0:
                    canvas[skirt_ypos][skirt_x] = HAIR_BROWN
                elif (sx + sy) % 3 == 1:
                    canvas[skirt_ypos][skirt_x] = HAIR_DARK
                else:
                    canvas[skirt_ypos][skirt_x] = HAIR_LIGHT
    
    # === TORSO (muscular) ===
    torso_y = base_y - 28
    for ty in range(16):
        torso_width = 10 - ty // 8
        for tx in range(-torso_width, torso_width + 1):
            torso_x = center_x + tx
            torso_ypos = torso_y - ty
            if 0 <= torso_x < width and 0 <= torso_ypos < height:
                # Muscular definition
                if ty > 8 and abs(tx) < 3:
                    # Abs definition
                    if (ty % 3 == 0):
                        canvas[torso_ypos][torso_x] = SKIN_SHADOW
                    else:
                        canvas[torso_ypos][torso_x] = SKIN_BASE
                elif tx < 0:
                    canvas[torso_ypos][torso_x] = SKIN_BASE if tx > -6 else SKIN_SHADOW
                else:
                    canvas[torso_ypos][torso_x] = SKIN_LIGHT if tx < 6 else SKIN_BASE
    
    # Pectoral definition
    for pec_y in range(4):
        for pec_x in range(-6, 7):
            if abs(pec_x) > 1:
                px = center_x + pec_x
                py = torso_y - 12 + pec_y
                if 0 <= px < width and 0 <= py < height:
                    canvas[py][px] = SKIN_SHADOW if pec_y == 3 else SKIN_BASE
    
    # === ARMS ===
    # Left arm (bent, hand on hip)
    arm_start_y = torso_y - 14
    for ay in range(12):
        arm_width = 3
        arm_x_offset = -10 - ay // 3
        for ax in range(-arm_width, arm_width + 1):
            arm_x = center_x + arm_x_offset + ax
            arm_y = arm_start_y + ay
            if 0 <= arm_x < width and 0 <= arm_y < height:
                canvas[arm_y][arm_x] = SKIN_BASE if ax > 0 else SKIN_SHADOW
    
    # Left hand
    for hy in range(5):
        for hx in range(-3, 3):
            hand_x = center_x - 14 + hx
            hand_y = arm_start_y + 12 + hy
            if 0 <= hand_x < width and 0 <= hand_y < height:
                canvas[hand_y][hand_x] = SKIN_LIGHT if hx > 0 else SKIN_DARK
    
    # Right arm (hanging down)
    for ay in range(14):
        arm_width = 3
        for ax in range(-arm_width, arm_width + 1):
            arm_x = center_x + 10 + ax
            arm_y = arm_start_y + ay
            if 0 <= arm_x < width and 0 <= arm_y < height:
                canvas[arm_y][arm_x] = SKIN_LIGHT if ax > 0 else SKIN_BASE
    
    # Right hand
    for hy in range(5):
        for hx in range(-3, 3):
            hand_x = center_x + 10 + hx
            hand_y = arm_start_y + 14 + hy
            if 0 <= hand_x < width and 0 <= hand_y < height:
                canvas[hand_y][hand_x] = SKIN_LIGHT if hx > 0 else SKIN_DARK
    
    # === SHOULDERS (broad) ===
    shoulder_y = torso_y - 15
    for sy in range(3):
        for sx in range(-12, 13):
            shoulder_x = center_x + sx
            shoulder_ypos = shoulder_y - sy
            if 0 <= shoulder_x < width and 0 <= shoulder_ypos < height and abs(sx) > 6:
                canvas[shoulder_ypos][shoulder_x] = SKIN_BASE if sx < 0 else SKIN_LIGHT
    
    # === NECK ===
    neck_y = torso_y - 16
    for ny in range(4):
        for nx in range(-3, 4):
            neck_x = center_x + nx
            neck_ypos = neck_y - ny
            if 0 <= neck_x < width and 0 <= neck_ypos < height:
                canvas[neck_ypos][neck_x] = SKIN_BASE if nx < 0 else SKIN_LIGHT
    
    # === HEAD ===
    head_y = neck_y - 6
    
    # Face (rounded)
    for fy in range(-8, 10):
        for fx in range(-8, 9):
            if abs(fx) * 1.1 + abs(fy) * 0.9 < 10:
                face_x = center_x + fx
                face_y = head_y + fy
                if 0 <= face_x < width and 0 <= face_y < height:
                    if fx < -2:
                        canvas[face_y][face_x] = SKIN_SHADOW
                    elif fx < 2:
                        canvas[face_y][face_x] = SKIN_BASE
                    else:
                        canvas[face_y][face_x] = SKIN_LIGHT
    
    # === SINGLE LARGE EYE (centered) ===
    eye_y = head_y - 2
    for ey in range(-5, 6):
        for ex in range(-5, 6):
            if ex * ex + ey * ey < 25:
                eye_x = center_x + ex
                eye_ypos = eye_y + ey
                if 0 <= eye_x < width and 0 <= eye_ypos < height:
                    # Eye white
                    canvas[eye_ypos][eye_x] = EYE_WHITE
    
    # Iris
    for ey in range(-3, 4):
        for ex in range(-3, 4):
            if ex * ex + ey * ey < 9:
                eye_x = center_x + ex
                eye_ypos = eye_y + ey
                if 0 <= eye_x < width and 0 <= eye_ypos < height:
                    canvas[eye_ypos][eye_x] = EYE_IRIS
    
    # Pupil
    for ey in range(-2, 3):
        for ex in range(-2, 3):
            if ex * ex + ey * ey < 4:
                eye_x = center_x + ex
                eye_ypos = eye_y + ey
                if 0 <= eye_x < width and 0 <= eye_ypos < height:
                    canvas[eye_ypos][eye_x] = EYE_PUPIL
    
    # === HORNS (two horns on sides of head) ===
    # Left horn
    for hy in range(10):
        horn_width = 2 - hy // 6
        horn_curve = hy // 2
        for hx in range(-horn_width, horn_width + 1):
            horn_x = center_x - 8 - horn_curve + hx
            horn_y = head_y - 8 - hy
            if 0 <= horn_x < width and 0 <= horn_y < height:
                canvas[horn_y][horn_x] = HORN_LIGHT if hx > 0 else HORN_DARK
    
    # Right horn
    for hy in range(10):
        horn_width = 2 - hy // 6
        horn_curve = hy // 2
        for hx in range(-horn_width, horn_width + 1):
            horn_x = center_x + 8 + horn_curve + hx
            horn_y = head_y - 8 - hy
            if 0 <= horn_x < width and 0 <= horn_y < height:
                canvas[horn_y][horn_x] = HORN_DARK if hx < 0 else HORN_LIGHT
    
    # === MOUTH (small, with visible teeth) ===
    mouth_y = head_y + 6
    for my in range(3):
        for mx in range(-4, 5):
            mouth_x = center_x + mx
            mouth_ypos = mouth_y + my
            if 0 <= mouth_x < width and 0 <= mouth_ypos < height:
                if my == 0:
                    canvas[mouth_ypos][mouth_x] = SKIN_SHADOW
                elif my == 1:
                    canvas[mouth_ypos][mouth_x] = MOUTH_DARK if abs(mx) < 3 else SKIN_SHADOW
                else:
                    canvas[mouth_ypos][mouth_x] = TEETH_WHITE if abs(mx) < 2 else MOUTH_DARK
    
    # === NOSE ===
    nose_y = head_y + 2
    for ny in range(3):
        for nx in range(-2, 3):
            if abs(nx) + ny < 3:
                nose_x = center_x + nx
                nose_ypos = nose_y + ny
                if 0 <= nose_x < width and 0 <= nose_ypos < height:
                    canvas[nose_ypos][nose_x] = SKIN_DARK if nx < 0 else SKIN_SHADOW
    
    # === HAIR/TEXTURE (bumpy skin texture on head) ===
    for tx in range(-6, 7):
        for ty in range(-6, -2):
            if (tx + ty) % 2 == 0 and abs(tx) < 6:
                texture_x = center_x + tx
                texture_y = head_y + ty
                if 0 <= texture_x < width and 0 <= texture_y < height:
                    # Add slight texture bumps
                    if canvas[texture_y][texture_x][3] > 0:
                        canvas[texture_y][texture_x] = SKIN_SHADOW
    
    return canvas


def create_cyclops_attack():
    """Create the attacking cyclops animation - raised fist punch."""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Same color palette
    SKIN_BASE = [210, 180, 140, 255]
    SKIN_LIGHT = [230, 200, 160, 255]
    SKIN_DARK = [170, 140, 100, 255]
    SKIN_SHADOW = [140, 110, 80, 255]
    HORN_LIGHT = [200, 180, 140, 255]
    HORN_DARK = [120, 100, 70, 255]
    HAIR_BROWN = [140, 100, 60, 255]
    HAIR_DARK = [100, 70, 40, 255]
    HAIR_LIGHT = [180, 130, 80, 255]
    EYE_WHITE = [240, 240, 240, 255]
    EYE_IRIS = [100, 80, 60, 255]
    EYE_PUPIL = [20, 20, 20, 255]
    MOUTH_DARK = [80, 50, 40, 255]
    TEETH_WHITE = [240, 230, 220, 255]
    IMPACT_YELLOW = [255, 240, 100, 200]
    IMPACT_WHITE = [255, 255, 255, 180]
    
    center_x = 32
    base_y = 58
    
    # === LEGS (same as default) ===
    # Left leg
    for ly in range(18):
        leg_width = 5 - ly // 8
        for lx in range(-leg_width, leg_width + 1):
            leg_x = center_x - 6 + lx
            leg_y = base_y - ly
            if 0 <= leg_x < width and 0 <= leg_y < height:
                if lx < 0:
                    canvas[leg_y][leg_x] = SKIN_BASE if abs(lx) < 2 else SKIN_SHADOW
                else:
                    canvas[leg_y][leg_x] = SKIN_LIGHT if lx < 2 else SKIN_BASE
    
    # Right leg
    for ly in range(18):
        leg_width = 5 - ly // 8
        for lx in range(-leg_width, leg_width + 1):
            leg_x = center_x + 6 + lx
            leg_y = base_y - ly
            if 0 <= leg_x < width and 0 <= leg_y < height:
                if lx < 0:
                    canvas[leg_y][leg_x] = SKIN_SHADOW
                else:
                    canvas[leg_y][leg_x] = SKIN_LIGHT if lx < 2 else SKIN_BASE
    
    # Feet
    for foot_offset in [-6, 6]:
        for fy in range(3):
            for fx in range(-3, 4):
                foot_x = center_x + foot_offset + fx
                foot_y = base_y + fy
                if 0 <= foot_x < width and 0 <= foot_y < height:
                    canvas[foot_y][foot_x] = SKIN_DARK if abs(fx) < 2 else SKIN_SHADOW
    
    # === GRASS SKIRT ===
    skirt_y = base_y - 18
    for sy in range(10):
        skirt_width = 12 - sy // 2
        for sx in range(-skirt_width, skirt_width + 1):
            skirt_x = center_x + sx
            skirt_ypos = skirt_y - sy
            if 0 <= skirt_x < width and 0 <= skirt_ypos < height:
                if (sx + sy) % 3 == 0:
                    canvas[skirt_ypos][skirt_x] = HAIR_BROWN
                elif (sx + sy) % 3 == 1:
                    canvas[skirt_ypos][skirt_x] = HAIR_DARK
                else:
                    canvas[skirt_ypos][skirt_x] = HAIR_LIGHT
    
    # === TORSO (leaning forward slightly) ===
    torso_y = base_y - 28
    for ty in range(16):
        torso_width = 10 - ty // 8
        for tx in range(-torso_width, torso_width + 1):
            torso_x = center_x + tx
            torso_ypos = torso_y - ty
            if 0 <= torso_x < width and 0 <= torso_ypos < height:
                # Muscular definition
                if ty > 8 and abs(tx) < 3:
                    if (ty % 3 == 0):
                        canvas[torso_ypos][torso_x] = SKIN_SHADOW
                    else:
                        canvas[torso_ypos][torso_x] = SKIN_BASE
                elif tx < 0:
                    canvas[torso_ypos][torso_x] = SKIN_BASE if tx > -6 else SKIN_SHADOW
                else:
                    canvas[torso_ypos][torso_x] = SKIN_LIGHT if tx < 6 else SKIN_BASE
    
    # Pectoral definition
    for pec_y in range(4):
        for pec_x in range(-6, 7):
            if abs(pec_x) > 1:
                px = center_x + pec_x
                py = torso_y - 12 + pec_y
                if 0 <= px < width and 0 <= py < height:
                    canvas[py][px] = SKIN_SHADOW if pec_y == 3 else SKIN_BASE
    
    # === ARMS ===
    arm_start_y = torso_y - 14
    
    # Left arm (pulled back)
    for ay in range(10):
        arm_width = 3
        arm_x_offset = -8 + ay // 4
        for ax in range(-arm_width, arm_width + 1):
            arm_x = center_x + arm_x_offset + ax
            arm_y = arm_start_y + ay + 4
            if 0 <= arm_x < width and 0 <= arm_y < height:
                canvas[arm_y][arm_x] = SKIN_BASE if ax > 0 else SKIN_SHADOW
    
    # Left fist
    for hy in range(4):
        for hx in range(-3, 3):
            hand_x = center_x - 5 + hx
            hand_y = arm_start_y + 14 + hy
            if 0 <= hand_x < width and 0 <= hand_y < height:
                canvas[hand_y][hand_x] = SKIN_LIGHT if hx > 0 else SKIN_DARK
    
    # Right arm (PUNCHING FORWARD AND UP - extended)
    punch_x = center_x + 18
    punch_y = arm_start_y - 8
    
    # Upper arm (angled upward)
    for ay in range(12):
        arm_width = 3
        for ax in range(-arm_width, arm_width + 1):
            arm_x = center_x + 8 + ay
            arm_y = arm_start_y + 2 - ay // 2
            if 0 <= arm_x < width and 0 <= arm_y < height:
                canvas[arm_y][arm_x] = SKIN_LIGHT if ax > 0 else SKIN_BASE
    
    # Forearm extending forward
    for ay in range(8):
        arm_width = 3 - ay // 4
        for ax in range(-arm_width, arm_width + 1):
            arm_x = punch_x + ay // 2 + ax
            arm_y = punch_y + ay // 3
            if 0 <= arm_x < width and 0 <= arm_y < height:
                canvas[arm_y][arm_x] = SKIN_LIGHT if ax > 0 else SKIN_DARK
    
    # LARGE FIST (clenched, prominent)
    fist_x = punch_x + 6
    fist_y = punch_y + 2
    for fy in range(6):
        for fx in range(-4, 5):
            if abs(fx) * 0.8 + abs(fy - 3) < 4:
                fist_xpos = fist_x + fx
                fist_ypos = fist_y + fy
                if 0 <= fist_xpos < width and 0 <= fist_ypos < height:
                    if fx < 0:
                        canvas[fist_ypos][fist_xpos] = SKIN_DARK
                    elif fx < 2:
                        canvas[fist_ypos][fist_xpos] = SKIN_BASE
                    else:
                        canvas[fist_ypos][fist_xpos] = SKIN_LIGHT
    
    # Knuckles (add definition)
    for knuckle in range(3):
        kx = fist_x - 2 + knuckle * 2
        ky = fist_y + 1
        if 0 <= kx < width and 0 <= ky < height:
            canvas[ky][kx] = SKIN_SHADOW
    
    # === SHOULDERS ===
    shoulder_y = torso_y - 15
    for sy in range(3):
        for sx in range(-12, 13):
            shoulder_x = center_x + sx
            shoulder_ypos = shoulder_y - sy
            if 0 <= shoulder_x < width and 0 <= shoulder_ypos < height and abs(sx) > 6:
                canvas[shoulder_ypos][shoulder_x] = SKIN_BASE if sx < 0 else SKIN_LIGHT
    
    # === NECK ===
    neck_y = torso_y - 16
    for ny in range(4):
        for nx in range(-3, 4):
            neck_x = center_x + nx
            neck_ypos = neck_y - ny
            if 0 <= neck_x < width and 0 <= neck_ypos < height:
                canvas[neck_ypos][neck_x] = SKIN_BASE if nx < 0 else SKIN_LIGHT
    
    # === HEAD (angry expression) ===
    head_y = neck_y - 6
    
    # Face
    for fy in range(-8, 10):
        for fx in range(-8, 9):
            if abs(fx) * 1.1 + abs(fy) * 0.9 < 10:
                face_x = center_x + fx
                face_y = head_y + fy
                if 0 <= face_x < width and 0 <= face_y < height:
                    if fx < -2:
                        canvas[face_y][face_x] = SKIN_SHADOW
                    elif fx < 2:
                        canvas[face_y][face_x] = SKIN_BASE
                    else:
                        canvas[face_y][face_x] = SKIN_LIGHT
    
    # === SINGLE LARGE EYE (wide with rage) ===
    eye_y = head_y - 2
    for ey in range(-6, 7):
        for ex in range(-6, 7):
            if ex * ex + ey * ey < 36:
                eye_x = center_x + ex
                eye_ypos = eye_y + ey
                if 0 <= eye_x < width and 0 <= eye_ypos < height:
                    canvas[eye_ypos][eye_x] = EYE_WHITE
    
    # Iris (larger, showing intensity)
    for ey in range(-4, 5):
        for ex in range(-4, 5):
            if ex * ex + ey * ey < 16:
                eye_x = center_x + ex
                eye_ypos = eye_y + ey
                if 0 <= eye_x < width and 0 <= eye_ypos < height:
                    canvas[eye_ypos][eye_x] = EYE_IRIS
    
    # Pupil (dilated)
    for ey in range(-2, 3):
        for ex in range(-2, 3):
            if ex * ex + ey * ey < 5:
                eye_x = center_x + ex
                eye_ypos = eye_y + ey
                if 0 <= eye_x < width and 0 <= eye_ypos < height:
                    canvas[eye_ypos][eye_x] = EYE_PUPIL
    
    # === HORNS ===
    # Left horn
    for hy in range(10):
        horn_width = 2 - hy // 6
        horn_curve = hy // 2
        for hx in range(-horn_width, horn_width + 1):
            horn_x = center_x - 8 - horn_curve + hx
            horn_y = head_y - 8 - hy
            if 0 <= horn_x < width and 0 <= horn_y < height:
                canvas[horn_y][horn_x] = HORN_LIGHT if hx > 0 else HORN_DARK
    
    # Right horn
    for hy in range(10):
        horn_width = 2 - hy // 6
        horn_curve = hy // 2
        for hx in range(-horn_width, horn_width + 1):
            horn_x = center_x + 8 + horn_curve + hx
            horn_y = head_y - 8 - hy
            if 0 <= horn_x < width and 0 <= horn_y < height:
                canvas[horn_y][horn_x] = HORN_DARK if hx < 0 else HORN_LIGHT
    
    # === MOUTH (open, roaring) ===
    mouth_y = head_y + 6
    for my in range(5):
        mouth_width = 6 - my // 2
        for mx in range(-mouth_width, mouth_width + 1):
            mouth_x = center_x + mx
            mouth_ypos = mouth_y + my
            if 0 <= mouth_x < width and 0 <= mouth_ypos < height:
                if my < 2:
                    canvas[mouth_ypos][mouth_x] = SKIN_SHADOW
                elif my < 4:
                    canvas[mouth_ypos][mouth_x] = MOUTH_DARK if abs(mx) < 4 else SKIN_SHADOW
                else:
                    canvas[mouth_ypos][mouth_x] = TEETH_WHITE if abs(mx) < 3 else MOUTH_DARK
    
    # Tusks
    for tusk_offset in [-4, 4]:
        for ty in range(4):
            tusk_x = center_x + tusk_offset
            tusk_y = mouth_y + 5 + ty
            if 0 <= tusk_x < width and 0 <= tusk_y < height:
                canvas[tusk_y][tusk_x] = TEETH_WHITE if ty < 3 else SKIN_SHADOW
    
    # === NOSE ===
    nose_y = head_y + 2
    for ny in range(3):
        for nx in range(-2, 3):
            if abs(nx) + ny < 3:
                nose_x = center_x + nx
                nose_ypos = nose_y + ny
                if 0 <= nose_x < width and 0 <= nose_ypos < height:
                    canvas[nose_ypos][nose_x] = SKIN_DARK if nx < 0 else SKIN_SHADOW
    
    # === IMPACT EFFECT (around fist) ===
    # Speed lines and impact burst
    for impact in range(8):
        angle = impact * 45
        rad = np.radians(angle)
        for dist in range(3, 8):
            impact_x = int(fist_x + 2 + dist * np.cos(rad))
            impact_y = int(fist_y + 3 + dist * np.sin(rad))
            if 0 <= impact_x < width and 0 <= impact_y < height:
                if dist < 5:
                    canvas[impact_y][impact_x] = IMPACT_WHITE
                else:
                    canvas[impact_y][impact_x] = IMPACT_YELLOW
    
    # Impact starburst
    for star in range(4):
        for sp in range(3):
            star_x = fist_x + 2 + star - 2
            star_y = fist_y + 3
            if 0 <= star_x < width and 0 <= star_y < height:
                canvas[star_y][star_x] = IMPACT_WHITE
            star_x = fist_x + 2
            star_y = fist_y + 3 + star - 2
            if 0 <= star_x < width and 0 <= star_y < height:
                canvas[star_y][star_x] = IMPACT_WHITE
    
    return canvas


def main():
    print("Creating cyclops monster images...")
    
    cyclops_default = create_cyclops_default()
    cyclops_attack = create_cyclops_attack()
    
    # Convert to PIL and scale up
    scale = 4
    
    # Default pose
    img_default = Image.fromarray(cyclops_default, 'RGBA')
    img_default_scaled = img_default.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_default_scaled.save('art/cyclops_monster.png')
    print(f"✓ Saved: art/cyclops_monster.png ({64 * scale}x{64 * scale})")
    
    # Attack animation
    img_attack = Image.fromarray(cyclops_attack, 'RGBA')
    img_attack_scaled = img_attack.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_attack_scaled.save('art/cyclops_monster_attack.png')
    print(f"✓ Saved: art/cyclops_monster_attack.png ({64 * scale}x{64 * scale})")
    
    print("\n✅ Cyclops monster creation complete!")
    print("\nFeatures:")
    print("- Default: Powerful standing pose with muscular build and grass skirt")
    print("- Attack: Dynamic punch animation with raised fist and impact effects")
    print("\nStyle: Classical cyclops with single large eye, horns, and tribal warrior appearance")
    print("Colors: Tan skin, brown hair/skirt, dark horns, prominent eye")


if __name__ == '__main__':
    main()
