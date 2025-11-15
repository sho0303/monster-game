"""
Manticore Monster Creator
Creates pixel art for a fearsome manticore - lion body, human face, dragon wings, scorpion tail.
Inspired by the classic mythological creature with distinctive features.

Resolution: 64x64 pixels (scaled 4x to 256x256)
Style: Pixel art with detailed creature features
Palette: Orange/brown fur, tan skin, dark wings, yellow spikes
"""

from PIL import Image
import numpy as np


def create_manticore_default():
    """Create the default aggressive manticore pose."""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette - inspired by the manticore image
    FUR_ORANGE = [200, 120, 60, 255]       # Orange fur
    FUR_LIGHT = [230, 150, 80, 255]        # Light orange
    FUR_DARK = [160, 90, 40, 255]          # Dark orange/brown
    FUR_BROWN = [120, 70, 30, 255]         # Brown shadows
    MANE_BROWN = [140, 80, 40, 255]        # Mane brown
    MANE_LIGHT = [170, 100, 50, 255]       # Light mane
    MANE_DARK = [100, 60, 25, 255]         # Dark mane
    SKIN_TAN = [220, 180, 140, 255]        # Human face skin
    SKIN_SHADOW = [180, 140, 100, 255]     # Face shadow
    EYE_YELLOW = [240, 220, 60, 255]       # Yellow eyes
    EYE_PUPIL = [20, 20, 20, 255]          # Black pupil
    TEETH_WHITE = [240, 240, 230, 255]     # White teeth
    TEETH_YELLOW = [220, 210, 180, 255]    # Yellowed teeth
    WING_MEMBRANE = [180, 100, 60, 255]    # Wing membrane
    WING_DARK = [140, 70, 40, 255]         # Wing shadow
    WING_BONE = [160, 140, 120, 255]       # Wing bones
    TAIL_ORANGE = [200, 110, 50, 255]      # Tail
    TAIL_DARK = [150, 80, 35, 255]         # Tail shadow
    SPIKE_YELLOW = [230, 200, 100, 255]    # Tail spikes
    SPIKE_DARK = [180, 150, 70, 255]       # Spike shadow
    CLAW_DARK = [80, 60, 40, 255]          # Claws
    
    center_x = 32
    base_y = 60
    
    # === BACK LEGS (lion haunches) ===
    # Left back leg
    for ly in range(12):
        leg_width = 5 - ly // 6
        for lx in range(-leg_width, leg_width + 1):
            leg_x = center_x - 12 + lx
            leg_y = base_y - ly
            if 0 <= leg_x < width and 0 <= leg_y < height:
                canvas[leg_y][leg_x] = FUR_ORANGE if lx >= 0 else FUR_DARK
    
    # Right back leg
    for ly in range(12):
        leg_width = 5 - ly // 6
        for lx in range(-leg_width, leg_width + 1):
            leg_x = center_x + 12 + lx
            leg_y = base_y - ly
            if 0 <= leg_x < width and 0 <= leg_y < height:
                canvas[leg_y][leg_x] = FUR_LIGHT if lx >= 0 else FUR_ORANGE
    
    # Back paws
    for paw_offset in [-12, 12]:
        for py in range(3):
            for px in range(-4, 4):
                paw_x = center_x + paw_offset + px
                paw_y = base_y + py
                if 0 <= paw_x < width and 0 <= paw_y < height:
                    canvas[paw_y][paw_x] = FUR_BROWN if py > 1 else FUR_DARK
    
    # === BODY (powerful lion body) ===
    body_y = base_y - 12
    for by in range(18):
        body_width = 14 - by // 6
        for bx in range(-body_width, body_width + 1):
            body_x = center_x + bx
            body_ypos = body_y - by
            if 0 <= body_x < width and 0 <= body_ypos < height:
                # Muscular body with stripes
                if by > 10 and abs(bx) < 6 and (by + bx) % 4 == 0:
                    canvas[body_ypos][body_x] = FUR_BROWN
                elif bx < -8:
                    canvas[body_ypos][body_x] = FUR_DARK
                elif bx < 0:
                    canvas[body_ypos][body_x] = FUR_ORANGE
                elif bx < 8:
                    canvas[body_ypos][body_x] = FUR_LIGHT
                else:
                    canvas[body_ypos][body_x] = FUR_ORANGE
    
    # === TAIL (scorpion-like with spikes) ===
    tail_start_x = center_x + 14
    tail_start_y = body_y - 8
    
    # Tail base (thick)
    for ty in range(8):
        tail_width = 4 - ty // 3
        for tx in range(-tail_width, tail_width + 1):
            tail_x = tail_start_x + tx
            tail_y = tail_start_y + ty
            if 0 <= tail_x < width and 0 <= tail_y < height:
                canvas[tail_y][tail_x] = TAIL_ORANGE if tx >= 0 else TAIL_DARK
    
    # Tail curve (going up)
    for ty in range(12):
        tail_curve = ty // 2
        tail_width = 3 - ty // 5
        for tx in range(-tail_width, tail_width + 1):
            tail_x = tail_start_x + 8 + tail_curve + tx
            tail_y = tail_start_y + 8 - ty
            if 0 <= tail_x < width and 0 <= tail_y < height:
                canvas[tail_y][tail_x] = TAIL_ORANGE if tx >= 0 else TAIL_DARK
    
    # Tail stinger bulb
    stinger_x = tail_start_x + 14
    stinger_y = tail_start_y - 4
    for sy in range(5):
        for sx in range(-3, 4):
            if abs(sx) * 0.8 + abs(sy - 2) < 3:
                sting_x = stinger_x + sx
                sting_y = stinger_y + sy
                if 0 <= sting_x < width and 0 <= sting_y < height:
                    canvas[sting_y][sting_x] = TAIL_DARK if sy > 2 else TAIL_ORANGE
    
    # Tail spikes (multiple spines)
    for spike_num in range(5):
        spike_x = tail_start_x + 10 + spike_num
        spike_y = tail_start_y - spike_num // 2
        for sy in range(4):
            spike_offset = sy // 2
            sx = stinger_x - spike_num * 2 + spike_offset
            if 0 <= sx < width and 0 <= spike_y - sy < height:
                canvas[spike_y - sy][sx] = SPIKE_YELLOW if sy < 2 else SPIKE_DARK
    
    # === WINGS (large dragon wings) ===
    wing_base_y = body_y - 14
    
    # Left wing
    for wy in range(16):
        wing_span = 12 + wy // 2
        for wx in range(wing_span):
            wing_x = center_x - 10 - wx
            wing_y = wing_base_y - wy // 2
            if 0 <= wing_x < width and 0 <= wing_y < height:
                # Wing membrane
                if wy % 3 == 0 or wx % 4 == 0:
                    canvas[wing_y][wing_x] = WING_DARK
                else:
                    canvas[wing_y][wing_x] = WING_MEMBRANE
    
    # Left wing bones/fingers
    for finger in range(3):
        for wy in range(12):
            bone_x = center_x - 12 - finger * 6 - wy // 2
            bone_y = wing_base_y - 2 - wy // 2 - finger * 2
            if 0 <= bone_x < width and 0 <= bone_y < height:
                canvas[bone_y][bone_x] = WING_BONE
    
    # Right wing
    for wy in range(14):
        wing_span = 10 + wy // 2
        for wx in range(wing_span):
            wing_x = center_x + 10 + wx
            wing_y = wing_base_y - wy // 2 + 2
            if 0 <= wing_x < width and 0 <= wing_y < height:
                if wy % 3 == 0 or wx % 4 == 0:
                    canvas[wing_y][wing_x] = WING_DARK
                else:
                    canvas[wing_y][wing_x] = WING_MEMBRANE
    
    # Right wing bones
    for finger in range(3):
        for wy in range(10):
            bone_x = center_x + 12 + finger * 5 + wy // 2
            bone_y = wing_base_y - wy // 2 - finger * 2 + 2
            if 0 <= bone_x < width and 0 <= bone_y < height:
                canvas[bone_y][bone_x] = WING_BONE
    
    # === FRONT LEGS ===
    front_leg_y = body_y - 16
    
    # Left front leg
    for ly in range(14):
        leg_width = 4 - ly // 8
        for lx in range(-leg_width, leg_width + 1):
            leg_x = center_x - 8 + lx
            leg_y = front_leg_y + ly
            if 0 <= leg_x < width and 0 <= leg_y < height:
                canvas[leg_y][leg_x] = FUR_ORANGE if lx >= 0 else FUR_DARK
    
    # Right front leg
    for ly in range(14):
        leg_width = 4 - ly // 8
        for lx in range(-leg_width, leg_width + 1):
            leg_x = center_x + 8 + lx
            leg_y = front_leg_y + ly
            if 0 <= leg_x < width and 0 <= leg_y < height:
                canvas[leg_y][leg_x] = FUR_LIGHT if lx >= 0 else FUR_ORANGE
    
    # Front paws with claws
    for paw_offset in [-8, 8]:
        for py in range(4):
            for px in range(-3, 3):
                paw_x = center_x + paw_offset + px
                paw_y = front_leg_y + 14 + py
                if 0 <= paw_x < width and 0 <= paw_y < height:
                    canvas[paw_y][paw_x] = FUR_BROWN if py > 2 else FUR_DARK
        
        # Claws
        for claw in range(3):
            claw_x = center_x + paw_offset + (claw - 1) * 2
            claw_y = front_leg_y + 18
            if 0 <= claw_x < width and 0 <= claw_y < height:
                canvas[claw_y][claw_x] = CLAW_DARK
    
    # === NECK AND SHOULDERS ===
    neck_y = body_y - 18
    for ny in range(6):
        neck_width = 6 - ny // 3
        for nx in range(-neck_width, neck_width + 1):
            neck_x = center_x + nx
            neck_ypos = neck_y - ny
            if 0 <= neck_x < width and 0 <= neck_ypos < height:
                canvas[neck_ypos][neck_x] = FUR_ORANGE if abs(nx) < 3 else FUR_DARK
    
    # === HEAD (human-like face with mane) ===
    head_y = neck_y - 8
    
    # Mane (wild, spiky)
    for my in range(12):
        mane_width = 10 - my // 3
        for mx in range(-mane_width, mane_width + 1):
            # Spiky mane effect
            if (mx + my) % 2 == 0:
                mane_x = center_x + mx
                mane_y = head_y - 6 - my
                if 0 <= mane_x < width and 0 <= mane_y < height:
                    if abs(mx) > mane_width - 2:
                        canvas[mane_y][mane_x] = MANE_DARK
                    elif my < 6:
                        canvas[mane_y][mane_x] = MANE_LIGHT
                    else:
                        canvas[mane_y][mane_x] = MANE_BROWN
    
    # Face (human-like but bestial)
    for fy in range(-6, 8):
        for fx in range(-6, 7):
            if abs(fx) * 1.1 + abs(fy) * 0.9 < 8:
                face_x = center_x + fx
                face_y = head_y + fy
                if 0 <= face_x < width and 0 <= face_y < height:
                    if fx < -2:
                        canvas[face_y][face_x] = SKIN_SHADOW
                    elif fx < 2:
                        canvas[face_y][face_x] = SKIN_TAN
                    else:
                        canvas[face_y][face_x] = SKIN_TAN if abs(fx) < 4 else SKIN_SHADOW
    
    # === EYES (fierce yellow eyes) ===
    eye_y = head_y - 2
    for eye_offset in [-3, 3]:
        for ey in range(-2, 3):
            for ex in range(-2, 3):
                if abs(ex) + abs(ey) < 3:
                    eye_x = center_x + eye_offset + ex
                    eye_ypos = eye_y + ey
                    if 0 <= eye_x < width and 0 <= eye_ypos < height:
                        canvas[eye_ypos][eye_x] = EYE_YELLOW
        
        # Pupil (vertical slit)
        for py in range(-2, 3):
            pupil_x = center_x + eye_offset
            pupil_y = eye_y + py
            if 0 <= pupil_x < width and 0 <= pupil_y < height:
                canvas[pupil_y][pupil_x] = EYE_PUPIL
    
    # Eyebrows (fierce)
    for brow_x in range(-5, 6):
        brow_y_offset = abs(brow_x) // 3
        brow_y = head_y - 4 + brow_y_offset
        brow_x_pos = center_x + brow_x
        if 0 <= brow_x_pos < width and 0 <= brow_y < height:
            canvas[brow_y][brow_x_pos] = MANE_DARK
    
    # === NOSE ===
    nose_y = head_y + 2
    for ny in range(3):
        for nx in range(-2, 3):
            if abs(nx) + ny < 3:
                nose_x = center_x + nx
                nose_ypos = nose_y + ny
                if 0 <= nose_x < width and 0 <= nose_ypos < height:
                    canvas[nose_ypos][nose_x] = SKIN_SHADOW
    
    # === MOUTH (snarling with teeth) ===
    mouth_y = head_y + 5
    for my in range(4):
        mouth_width = 5 - my // 2
        for mx in range(-mouth_width, mouth_width + 1):
            mouth_x = center_x + mx
            mouth_ypos = mouth_y + my
            if 0 <= mouth_x < width and 0 <= mouth_ypos < height:
                if my < 2:
                    canvas[mouth_ypos][mouth_x] = SKIN_SHADOW
                elif my == 2:
                    # Upper teeth
                    if abs(mx) % 2 == 1:
                        canvas[mouth_ypos][mouth_x] = TEETH_WHITE
                    else:
                        canvas[mouth_ypos][mouth_x] = SKIN_SHADOW
                else:
                    # Lower jaw
                    if abs(mx) < 3:
                        canvas[mouth_ypos][mouth_x] = TEETH_YELLOW
                    else:
                        canvas[mouth_ypos][mouth_x] = SKIN_SHADOW
    
    # Fangs (prominent)
    for fang_offset in [-2, 2]:
        for fy in range(2):
            fang_x = center_x + fang_offset
            fang_y = mouth_y + 4 + fy
            if 0 <= fang_x < width and 0 <= fang_y < height:
                canvas[fang_y][fang_x] = TEETH_WHITE
    
    return canvas


