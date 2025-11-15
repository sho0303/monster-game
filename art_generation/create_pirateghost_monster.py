"""
PirateGhost Monster Creator
Creates pixel art for a spectral pirate ghost - translucent green ghost with pirate hat, beard, hook hand.
Inspired by the ghostly pirate with skull and crossbones hat and ethereal appearance.

Resolution: 64x64 pixels (scaled 4x to 256x256)
Style: Pixel art with ghostly translucent effects
Palette: Green/cyan ghost colors, dark outlines, glowing elements
"""

from PIL import Image
import numpy as np


def create_pirateghost_default():
    """Create the default floating pirate ghost pose."""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette - inspired by the ghost pirate image
    GHOST_GREEN = [120, 220, 180, 255]      # Main ghost green
    GHOST_LIGHT = [160, 240, 210, 255]      # Light ghost highlights
    GHOST_CYAN = [100, 200, 200, 255]       # Cyan tint
    GHOST_DARK = [80, 160, 140, 255]        # Dark ghost shadows
    GHOST_TRANS = [120, 220, 180, 180]      # Semi-transparent ghost
    OUTLINE_DARK = [40, 20, 80, 255]        # Dark purple outline
    HAT_DARK = [50, 30, 90, 255]            # Dark pirate hat
    HAT_SHADOW = [35, 20, 65, 255]          # Hat shadow
    SKULL_CYAN = [140, 230, 220, 255]       # Skull emblem
    BEARD_GREEN = [100, 190, 170, 255]      # Beard color
    BEARD_LIGHT = [130, 210, 190, 255]      # Light beard
    EYE_GLOW = [200, 255, 240, 255]         # Glowing eyes
    EYE_DARK = [30, 15, 60, 255]            # Eye socket
    HOOK_METAL = [100, 180, 190, 255]       # Hook metal
    HOOK_DARK = [70, 140, 150, 255]         # Hook shadow
    GLOW_BRIGHT = [180, 255, 230, 200]      # Bright glow effect
    
    center_x = 32
    base_y = 58
    
    # === GHOSTLY TAIL (wispy bottom) ===
    tail_y = base_y
    for ty in range(12):
        tail_width = 8 - ty // 2
        wave = int(np.sin(ty * 0.5) * 2)
        for tx in range(-tail_width, tail_width + 1):
            tail_x = center_x + tx + wave
            tail_ypos = tail_y - ty
            if 0 <= tail_x < width and 0 <= tail_ypos < height:
                # Wispy, fading effect
                if abs(tx) > tail_width - 2:
                    canvas[tail_ypos][tail_x] = GHOST_TRANS
                elif ty > 8:
                    canvas[tail_ypos][tail_x] = GHOST_TRANS
                elif tx < 0:
                    canvas[tail_ypos][tail_x] = GHOST_DARK
                else:
                    canvas[tail_ypos][tail_x] = GHOST_GREEN
    
    # === LOWER BODY (ghostly torso fading down) ===
    torso_y = base_y - 12
    for ty in range(16):
        torso_width = 11 - ty // 8
        for tx in range(-torso_width, torso_width + 1):
            torso_x = center_x + tx
            torso_ypos = torso_y - ty
            if 0 <= torso_x < width and 0 <= torso_ypos < height:
                # Ghostly body with shading
                if abs(tx) > torso_width - 2:
                    canvas[torso_ypos][torso_x] = GHOST_TRANS
                elif tx < -6:
                    canvas[torso_ypos][torso_x] = GHOST_DARK
                elif tx < -2:
                    canvas[torso_ypos][torso_x] = GHOST_GREEN
                elif tx < 2:
                    canvas[torso_ypos][torso_x] = GHOST_LIGHT
                elif tx < 6:
                    canvas[torso_ypos][torso_x] = GHOST_CYAN
                else:
                    canvas[torso_ypos][torso_x] = GHOST_DARK
    
    # === PIRATE COAT DETAILS (dark lines on torso) ===
    coat_y = torso_y - 8
    # Coat buttons/line
    for cy in range(10):
        coat_x = center_x
        coat_ypos = coat_y + cy
        if 0 <= coat_x < width and 0 <= coat_ypos < height:
            canvas[coat_ypos][coat_x] = OUTLINE_DARK
    
    # Coat lapels
    for cy in range(8):
        for lapel_offset in [-4, 4]:
            lapel_x = center_x + lapel_offset
            lapel_y = coat_y + cy
            if 0 <= lapel_x < width and 0 <= lapel_y < height:
                canvas[lapel_y][lapel_x] = OUTLINE_DARK
    
    # === ARMS (ghostly, one with hook) ===
    arm_y = torso_y - 14
    
    # Left arm (regular ghost arm)
    for ay in range(14):
        arm_width = 4 - ay // 8
        arm_out = ay // 3
        for ax in range(-arm_width, arm_width + 1):
            arm_x = center_x - 10 - arm_out + ax
            arm_ypos = arm_y + ay
            if 0 <= arm_x < width and 0 <= arm_ypos < height:
                if abs(ax) > arm_width - 1:
                    canvas[arm_ypos][arm_x] = GHOST_TRANS
                elif ax < 0:
                    canvas[arm_ypos][arm_x] = GHOST_DARK
                else:
                    canvas[arm_ypos][arm_x] = GHOST_GREEN
    
    # Left hand (ghostly)
    left_hand_x = center_x - 14
    left_hand_y = arm_y + 14
    for hy in range(5):
        for hx in range(-3, 4):
            hand_x = left_hand_x + hx
            hand_y = left_hand_y + hy
            if 0 <= hand_x < width and 0 <= hand_y < height and abs(hx) + hy < 6:
                canvas[hand_y][hand_x] = GHOST_CYAN if hx < 0 else GHOST_LIGHT
    
    # Fingers
    for finger in range(3):
        for fy in range(3):
            finger_x = left_hand_x + (finger - 1) * 2
            finger_y = left_hand_y + 5 + fy
            if 0 <= finger_x < width and 0 <= finger_y < height:
                canvas[finger_y][finger_x] = GHOST_GREEN
    
    # Right arm (with hook)
    for ay in range(14):
        arm_width = 4 - ay // 8
        arm_out = ay // 3
        for ax in range(-arm_width, arm_width + 1):
            arm_x = center_x + 10 + arm_out + ax
            arm_ypos = arm_y + ay
            if 0 <= arm_x < width and 0 <= arm_ypos < height:
                if abs(ax) > arm_width - 1:
                    canvas[arm_ypos][arm_x] = GHOST_TRANS
                elif ax < 0:
                    canvas[arm_ypos][arm_x] = GHOST_GREEN
                else:
                    canvas[arm_ypos][arm_x] = GHOST_CYAN
    
    # Hook hand
    hook_base_x = center_x + 14
    hook_base_y = arm_y + 14
    
    # Hook base (stump)
    for hy in range(4):
        for hx in range(-3, 4):
            base_x = hook_base_x + hx
            base_y = hook_base_y + hy
            if 0 <= base_x < width and 0 <= base_y < height and abs(hx) + hy < 5:
                canvas[base_y][base_x] = GHOST_CYAN
    
    # Hook (curved metal)
    for hy in range(8):
        hook_curve = hy // 2
        for hx in range(2):
            hook_x = hook_base_x + hx - hook_curve
            hook_y = hook_base_y + 4 + hy
            if 0 <= hook_x < width and 0 <= hook_y < height:
                canvas[hook_y][hook_x] = HOOK_METAL if hx == 0 else HOOK_DARK
    
    # Hook point
    for hp in range(4):
        point_x = hook_base_x - 4 + hp
        point_y = hook_base_y + 12 - hp
        if 0 <= point_x < width and 0 <= point_y < height:
            canvas[point_y][point_x] = HOOK_METAL
    
    # === SHOULDERS ===
    shoulder_y = torso_y - 16
    for sy in range(4):
        for sx in range(-12, 13):
            shoulder_x = center_x + sx
            shoulder_ypos = shoulder_y - sy
            if 0 <= shoulder_x < width and 0 <= shoulder_ypos < height:
                if abs(sx) > 10:
                    canvas[shoulder_ypos][shoulder_x] = GHOST_TRANS
                elif abs(sx) > 6:
                    canvas[shoulder_ypos][shoulder_x] = GHOST_DARK
                else:
                    canvas[shoulder_ypos][shoulder_x] = GHOST_GREEN
    
    # === NECK ===
    neck_y = shoulder_y - 4
    for ny in range(4):
        neck_width = 4 - ny // 2
        for nx in range(-neck_width, neck_width + 1):
            neck_x = center_x + nx
            neck_ypos = neck_y - ny
            if 0 <= neck_x < width and 0 <= neck_ypos < height:
                canvas[neck_ypos][neck_x] = GHOST_CYAN if abs(nx) < 2 else GHOST_DARK
    
    # === HEAD (ghostly skull-like face) ===
    head_y = neck_y - 6
    
    # Head shape
    for hy in range(12):
        head_width = 7 - hy // 5
        for hx in range(-head_width, head_width + 1):
            if abs(hx) * 1.2 + abs(hy - 6) * 0.8 < 8:
                head_x = center_x + hx
                head_ypos = head_y - hy
                if 0 <= head_x < width and 0 <= head_ypos < height:
                    # Ghostly face coloring
                    if abs(hx) > 5:
                        canvas[head_ypos][head_x] = GHOST_TRANS
                    elif hx < -3:
                        canvas[head_ypos][head_x] = GHOST_DARK
                    elif hx < 0:
                        canvas[head_ypos][head_x] = GHOST_GREEN
                    elif hx < 3:
                        canvas[head_ypos][head_x] = GHOST_LIGHT
                    else:
                        canvas[head_ypos][head_x] = GHOST_CYAN
    
    # === BEARD (long ghostly beard) ===
    beard_y = head_y + 6
    for by in range(10):
        beard_width = 5 + by // 3
        wave = int(np.sin(by * 0.7) * 1.5)
        for bx in range(-beard_width, beard_width + 1):
            # Wispy beard strands
            if (bx + by) % 2 == 0:
                beard_x = center_x + bx + wave
                beard_ypos = beard_y + by
                if 0 <= beard_x < width and 0 <= beard_ypos < height:
                    if abs(bx) > beard_width - 2:
                        canvas[beard_ypos][beard_x] = GHOST_TRANS
                    elif bx < -2:
                        canvas[beard_ypos][beard_x] = BEARD_GREEN
                    elif bx < 2:
                        canvas[beard_ypos][beard_x] = BEARD_LIGHT
                    else:
                        canvas[beard_ypos][beard_x] = BEARD_GREEN
    
    # === EYES (glowing sockets) ===
    eye_y = head_y - 3
    for eye_offset in [-3, 3]:
        # Eye socket (dark)
        for ey in range(-2, 3):
            for ex in range(-2, 3):
                if abs(ex) + abs(ey) < 3:
                    eye_x = center_x + eye_offset + ex
                    eye_ypos = eye_y + ey
                    if 0 <= eye_x < width and 0 <= eye_ypos < height:
                        canvas[eye_ypos][eye_x] = EYE_DARK
        
        # Glowing eye
        for ey in range(-1, 2):
            eye_x = center_x + eye_offset
            eye_ypos = eye_y + ey
            if 0 <= eye_x < width and 0 <= eye_ypos < height:
                canvas[eye_ypos][eye_x] = EYE_GLOW
        
        # Eye glow effect
        for ey in range(-2, 3):
            for ex in range(-2, 3):
                if abs(ex) + abs(ey) == 3:
                    glow_x = center_x + eye_offset + ex
                    glow_y = eye_y + ey
                    if 0 <= glow_x < width and 0 <= glow_y < height:
                        canvas[glow_y][glow_x] = GLOW_BRIGHT
    
    # === NOSE (small ghost nose) ===
    nose_y = head_y + 1
    for ny in range(2):
        nose_x = center_x
        nose_ypos = nose_y + ny
        if 0 <= nose_x < width and 0 <= nose_ypos < height:
            canvas[nose_ypos][nose_x] = GHOST_DARK
    
    # === MOUTH (grinning) ===
    mouth_y = head_y + 3
    for mx in range(-4, 5):
        mouth_curve = abs(mx) // 2
        mouth_x = center_x + mx
        mouth_ypos = mouth_y + mouth_curve
        if 0 <= mouth_x < width and 0 <= mouth_ypos < height:
            canvas[mouth_ypos][mouth_x] = OUTLINE_DARK
    
    # === PIRATE HAT (large tricorn with skull) ===
    hat_y = head_y - 12
    
    # Hat brim (wide)
    for brim_y in range(3):
        brim_width = 16 - brim_y * 2
        for bx in range(-brim_width, brim_width + 1):
            # Curved brim shape
            brim_curve = abs(bx) // 6
            brim_x = center_x + bx
            brim_ypos = hat_y + brim_y + brim_curve
            if 0 <= brim_x < width and 0 <= brim_ypos < height:
                if abs(bx) > brim_width - 2:
                    canvas[brim_ypos][brim_x] = HAT_SHADOW
                else:
                    canvas[brim_ypos][brim_x] = HAT_DARK
    
    # Hat crown (tall pointed)
    for hy in range(8):
        hat_width = 10 - hy
        for hx in range(-hat_width, hat_width + 1):
            hat_x = center_x + hx
            hat_ypos = hat_y - hy
            if 0 <= hat_x < width and 0 <= hat_ypos < height:
                if abs(hx) > hat_width - 2:
                    canvas[hat_ypos][hat_x] = HAT_SHADOW
                elif hx < 0:
                    canvas[hat_ypos][hat_x] = HAT_DARK
                else:
                    canvas[hat_ypos][hat_x] = HAT_SHADOW
    
    # === SKULL AND CROSSBONES EMBLEM ===
    emblem_y = hat_y - 2
    
    # Skull (small)
    for sy in range(4):
        skull_width = 3 - sy // 2
        for sx in range(-skull_width, skull_width + 1):
            skull_x = center_x + sx
            skull_ypos = emblem_y - sy
            if 0 <= skull_x < width and 0 <= skull_ypos < height:
                canvas[skull_ypos][skull_x] = SKULL_CYAN
    
    # Skull eyes
    for eye_offset in [-1, 1]:
        skull_eye_x = center_x + eye_offset
        skull_eye_y = emblem_y - 2
        if 0 <= skull_eye_x < width and 0 <= skull_eye_y < height:
            canvas[skull_eye_y][skull_eye_x] = OUTLINE_DARK
    
    # Crossbones (behind skull)
    for bone_angle in [-1, 1]:
        for bx in range(6):
            bone_x = center_x + (bx - 3) + bone_angle
            bone_y = emblem_y + 1 - bone_angle * (bx - 3) // 2
            if 0 <= bone_x < width and 0 <= bone_y < height:
                canvas[bone_y][bone_x] = SKULL_CYAN
    
    return canvas


