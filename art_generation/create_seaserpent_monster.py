"""
SeaSerpent Monster Generator
Creates pixel art images for the SeaSerpent monster (default and attack poses).
Inspired by: Dark blue/cyan aquatic dragon with wings, serpentine body, flowing fins.
Resolution: 64x64 scaled to 256x256
"""

from PIL import Image
import numpy as np

# Color palette - dark blue/cyan aquatic dragon
BODY_DARK = np.array([20, 30, 45, 255])        # Deep dark blue
BODY_MID = np.array([30, 50, 70, 255])         # Mid dark blue
BODY_BASE = np.array([40, 70, 100, 255])       # Base body blue
BODY_LIGHT = np.array([60, 100, 140, 255])     # Light blue highlights

CYAN_BRIGHT = np.array([0, 180, 220, 255])     # Bright cyan accents
CYAN_MID = np.array([0, 140, 180, 255])        # Mid cyan
CYAN_DARK = np.array([0, 100, 140, 255])       # Dark cyan

WING_MEMBRANE = np.array([0, 160, 200, 200])   # Semi-transparent cyan wings
WING_DARK = np.array([15, 25, 40, 255])        # Dark wing edges
WING_LIGHT = np.array([20, 120, 160, 255])     # Light wing highlights

SCALE_HIGHLIGHT = np.array([80, 130, 180, 255]) # Scale highlights
SCALE_PATTERN = np.array([0, 120, 160, 255])   # Scale pattern cyan

EYE_GLOW = np.array([0, 220, 255, 255])        # Bright glowing cyan eyes
EYE_CORE = np.array([180, 240, 255, 255])      # Bright eye core

SPINE_CYAN = np.array([0, 200, 240, 255])      # Cyan spines/fins
CLAW_DARK = np.array([15, 20, 30, 255])        # Dark claws
CLAW_LIGHT = np.array([40, 60, 80, 255])       # Light claw edges

HORN_DARK = np.array([10, 15, 25, 255])        # Dark horns
HORN_LIGHT = np.array([30, 45, 65, 255])       # Light horn edges

BELLY_LIGHT = np.array([50, 90, 120, 255])     # Lighter belly scales

MOTION_BLUR = np.array([0, 180, 220, 120])     # Motion blur effect

