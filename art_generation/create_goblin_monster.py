"""
Goblin Monster Creator
Creates pixel art for a mischievous goblin warrior with axe and armor.
Inspired by the classic fantasy goblin with large ears, green skin, and tribal gear.

Resolution: 64x64 pixels (scaled 4x to 256x256)
Style: Pixel art with character detail
Palette: Green skin, brown leather armor, metal axe
"""

from PIL import Image
import numpy as np


def create_goblin_default():
    """Create the default standing goblin pose."""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette - inspired by the goblin image
    SKIN_GREEN = [120, 160, 80, 255]       # Base green skin
    SKIN_LIGHT = [150, 190, 100, 255]      # Light green highlights
    SKIN_DARK = [90, 130, 60, 255]         # Dark green shadows
    SKIN_SHADOW = [60, 90, 40, 255]        # Deep shadows
    EYE_WHITE = [240, 240, 230, 255]       # Eye whites
    EYE_IRIS = [100, 70, 50, 255]          # Brown iris
    EYE_PUPIL = [20, 20, 20, 255]          # Black pupil
    TEETH_WHITE = [240, 230, 220, 255]     # Teeth/tusks
    TEETH_YELLOW = [220, 210, 180, 255]    # Yellowed teeth
    LEATHER_BROWN = [120, 80, 50, 255]     # Leather armor
    LEATHER_DARK = [80, 50, 30, 255]       # Dark leather
    LEATHER_LIGHT = [160, 110, 70, 255]    # Light leather
    BELT_BROWN = [100, 70, 45, 255]        # Belt
    BUCKLE_METAL = [180, 180, 170, 255]    # Metal buckle
    BUCKLE_DARK = [120, 120, 110, 255]     # Buckle shadow
    AXE_METAL = [200, 200, 200, 255]       # Axe blade
    AXE_DARK = [140, 140, 140, 255]        # Axe shadow
    WOOD_BROWN = [110, 80, 50, 255]        # Axe handle
    WOOD_DARK = [70, 50, 30, 255]          # Handle shadow
    WOOD_LIGHT = [140, 100, 60, 255]       # Handle highlight
    
    center_x = 32
    base_y = 60
    
    # === FEET (large goblin feet) ===
    # Left foot
    for fy in range(4):
        for fx in range(-4, 4):
            foot_x = center_x - 6 + fx
            foot_y = base_y + fy
            if 0 <= foot_x < width and 0 <= foot_y < height:
                if fy < 2:
                    canvas[foot_y][foot_x] = SKIN_DARK if fx < 0 else SKIN_GREEN
                else:
                    canvas[foot_y][foot_x] = SKIN_SHADOW
    
    # Right foot
    for fy in range(4):
        for fx in range(-4, 4):
            foot_x = center_x + 6 + fx
            foot_y = base_y + fy
            if 0 <= foot_x < width and 0 <= foot_y < height:
                if fy < 2:
                    canvas[foot_y][foot_x] = SKIN_DARK if fx < 0 else SKIN_LIGHT
                else:
                    canvas[foot_y][foot_x] = SKIN_SHADOW
    
    # Toes (3 per foot)
    for foot_offset in [-6, 6]:
        for toe in range(3):
            toe_x = center_x + foot_offset + (toe - 1) * 2
            toe_y = base_y + 3
            if 0 <= toe_x < width and 0 <= toe_y < height:
                canvas[toe_y][toe_x] = SKIN_DARK
    
    # === LEGS ===
    # Left leg
    for ly in range(16):
        leg_width = 4 - ly // 8
        for lx in range(-leg_width, leg_width + 1):
            leg_x = center_x - 6 + lx
            leg_y = base_y - ly
            if 0 <= leg_x < width and 0 <= leg_y < height:
                canvas[leg_y][leg_x] = SKIN_GREEN if lx >= 0 else SKIN_DARK
    
    # Right leg
    for ly in range(16):
        leg_width = 4 - ly // 8
        for lx in range(-leg_width, leg_width + 1):
            leg_x = center_x + 6 + lx
            leg_y = base_y - ly
            if 0 <= leg_x < width and 0 <= leg_y < height:
                canvas[leg_y][leg_x] = SKIN_LIGHT if lx >= 0 else SKIN_GREEN
    
    # === LEATHER SKIRT/LOINCLOTH ===
    skirt_y = base_y - 16
    for sy in range(8):
        skirt_width = 10 - sy // 3
        for sx in range(-skirt_width, skirt_width + 1):
            skirt_x = center_x + sx
            skirt_ypos = skirt_y - sy
            if 0 <= skirt_x < width and 0 <= skirt_ypos < height:
                # Jagged bottom edge
                if sy < 2 and abs(sx) % 3 == 0:
                    continue
                canvas[skirt_ypos][skirt_x] = LEATHER_DARK if sx < 0 else LEATHER_BROWN
    
    # === BELT ===
    belt_y = skirt_y - 8
    for by in range(3):
        for bx in range(-10, 11):
            belt_x = center_x + bx
            belt_ypos = belt_y + by
            if 0 <= belt_x < width and 0 <= belt_ypos < height:
                canvas[belt_ypos][belt_x] = BELT_BROWN if by > 0 else LEATHER_DARK
    
    # Belt buckle
    for by in range(4):
        for bx in range(-3, 4):
            buckle_x = center_x + bx
            buckle_y = belt_y + by - 1
            if 0 <= buckle_x < width and 0 <= buckle_y < height:
                if abs(bx) == 3 or by == 0 or by == 3:
                    canvas[buckle_y][buckle_x] = BUCKLE_DARK
                else:
                    canvas[buckle_y][buckle_x] = BUCKLE_METAL
    
    # === TORSO (muscular but small) ===
    torso_y = belt_y - 3
    for ty in range(12):
        torso_width = 8 - ty // 6
        for tx in range(-torso_width, torso_width + 1):
            torso_x = center_x + tx
            torso_ypos = torso_y - ty
            if 0 <= torso_x < width and 0 <= torso_ypos < height:
                # Bare chest with green skin
                if tx < 0:
                    canvas[torso_ypos][torso_x] = SKIN_GREEN if tx > -5 else SKIN_DARK
                else:
                    canvas[torso_ypos][torso_x] = SKIN_LIGHT if tx < 5 else SKIN_GREEN
    
    # Shoulder strap (leather)
    for sy in range(15):
        for sx in range(2):
            strap_x = center_x - 4 + sx
            strap_y = torso_y - sy
            if 0 <= strap_x < width and 0 <= strap_y < height:
                canvas[strap_y][strap_x] = LEATHER_BROWN if sx == 0 else LEATHER_DARK
    
    # === ARMS ===
    arm_start_y = torso_y - 10
    
    # Left arm (holding axe)
    for ay in range(14):
        arm_width = 3 - ay // 8
        for ax in range(-arm_width, arm_width + 1):
            arm_x = center_x - 10 + ax - ay // 4
            arm_y = arm_start_y + ay
            if 0 <= arm_x < width and 0 <= arm_y < height:
                canvas[arm_y][arm_x] = SKIN_DARK if ax < 0 else SKIN_GREEN
    
    # Left hand (gripping axe)
    for hy in range(5):
        for hx in range(-3, 3):
            hand_x = center_x - 14 + hx
            hand_y = arm_start_y + 14 + hy
            if 0 <= hand_x < width and 0 <= hand_y < height:
                canvas[hand_y][hand_x] = SKIN_GREEN if hx >= 0 else SKIN_DARK
    
    # Right arm (at side)
    for ay in range(12):
        arm_width = 3 - ay // 8
        for ax in range(-arm_width, arm_width + 1):
            arm_x = center_x + 10 + ax
            arm_y = arm_start_y + 2 + ay
            if 0 <= arm_x < width and 0 <= arm_y < height:
                canvas[arm_y][arm_x] = SKIN_LIGHT if ax >= 0 else SKIN_GREEN
    
    # Right hand
    for hy in range(4):
        for hx in range(-2, 3):
            hand_x = center_x + 10 + hx
            hand_y = arm_start_y + 14 + hy
            if 0 <= hand_x < width and 0 <= hand_y < height:
                canvas[hand_y][hand_x] = SKIN_LIGHT if hx >= 0 else SKIN_DARK
    
    # === AXE (double-bladed battle axe) ===
    axe_handle_x = center_x - 14
    axe_top_y = arm_start_y - 10
    
    # Axe handle
    for hy in range(28):
        for hx in range(2):
            handle_x = axe_handle_x + hx
            handle_y = axe_top_y + hy
            if 0 <= handle_x < width and 0 <= handle_y < height:
                if hy % 4 < 2:
                    canvas[handle_y][handle_x] = WOOD_BROWN if hx == 0 else WOOD_DARK
                else:
                    canvas[handle_y][handle_x] = WOOD_DARK if hx == 0 else WOOD_LIGHT
    
    # Axe blade (top)
    for by in range(6):
        blade_width = 8 - by
        for bx in range(blade_width):
            blade_x = axe_handle_x - bx
            blade_y = axe_top_y + 8 + by
            if 0 <= blade_x < width and 0 <= blade_y < height:
                if by < 2 or bx < 2:
                    canvas[blade_y][blade_x] = AXE_METAL
                else:
                    canvas[blade_y][blade_x] = AXE_DARK
    
    # Axe blade (bottom mirror)
    for by in range(6):
        blade_width = 8 - by
        for bx in range(blade_width):
            blade_x = axe_handle_x - bx
            blade_y = axe_top_y + 14 - by
            if 0 <= blade_x < width and 0 <= blade_y < height:
                if by < 2 or bx < 2:
                    canvas[blade_y][blade_x] = AXE_METAL
                else:
                    canvas[blade_y][blade_x] = AXE_DARK
    
    # Axe blade (right side)
    for by in range(6):
        blade_width = 6 - by
        for bx in range(blade_width):
            blade_x = axe_handle_x + 2 + bx
            blade_y = axe_top_y + 8 + by
            if 0 <= blade_x < width and 0 <= blade_y < height:
                canvas[blade_y][blade_x] = AXE_METAL if bx < 3 else AXE_DARK
    
    for by in range(6):
        blade_width = 6 - by
        for bx in range(blade_width):
            blade_x = axe_handle_x + 2 + bx
            blade_y = axe_top_y + 14 - by
            if 0 <= blade_x < width and 0 <= blade_y < height:
                canvas[blade_y][blade_x] = AXE_METAL if bx < 3 else AXE_DARK
    
    # === NECK ===
    neck_y = torso_y - 12
    for ny in range(3):
        for nx in range(-3, 4):
            neck_x = center_x + nx
            neck_ypos = neck_y - ny
            if 0 <= neck_x < width and 0 <= neck_ypos < height:
                canvas[neck_ypos][neck_x] = SKIN_GREEN if nx >= 0 else SKIN_DARK
    
    # === HEAD (large goblin head) ===
    head_y = neck_y - 5
    
    # Face (rounded with pointed chin)
    for fy in range(-8, 10):
        for fx in range(-7, 8):
            # Egg-shaped head
            if abs(fx) * 1.2 + abs(fy) * 0.9 < 10:
                face_x = center_x + fx
                face_y = head_y + fy
                if 0 <= face_x < width and 0 <= face_y < height:
                    if fx < -2:
                        canvas[face_y][face_x] = SKIN_DARK
                    elif fx < 2:
                        canvas[face_y][face_x] = SKIN_GREEN
                    else:
                        canvas[face_y][face_x] = SKIN_LIGHT
    
    # === LARGE POINTY EARS ===
    # Left ear
    for ey in range(10):
        ear_width = 4 - ey // 4
        ear_curve = ey // 2
        for ex in range(-ear_width, ear_width + 1):
            ear_x = center_x - 9 - ear_curve + ex
            ear_y = head_y - 4 + ey
            if 0 <= ear_x < width and 0 <= ear_y < height:
                if ex < -1:
                    canvas[ear_y][ear_x] = SKIN_DARK
                elif ex < 1:
                    canvas[ear_y][ear_x] = SKIN_GREEN
                else:
                    canvas[ear_y][ear_x] = SKIN_SHADOW
    
    # Right ear
    for ey in range(10):
        ear_width = 4 - ey // 4
        ear_curve = ey // 2
        for ex in range(-ear_width, ear_width + 1):
            ear_x = center_x + 9 + ear_curve + ex
            ear_y = head_y - 4 + ey
            if 0 <= ear_x < width and 0 <= ear_y < height:
                if ex < 0:
                    canvas[ear_y][ear_x] = SKIN_GREEN
                elif ex < 2:
                    canvas[ear_y][ear_x] = SKIN_LIGHT
                else:
                    canvas[ear_y][ear_x] = SKIN_SHADOW
    
    # === EYES (large expressive eyes) ===
    eye_y = head_y - 2
    
    # Left eye
    for ey in range(-3, 4):
        for ex in range(-3, 4):
            if abs(ex) + abs(ey) < 5:
                eye_x = center_x - 3 + ex
                eye_ypos = eye_y + ey
                if 0 <= eye_x < width and 0 <= eye_ypos < height:
                    if abs(ex) + abs(ey) < 3:
                        canvas[eye_ypos][eye_x] = EYE_WHITE
                    else:
                        canvas[eye_ypos][eye_x] = SKIN_SHADOW
    
    # Right eye
    for ey in range(-3, 4):
        for ex in range(-3, 4):
            if abs(ex) + abs(ey) < 5:
                eye_x = center_x + 3 + ex
                eye_ypos = eye_y + ey
                if 0 <= eye_x < width and 0 <= eye_ypos < height:
                    if abs(ex) + abs(ey) < 3:
                        canvas[eye_ypos][eye_x] = EYE_WHITE
                    else:
                        canvas[eye_ypos][eye_x] = SKIN_SHADOW
    
    # Irises
    for eye_offset in [-3, 3]:
        for ey in range(-2, 3):
            for ex in range(-2, 3):
                if ex * ex + ey * ey < 4:
                    iris_x = center_x + eye_offset + ex
                    iris_y = eye_y + ey
                    if 0 <= iris_x < width and 0 <= iris_y < height:
                        canvas[iris_y][iris_x] = EYE_IRIS
    
    # Pupils
    for eye_offset in [-3, 3]:
        for ey in range(-1, 2):
            for ex in range(-1, 2):
                if abs(ex) + abs(ey) < 2:
                    pupil_x = center_x + eye_offset + ex
                    pupil_y = eye_y + ey
                    if 0 <= pupil_x < width and 0 <= pupil_y < height:
                        canvas[pupil_y][pupil_x] = EYE_PUPIL
    
    # === NOSE (pointed, prominent) ===
    nose_y = head_y + 2
    for ny in range(4):
        nose_width = 2 - ny // 3
        for nx in range(-nose_width, nose_width + 1):
            nose_x = center_x + nx
            nose_ypos = nose_y + ny
            if 0 <= nose_x < width and 0 <= nose_ypos < height:
                canvas[nose_ypos][nose_x] = SKIN_DARK if nx < 0 else SKIN_SHADOW
    
    # === MOUTH (wide grin with teeth) ===
    mouth_y = head_y + 6
    for my in range(4):
        mouth_width = 5 - my // 2
        for mx in range(-mouth_width, mouth_width + 1):
            mouth_x = center_x + mx
            mouth_ypos = mouth_y + my
            if 0 <= mouth_x < width and 0 <= mouth_ypos < height:
                if my == 0:
                    canvas[mouth_ypos][mouth_x] = SKIN_SHADOW
                elif my < 3:
                    canvas[mouth_ypos][mouth_x] = SKIN_SHADOW if abs(mx) < 3 else SKIN_DARK
                else:
                    # Teeth
                    if abs(mx) < 4 and mx % 2 == 0:
                        canvas[mouth_ypos][mouth_x] = TEETH_WHITE
                    else:
                        canvas[mouth_ypos][mouth_x] = TEETH_YELLOW
    
    # Small tusks
    for tusk_offset in [-3, 3]:
        for ty in range(2):
            tusk_x = center_x + tusk_offset
            tusk_y = mouth_y + 4 + ty
            if 0 <= tusk_x < width and 0 <= tusk_y < height:
                canvas[tusk_y][tusk_x] = TEETH_WHITE
    
    return canvas