def create_manticore_attack():
    """Create the attacking manticore - lunging with tail raised."""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Same color palette
    FUR_ORANGE = [200, 120, 60, 255]
    FUR_LIGHT = [230, 150, 80, 255]
    FUR_DARK = [160, 90, 40, 255]
    FUR_BROWN = [120, 70, 30, 255]
    MANE_BROWN = [140, 80, 40, 255]
    MANE_LIGHT = [170, 100, 50, 255]
    MANE_DARK = [100, 60, 25, 255]
    SKIN_TAN = [220, 180, 140, 255]
    SKIN_SHADOW = [180, 140, 100, 255]
    EYE_YELLOW = [240, 220, 60, 255]
    EYE_PUPIL = [20, 20, 20, 255]
    TEETH_WHITE = [240, 240, 230, 255]
    TEETH_YELLOW = [220, 210, 180, 255]
    WING_MEMBRANE = [180, 100, 60, 255]
    WING_DARK = [140, 70, 40, 255]
    WING_BONE = [160, 140, 120, 255]
    TAIL_ORANGE = [200, 110, 50, 255]
    TAIL_DARK = [150, 80, 35, 255]
    SPIKE_YELLOW = [230, 200, 100, 255]
    SPIKE_DARK = [180, 150, 70, 255]
    CLAW_DARK = [80, 60, 40, 255]
    MOTION_BLUR = [200, 200, 100, 150]
    
    center_x = 32
    base_y = 60
    
    # === BACK LEGS (crouched) ===
    # Left back leg
    for ly in range(12):
        leg_width = 5 - ly // 6
        for lx in range(-leg_width, leg_width + 1):
            leg_x = center_x - 10 + lx
            leg_y = base_y - ly
            if 0 <= leg_x < width and 0 <= leg_y < height:
                canvas[leg_y][leg_x] = FUR_ORANGE if lx >= 0 else FUR_DARK
    
    # Right back leg
    for ly in range(12):
        leg_width = 5 - ly // 6
        for lx in range(-leg_width, leg_width + 1):
            leg_x = center_x + 10 + lx
            leg_y = base_y - ly
            if 0 <= leg_x < width and 0 <= leg_y < height:
                canvas[leg_y][leg_x] = FUR_LIGHT if lx >= 0 else FUR_ORANGE
    
    # Back paws
    for paw_offset in [-10, 10]:
        for py in range(3):
            for px in range(-4, 4):
                paw_x = center_x + paw_offset + px
                paw_y = base_y + py
                if 0 <= paw_x < width and 0 <= paw_y < height:
                    canvas[paw_y][paw_x] = FUR_BROWN if py > 1 else FUR_DARK
    
    # === BODY (lunging forward) ===
    body_y = base_y - 12
    for by in range(18):
        body_width = 14 - by // 6
        for bx in range(-body_width, body_width + 1):
            body_x = center_x + bx
            body_ypos = body_y - by
            if 0 <= body_x < width and 0 <= body_ypos < height:
                if by > 10 and abs(bx) < 6 and (by + bx) % 4 == 0:
                    canvas[body_ypos][body_x] = FUR_BROWN
                elif bx < -8:
                    canvas[body_ypos][body_x] = FUR_DARK
                elif bx < 0:
                    canvas[body_ypos][body_x] = FUR_ORANGE
                elif bx < 8:
                    canvas[body_ypos][body_x] = FUR_LIGHT
                else:
                    canvas[body_ypos][body_x] = FUR_ORANGE
    
    # === TAIL (RAISED HIGH - ready to strike) ===
    tail_start_x = center_x + 12
    tail_start_y = body_y - 10
    
    # Tail base going up
    for ty in range(10):
        tail_width = 4 - ty // 4
        for tx in range(-tail_width, tail_width + 1):
            tail_x = tail_start_x + tx
            tail_y = tail_start_y - ty
            if 0 <= tail_x < width and 0 <= tail_y < height:
                canvas[tail_y][tail_x] = TAIL_ORANGE if tx >= 0 else TAIL_DARK
    
    # Tail curve (arcing forward)
    for ty in range(14):
        tail_curve = -ty // 2
        tail_width = 3 - ty // 6
        for tx in range(-tail_width, tail_width + 1):
            tail_x = tail_start_x + tail_curve + tx
            tail_y = tail_start_y - 10 - ty // 2
            if 0 <= tail_x < width and 0 <= tail_y < height:
                canvas[tail_y][tail_x] = TAIL_ORANGE if tx >= 0 else TAIL_DARK
    
    # Tail stinger bulb (prominent)
    stinger_x = tail_start_x - 7
    stinger_y = tail_start_y - 17
    for sy in range(6):
        for sx in range(-4, 5):
            if abs(sx) * 0.7 + abs(sy - 3) < 4:
                sting_x = stinger_x + sx
                sting_y = stinger_y + sy
                if 0 <= sting_x < width and 0 <= sting_y < height:
                    canvas[sting_y][sting_x] = TAIL_DARK if sy > 3 else TAIL_ORANGE
    
    # Tail spikes (long, deadly)
    for spike_num in range(6):
        spike_base_x = tail_start_x - spike_num
        spike_base_y = tail_start_y - 12 - spike_num
        for sy in range(5):
            spike_x = spike_base_x - sy // 2
            spike_y = spike_base_y - sy
            if 0 <= spike_x < width and 0 <= spike_y < height:
                canvas[spike_y][spike_x] = SPIKE_YELLOW if sy < 3 else SPIKE_DARK
    
    # === WINGS (SPREAD WIDE for intimidation) ===
    wing_base_y = body_y - 14
    
    # Left wing (extended)
    for wy in range(18):
        wing_span = 14 + wy // 2
        for wx in range(wing_span):
            wing_x = center_x - 8 - wx
            wing_y = wing_base_y - wy // 2
            if 0 <= wing_x < width and 0 <= wing_y < height:
                if wy % 3 == 0 or wx % 4 == 0:
                    canvas[wing_y][wing_x] = WING_DARK
                else:
                    canvas[wing_y][wing_x] = WING_MEMBRANE
    
    # Left wing bones
    for finger in range(4):
        for wy in range(14):
            bone_x = center_x - 10 - finger * 5 - wy // 2
            bone_y = wing_base_y - wy // 2 - finger * 3
            if 0 <= bone_x < width and 0 <= bone_y < height:
                canvas[bone_y][bone_x] = WING_BONE
    
    # Right wing (extended)
    for wy in range(16):
        wing_span = 12 + wy // 2
        for wx in range(wing_span):
            wing_x = center_x + 8 + wx
            wing_y = wing_base_y - wy // 2 + 2
            if 0 <= wing_x < width and 0 <= wing_y < height:
                if wy % 3 == 0 or wx % 4 == 0:
                    canvas[wing_y][wing_x] = WING_DARK
                else:
                    canvas[wing_y][wing_x] = WING_MEMBRANE
    
    # Right wing bones
    for finger in range(3):
        for wy in range(12):
            bone_x = center_x + 10 + finger * 6 + wy // 2
            bone_y = wing_base_y - wy // 2 - finger * 2 + 2
            if 0 <= bone_x < width and 0 <= bone_y < height:
                canvas[bone_y][bone_x] = WING_BONE
    
    # === FRONT LEGS (reaching/clawing) ===
    front_leg_y = body_y - 16
    
    # Left front leg (extended forward)
    for ly in range(16):
        leg_width = 4 - ly // 9
        leg_forward = ly // 2
        for lx in range(-leg_width, leg_width + 1):
            leg_x = center_x - 10 - leg_forward + lx
            leg_y = front_leg_y + ly - 2
            if 0 <= leg_x < width and 0 <= leg_y < height:
                canvas[leg_y][leg_x] = FUR_ORANGE if lx >= 0 else FUR_DARK
    
    # Right front leg
    for ly in range(14):
        leg_width = 4 - ly // 8
        for lx in range(-leg_width, leg_width + 1):
            leg_x = center_x + 6 + lx
            leg_y = front_leg_y + ly
            if 0 <= leg_x < width and 0 <= leg_y < height:
                canvas[leg_y][leg_x] = FUR_LIGHT if lx >= 0 else FUR_ORANGE
    
    # Front paws with extended claws
    for paw_offset, paw_y_offset in [(-18, -2), (6, 0)]:
        for py in range(4):
            for px in range(-3, 3):
                paw_x = center_x + paw_offset + px
                paw_y = front_leg_y + 14 + py + paw_y_offset
                if 0 <= paw_x < width and 0 <= paw_y < height:
                    canvas[paw_y][paw_x] = FUR_BROWN if py > 2 else FUR_DARK
        
        # Long claws
        for claw in range(3):
            for cy in range(3):
                claw_x = center_x + paw_offset + (claw - 1) * 2
                claw_y = front_leg_y + 18 + cy + paw_y_offset
                if 0 <= claw_x < width and 0 <= claw_y < height:
                    canvas[claw_y][claw_x] = CLAW_DARK
    
    # === NECK ===
    neck_y = body_y - 18
    for ny in range(6):
        neck_width = 6 - ny // 3
        for nx in range(-neck_width, neck_width + 1):
            neck_x = center_x + nx
            neck_ypos = neck_y - ny
            if 0 <= neck_x < width and 0 <= neck_ypos < height:
                canvas[neck_ypos][neck_x] = FUR_ORANGE if abs(nx) < 3 else FUR_DARK
    
    # === HEAD (ROARING) ===
    head_y = neck_y - 8
    
    # Mane (wild, bristling)
    for my in range(14):
        mane_width = 11 - my // 3
        for mx in range(-mane_width, mane_width + 1):
            if (mx + my) % 2 == 0:
                mane_x = center_x + mx
                mane_y = head_y - 6 - my
                if 0 <= mane_x < width and 0 <= mane_y < height:
                    if abs(mx) > mane_width - 2:
                        canvas[mane_y][mane_x] = MANE_DARK
                    elif my < 7:
                        canvas[mane_y][mane_x] = MANE_LIGHT
                    else:
                        canvas[mane_y][mane_x] = MANE_BROWN
    
    # Face
    for fy in range(-6, 8):
        for fx in range(-6, 7):
            if abs(fx) * 1.1 + abs(fy) * 0.9 < 8:
                face_x = center_x + fx
                face_y = head_y + fy
                if 0 <= face_x < width and 0 <= face_y < height:
                    if fx < -2:
                        canvas[face_y][face_x] = SKIN_SHADOW
                    elif fx < 2:
                        canvas[face_y][face_x] = SKIN_TAN
                    else:
                        canvas[face_y][face_x] = SKIN_TAN if abs(fx) < 4 else SKIN_SHADOW
    
    # === EYES (WIDE WITH RAGE) ===
    eye_y = head_y - 2
    for eye_offset in [-3, 3]:
        for ey in range(-3, 4):
            for ex in range(-2, 3):
                if abs(ex) + abs(ey) < 4:
                    eye_x = center_x + eye_offset + ex
                    eye_ypos = eye_y + ey
                    if 0 <= eye_x < width and 0 <= eye_ypos < height:
                        canvas[eye_ypos][eye_x] = EYE_YELLOW
        
        # Dilated pupil
        for py in range(-2, 3):
            pupil_x = center_x + eye_offset
            pupil_y = eye_y + py
            if 0 <= pupil_x < width and 0 <= pupil_y < height:
                canvas[pupil_y][pupil_x] = EYE_PUPIL
    
    # Fierce eyebrows
    for brow_x in range(-5, 6):
        brow_y_offset = abs(brow_x) // 3
        brow_y = head_y - 5 + brow_y_offset
        brow_x_pos = center_x + brow_x
        if 0 <= brow_x_pos < width and 0 <= brow_y < height:
            canvas[brow_y][brow_x_pos] = MANE_DARK
    
    # === NOSE ===
    nose_y = head_y + 2
    for ny in range(3):
        for nx in range(-2, 3):
            if abs(nx) + ny < 3:
                nose_x = center_x + nx
                nose_ypos = nose_y + ny
                if 0 <= nose_x < width and 0 <= nose_ypos < height:
                    canvas[nose_ypos][nose_x] = SKIN_SHADOW
    
    # === MOUTH (OPEN ROAR) ===
    mouth_y = head_y + 5
    for my in range(6):
        mouth_width = 6 - my // 2
        for mx in range(-mouth_width, mouth_width + 1):
            mouth_x = center_x + mx
            mouth_ypos = mouth_y + my
            if 0 <= mouth_x < width and 0 <= mouth_ypos < height:
                if my < 2:
                    canvas[mouth_ypos][mouth_x] = SKIN_SHADOW
                elif my < 4:
                    # Upper teeth row
                    if abs(mx) % 2 == 1 and abs(mx) < 5:
                        canvas[mouth_ypos][mouth_x] = TEETH_WHITE
                    else:
                        canvas[mouth_ypos][mouth_x] = SKIN_SHADOW
                else:
                    # Lower jaw with teeth
                    if abs(mx) < 4 and mx % 2 == 0:
                        canvas[mouth_ypos][mouth_x] = TEETH_YELLOW
                    else:
                        canvas[mouth_ypos][mouth_x] = SKIN_SHADOW
    
    # Large fangs
    for fang_offset in [-3, 3]:
        for fy in range(3):
            fang_x = center_x + fang_offset
            fang_y = mouth_y + 4 + fy
            if 0 <= fang_x < width and 0 <= fang_y < height:
                canvas[fang_y][fang_x] = TEETH_WHITE
    
    # === MOTION EFFECTS ===
    # Tail strike motion blur
    for blur in range(6):
        blur_x = stinger_x + 5 + blur
        blur_y = stinger_y + blur // 2
        if 0 <= blur_x < width and 0 <= blur_y < height:
            canvas[blur_y][blur_x] = MOTION_BLUR
    
    return canvas


def main():
    print("Creating manticore monster images...")
    
    manticore_default = create_manticore_default()
    manticore_attack = create_manticore_attack()
    
    # Convert to PIL and scale up
    scale = 4
    
    # Default pose
    img_default = Image.fromarray(manticore_default, 'RGBA')
    img_default_scaled = img_default.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_default_scaled.save('art/manticore_monster.png')
    print(f"✓ Saved: art/manticore_monster.png ({64 * scale}x{64 * scale})")
    
    # Attack animation
    img_attack = Image.fromarray(manticore_attack, 'RGBA')
    img_attack_scaled = img_attack.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_attack_scaled.save('art/manticore_monster_attack.png')
    print(f"✓ Saved: art/manticore_monster_attack.png ({64 * scale}x{64 * scale})")
    
    print("\n✅ Manticore monster creation complete!")
    print("\nFeatures:")
    print("- Default: Aggressive stance with human face, lion body, dragon wings, scorpion tail")
    print("- Attack: Lunging pose with raised tail, spread wings, and roaring mouth")
    print("\nStyle: Mythological manticore with detailed features")
    print("Colors: Orange/brown fur, tan skin, brown mane, yellow spikes on tail")


if __name__ == '__main__':
    main()