def create_seaserpent_default():
    """Create default SeaSerpent pose - serpentine coiled body with wings spread"""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    center_x = 32
    
    # === SERPENTINE BODY (S-curve coil) ===
    # Lower coil (bottom)
    for segment in range(15):
        seg_y = 50 - segment
        seg_x = center_x + 10 - segment // 2
        seg_width = 5 - segment // 6
        
        for sy in range(-seg_width, seg_width + 1):
            for sx in range(-seg_width, seg_width + 1):
                body_x = seg_x + sx
                body_y = seg_y + sy
                if 0 <= body_x < width and 0 <= body_y < height:
                    if abs(sx) == seg_width or abs(sy) == seg_width:
                        canvas[body_y][body_x] = BODY_DARK
                    elif abs(sx) < 2 and abs(sy) < 2:
                        canvas[body_y][body_x] = BODY_LIGHT
                    elif sx < 0:
                        canvas[body_y][body_x] = BODY_BASE
                    else:
                        canvas[body_y][body_x] = BODY_MID
    
    # Middle coil (curves back)
    for segment in range(18):
        seg_y = 38 - segment // 2
        seg_x = center_x - 8 + segment
        seg_width = 5 - segment // 7
        
        for sy in range(-seg_width, seg_width + 1):
            for sx in range(-seg_width, seg_width + 1):
                body_x = seg_x + sx
                body_y = seg_y + sy
                if 0 <= body_x < width and 0 <= body_y < height:
                    if abs(sx) == seg_width or abs(sy) == seg_width:
                        canvas[body_y][body_x] = BODY_DARK
                    elif abs(sx) < 2 and abs(sy) < 2:
                        canvas[body_y][body_x] = BODY_LIGHT
                    elif sx > 0:
                        canvas[body_y][body_x] = BODY_BASE
                    else:
                        canvas[body_y][body_x] = BODY_MID
    
    # Upper body/neck (curves to head)
    for segment in range(12):
        seg_y = 30 - segment
        seg_x = center_x + 8 - segment // 2
        seg_width = 4 - segment // 5
        
        for sy in range(-seg_width, seg_width + 1):
            for sx in range(-seg_width, seg_width + 1):
                body_x = seg_x + sx
                body_y = seg_y + sy
                if 0 <= body_x < width and 0 <= body_y < height:
                    if abs(sx) == seg_width or abs(sy) == seg_width:
                        canvas[body_y][body_x] = BODY_DARK
                    elif abs(sx) < 2:
                        canvas[body_y][body_x] = BODY_LIGHT
                    else:
                        canvas[body_y][body_x] = BODY_BASE
    
    # === SCALE PATTERNS on body ===
    scale_positions = [
        (center_x + 8, 46), (center_x + 6, 44), (center_x + 4, 42),
        (center_x - 5, 35), (center_x - 2, 33), (center_x + 1, 31),
        (center_x + 6, 26), (center_x + 4, 24)
    ]
    
    for sx, sy in scale_positions:
        if 0 <= sx < width and 0 <= sy < height:
            canvas[sy][sx] = SCALE_PATTERN
            if sx + 1 < width:
                canvas[sy][sx + 1] = CYAN_DARK
    
    # === LEFT WING (large, spread) ===
    wing_base_x = center_x - 2
    wing_base_y = 30
    
    # Wing membrane (curved shape)
    for wy in range(20):
        wing_width = 8 + wy // 2
        wing_curve = wy // 3
        for wx in range(wing_width):
            wing_x = wing_base_x - wx - 3
            wing_y = wing_base_y - 5 - wy + wing_curve
            if 0 <= wing_x < width and 0 <= wing_y < height:
                if wx == 0 or wy == 0 or wx == wing_width - 1:
                    canvas[wing_y][wing_x] = WING_DARK
                elif wx < 3:
                    canvas[wing_y][wing_x] = WING_LIGHT
                else:
                    canvas[wing_y][wing_x] = WING_MEMBRANE
    
    # Wing bones/fingers
    for finger in range(3):
        for fb in range(15 + finger * 3):
            bone_x = wing_base_x - 5 - fb // 2 - finger * 3
            bone_y = wing_base_y - 10 - fb + finger * 5
            if 0 <= bone_x < width and 0 <= bone_y < height:
                canvas[bone_y][bone_x] = WING_DARK
    
    # === RIGHT WING (partially visible behind body) ===
    wing_base_x_r = center_x + 4
    wing_base_y_r = 32
    
    for wy in range(12):
        wing_width = 6 + wy // 3
        for wx in range(wing_width):
            wing_x = wing_base_x_r + wx + 2
            wing_y = wing_base_y_r - 3 - wy
            if 0 <= wing_x < width and 0 <= wing_y < height:
                if wx == 0 or wy == 0:
                    canvas[wing_y][wing_x] = WING_DARK
                else:
                    # Check if not overlapping body (only show partial)
                    if canvas[wing_y][wing_x][3] == 0:
                        canvas[wing_y][wing_x] = WING_MEMBRANE
    
    # === HEAD (dragon-like) ===
    head_x = center_x + 3
    head_y = 18
    
    # Main head shape
    for hy in range(8):
        head_width = 4 - hy // 3
        for hx in range(-head_width, head_width + 1):
            h_x = head_x + hx
            h_y = head_y + hy
            if 0 <= h_x < width and 0 <= h_y < height:
                if abs(hx) == head_width or hy == 0 or hy == 7:
                    canvas[h_y][h_x] = BODY_DARK
                elif hx < 0:
                    canvas[h_y][h_x] = BODY_BASE
                else:
                    canvas[h_y][h_x] = BODY_MID
    
    # Snout
    for sn in range(4):
        snout_x = head_x - 3 - sn
        snout_y = head_y + 3
        if 0 <= snout_x < width and 0 <= snout_y < width:
            canvas[snout_y][snout_x] = BODY_DARK
            canvas[snout_y + 1][snout_x] = BODY_MID
    
    # Eyes (glowing cyan)
    eye_positions = [(head_x - 1, head_y + 2), (head_x + 1, head_y + 2)]
    for ex, ey in eye_positions:
        if 0 <= ex < width and 0 <= ey < height:
            canvas[ey][ex] = EYE_CORE
            if ex - 1 >= 0:
                canvas[ey][ex - 1] = EYE_GLOW
            if ey - 1 >= 0:
                canvas[ey - 1][ex] = EYE_GLOW
    
    # Horns (curved back)
    for horn_idx in range(2):
        horn_x_base = head_x - 2 + horn_idx * 4
        horn_y_base = head_y
        for hn in range(6):
            horn_x = horn_x_base + hn // 2
            horn_y = horn_y_base - hn
            if 0 <= horn_x < width and 0 <= horn_y < height:
                canvas[horn_y][horn_x] = HORN_DARK
                if horn_x + 1 < width:
                    canvas[horn_y][horn_x + 1] = HORN_LIGHT
    
    # === DORSAL FINS/SPINES (cyan glowing) ===
    spine_positions = [
        (center_x + 2, 22), (center_x + 4, 26), (center_x + 6, 30),
        (center_x + 3, 34), (center_x - 3, 36), (center_x - 6, 38)
    ]
    
    for spx, spy in spine_positions:
        for sp in range(4):
            spine_x = spx
            spine_y = spy - sp
            if 0 <= spine_x < width and 0 <= spine_y < height:
                if sp == 0:
                    canvas[spine_y][spine_x] = SPINE_CYAN
                else:
                    canvas[spine_y][spine_x] = CYAN_MID
    
    # === TAIL FIN (flowing at bottom) ===
    tail_base_x = center_x + 15
    tail_base_y = 52
    
    for tf in range(8):
        tail_width = 3 - tf // 3
        for tw in range(-tail_width, tail_width + 1):
            tail_x = tail_base_x + tf // 2
            tail_y = tail_base_y + tw
            if 0 <= tail_x < width and 0 <= tail_y < height:
                if abs(tw) == tail_width:
                    canvas[tail_y][tail_x] = CYAN_DARK
                else:
                    canvas[tail_y][tail_x] = CYAN_BRIGHT
    
    # === FRONT CLAWS (visible on left side) ===
    claw_x = center_x - 10
    claw_y = 32
    
    for claw in range(3):
        for cl in range(4):
            c_x = claw_x - claw + cl // 2
            c_y = claw_y + claw + cl
            if 0 <= c_x < width and 0 <= c_y < height:
                if cl == 0:
                    canvas[c_y][c_x] = CLAW_DARK
                else:
                    canvas[c_y][c_x] = CLAW_LIGHT
    
    return canvas