def create_goblin_attack():
    """Create the attacking goblin - swinging axe with aggressive stance."""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Same color palette
    SKIN_GREEN = [120, 160, 80, 255]
    SKIN_LIGHT = [150, 190, 100, 255]
    SKIN_DARK = [90, 130, 60, 255]
    SKIN_SHADOW = [60, 90, 40, 255]
    EYE_WHITE = [240, 240, 230, 255]
    EYE_IRIS = [100, 70, 50, 255]
    EYE_PUPIL = [20, 20, 20, 255]
    TEETH_WHITE = [240, 230, 220, 255]
    TEETH_YELLOW = [220, 210, 180, 255]
    LEATHER_BROWN = [120, 80, 50, 255]
    LEATHER_DARK = [80, 50, 30, 255]
    LEATHER_LIGHT = [160, 110, 70, 255]
    BELT_BROWN = [100, 70, 45, 255]
    BUCKLE_METAL = [180, 180, 170, 255]
    BUCKLE_DARK = [120, 120, 110, 255]
    AXE_METAL = [200, 200, 200, 255]
    AXE_DARK = [140, 140, 140, 255]
    WOOD_BROWN = [110, 80, 50, 255]
    WOOD_DARK = [70, 50, 30, 255]
    WOOD_LIGHT = [140, 100, 60, 255]
    MOTION_BLUR = [200, 200, 200, 150]
    
    center_x = 32
    base_y = 60
    
    # === FEET (same position) ===
    # Left foot
    for fy in range(4):
        for fx in range(-4, 4):
            foot_x = center_x - 6 + fx
            foot_y = base_y + fy
            if 0 <= foot_x < width and 0 <= foot_y < height:
                if fy < 2:
                    canvas[foot_y][foot_x] = SKIN_DARK if fx < 0 else SKIN_GREEN
                else:
                    canvas[foot_y][foot_x] = SKIN_SHADOW
    
    # Right foot
    for fy in range(4):
        for fx in range(-4, 4):
            foot_x = center_x + 6 + fx
            foot_y = base_y + fy
            if 0 <= foot_x < width and 0 <= foot_y < height:
                if fy < 2:
                    canvas[foot_y][foot_x] = SKIN_DARK if fx < 0 else SKIN_LIGHT
                else:
                    canvas[foot_y][foot_x] = SKIN_SHADOW
    
    # Toes
    for foot_offset in [-6, 6]:
        for toe in range(3):
            toe_x = center_x + foot_offset + (toe - 1) * 2
            toe_y = base_y + 3
            if 0 <= toe_x < width and 0 <= toe_y < height:
                canvas[toe_y][toe_x] = SKIN_DARK
    
    # === LEGS ===
    for ly in range(16):
        leg_width = 4 - ly // 8
        for lx in range(-leg_width, leg_width + 1):
            leg_x = center_x - 6 + lx
            leg_y = base_y - ly
            if 0 <= leg_x < width and 0 <= leg_y < height:
                canvas[leg_y][leg_x] = SKIN_GREEN if lx >= 0 else SKIN_DARK
    
    for ly in range(16):
        leg_width = 4 - ly // 8
        for lx in range(-leg_width, leg_width + 1):
            leg_x = center_x + 6 + lx
            leg_y = base_y - ly
            if 0 <= leg_x < width and 0 <= leg_y < height:
                canvas[leg_y][leg_x] = SKIN_LIGHT if lx >= 0 else SKIN_GREEN
    
    # === LEATHER SKIRT ===
    skirt_y = base_y - 16
    for sy in range(8):
        skirt_width = 10 - sy // 3
        for sx in range(-skirt_width, skirt_width + 1):
            skirt_x = center_x + sx
            skirt_ypos = skirt_y - sy
            if 0 <= skirt_x < width and 0 <= skirt_ypos < height:
                if sy < 2 and abs(sx) % 3 == 0:
                    continue
                canvas[skirt_ypos][skirt_x] = LEATHER_DARK if sx < 0 else LEATHER_BROWN
    
    # === BELT ===
    belt_y = skirt_y - 8
    for by in range(3):
        for bx in range(-10, 11):
            belt_x = center_x + bx
            belt_ypos = belt_y + by
            if 0 <= belt_x < width and 0 <= belt_ypos < height:
                canvas[belt_ypos][belt_x] = BELT_BROWN if by > 0 else LEATHER_DARK
    
    # Belt buckle
    for by in range(4):
        for bx in range(-3, 4):
            buckle_x = center_x + bx
            buckle_y = belt_y + by - 1
            if 0 <= buckle_x < width and 0 <= buckle_y < height:
                if abs(bx) == 3 or by == 0 or by == 3:
                    canvas[buckle_y][buckle_x] = BUCKLE_DARK
                else:
                    canvas[buckle_y][buckle_x] = BUCKLE_METAL
    
    # === TORSO ===
    torso_y = belt_y - 3
    for ty in range(12):
        torso_width = 8 - ty // 6
        for tx in range(-torso_width, torso_width + 1):
            torso_x = center_x + tx
            torso_ypos = torso_y - ty
            if 0 <= torso_x < width and 0 <= torso_ypos < height:
                if tx < 0:
                    canvas[torso_ypos][torso_x] = SKIN_GREEN if tx > -5 else SKIN_DARK
                else:
                    canvas[torso_ypos][torso_x] = SKIN_LIGHT if tx < 5 else SKIN_GREEN
    
    # Shoulder strap
    for sy in range(15):
        for sx in range(2):
            strap_x = center_x - 4 + sx
            strap_y = torso_y - sy
            if 0 <= strap_x < width and 0 <= strap_y < height:
                canvas[strap_y][strap_x] = LEATHER_BROWN if sx == 0 else LEATHER_DARK
    
    # === ARMS (RAISED - swinging axe) ===
    arm_start_y = torso_y - 10
    
    # Right arm (raised high with axe)
    for ay in range(16):
        arm_width = 3 - ay // 10
        arm_angle = ay // 3
        for ax in range(-arm_width, arm_width + 1):
            arm_x = center_x + 6 + arm_angle + ax
            arm_y = arm_start_y - ay
            if 0 <= arm_x < width and 0 <= arm_y < height:
                canvas[arm_y][arm_x] = SKIN_LIGHT if ax >= 0 else SKIN_GREEN
    
    # Right hand (gripping axe high)
    for hy in range(4):
        for hx in range(-2, 3):
            hand_x = center_x + 12 + hx
            hand_y = arm_start_y - 16 + hy
            if 0 <= hand_x < width and 0 <= hand_y < height:
                canvas[hand_y][hand_x] = SKIN_LIGHT if hx >= 0 else SKIN_DARK
    
    # Left arm (supporting swing)
    for ay in range(12):
        arm_width = 3 - ay // 8
        for ax in range(-arm_width, arm_width + 1):
            arm_x = center_x - 8 + ax
            arm_y = arm_start_y - 4 + ay // 2
            if 0 <= arm_x < width and 0 <= arm_y < height:
                canvas[arm_y][arm_x] = SKIN_DARK if ax < 0 else SKIN_GREEN
    
    # Left hand
    for hy in range(4):
        for hx in range(-2, 3):
            hand_x = center_x - 8 + hx
            hand_y = arm_start_y + 2 + hy
            if 0 <= hand_x < width and 0 <= hand_y < height:
                canvas[hand_y][hand_x] = SKIN_GREEN if hx >= 0 else SKIN_DARK
    
    # === AXE (RAISED OVERHEAD) ===
    axe_handle_x = center_x + 12
    axe_top_y = arm_start_y - 28
    
    # Axe handle (angled)
    for hy in range(20):
        handle_offset = hy // 3
        for hx in range(2):
            handle_x = axe_handle_x + handle_offset + hx
            handle_y = axe_top_y + hy
            if 0 <= handle_x < width and 0 <= handle_y < height:
                if hy % 4 < 2:
                    canvas[handle_y][handle_x] = WOOD_BROWN if hx == 0 else WOOD_DARK
                else:
                    canvas[handle_y][handle_x] = WOOD_DARK if hx == 0 else WOOD_LIGHT
    
    # Axe blade (larger, menacing)
    blade_center_x = axe_handle_x + 2
    blade_center_y = axe_top_y + 4
    
    # Top blade
    for by in range(7):
        blade_width = 10 - by
        for bx in range(blade_width):
            blade_x = blade_center_x - bx
            blade_y = blade_center_y + by
            if 0 <= blade_x < width and 0 <= blade_y < height:
                if by < 2 or bx < 2:
                    canvas[blade_y][blade_x] = AXE_METAL
                else:
                    canvas[blade_y][blade_x] = AXE_DARK
    
    # Bottom blade
    for by in range(7):
        blade_width = 10 - by
        for bx in range(blade_width):
            blade_x = blade_center_x - bx
            blade_y = blade_center_y + 8 - by
            if 0 <= blade_x < width and 0 <= blade_y < height:
                if by < 2 or bx < 2:
                    canvas[blade_y][blade_x] = AXE_METAL
                else:
                    canvas[blade_y][blade_x] = AXE_DARK
    
    # Right side blade
    for by in range(7):
        blade_width = 8 - by
        for bx in range(blade_width):
            blade_x = blade_center_x + bx
            blade_y = blade_center_y + by
            if 0 <= blade_x < width and 0 <= blade_y < height:
                canvas[blade_y][blade_x] = AXE_METAL if bx < 4 else AXE_DARK
    
    for by in range(7):
        blade_width = 8 - by
        for bx in range(blade_width):
            blade_x = blade_center_x + bx
            blade_y = blade_center_y + 8 - by
            if 0 <= blade_x < width and 0 <= blade_y < height:
                canvas[blade_y][blade_x] = AXE_METAL if bx < 4 else AXE_DARK
    
    # === MOTION BLUR (swing effect) ===
    for blur in range(5):
        blur_y = blade_center_y + 6 - blur * 2
        for bx in range(8):
            blur_x = blade_center_x - 12 - bx
            if 0 <= blur_x < width and 0 <= blur_y < height:
                if bx < 5:
                    canvas[blur_y][blur_x] = MOTION_BLUR
    
    # === NECK ===
    neck_y = torso_y - 12
    for ny in range(3):
        for nx in range(-3, 4):
            neck_x = center_x + nx
            neck_ypos = neck_y - ny
            if 0 <= neck_x < width and 0 <= neck_ypos < height:
                canvas[neck_ypos][neck_x] = SKIN_GREEN if nx >= 0 else SKIN_DARK
    
    # === HEAD (AGGRESSIVE EXPRESSION) ===
    head_y = neck_y - 5
    
    # Face
    for fy in range(-8, 10):
        for fx in range(-7, 8):
            if abs(fx) * 1.2 + abs(fy) * 0.9 < 10:
                face_x = center_x + fx
                face_y = head_y + fy
                if 0 <= face_x < width and 0 <= face_y < height:
                    if fx < -2:
                        canvas[face_y][face_x] = SKIN_DARK
                    elif fx < 2:
                        canvas[face_y][face_x] = SKIN_GREEN
                    else:
                        canvas[face_y][face_x] = SKIN_LIGHT
    
    # === EARS ===
    # Left ear
    for ey in range(10):
        ear_width = 4 - ey // 4
        ear_curve = ey // 2
        for ex in range(-ear_width, ear_width + 1):
            ear_x = center_x - 9 - ear_curve + ex
            ear_y = head_y - 4 + ey
            if 0 <= ear_x < width and 0 <= ear_y < height:
                if ex < -1:
                    canvas[ear_y][ear_x] = SKIN_DARK
                elif ex < 1:
                    canvas[ear_y][ear_x] = SKIN_GREEN
                else:
                    canvas[ear_y][ear_x] = SKIN_SHADOW
    
    # Right ear
    for ey in range(10):
        ear_width = 4 - ey // 4
        ear_curve = ey // 2
        for ex in range(-ear_width, ear_width + 1):
            ear_x = center_x + 9 + ear_curve + ex
            ear_y = head_y - 4 + ey
            if 0 <= ear_x < width and 0 <= ear_y < height:
                if ex < 0:
                    canvas[ear_y][ear_x] = SKIN_GREEN
                elif ex < 2:
                    canvas[ear_y][ear_x] = SKIN_LIGHT
                else:
                    canvas[ear_y][ear_x] = SKIN_SHADOW
    
    # === EYES (WIDE WITH BATTLE RAGE) ===
    eye_y = head_y - 2
    
    # Left eye (wider)
    for ey in range(-4, 5):
        for ex in range(-3, 4):
            if abs(ex) + abs(ey) < 6:
                eye_x = center_x - 3 + ex
                eye_ypos = eye_y + ey
                if 0 <= eye_x < width and 0 <= eye_ypos < height:
                    if abs(ex) + abs(ey) < 4:
                        canvas[eye_ypos][eye_x] = EYE_WHITE
                    else:
                        canvas[eye_ypos][eye_x] = SKIN_SHADOW
    
    # Right eye
    for ey in range(-4, 5):
        for ex in range(-3, 4):
            if abs(ex) + abs(ey) < 6:
                eye_x = center_x + 3 + ex
                eye_ypos = eye_y + ey
                if 0 <= eye_x < width and 0 <= eye_ypos < height:
                    if abs(ex) + abs(ey) < 4:
                        canvas[eye_ypos][eye_x] = EYE_WHITE
                    else:
                        canvas[eye_ypos][eye_x] = SKIN_SHADOW
    
    # Irises (dilated)
    for eye_offset in [-3, 3]:
        for ey in range(-2, 3):
            for ex in range(-2, 3):
                if ex * ex + ey * ey < 5:
                    iris_x = center_x + eye_offset + ex
                    iris_y = eye_y + ey
                    if 0 <= iris_x < width and 0 <= iris_y < height:
                        canvas[iris_y][iris_x] = EYE_IRIS
    
    # Pupils
    for eye_offset in [-3, 3]:
        pupil_x = center_x + eye_offset
        pupil_y = eye_y
        if 0 <= pupil_x < width and 0 <= pupil_y < height:
            canvas[pupil_y][pupil_x] = EYE_PUPIL
            canvas[pupil_y + 1][pupil_x] = EYE_PUPIL
    
    # === NOSE ===
    nose_y = head_y + 2
    for ny in range(4):
        nose_width = 2 - ny // 3
        for nx in range(-nose_width, nose_width + 1):
            nose_x = center_x + nx
            nose_ypos = nose_y + ny
            if 0 <= nose_x < width and 0 <= nose_ypos < height:
                canvas[nose_ypos][nose_x] = SKIN_DARK if nx < 0 else SKIN_SHADOW
    
    # === MOUTH (OPEN ROAR) ===
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
                    canvas[mouth_ypos][mouth_x] = SKIN_SHADOW if abs(mx) < 4 else SKIN_DARK
                else:
                    # Teeth showing
                    if abs(mx) < 5 and mx % 2 == 0:
                        canvas[mouth_ypos][mouth_x] = TEETH_WHITE
                    else:
                        canvas[mouth_ypos][mouth_x] = TEETH_YELLOW
    
    # Prominent tusks
    for tusk_offset in [-4, 4]:
        for ty in range(3):
            tusk_x = center_x + tusk_offset
            tusk_y = mouth_y + 5 + ty
            if 0 <= tusk_x < width and 0 <= tusk_y < height:
                canvas[tusk_y][tusk_x] = TEETH_WHITE
    
    return canvas


def main():
    print("Creating goblin monster images...")
    
    goblin_default = create_goblin_default()
    goblin_attack = create_goblin_attack()
    
    # Convert to PIL and scale up
    scale = 4
    
    # Default pose
    img_default = Image.fromarray(goblin_default, 'RGBA')
    img_default_scaled = img_default.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_default_scaled.save('art/goblin_monster.png')
    print(f"✓ Saved: art/goblin_monster.png ({64 * scale}x{64 * scale})")
    
    # Attack animation
    img_attack = Image.fromarray(goblin_attack, 'RGBA')
    img_attack_scaled = img_attack.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_attack_scaled.save('art/goblin_monster_attack.png')
    print(f"✓ Saved: art/goblin_monster_attack.png ({64 * scale}x{64 * scale})")
    
    print("\n✅ Goblin monster creation complete!")
    print("\nFeatures:")
    print("- Default: Standing goblin warrior with double-bladed axe and leather gear")
    print("- Attack: Aggressive axe swing with raised weapon and battle roar")
    print("\nStyle: Classic fantasy goblin with large ears, green skin, and tribal warrior appearance")
    print("Colors: Green skin, brown leather armor, metal axe, expressive features")


if __name__ == '__main__':
    main()
