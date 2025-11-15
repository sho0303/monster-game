"""
Create pixel art wyvern monster images
Inspired by dragon with wings and reptilian features
"""
from PIL import Image
import numpy as np

def create_wyvern_default():
    """Create wyvern in standing/ready pose with wings spread"""
    width = 64
    height = 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette - dragon/wyvern theme
    SCALE_GREEN = [100, 110, 80, 255]        # Green scales
    SCALE_DARK = [70, 80, 60, 255]           # Dark green
    SCALE_LIGHT = [130, 140, 100, 255]       # Light green
    
    BELLY_TAN = [140, 130, 100, 255]         # Tan belly scales
    BELLY_LIGHT = [160, 150, 120, 255]       # Light tan
    BELLY_SHADOW = [110, 100, 80, 255]       # Tan shadow
    
    WING_OLIVE = [90, 85, 70, 255]           # Olive wing membrane
    WING_DARK = [60, 55, 45, 255]            # Dark wing
    WING_BROWN = [120, 100, 75, 255]         # Brown wing edge
    
    HORN_BONE = [180, 170, 150, 255]         # Bone horns/spikes
    HORN_DARK = [140, 130, 115, 255]         # Dark horn
    
    CLAW_GRAY = [100, 95, 90, 255]           # Gray claws
    CLAW_DARK = [70, 65, 60, 255]            # Dark claws
    
    EYE_YELLOW = [200, 180, 60, 255]         # Yellow eye
    EYE_DARK = [40, 35, 30, 255]             # Eye pupil
    
    TOOTH_WHITE = [220, 215, 200, 255]       # Teeth
    
    center_x = 32
    base_y = 58
    
    # === TAIL (long, serpentine) ===
    tail_segments = [
        (center_x + 8, base_y - 2),
        (center_x + 12, base_y - 4),
        (center_x + 16, base_y - 6),
        (center_x + 19, base_y - 9),
        (center_x + 21, base_y - 13),
        (center_x + 22, base_y - 17),
    ]
    
    for i, (tx, ty) in enumerate(tail_segments):
        width_val = 4 - i // 2
        for dy in range(-width_val, width_val + 1):
            for dx in range(-width_val, width_val + 1):
                if abs(dx) + abs(dy) <= width_val:
                    if 0 <= tx + dx < width and 0 <= ty + dy < height:
                        canvas[ty + dy][tx + dx] = SCALE_DARK if dy < 0 else SCALE_GREEN
    
    # Tail spikes
    for i in range(0, len(tail_segments) - 1, 2):
        tx, ty = tail_segments[i]
        for spike in range(3):
            sy = ty - 3 - spike
            if 0 <= tx < width and 0 <= sy < height:
                canvas[sy][tx] = HORN_BONE if spike < 2 else HORN_DARK
    
    # === BACK LEGS ===
    left_leg_x = center_x + 4
    right_leg_x = center_x + 10
    leg_y = base_y - 8
    
    for leg_x in [left_leg_x, right_leg_x]:
        # Upper leg
        for dy in range(8):
            for dx in range(-3, 4):
                lx = leg_x + dx
                ly = leg_y + dy
                if 0 <= lx < width and 0 <= ly < height:
                    canvas[ly][lx] = SCALE_GREEN if dx > 0 else SCALE_DARK
        
        # Foot
        foot_y = leg_y + 8
        for dy in range(4):
            for dx in range(-4, 5):
                fx = leg_x + dx
                fy = foot_y + dy
                if 0 <= fx < width and 0 <= fy < height:
                    canvas[fy][fx] = SCALE_DARK if abs(dx) < 2 else SCALE_GREEN
        
        # Claws
        for claw_dx in [-3, 0, 3]:
            for dy in range(2):
                cx = leg_x + claw_dx
                cy = foot_y + 4 + dy
                if 0 <= cx < width and 0 <= cy < height:
                    canvas[cy][cx] = CLAW_GRAY if dy == 0 else CLAW_DARK
    
    # === BODY ===
    body_y = base_y - 20
    
    for dy in range(-8, 12):
        body_width = 10 - abs(dy) // 3
        for dx in range(-body_width, body_width + 1):
            bx = center_x + dx
            by = body_y + dy
            if 0 <= bx < width and 0 <= by < height:
                if abs(dx) < 4:
                    # Belly scales
                    canvas[by][bx] = BELLY_TAN if abs(dx) < 2 else BELLY_LIGHT
                else:
                    # Side scales
                    canvas[by][bx] = SCALE_GREEN if dx > 0 else SCALE_DARK
    
    # Ridge spikes along back
    for spike_x in range(center_x - 6, center_x + 7, 4):
        for i in range(4):
            sx = spike_x
            sy = body_y - 8 - i
            if 0 <= sx < width and 0 <= sy < height:
                canvas[sy][sx] = HORN_BONE if i < 3 else HORN_DARK
                if sx - 1 >= 0:
                    canvas[sy][sx - 1] = HORN_BONE if i < 2 else HORN_DARK
    
    # === WINGS (spread out) ===
    wing_y = body_y - 4
    
    # Left wing
    for i in range(20):
        wx = center_x - 8 - i
        wy = wing_y - i // 3
        if 0 <= wx < width and 0 <= wy < height:
            # Wing bone/arm
            for dy in range(-2, 3):
                if 0 <= wy + dy < height:
                    canvas[wy + dy][wx] = SCALE_DARK if abs(dy) > 1 else SCALE_GREEN
            
            # Wing membrane
            if i > 3 and i < 18:
                membrane_height = 8 + i // 2
                for my in range(membrane_height):
                    wy_mem = wy + 3 + my
                    if 0 <= wx < width and 0 <= wy_mem < height:
                        if my < 2:
                            canvas[wy_mem][wx] = WING_BROWN
                        else:
                            canvas[wy_mem][wx] = WING_OLIVE if my % 2 == 0 else WING_DARK
    
    # Right wing
    for i in range(20):
        wx = center_x + 8 + i
        wy = wing_y - i // 3
        if 0 <= wx < width and 0 <= wy < height:
            # Wing bone/arm
            for dy in range(-2, 3):
                if 0 <= wy + dy < height:
                    canvas[wy + dy][wx] = SCALE_DARK if abs(dy) > 1 else SCALE_GREEN
            
            # Wing membrane
            if i > 3 and i < 18:
                membrane_height = 8 + i // 2
                for my in range(membrane_height):
                    wy_mem = wy + 3 + my
                    if 0 <= wx < width and 0 <= wy_mem < height:
                        if my < 2:
                            canvas[wy_mem][wx] = WING_BROWN
                        else:
                            canvas[wy_mem][wx] = WING_OLIVE if my % 2 == 0 else WING_DARK
    
    # === FRONT LEGS/ARMS ===
    left_arm_x = center_x - 6
    right_arm_x = center_x - 2
    arm_y = body_y + 4
    
    for arm_x in [left_arm_x, right_arm_x]:
        # Arm
        for dy in range(10):
            for dx in range(-2, 3):
                ax = arm_x + dx
                ay = arm_y + dy
                if 0 <= ax < width and 0 <= ay < height:
                    canvas[ay][ax] = SCALE_DARK if dx < 0 else SCALE_GREEN
        
        # Hand/claw
        hand_y = arm_y + 10
        for dy in range(3):
            for dx in range(-3, 4):
                hx = arm_x + dx
                hy = hand_y + dy
                if 0 <= hx < width and 0 <= hy < height:
                    canvas[hy][hx] = SCALE_GREEN if abs(dx) < 2 else SCALE_DARK
        
        # Claws
        for claw_dx in [-2, 0, 2]:
            for dy in range(2):
                cx = arm_x + claw_dx
                cy = hand_y + 3 + dy
                if 0 <= cx < width and 0 <= cy < height:
                    canvas[cy][cx] = CLAW_GRAY if dy == 0 else CLAW_DARK
    
    # === NECK ===
    neck_y = body_y - 10
    for dy in range(8):
        neck_width = 5 - dy // 3
        for dx in range(-neck_width, neck_width + 1):
            nx = center_x + dx
            ny = neck_y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if abs(dx) < 2:
                    canvas[ny][nx] = BELLY_LIGHT
                else:
                    canvas[ny][nx] = SCALE_GREEN if dx > 0 else SCALE_DARK
    
    # === HEAD ===
    head_y = neck_y - 8
    
    # Skull shape
    for dy in range(-6, 8):
        for dx in range(-5, 6):
            if abs(dx) + abs(dy) * 0.7 < 7:
                hx = center_x + dx
                hy = head_y + dy
                if 0 <= hx < width and 0 <= hy < height:
                    if dy < 0:
                        canvas[hy][hx] = SCALE_GREEN if abs(dx) < 2 else SCALE_DARK
                    elif dy < 4:
                        canvas[hy][hx] = SCALE_DARK if dx < 0 else SCALE_GREEN
                    else:
                        # Lower jaw
                        if abs(dx) < 4:
                            canvas[hy][hx] = BELLY_SHADOW
    
    # Snout extension
    for i in range(6):
        sx = center_x - 5 - i
        sy = head_y + 2
        if 0 <= sx < width and 0 <= sy < height:
            for dy in range(-2, 3):
                if 0 <= sy + dy < height:
                    if abs(dy) < 2:
                        canvas[sy + dy][sx] = SCALE_DARK if dy < 0 else SCALE_GREEN
    
    # Horns
    for horn_side in [-1, 1]:
        for i in range(6):
            horn_x = center_x + horn_side * (4 + i // 2)
            horn_y = head_y - 6 - i
            if 0 <= horn_x < width and 0 <= horn_y < height:
                canvas[horn_y][horn_x] = HORN_BONE if i < 4 else HORN_DARK
    
    # Eye
    eye_x = center_x + 2
    eye_y = head_y - 2
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            if abs(dx) + abs(dy) < 3:
                ex = eye_x + dx
                ey = eye_y + dy
                if 0 <= ex < width and 0 <= ey < height:
                    if abs(dx) + abs(dy) < 2:
                        canvas[ey][ex] = EYE_YELLOW
                        if dx == 0 and dy == 0:
                            canvas[ey][ex] = EYE_DARK
                    else:
                        canvas[ey][ex] = SCALE_DARK
    
    # Teeth/fangs
    for tooth_x in range(center_x - 7, center_x - 2, 2):
        for dy in range(2):
            ty = head_y + 6 + dy
            if 0 <= tooth_x < width and 0 <= ty < height:
                canvas[ty][tooth_x] = TOOTH_WHITE if dy == 0 else HORN_DARK
    
    return canvas


def create_wyvern_attack():
    """Create wyvern attack animation - lunging with claws"""
    width = 64
    height = 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Same color palette
    SCALE_GREEN = [100, 110, 80, 255]
    SCALE_DARK = [70, 80, 60, 255]
    SCALE_LIGHT = [130, 140, 100, 255]
    
    BELLY_TAN = [140, 130, 100, 255]
    BELLY_LIGHT = [160, 150, 120, 255]
    BELLY_SHADOW = [110, 100, 80, 255]
    
    WING_OLIVE = [90, 85, 70, 255]
    WING_DARK = [60, 55, 45, 255]
    WING_BROWN = [120, 100, 75, 255]
    
    HORN_BONE = [180, 170, 150, 255]
    HORN_DARK = [140, 130, 115, 255]
    
    CLAW_GRAY = [100, 95, 90, 255]
    CLAW_DARK = [70, 65, 60, 255]
    
    EYE_YELLOW = [200, 180, 60, 255]
    EYE_DARK = [40, 35, 30, 255]
    
    TOOTH_WHITE = [220, 215, 200, 255]
    
    FIRE_ORANGE = [220, 100, 40, 180]
    FIRE_YELLOW = [240, 180, 60, 160]
    
    center_x = 32
    base_y = 58
    
    # === TAIL (curved back) ===
    tail_segments = [
        (center_x + 10, base_y - 2),
        (center_x + 14, base_y - 3),
        (center_x + 18, base_y - 5),
        (center_x + 21, base_y - 8),
        (center_x + 23, base_y - 12),
    ]
    
    for i, (tx, ty) in enumerate(tail_segments):
        width_val = 4 - i // 2
        for dy in range(-width_val, width_val + 1):
            for dx in range(-width_val, width_val + 1):
                if abs(dx) + abs(dy) <= width_val:
                    if 0 <= tx + dx < width and 0 <= ty + dy < height:
                        canvas[ty + dy][tx + dx] = SCALE_DARK if dy < 0 else SCALE_GREEN
    
    # Tail spikes
    for i in range(0, len(tail_segments) - 1, 2):
        tx, ty = tail_segments[i]
        for spike in range(3):
            sy = ty - 3 - spike
            if 0 <= tx < width and 0 <= sy < height:
                canvas[sy][tx] = HORN_BONE if spike < 2 else HORN_DARK
    
    # === BACK LEGS (pushing forward) ===
    left_leg_x = center_x + 6
    right_leg_x = center_x + 12
    leg_y = base_y - 8
    
    for leg_x in [left_leg_x, right_leg_x]:
        # Upper leg
        for dy in range(8):
            for dx in range(-3, 4):
                lx = leg_x + dx
                ly = leg_y + dy
                if 0 <= lx < width and 0 <= ly < height:
                    canvas[ly][lx] = SCALE_GREEN if dx > 0 else SCALE_DARK
        
        # Foot
        foot_y = leg_y + 8
        for dy in range(4):
            for dx in range(-4, 5):
                fx = leg_x + dx
                fy = foot_y + dy
                if 0 <= fx < width and 0 <= fy < height:
                    canvas[fy][fx] = SCALE_DARK if abs(dx) < 2 else SCALE_GREEN
        
        # Claws
        for claw_dx in [-3, 0, 3]:
            for dy in range(2):
                cx = leg_x + claw_dx
                cy = foot_y + 4 + dy
                if 0 <= cx < width and 0 <= cy < height:
                    canvas[cy][cx] = CLAW_GRAY if dy == 0 else CLAW_DARK
    
    # === BODY (leaning forward) ===
    body_y = base_y - 20
    
    for dy in range(-8, 12):
        body_width = 10 - abs(dy) // 3
        for dx in range(-body_width, body_width + 1):
            bx = center_x + dx
            by = body_y + dy
            if 0 <= bx < width and 0 <= by < height:
                if abs(dx) < 4:
                    canvas[by][bx] = BELLY_TAN if abs(dx) < 2 else BELLY_LIGHT
                else:
                    canvas[by][bx] = SCALE_GREEN if dx > 0 else SCALE_DARK
    
    # Ridge spikes
    for spike_x in range(center_x - 6, center_x + 7, 4):
        for i in range(4):
            sx = spike_x
            sy = body_y - 8 - i
            if 0 <= sx < width and 0 <= sy < height:
                canvas[sy][sx] = HORN_BONE if i < 3 else HORN_DARK
                if sx - 1 >= 0:
                    canvas[sy][sx - 1] = HORN_BONE if i < 2 else HORN_DARK
    
    # === WINGS (pulled back for attack) ===
    wing_y = body_y - 4
    
    # Left wing (partially folded)
    for i in range(12):
        wx = center_x - 8 - i
        wy = wing_y + i // 2
        if 0 <= wx < width and 0 <= wy < height:
            for dy in range(-2, 3):
                if 0 <= wy + dy < height:
                    canvas[wy + dy][wx] = SCALE_DARK if abs(dy) > 1 else SCALE_GREEN
            
            if i > 2 and i < 10:
                membrane_height = 6 + i // 3
                for my in range(membrane_height):
                    wy_mem = wy + 2 + my
                    if 0 <= wx < width and 0 <= wy_mem < height:
                        canvas[wy_mem][wx] = WING_OLIVE if my % 2 == 0 else WING_DARK
    
    # Right wing (partially folded)
    for i in range(12):
        wx = center_x + 8 + i
        wy = wing_y + i // 2
        if 0 <= wx < width and 0 <= wy < height:
            for dy in range(-2, 3):
                if 0 <= wy + dy < height:
                    canvas[wy + dy][wx] = SCALE_DARK if abs(dy) > 1 else SCALE_GREEN
            
            if i > 2 and i < 10:
                membrane_height = 6 + i // 3
                for my in range(membrane_height):
                    wy_mem = wy + 2 + my
                    if 0 <= wx < width and 0 <= wy_mem < height:
                        canvas[wy_mem][wx] = WING_OLIVE if my % 2 == 0 else WING_DARK
    
    # === FRONT LEGS/ARMS (reaching forward to attack) ===
    left_arm_x = center_x - 8
    right_arm_x = center_x - 4
    arm_y = body_y + 4
    
    for arm_x in [left_arm_x, right_arm_x]:
        # Arm extending forward
        for i in range(14):
            ax = arm_x - i // 2
            ay = arm_y + i
            for dx in range(-2, 3):
                px = ax + dx
                if 0 <= px < width and 0 <= ay < height:
                    canvas[ay][px] = SCALE_DARK if dx < 0 else SCALE_GREEN
        
        # Hand/claw
        hand_x = arm_x - 7
        hand_y = arm_y + 14
        for dy in range(3):
            for dx in range(-3, 4):
                hx = hand_x + dx
                hy = hand_y + dy
                if 0 <= hx < width and 0 <= hy < height:
                    canvas[hy][hx] = SCALE_GREEN if abs(dx) < 2 else SCALE_DARK
        
        # Claws extended
        for claw_dx in [-3, 0, 3]:
            for dy in range(3):
                cx = hand_x + claw_dx
                cy = hand_y + 3 + dy
                if 0 <= cx < width and 0 <= cy < height:
                    canvas[cy][cx] = CLAW_GRAY if dy < 2 else CLAW_DARK
    
    # === NECK (extended forward) ===
    neck_y = body_y - 10
    for dy in range(8):
        neck_width = 5 - dy // 3
        for dx in range(-neck_width, neck_width + 1):
            nx = center_x + dx - 2
            ny = neck_y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if abs(dx) < 2:
                    canvas[ny][nx] = BELLY_LIGHT
                else:
                    canvas[ny][nx] = SCALE_GREEN if dx > 0 else SCALE_DARK
    
    # === HEAD (open mouth, breathing fire) ===
    head_y = neck_y - 8
    head_x = center_x - 2
    
    # Skull shape
    for dy in range(-6, 8):
        for dx in range(-5, 6):
            if abs(dx) + abs(dy) * 0.7 < 7:
                hx = head_x + dx
                hy = head_y + dy
                if 0 <= hx < width and 0 <= hy < height:
                    if dy < 0:
                        canvas[hy][hx] = SCALE_GREEN if abs(dx) < 2 else SCALE_DARK
                    elif dy < 4:
                        canvas[hy][hx] = SCALE_DARK if dx < 0 else SCALE_GREEN
                    else:
                        # Lower jaw (open)
                        if abs(dx) < 5:
                            canvas[hy][hx] = BELLY_SHADOW
    
    # Snout
    for i in range(6):
        sx = head_x - 5 - i
        sy = head_y + 1
        if 0 <= sx < width and 0 <= sy < height:
            for dy in range(-2, 3):
                if 0 <= sy + dy < height:
                    if abs(dy) < 2:
                        canvas[sy + dy][sx] = SCALE_DARK if dy < 0 else SCALE_GREEN
    
    # Fire breath
    fire_start_x = head_x - 12
    fire_start_y = head_y + 2
    for i in range(15):
        fx = fire_start_x - i
        fy = fire_start_y + (i // 3) - 2
        fire_width = 3 + i // 4
        for dy in range(-fire_width, fire_width + 1):
            if 0 <= fx < width and 0 <= fy + dy < height:
                if i < 8:
                    canvas[fy + dy][fx] = FIRE_YELLOW if abs(dy) < fire_width - 1 else FIRE_ORANGE
                else:
                    canvas[fy + dy][fx] = FIRE_ORANGE
    
    # Horns
    for horn_side in [-1, 1]:
        for i in range(6):
            horn_x = head_x + horn_side * (4 + i // 2)
            horn_y = head_y - 6 - i
            if 0 <= horn_x < width and 0 <= horn_y < height:
                canvas[horn_y][horn_x] = HORN_BONE if i < 4 else HORN_DARK
    
    # Eye (intense)
    eye_x = head_x + 2
    eye_y = head_y - 2
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            if abs(dx) + abs(dy) < 3:
                ex = eye_x + dx
                ey = eye_y + dy
                if 0 <= ex < width and 0 <= ey < height:
                    if abs(dx) + abs(dy) < 2:
                        canvas[ey][ex] = EYE_YELLOW
                        if dx == 0 and dy == 0:
                            canvas[ey][ex] = EYE_DARK
                    else:
                        canvas[ey][ex] = SCALE_DARK
    
    # Teeth
    for tooth_x in range(head_x - 8, head_x - 2, 2):
        for dy in range(2):
            ty = head_y + 5 + dy
            if 0 <= tooth_x < width and 0 <= ty < height:
                canvas[ty][tooth_x] = TOOTH_WHITE if dy == 0 else HORN_DARK
    
    # Lower jaw teeth
    for tooth_x in range(head_x - 7, head_x - 1, 3):
        for dy in range(2):
            ty = head_y + 8 - dy
            if 0 <= tooth_x < width and 0 <= ty < height:
                canvas[ty][tooth_x] = TOOTH_WHITE if dy == 1 else HORN_DARK
    
    return canvas


def main():
    """Create and save wyvern monster images"""
    print("Creating wyvern monster images...")
    
    # Create both images
    wyvern_default = create_wyvern_default()
    wyvern_attack = create_wyvern_attack()
    
    # Convert to PIL and scale up
    scale = 4
    
    # Default pose
    img_default = Image.fromarray(wyvern_default, 'RGBA')
    img_default_scaled = img_default.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_default_scaled.save('wyvern_monster.png')
    print(f"✓ Saved: wyvern_monster.png ({64 * scale}x{64 * scale})")
    
    # Attack animation
    img_attack = Image.fromarray(wyvern_attack, 'RGBA')
    img_attack_scaled = img_attack.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_attack_scaled.save('wyvern_monster_attack.png')
    print(f"✓ Saved: wyvern_monster_attack.png ({64 * scale}x{64 * scale})")
    
    print("\n✅ Wyvern monster creation complete!")
    print("\nFeatures:")
    print("- Default: Majestic wyvern with wings spread and spikes")
    print("- Attack: Aggressive lunge with fire breath and extended claws")
    print("\nStyle: Pixel art inspired by dragon")
    print("Colors: Green scales, tan belly, olive wings, bone horns, yellow eyes")


if __name__ == '__main__':
    main()