def create_seaserpent_attack():
    """Create attack SeaSerpent pose - lunging forward with jaws open, wings flared"""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    center_x = 28  # Shifted for lunge
    
    # === SERPENTINE BODY (more forward, aggressive S-curve) ===
    # Lower body coil
    for segment in range(18):
        seg_y = 54 - segment // 2
        seg_x = center_x + 15 - segment
        seg_width = 5 - segment // 7
        
        for sy in range(-seg_width, seg_width + 1):
            for sx in range(-seg_width, seg_width + 1):
                body_x = seg_x + sx
                body_y = seg_y + sy
                if 0 <= body_x < width and 0 <= body_y < height:
                    if abs(sx) == seg_width or abs(sy) == seg_width:
                        canvas[body_y][body_x] = BODY_DARK
                    elif abs(sx) < 2 and abs(sy) < 2:
                        canvas[body_y][body_x] = BODY_LIGHT
                    elif sx < 0:
                        canvas[body_y][body_x] = BODY_BASE
                    else:
                        canvas[body_y][body_x] = BODY_MID
    
    # Middle body (curves up)
    for segment in range(15):
        seg_y = 45 - segment
        seg_x = center_x + segment // 2
        seg_width = 5 - segment // 6
        
        for sy in range(-seg_width, seg_width + 1):
            for sx in range(-seg_width, seg_width + 1):
                body_x = seg_x + sx
                body_y = seg_y + sy
                if 0 <= body_x < width and 0 <= body_y < height:
                    if abs(sx) == seg_width or abs(sy) == seg_width:
                        canvas[body_y][body_x] = BODY_DARK
                    elif abs(sx) < 2:
                        canvas[body_y][body_x] = BODY_LIGHT
                    else:
                        canvas[body_y][body_x] = BODY_BASE
    
    # Neck/upper body (lunging forward)
    for segment in range(10):
        seg_y = 30 - segment * 2
        seg_x = center_x + 5 - segment
        seg_width = 4 - segment // 4
        
        for sy in range(-seg_width, seg_width + 1):
            for sx in range(-seg_width, seg_width + 1):
                body_x = seg_x + sx
                body_y = seg_y + sy
                if 0 <= body_x < width and 0 <= body_y < height:
                    if abs(sx) == seg_width or abs(sy) == seg_width:
                        canvas[body_y][body_x] = BODY_DARK
                    elif abs(sx) < 2:
                        canvas[body_y][body_x] = BODY_LIGHT
                    else:
                        canvas[body_y][body_x] = BODY_MID
    
    # Scale patterns
    scale_positions = [
        (center_x + 12, 50), (center_x + 8, 48), (center_x + 6, 46),
        (center_x + 4, 42), (center_x + 5, 38), (center_x + 3, 34)
    ]
    
    for sx, sy in scale_positions:
        if 0 <= sx < width and 0 <= sy < height:
            canvas[sy][sx] = SCALE_PATTERN
    
    # === WINGS (FLARED WIDE for attack) ===
    # Left wing (fully extended)
    wing_base_x = center_x + 2
    wing_base_y = 32
    
    for wy in range(25):
        wing_width = 10 + wy // 2
        wing_curve = wy // 2
        for wx in range(wing_width):
            wing_x = wing_base_x - wx - 5
            wing_y = wing_base_y - 8 - wy + wing_curve
            if 0 <= wing_x < width and 0 <= wing_y < height:
                if wx == 0 or wy == 0 or wx == wing_width - 1:
                    canvas[wing_y][wing_x] = WING_DARK
                elif wx < 4:
                    canvas[wing_y][wing_x] = WING_LIGHT
                else:
                    canvas[wing_y][wing_x] = WING_MEMBRANE
    
    # Wing fingers (extended)
    for finger in range(4):
        for fb in range(18 + finger * 2):
            bone_x = wing_base_x - 8 - fb // 2 - finger * 4
            bone_y = wing_base_y - 15 - fb + finger * 6
            if 0 <= bone_x < width and 0 <= bone_y < height:
                canvas[bone_y][bone_x] = WING_DARK
    
    # Right wing (extended back)
    wing_base_x_r = center_x + 8
    wing_base_y_r = 34
    
    for wy in range(18):
        wing_width = 8 + wy // 3
        for wx in range(wing_width):
            wing_x = wing_base_x_r + wx + 3
            wing_y = wing_base_y_r - 5 - wy + wx // 3
            if 0 <= wing_x < width and 0 <= wing_y < height:
                if wx == 0 or wy == 0:
                    canvas[wing_y][wing_x] = WING_DARK
                else:
                    if canvas[wing_y][wing_x][3] == 0:
                        canvas[wing_y][wing_x] = WING_MEMBRANE
    
    # === HEAD (lunging forward, jaws OPEN) ===
    head_x = center_x
    head_y = 10
    
    # Upper jaw
    for hy in range(6):
        head_width = 4 - hy // 2
        for hx in range(-head_width, head_width + 1):
            h_x = head_x + hx
            h_y = head_y + hy
            if 0 <= h_x < width and 0 <= h_y < height:
                if abs(hx) == head_width or hy == 0:
                    canvas[h_y][h_x] = BODY_DARK
                elif hx < 0:
                    canvas[h_y][h_x] = BODY_BASE
                else:
                    canvas[h_y][h_x] = BODY_MID
    
    # Lower jaw (open)
    for ly in range(5):
        jaw_width = 3 - ly // 2
        for lx in range(-jaw_width, jaw_width + 1):
            j_x = head_x + lx
            j_y = head_y + 8 + ly
            if 0 <= j_x < width and 0 <= j_y < height:
                if abs(lx) == jaw_width or ly == 4:
                    canvas[j_y][j_x] = BODY_DARK
                else:
                    canvas[j_y][j_x] = BODY_MID
    
    # Open mouth interior (dark)
    for my in range(5):
        for mx in range(-2, 3):
            m_x = head_x + mx
            m_y = head_y + 4 + my
            if 0 <= m_x < width and 0 <= m_y < height:
                if canvas[m_y][m_x][3] == 0:
                    canvas[m_y][m_x] = BODY_DARK
    
    # Teeth (white/cyan points)
    teeth_positions = [
        (head_x - 2, head_y + 4), (head_x, head_y + 3), (head_x + 2, head_y + 4),
        (head_x - 2, head_y + 8), (head_x, head_y + 9), (head_x + 2, head_y + 8)
    ]
    
    for tx, ty in teeth_positions:
        if 0 <= tx < width and 0 <= ty < height:
            canvas[ty][tx] = EYE_CORE
            canvas[ty + 1][tx] = CYAN_BRIGHT
    
    # Snout (elongated)
    for sn in range(5):
        snout_x = head_x - 3 - sn
        snout_y = head_y + 2
        if 0 <= snout_x < width and 0 <= snout_y < height:
            canvas[snout_y][snout_x] = BODY_DARK
            if snout_y + 1 < height:
                canvas[snout_y + 1][snout_x] = BODY_BASE
    
    # Eyes (glowing intensely)
    eye_positions = [(head_x - 1, head_y + 1), (head_x + 2, head_y + 1)]
    for ex, ey in eye_positions:
        if 0 <= ex < width and 0 <= ey < height:
            canvas[ey][ex] = EYE_CORE
            # Glow around eyes
            for gx in range(-1, 2):
                for gy in range(-1, 2):
                    g_x = ex + gx
                    g_y = ey + gy
                    if 0 <= g_x < width and 0 <= g_y < height:
                        if canvas[g_y][g_x][3] == 0 or (gx == 0 and gy == 0):
                            if gx == 0 and gy == 0:
                                continue
                            canvas[g_y][g_x] = EYE_GLOW
    
    # Horns (swept back aggressively)
    for horn_idx in range(2):
        horn_x_base = head_x - 2 + horn_idx * 5
        horn_y_base = head_y
        for hn in range(7):
            horn_x = horn_x_base + hn // 2
            horn_y = horn_y_base - hn
            if 0 <= horn_x < width and 0 <= horn_y < height:
                canvas[horn_y][horn_x] = HORN_DARK
                if horn_x + 1 < width:
                    canvas[horn_y][horn_x + 1] = HORN_LIGHT
    
    # === DORSAL SPINES (glowing bright for attack) ===
    spine_positions = [
        (center_x + 1, 15), (center_x + 3, 22), (center_x + 5, 28),
        (center_x + 6, 34), (center_x + 7, 40)
    ]
    
    for spx, spy in spine_positions:
        for sp in range(5):
            spine_x = spx
            spine_y = spy - sp
            if 0 <= spine_x < width and 0 <= spine_y < height:
                if sp < 2:
                    canvas[spine_y][spine_x] = SPINE_CYAN
                else:
                    canvas[spine_y][spine_x] = CYAN_MID
    
    # === CLAWS (reaching forward) ===
    # Left claw (extended)
    claw_x = center_x - 8
    claw_y = 25
    
    for claw in range(4):
        for cl in range(5):
            c_x = claw_x - claw * 2 + cl // 2
            c_y = claw_y + claw + cl
            if 0 <= c_x < width and 0 <= c_y < height:
                if cl == 0 or cl == 4:
                    canvas[c_y][c_x] = CLAW_DARK
                else:
                    canvas[c_y][c_x] = CLAW_LIGHT
    
    # Right claw
    claw_x_r = center_x + 8
    claw_y_r = 28
    
    for claw in range(3):
        for cl in range(4):
            c_x = claw_x_r + claw
            c_y = claw_y_r + claw + cl
            if 0 <= c_x < width and 0 <= c_y < height:
                if cl == 0:
                    canvas[c_y][c_x] = CLAW_DARK
                else:
                    canvas[c_y][c_x] = CLAW_LIGHT
    
    # === TAIL FIN (flowing with motion) ===
    tail_base_x = center_x + 20
    tail_base_y = 54
    
    for tf in range(10):
        tail_width = 4 - tf // 3
        for tw in range(-tail_width, tail_width + 1):
            tail_x = tail_base_x + tf // 2
            tail_y = tail_base_y + tw - tf // 2
            if 0 <= tail_x < width and 0 <= tail_y < height:
                if abs(tw) == tail_width:
                    canvas[tail_y][tail_x] = CYAN_DARK
                else:
                    canvas[tail_y][tail_x] = CYAN_BRIGHT
    
    # === MOTION BLUR (around head and wings) ===
    # Head motion trail
    for mb in range(8):
        for my in range(3):
            blur_x = head_x + 8 + mb
            blur_y = head_y + 4 + my
            if 0 <= blur_x < width and 0 <= blur_y < height:
                if canvas[blur_y][blur_x][3] == 0:
                    canvas[blur_y][blur_x] = MOTION_BLUR
    
    # Wing motion blur
    for mb in range(6):
        blur_x = wing_base_x - 15 - mb
        blur_y = wing_base_y - 10
        if 0 <= blur_x < width and 0 <= blur_y < height:
            for by in range(3):
                if canvas[blur_y + by][blur_x][3] == 0:
                    canvas[blur_y + by][blur_x] = MOTION_BLUR
    
    return canvas