def create_pirateghost_attack():
    """Create the attacking pirate ghost - lunging forward with hook raised."""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Same color palette
    GHOST_GREEN = [120, 220, 180, 255]
    GHOST_LIGHT = [160, 240, 210, 255]
    GHOST_CYAN = [100, 200, 200, 255]
    GHOST_DARK = [80, 160, 140, 255]
    GHOST_TRANS = [120, 220, 180, 180]
    OUTLINE_DARK = [40, 20, 80, 255]
    HAT_DARK = [50, 30, 90, 255]
    HAT_SHADOW = [35, 20, 65, 255]
    SKULL_CYAN = [140, 230, 220, 255]
    BEARD_GREEN = [100, 190, 170, 255]
    BEARD_LIGHT = [130, 210, 190, 255]
    EYE_GLOW = [200, 255, 240, 255]
    EYE_DARK = [30, 15, 60, 255]
    HOOK_METAL = [100, 180, 190, 255]
    HOOK_DARK = [70, 140, 150, 255]
    GLOW_BRIGHT = [180, 255, 230, 200]
    MOTION_GLOW = [120, 220, 180, 120]
    
    center_x = 30  # Shifted for lunging pose
    base_y = 58
    
    # === GHOSTLY TAIL (more agitated) ===
    tail_y = base_y
    for ty in range(10):
        tail_width = 7 - ty // 2
        wave = int(np.sin(ty * 0.8) * 3)
        for tx in range(-tail_width, tail_width + 1):
            tail_x = center_x + tx + wave
            tail_ypos = tail_y - ty
            if 0 <= tail_x < width and 0 <= tail_ypos < height:
                if abs(tx) > tail_width - 2:
                    canvas[tail_ypos][tail_x] = GHOST_TRANS
                elif ty > 7:
                    canvas[tail_ypos][tail_x] = GHOST_TRANS
                elif tx < 0:
                    canvas[tail_ypos][tail_x] = GHOST_DARK
                else:
                    canvas[tail_ypos][tail_x] = GHOST_GREEN
    
    # === LOWER BODY (leaning forward) ===
    torso_y = base_y - 10
    for ty in range(16):
        torso_width = 11 - ty // 8
        torso_lean = ty // 4
        for tx in range(-torso_width, torso_width + 1):
            torso_x = center_x + tx - torso_lean
            torso_ypos = torso_y - ty
            if 0 <= torso_x < width and 0 <= torso_ypos < height:
                if abs(tx) > torso_width - 2:
                    canvas[torso_ypos][torso_x] = GHOST_TRANS
                elif tx < -6:
                    canvas[torso_ypos][torso_x] = GHOST_DARK
                elif tx < -2:
                    canvas[torso_ypos][torso_x] = GHOST_GREEN
                elif tx < 2:
                    canvas[torso_ypos][torso_x] = GHOST_LIGHT
                elif tx < 6:
                    canvas[torso_ypos][torso_x] = GHOST_CYAN
                else:
                    canvas[torso_ypos][torso_x] = GHOST_DARK
    
    # Coat details
    coat_y = torso_y - 8
    for cy in range(10):
        coat_x = center_x - cy // 4
        coat_ypos = coat_y + cy
        if 0 <= coat_x < width and 0 <= coat_ypos < height:
            canvas[coat_ypos][coat_x] = OUTLINE_DARK
    
    for cy in range(8):
        for lapel_offset in [-4, 4]:
            lapel_x = center_x + lapel_offset - cy // 4
            lapel_y = coat_y + cy
            if 0 <= lapel_x < width and 0 <= lapel_y < height:
                canvas[lapel_y][lapel_x] = OUTLINE_DARK
    
    # === ARMS (aggressive pose) ===
    arm_y = torso_y - 14
    
    # Left arm (reaching forward)
    for ay in range(16):
        arm_width = 4 - ay // 9
        arm_forward = ay // 2
        for ax in range(-arm_width, arm_width + 1):
            arm_x = center_x - 12 - arm_forward + ax
            arm_ypos = arm_y + ay - 3
            if 0 <= arm_x < width and 0 <= arm_ypos < height:
                if abs(ax) > arm_width - 1:
                    canvas[arm_ypos][arm_x] = GHOST_TRANS
                elif ax < 0:
                    canvas[arm_ypos][arm_x] = GHOST_DARK
                else:
                    canvas[arm_ypos][arm_x] = GHOST_GREEN
    
    # Left hand (grasping)
    left_hand_x = center_x - 20
    left_hand_y = arm_y + 10
    for hy in range(6):
        for hx in range(-3, 4):
            hand_x = left_hand_x + hx
            hand_y = left_hand_y + hy
            if 0 <= hand_x < width and 0 <= hand_y < height and abs(hx) + hy < 7:
                canvas[hand_y][hand_x] = GHOST_CYAN if hx < 0 else GHOST_LIGHT
    
    # Fingers (clawing)
    for finger in range(4):
        finger_spread = (finger - 1.5) * 0.5
        for fy in range(4):
            finger_x = left_hand_x + (finger - 1.5) * 2 + int(fy * finger_spread)
            finger_y = left_hand_y + 6 + fy
            if 0 <= finger_x < width and 0 <= finger_y < height:
                canvas[int(finger_y)][int(finger_x)] = GHOST_GREEN
    
    # Right arm (HOOK RAISED for attack)
    for ay in range(18):
        arm_width = 4 - ay // 10
        arm_up = ay // 3
        for ax in range(-arm_width, arm_width + 1):
            arm_x = center_x + 8 + ax
            arm_ypos = arm_y - arm_up + ay // 2
            if 0 <= arm_x < width and 0 <= arm_ypos < height:
                if abs(ax) > arm_width - 1:
                    canvas[arm_ypos][arm_x] = GHOST_TRANS
                elif ax < 0:
                    canvas[arm_ypos][arm_x] = GHOST_GREEN
                else:
                    canvas[arm_ypos][arm_x] = GHOST_CYAN
    
    # Hook hand (raised high)
    hook_base_x = center_x + 8
    hook_base_y = arm_y - 6
    
    # Hook base
    for hy in range(5):
        for hx in range(-3, 4):
            base_x = hook_base_x + hx
            base_y = hook_base_y + hy
            if 0 <= base_x < width and 0 <= base_y < height and abs(hx) + hy < 6:
                canvas[base_y][base_x] = GHOST_CYAN
    
    # Hook (menacing)
    for hy in range(10):
        hook_curve = hy // 2
        for hx in range(2):
            hook_x = hook_base_x + hx - hook_curve
            hook_y = hook_base_y + 5 + hy
            if 0 <= hook_x < width and 0 <= hook_y < height:
                canvas[hook_y][hook_x] = HOOK_METAL if hx == 0 else HOOK_DARK
    
    # Hook point (sharp)
    for hp in range(5):
        point_x = hook_base_x - 5 + hp
        point_y = hook_base_y + 15 - hp
        if 0 <= point_x < width and 0 <= point_y < height:
            canvas[point_y][point_x] = HOOK_METAL
    
    # === SHOULDERS ===
    shoulder_y = torso_y - 16
    for sy in range(4):
        for sx in range(-12, 13):
            shoulder_x = center_x + sx - 2
            shoulder_ypos = shoulder_y - sy
            if 0 <= shoulder_x < width and 0 <= shoulder_ypos < height:
                if abs(sx) > 10:
                    canvas[shoulder_ypos][shoulder_x] = GHOST_TRANS
                elif abs(sx) > 6:
                    canvas[shoulder_ypos][shoulder_x] = GHOST_DARK
                else:
                    canvas[shoulder_ypos][shoulder_x] = GHOST_GREEN
    
    # === NECK ===
    neck_y = shoulder_y - 4
    for ny in range(4):
        neck_width = 4 - ny // 2
        for nx in range(-neck_width, neck_width + 1):
            neck_x = center_x + nx - 2
            neck_ypos = neck_y - ny
            if 0 <= neck_x < width and 0 <= neck_ypos < height:
                canvas[neck_ypos][neck_x] = GHOST_CYAN if abs(nx) < 2 else GHOST_DARK
    
    # === HEAD (aggressive angle) ===
    head_y = neck_y - 6
    
    for hy in range(12):
        head_width = 7 - hy // 5
        for hx in range(-head_width, head_width + 1):
            if abs(hx) * 1.2 + abs(hy - 6) * 0.8 < 8:
                head_x = center_x + hx - 2
                head_ypos = head_y - hy
                if 0 <= head_x < width and 0 <= head_ypos < height:
                    if abs(hx) > 5:
                        canvas[head_ypos][head_x] = GHOST_TRANS
                    elif hx < -3:
                        canvas[head_ypos][head_x] = GHOST_DARK
                    elif hx < 0:
                        canvas[head_ypos][head_x] = GHOST_GREEN
                    elif hx < 3:
                        canvas[head_ypos][head_x] = GHOST_LIGHT
                    else:
                        canvas[head_ypos][head_x] = GHOST_CYAN
    
    # === BEARD (flowing with movement) ===
    beard_y = head_y + 6
    for by in range(11):
        beard_width = 5 + by // 3
        wave = int(np.sin(by * 0.8) * 2) - 2  # Flowing left
        for bx in range(-beard_width, beard_width + 1):
            if (bx + by) % 2 == 0:
                beard_x = center_x + bx + wave - 2
                beard_ypos = beard_y + by
                if 0 <= beard_x < width and 0 <= beard_ypos < height:
                    if abs(bx) > beard_width - 2:
                        canvas[beard_ypos][beard_x] = GHOST_TRANS
                    elif bx < -2:
                        canvas[beard_ypos][beard_x] = BEARD_GREEN
                    elif bx < 2:
                        canvas[beard_ypos][beard_x] = BEARD_LIGHT
                    else:
                        canvas[beard_ypos][beard_x] = BEARD_GREEN
    
    # === EYES (WIDE, intense) ===
    eye_y = head_y - 3
    for eye_offset in [-3, 3]:
        # Eye socket
        for ey in range(-3, 4):
            for ex in range(-2, 3):
                if abs(ex) + abs(ey) < 4:
                    eye_x = center_x + eye_offset + ex - 2
                    eye_ypos = eye_y + ey
                    if 0 <= eye_x < width and 0 <= eye_ypos < height:
                        canvas[eye_ypos][eye_x] = EYE_DARK
        
        # Glowing eye (larger)
        for ey in range(-2, 3):
            for ex in range(-1, 2):
                if abs(ex) + abs(ey) < 3:
                    eye_x = center_x + eye_offset + ex - 2
                    eye_ypos = eye_y + ey
                    if 0 <= eye_x < width and 0 <= eye_ypos < height:
                        canvas[eye_ypos][eye_x] = EYE_GLOW
        
        # Bright glow
        for ey in range(-3, 4):
            for ex in range(-3, 4):
                if abs(ex) + abs(ey) == 4 or abs(ex) + abs(ey) == 3:
                    glow_x = center_x + eye_offset + ex - 2
                    glow_y = eye_y + ey
                    if 0 <= glow_x < width and 0 <= glow_y < height:
                        canvas[glow_y][glow_x] = GLOW_BRIGHT
    
    # === NOSE ===
    nose_y = head_y + 1
    for ny in range(2):
        nose_x = center_x - 2
        nose_ypos = nose_y + ny
        if 0 <= nose_x < width and 0 <= nose_ypos < height:
            canvas[nose_ypos][nose_x] = GHOST_DARK
    
    # === MOUTH (OPEN ROAR) ===
    mouth_y = head_y + 3
    for my in range(4):
        mouth_width = 5 - my
        for mx in range(-mouth_width, mouth_width + 1):
            mouth_x = center_x + mx - 2
            mouth_ypos = mouth_y + my
            if 0 <= mouth_x < width and 0 <= mouth_ypos < height:
                canvas[mouth_ypos][mouth_x] = OUTLINE_DARK
    
    # === PIRATE HAT (tilted) ===
    hat_y = head_y - 12
    
    # Hat brim
    for brim_y in range(3):
        brim_width = 16 - brim_y * 2
        for bx in range(-brim_width, brim_width + 1):
            brim_curve = abs(bx) // 6
            brim_x = center_x + bx - 2
            brim_ypos = hat_y + brim_y + brim_curve
            if 0 <= brim_x < width and 0 <= brim_ypos < height:
                if abs(bx) > brim_width - 2:
                    canvas[brim_ypos][brim_x] = HAT_SHADOW
                else:
                    canvas[brim_ypos][brim_x] = HAT_DARK
    
    # Hat crown
    for hy in range(8):
        hat_width = 10 - hy
        for hx in range(-hat_width, hat_width + 1):
            hat_x = center_x + hx - 2
            hat_ypos = hat_y - hy
            if 0 <= hat_x < width and 0 <= hat_ypos < height:
                if abs(hx) > hat_width - 2:
                    canvas[hat_ypos][hat_x] = HAT_SHADOW
                elif hx < 0:
                    canvas[hat_ypos][hat_x] = HAT_DARK
                else:
                    canvas[hat_ypos][hat_x] = HAT_SHADOW
    
    # === SKULL AND CROSSBONES ===
    emblem_y = hat_y - 2
    
    # Skull
    for sy in range(4):
        skull_width = 3 - sy // 2
        for sx in range(-skull_width, skull_width + 1):
            skull_x = center_x + sx - 2
            skull_ypos = emblem_y - sy
            if 0 <= skull_x < width and 0 <= skull_ypos < height:
                canvas[skull_ypos][skull_x] = SKULL_CYAN
    
    # Skull eyes
    for eye_offset in [-1, 1]:
        skull_eye_x = center_x + eye_offset - 2
        skull_eye_y = emblem_y - 2
        if 0 <= skull_eye_x < width and 0 <= skull_eye_y < height:
            canvas[skull_eye_y][skull_eye_x] = OUTLINE_DARK
    
    # Crossbones
    for bone_angle in [-1, 1]:
        for bx in range(6):
            bone_x = center_x + (bx - 3) + bone_angle - 2
            bone_y = emblem_y + 1 - bone_angle * (bx - 3) // 2
            if 0 <= bone_x < width and 0 <= bone_y < height:
                canvas[bone_y][bone_x] = SKULL_CYAN
    
    # === MOTION EFFECTS ===
    # Ghostly trail from hook
    for trail in range(8):
        for ty in range(2):
            trail_x = hook_base_x + 12 + trail
            trail_y = hook_base_y - 6 + ty
            if 0 <= trail_x < width and 0 <= trail_y < height:
                canvas[trail_y][trail_x] = MOTION_GLOW
    
    return canvas


