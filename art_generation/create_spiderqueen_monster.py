"""
SpiderQueen Monster Generator
Creates pixel art images for the SpiderQueen monster (default and attack poses).
Inspired by: Horror spider with skull-like head, red/orange markings, tan/brown fur, menacing appearance with 8 hairy legs.
Resolution: 64x64 scaled to 256x256
"""

from PIL import Image
import numpy as np

# Color palette - realistic horror spider
SKULL_BONE = np.array([220, 210, 190, 255])       # Skull bone color
SKULL_SHADOW = np.array([160, 150, 130, 255])     # Skull shadows
SKULL_DARK = np.array([100, 90, 75, 255])         # Dark skull areas
SKULL_SOCKET = np.array([40, 35, 30, 255])        # Eye sockets/dark areas

MARKING_RED = np.array([180, 60, 40, 255])        # Red markings
MARKING_ORANGE = np.array([200, 90, 50, 255])     # Orange markings
MARKING_DARK_RED = np.array([120, 40, 30, 255])   # Dark red markings

BODY_BROWN = np.array([90, 70, 55, 255])          # Brown spider body
BODY_TAN = np.array([140, 110, 85, 255])          # Tan body highlights
BODY_DARK_BROWN = np.array([60, 45, 35, 255])     # Dark brown
BODY_BLACK = np.array([30, 25, 20, 255])          # Black body areas

FUR_TAN = np.array([170, 140, 110, 255])          # Tan fur
FUR_BROWN = np.array([120, 95, 70, 255])          # Brown fur
FUR_DARK = np.array([70, 55, 40, 255])            # Dark fur
FUR_LIGHT = np.array([200, 170, 140, 255])        # Light fur highlights

LEG_BLACK = np.array([35, 30, 25, 255])           # Black leg segments
LEG_RED = np.array([160, 50, 35, 255])            # Red leg segments
LEG_TAN = np.array([150, 120, 90, 255])           # Tan leg fur
LEG_DARK = np.array([45, 35, 30, 255])            # Dark leg shadows
LEG_JOINT = np.array([25, 20, 18, 255])           # Leg joints (darker)

EYE_ORANGE = np.array([255, 140, 60, 255])        # Orange glowing eyes
EYE_YELLOW = np.array([255, 200, 100, 255])       # Yellow eye glow
EYE_RED = np.array([200, 60, 30, 255])            # Red eye base

FANG_WHITE = np.array([240, 235, 220, 255])       # White fangs
FANG_SHADOW = np.array([180, 175, 160, 255])      # Fang shadows

SPINE_GRAY = np.array([120, 115, 105, 255])       # Gray spines on back
SPINE_LIGHT = np.array([160, 155, 145, 255])      # Light spine highlights

MOTION_BLUR = np.array([90, 70, 55, 120])         # Motion blur effect

def draw_legs(canvas, leg_groups, width, height):
    """Helper function to draw spider legs with fur texture"""
    for legs_list in leg_groups:
        for leg_points in legs_list:
            for i in range(len(leg_points) - 1):
                x1, y1 = leg_points[i]
                x2, y2 = leg_points[i + 1]
                
                steps = max(abs(x2 - x1), abs(y2 - y1)) + 1
                for step in range(steps):
                    t = step / steps
                    lx = int(x1 + (x2 - x1) * t)
                    ly = int(y1 + (y2 - y1) * t)
                    
                    thickness = 3 if i == 0 else (2 if i == 1 else 1)
                    segment_color = LEG_RED if (i % 2 == 0) else LEG_BLACK
                    
                    for dy in range(-thickness, thickness + 1):
                        for dx in range(-thickness, thickness + 1):
                            leg_x = lx + dx
                            leg_y = ly + dy
                            if 0 <= leg_x < width and 0 <= leg_y < height:
                                if abs(dx) == thickness or abs(dy) == thickness:
                                    canvas[leg_y][leg_x] = LEG_DARK
                                elif abs(dx) == thickness - 1 or abs(dy) == thickness - 1:
                                    canvas[leg_y][leg_x] = FUR_DARK if (lx + ly) % 3 == 0 else FUR_BROWN
                                else:
                                    canvas[leg_y][leg_x] = segment_color
                
                # Joint
                if i < len(leg_points) - 1:
                    jx, jy = leg_points[i + 1]
                    for jdy in range(-2, 3):
                        for jdx in range(-2, 3):
                            joint_x = jx + jdx
                            joint_y = jy + jdy
                            if 0 <= joint_x < width and 0 <= joint_y < height:
                                if abs(jdx) <= 1 and abs(jdy) <= 1:
                                    canvas[joint_y][joint_x] = LEG_JOINT
                                else:
                                    canvas[joint_y][joint_x] = LEG_BLACK