def main():
    print("Creating SeaSerpent monster images...")
    
    # Create both poses
    seaserpent_default = create_seaserpent_default()
    seaserpent_attack = create_seaserpent_attack()
    
    # Scale up 4x (64x64 -> 256x256) using nearest neighbor
    img_default = Image.fromarray(seaserpent_default, 'RGBA')
    img_default = img_default.resize((256, 256), Image.Resampling.NEAREST)
    img_default.save('art/seaserpent_monster.png')
    print("✓ Saved: art/seaserpent_monster.png (256x256)")
    
    img_attack = Image.fromarray(seaserpent_attack, 'RGBA')
    img_attack = img_attack.resize((256, 256), Image.Resampling.NEAREST)
    img_attack.save('art/seaserpent_monster_attack.png')
    print("✓ Saved: art/seaserpent_monster_attack.png (256x256)")
    
    print("\n✅ SeaSerpent monster creation complete!")
    print("\nFeatures:")
    print("- Default: Serpentine coiled pose with wings spread, glowing cyan eyes")
    print("- Attack: Lunging forward with jaws open, wings flared, teeth visible")
    print("\nStyle: Aquatic dragon with dark blue/cyan coloring")
    print("Colors: Deep blue body, bright cyan accents, glowing eyes and spines")


if __name__ == "__main__":
    main()