def main():
    print("Creating pirate ghost monster images...")
    
    pirateghost_default = create_pirateghost_default()
    pirateghost_attack = create_pirateghost_attack()
    
    # Convert to PIL and scale up
    scale = 4
    
    # Default pose
    img_default = Image.fromarray(pirateghost_default, 'RGBA')
    img_default_scaled = img_default.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_default_scaled.save('art/pirateghost_monster.png')
    print(f"✓ Saved: art/pirateghost_monster.png ({64 * scale}x{64 * scale})")
    
    # Attack animation
    img_attack = Image.fromarray(pirateghost_attack, 'RGBA')
    img_attack_scaled = img_attack.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_attack_scaled.save('art/pirateghost_monster_attack.png')
    print(f"✓ Saved: art/pirateghost_monster_attack.png ({64 * scale}x{64 * scale})")
    
    print("\n✅ Pirate ghost monster creation complete!")
    print("\nFeatures:")
    print("- Default: Floating ghost with pirate hat, hook hand, long beard, glowing eyes")
    print("- Attack: Lunging forward with hook raised, wide eyes, flowing beard")
    print("\nStyle: Spectral pirate with translucent green ghost effects")
    print("Colors: Green/cyan ghost, dark purple hat, glowing eyes, skull emblem on hat")


if __name__ == '__main__':
    main()