def create_spiderqueen_default():
    """Create default SpiderQueen pose - horror spider with skull head, standing menacingly"""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    center_x = 32
    body_y = 28
    
    # === SPIDER LEGS (8 legs, 4 per side - hairy, segmented) ===
    back_left_legs = [
        [(center_x - 10, body_y + 8), (center_x - 16, body_y + 14), (center_x - 23, body_y + 18), (center_x - 28, body_y + 24)],
        [(center_x - 8, body_y + 5), (center_x - 14, body_y + 10), (center_x - 20, body_y + 14), (center_x - 24, body_y + 20)]
    ]
    
    back_right_legs = [
        [(center_x + 10, body_y + 8), (center_x + 16, body_y + 14), (center_x + 23, body_y + 18), (center_x + 28, body_y + 24)],
        [(center_x + 8, body_y + 5), (center_x + 14, body_y + 10), (center_x + 20, body_y + 14), (center_x + 24, body_y + 20)]
    ]
    
    front_left_legs = [
        [(center_x - 6, body_y + 2), (center_x - 11, body_y + 6), (center_x - 16, body_y + 10), (center_x - 20, body_y + 16)],
        [(center_x - 5, body_y - 1), (center_x - 9, body_y + 3), (center_x - 13, body_y + 7), (center_x - 16, body_y + 13)]
    ]
    
    front_right_legs = [
        [(center_x + 6, body_y + 2), (center_x + 11, body_y + 6), (center_x + 16, body_y + 10), (center_x + 20, body_y + 16)],
        [(center_x + 5, body_y - 1), (center_x + 9, body_y + 3), (center_x + 13, body_y + 7), (center_x + 16, body_y + 13)]
    ]
    
    # Draw back legs first (behind body)
    draw_legs(canvas, [back_left_legs, back_right_legs], width, height)
    
    # === SPIDER ABDOMEN (large bulbous body with fur) ===
    abdomen_y = body_y + 10
    
    for seg in range(14):
        seg_y = abdomen_y + seg
        seg_width = int(11 - abs(seg - 7) * 1.3)
        
        for sx in range(-seg_width, seg_width + 1):
            abd_x = center_x + sx
            abd_y = seg_y
            if 0 <= abd_x < width and 0 <= abd_y < height:
                if abs(sx) == seg_width or seg == 0 or seg == 13:
                    canvas[abd_y][abd_x] = BODY_BLACK
                elif abs(sx) == seg_width - 1:
                    canvas[abd_y][abd_x] = FUR_DARK if (abd_x + abd_y) % 2 == 0 else FUR_BROWN
                elif seg > 8 and abs(sx) < 4:
                    canvas[abd_y][abd_x] = BODY_DARK_BROWN
                elif sx < -seg_width // 2:
                    canvas[abd_y][abd_x] = BODY_TAN if seg < 7 else BODY_BROWN
                elif sx > seg_width // 2:
                    canvas[abd_y][abd_x] = BODY_BROWN
                else:
                    canvas[abd_y][abd_x] = BODY_BROWN if seg < 7 else BODY_DARK_BROWN
    
    # Fur patches
    for fx, fy in [(center_x - 8, abdomen_y + 3), (center_x + 8, abdomen_y + 3), (center_x - 6, abdomen_y + 8), (center_x + 6, abdomen_y + 8)]:
        if 0 <= fx < width and 0 <= fy < height:
            canvas[fy][fx] = FUR_TAN
    
    # === CEPHALOTHORAX ===
    ceph_y = body_y - 4
    
    for cy in range(10):
        ceph_width = int(8 - cy * 0.7)
        for cx in range(-ceph_width, ceph_width + 1):
            c_x = center_x + cx
            c_y = ceph_y + cy
            if 0 <= c_x < width and 0 <= c_y < height:
                if abs(cx) == ceph_width or cy == 0 or cy == 9:
                    canvas[c_y][c_x] = BODY_BLACK
                elif abs(cx) == ceph_width - 1:
                    canvas[c_y][c_x] = FUR_BROWN if (c_x + c_y) % 2 == 0 else FUR_DARK
                elif cy < 5:
                    canvas[c_y][c_x] = BODY_TAN if cx < 0 else BODY_BROWN
                else:
                    canvas[c_y][c_x] = BODY_BROWN if cx < 0 else BODY_DARK_BROWN
    
    # === SKULL HEAD ===
    head_y = ceph_y - 8
    
    for hy in range(10):
        head_width = int(6 - abs(hy - 5) * 0.8)
        for hx in range(-head_width, head_width + 1):
            h_x = center_x + hx
            h_y = head_y + hy
            if 0 <= h_x < width and 0 <= h_y < height:
                if abs(hx) == head_width or hy == 0 or hy == 9:
                    canvas[h_y][h_x] = SKULL_DARK
                elif hy < 4:
                    canvas[h_y][h_x] = SKULL_BONE if hx < 0 else SKULL_SHADOW
                else:
                    canvas[h_y][h_x] = SKULL_SHADOW if abs(hx) < 2 else (SKULL_BONE if hx < 0 else SKULL_SHADOW)
    
    # Red marking
    for ry in range(8):
        mark_y = head_y + 1 + ry
        if 0 <= center_x < width and 0 <= mark_y < height:
            canvas[mark_y][center_x] = MARKING_ORANGE if ry < 4 else MARKING_RED
    
    # Eyes
    eye_y = head_y + 3
    for eye_x in [center_x - 3, center_x + 3]:
        for ey in range(3):
            for ex in range(2):
                e_x = eye_x + ex - 1
                e_y = eye_y + ey
                if 0 <= e_x < width and 0 <= e_y < height:
                    if ey == 1 and ex == 0:
                        canvas[e_y][e_x] = EYE_YELLOW
                    elif ey == 1:
                        canvas[e_y][e_x] = EYE_ORANGE
                    else:
                        canvas[e_y][e_x] = SKULL_SOCKET
    
    # Small spider eyes
    for sex, sey in [(center_x - 5, head_y + 2), (center_x + 5, head_y + 2), (center_x - 4, head_y + 1), (center_x + 4, head_y + 1)]:
        if 0 <= sex < width and 0 <= sey < height:
            canvas[sey][sex] = EYE_RED
    
    # Fangs
    for side in [-1, 1]:
        for fang_seg in range(5):
            fang_x = center_x + side * 2
            fang_y = head_y + 8 + fang_seg
            if 0 <= fang_x < width and 0 <= fang_y < height:
                canvas[fang_y][fang_x] = FANG_WHITE if fang_seg < 3 else FANG_SHADOW
                if fang_seg < 3 and 0 <= fang_x - side < width:
                    canvas[fang_y][fang_x - side] = FANG_SHADOW
    
    # Spines
    for spx, spy in [(center_x - 6, ceph_y + 2), (center_x - 4, ceph_y + 1), (center_x - 2, ceph_y), (center_x + 2, ceph_y), (center_x + 4, ceph_y + 1), (center_x + 6, ceph_y + 2)]:
        for sp in range(3):
            spine_y = spy - sp
            if 0 <= spx < width and 0 <= spine_y < height:
                canvas[spine_y][spx] = SPINE_LIGHT if sp == 0 else SPINE_GRAY
    
    # Draw front legs last
    draw_legs(canvas, [front_left_legs, front_right_legs], width, height)
    
    return canvas


def create_spiderqueen_attack():
    """Create attack SpiderQueen pose - lunging forward with fangs bared"""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    center_x = 28
    body_y = 30
    
    # === LEGS (reared up) ===
    back_left_legs = [
        [(center_x - 8, body_y + 10), (center_x - 14, body_y + 16), (center_x - 20, body_y + 20), (center_x - 26, body_y + 26)],
        [(center_x - 6, body_y + 8), (center_x - 12, body_y + 13), (center_x - 17, body_y + 17), (center_x - 22, body_y + 23)]
    ]
    
    back_right_legs = [
        [(center_x + 8, body_y + 10), (center_x + 14, body_y + 16), (center_x + 20, body_y + 20), (center_x + 26, body_y + 26)],
        [(center_x + 6, body_y + 8), (center_x + 12, body_y + 13), (center_x + 17, body_y + 17), (center_x + 22, body_y + 23)]
    ]
    
    front_left_legs = [
        [(center_x - 5, body_y + 2), (center_x - 9, body_y - 3), (center_x - 12, body_y - 7), (center_x - 14, body_y - 8)],
        [(center_x - 4, body_y), (center_x - 7, body_y - 5), (center_x - 9, body_y - 9), (center_x - 11, body_y - 10)]
    ]
    
    front_right_legs = [
        [(center_x + 5, body_y + 2), (center_x + 9, body_y - 3), (center_x + 12, body_y - 7), (center_x + 14, body_y - 8)],
        [(center_x + 4, body_y), (center_x + 7, body_y - 5), (center_x + 9, body_y - 9), (center_x + 11, body_y - 10)]
    ]
    
    draw_legs(canvas, [back_left_legs, back_right_legs, front_left_legs, front_right_legs], width, height)
    
    # === ABDOMEN ===
    abdomen_y = body_y + 12
    
    for seg in range(12):
        seg_y = abdomen_y + seg
        seg_width = int(10 - abs(seg - 6) * 1.4)
        
        for sx in range(-seg_width, seg_width + 1):
            abd_x = center_x + sx
            abd_y = seg_y
            if 0 <= abd_x < width and 0 <= abd_y < height:
                if abs(sx) == seg_width or seg == 0 or seg == 11:
                    canvas[abd_y][abd_x] = BODY_BLACK
                elif abs(sx) == seg_width - 1:
                    canvas[abd_y][abd_x] = FUR_DARK if (abd_x + abd_y) % 2 == 0 else FUR_BROWN
                elif sx < -seg_width // 2:
                    canvas[abd_y][abd_x] = BODY_TAN if seg < 6 else BODY_BROWN
                elif sx > seg_width // 2:
                    canvas[abd_y][abd_x] = BODY_BROWN
                else:
                    canvas[abd_y][abd_x] = BODY_BROWN if seg < 6 else BODY_DARK_BROWN
    
    # === CEPHALOTHORAX ===
    ceph_y = body_y - 6
    
    for cy in range(12):
        ceph_width = int(9 - cy * 0.7)
        for cx in range(-ceph_width, ceph_width + 1):
            c_x = center_x + cx
            c_y = ceph_y + cy
            if 0 <= c_x < width and 0 <= c_y < height:
                if abs(cx) == ceph_width or cy == 0 or cy == 11:
                    canvas[c_y][c_x] = BODY_BLACK
                elif abs(cx) == ceph_width - 1:
                    canvas[c_y][c_x] = FUR_BROWN if (c_x + c_y) % 2 == 0 else FUR_DARK
                elif cy < 6:
                    canvas[c_y][c_x] = BODY_TAN if cx < 0 else BODY_BROWN
                else:
                    canvas[c_y][c_x] = BODY_BROWN if cx < 0 else BODY_DARK_BROWN
    
    # === SKULL HEAD ===
    head_y = ceph_y - 10
    
    for hy in range(11):
        head_width = int(7 - abs(hy - 5) * 0.9)
        for hx in range(-head_width, head_width + 1):
            h_x = center_x + hx
            h_y = head_y + hy
            if 0 <= h_x < width and 0 <= h_y < height:
                if abs(hx) == head_width or hy == 0 or hy == 10:
                    canvas[h_y][h_x] = SKULL_DARK
                elif hy < 5:
                    canvas[h_y][h_x] = SKULL_BONE if hx < 0 else SKULL_SHADOW
                else:
                    canvas[h_y][h_x] = SKULL_SHADOW if abs(hx) < 2 else (SKULL_BONE if hx < 0 else SKULL_SHADOW)
    
    # Red marking (brighter)
    for ry in range(9):
        mark_y = head_y + 1 + ry
        if 0 <= center_x < width and 0 <= mark_y < height:
            if ry < 5:
                canvas[mark_y][center_x] = MARKING_ORANGE
                for side in [-1, 1]:
                    if 0 <= center_x + side < width:
                        canvas[mark_y][center_x + side] = MARKING_RED
            else:
                canvas[mark_y][center_x] = MARKING_RED
    
    # Eyes (glowing)
    eye_y = head_y + 4
    for eye_x in [center_x - 3, center_x + 3]:
        for ey in range(3):
            for ex in range(3):
                e_x = eye_x + ex - 1
                e_y = eye_y + ey - 1
                if 0 <= e_x < width and 0 <= e_y < height:
                    if ey == 1 and ex == 1:
                        canvas[e_y][e_x] = EYE_YELLOW
                    elif ey == 1 or ex == 1:
                        canvas[e_y][e_x] = EYE_ORANGE
                    else:
                        canvas[e_y][e_x] = SKULL_SOCKET
    
    # Small spider eyes
    for sex, sey in [(center_x - 5, head_y + 2), (center_x + 5, head_y + 2), (center_x - 4, head_y + 1), (center_x + 4, head_y + 1)]:
        if 0 <= sex < width and 0 <= sey < height:
            canvas[sey][sex] = EYE_ORANGE
    
    # Fangs (extended)
    for side in [-1, 1]:
        for fang_seg in range(7):
            fang_x = center_x + side * (2 + fang_seg // 3)
            fang_y = head_y + 9 + fang_seg
            if 0 <= fang_x < width and 0 <= fang_y < height:
                canvas[fang_y][fang_x] = FANG_WHITE if fang_seg < 4 else FANG_SHADOW
                if fang_seg < 4 and 0 <= fang_x - side < width:
                    canvas[fang_y][fang_x - side] = FANG_SHADOW
    
    # Spines (bristling)
    for spx, spy in [(center_x - 7, ceph_y + 2), (center_x - 5, ceph_y + 1), (center_x - 3, ceph_y), (center_x - 1, ceph_y - 1), (center_x + 1, ceph_y - 1), (center_x + 3, ceph_y), (center_x + 5, ceph_y + 1), (center_x + 7, ceph_y + 2)]:
        for sp in range(4):
            spine_y = spy - sp
            if 0 <= spx < width and 0 <= spine_y < height:
                canvas[spine_y][spx] = SPINE_LIGHT if sp < 2 else SPINE_GRAY
    
    # Motion blur
    for mb in range(10):
        blur_x = center_x + 8 + mb
        blur_y = head_y + 3
        blur_height = 5 - mb // 3
        
        for by in range(-blur_height, blur_height + 1):
            b_y = blur_y + by
            if 0 <= blur_x < width and 0 <= b_y < height:
                if canvas[b_y][blur_x][3] == 0:
                    canvas[b_y][blur_x] = MOTION_BLUR
    
    return canvas


def main():
    print("Creating SpiderQueen monster images...")
    
    spiderqueen_default = create_spiderqueen_default()
    spiderqueen_attack = create_spiderqueen_attack()
    
    img_default = Image.fromarray(spiderqueen_default, 'RGBA')
    img_default = img_default.resize((256, 256), Image.Resampling.NEAREST)
    img_default.save('art/spiderqueen_monster.png')
    print("✓ Saved: art/spiderqueen_monster.png (256x256)")
    
    img_attack = Image.fromarray(spiderqueen_attack, 'RGBA')
    img_attack = img_attack.resize((256, 256), Image.Resampling.NEAREST)
    img_attack.save('art/spiderqueen_monster_attack.png')
    print("✓ Saved: art/spiderqueen_monster_attack.png (256x256)")
    
    print("\n✅ SpiderQueen monster creation complete!")
    print("\nFeatures:")
    print("- Default: Horror spider with skull head, 8 hairy legs, red/orange markings")
    print("- Attack: Lunging forward with front legs raised, fangs extended, eyes glowing")
    print("\nStyle: Realistic horror spider")
    print("Colors: Brown/tan fur, skull-like head, red/orange markings, glowing eyes")


if __name__ == "__main__":
    main()
