"""
Create pixel art Hydra monster images
Inspired by dark fantasy vampire aesthetic - multi-headed serpent beast
"""
from PIL import Image
import numpy as np

def create_hydra_default():
    """Create Hydra in standing/ready pose with three heads"""
    width = 64
    height = 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette - dark fantasy hydra theme
    SCALE_DARK_GREEN = [40, 60, 45, 255]      # Dark green scales
    SCALE_GREEN = [60, 90, 65, 255]            # Green scales
    SCALE_LIGHT = [80, 110, 85, 255]           # Light green
    
    BELLY_GRAY = [70, 75, 70, 255]             # Gray belly
    BELLY_LIGHT = [90, 95, 90, 255]            # Light gray
    
    HEAD_DARK = [35, 55, 40, 255]              # Dark head
    HEAD_GREEN = [55, 80, 60, 255]             # Head green
    
    EYE_RED = [180, 30, 30, 255]               # Red glowing eyes
    EYE_DARK = [100, 15, 15, 255]              # Dark red
    
    FANG_WHITE = [220, 215, 200, 255]          # White fangs
    FANG_YELLOW = [200, 190, 150, 255]         # Yellow fangs
    
    TONGUE_RED = [160, 40, 40, 255]            # Red tongue
    
    SHADOW_BLACK = [20, 25, 20, 255]           # Shadow
    
    center_x = 32
    base_y = 58
    
    # === TAIL (serpentine, coiled) ===
    tail_segments = [
        (center_x + 10, base_y - 2),
        (center_x + 14, base_y - 3),
        (center_x + 17, base_y - 5),
        (center_x + 19, base_y - 8),
        (center_x + 20, base_y - 12),
    ]
    
    for i, (tx, ty) in enumerate(tail_segments):
        width_val = 5 - i // 2
        for dy in range(-width_val, width_val + 1):
            for dx in range(-width_val, width_val + 1):
                if abs(dx) + abs(dy) <= width_val:
                    if 0 <= tx + dx < width and 0 <= ty + dy < height:
                        canvas[ty + dy][tx + dx] = SCALE_DARK_GREEN if dy < 0 else SCALE_GREEN
    
    # Tail spikes
    for i in range(0, len(tail_segments), 2):
        tx, ty = tail_segments[i]
        for spike in range(3):
            sy = ty - 2 - spike
            if 0 <= tx < width and 0 <= sy < height:
                canvas[sy][tx] = SCALE_LIGHT if spike == 0 else SCALE_GREEN
    
    # === MAIN BODY (thick serpentine body) ===
    body_y = base_y - 18
    
    for dy in range(-10, 14):
        body_width = 12 - abs(dy) // 4
        for dx in range(-body_width, body_width + 1):
            bx = center_x + dx
            by = body_y + dy
            if 0 <= bx < width and 0 <= by < height:
                if abs(dx) < 5:
                    # Belly
                    canvas[by][bx] = BELLY_GRAY if abs(dx) < 3 else BELLY_LIGHT
                else:
                    # Side scales
                    canvas[by][bx] = SCALE_GREEN if dx > 0 else SCALE_DARK_GREEN
    
    # Scale texture on body
    for sy in range(body_y - 8, body_y + 12, 3):
        for sx in range(center_x - 10, center_x + 11, 4):
            if 0 <= sx < width and 0 <= sy < height:
                canvas[sy][sx] = SCALE_LIGHT
                if sx + 1 < width:
                    canvas[sy][sx + 1] = SCALE_LIGHT
    
    # === NECK BASE ===
    neck_base_y = body_y - 12
    for dy in range(6):
        neck_width = 8 - dy // 2
        for dx in range(-neck_width, neck_width + 1):
            nx = center_x + dx
            ny = neck_base_y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if abs(dx) < 3:
                    canvas[ny][nx] = BELLY_LIGHT
                else:
                    canvas[ny][nx] = SCALE_GREEN if dx > 0 else SCALE_DARK_GREEN
    
    # === THREE HYDRA HEADS ===
    # Center head (largest, most prominent)
    center_head_x = center_x
    center_head_y = neck_base_y - 12
    
    # Center neck
    for dy in range(8):
        for dx in range(-3, 4):
            nx = center_head_x + dx
            ny = neck_base_y - 6 + dy
            if 0 <= nx < width and 0 <= ny < height:
                if abs(dx) < 2:
                    canvas[ny][nx] = BELLY_LIGHT
                else:
                    canvas[ny][nx] = HEAD_GREEN if dx > 0 else HEAD_DARK
    
    # Center head shape
    for dy in range(-5, 6):
        for dx in range(-4, 5):
            if abs(dx) * 1.2 + abs(dy) * 0.8 < 6:
                hx = center_head_x + dx
                hy = center_head_y + dy
                if 0 <= hx < width and 0 <= hy < height:
                    if dy < 2:
                        canvas[hy][hx] = HEAD_GREEN if dx > 0 else HEAD_DARK
                    else:
                        # Lower jaw
                        canvas[hy][hx] = HEAD_DARK if dx < 0 else HEAD_GREEN
    
    # Center snout
    for i in range(5):
        sx = center_head_x - 4 - i
        sy = center_head_y + 1
        if 0 <= sx < width and 0 <= sy < height:
            for dy in range(-1, 2):
                if 0 <= sy + dy < height:
                    canvas[sy + dy][sx] = HEAD_DARK if dy < 0 else HEAD_GREEN
    
    # Center eye
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if abs(dx) + abs(dy) < 2:
                ex = center_head_x + 1
                ey = center_head_y - 1
                if 0 <= ex + dx < width and 0 <= ey + dy < height:
                    canvas[ey + dy][ex + dx] = EYE_RED if abs(dx) + abs(dy) == 0 else EYE_DARK
    
    # Center fangs
    for fx in [center_head_x - 6, center_head_x - 4]:
        for dy in range(2):
            fy = center_head_y + 4 + dy
            if 0 <= fx < width and 0 <= fy < height:
                canvas[fy][fx] = FANG_WHITE if dy == 0 else FANG_YELLOW
    
    # Left head (smaller, angled left and up)
    left_head_x = center_x - 10
    left_head_y = neck_base_y - 8
    
    # Left neck
    for dy in range(6):
        for dx in range(-2, 3):
            nx = left_head_x + dx
            ny = neck_base_y - 4 + dy
            if 0 <= nx < width and 0 <= ny < height:
                canvas[ny][nx] = HEAD_GREEN if dx > 0 else HEAD_DARK
    
    # Left head shape (smaller)
    for dy in range(-4, 5):
        for dx in range(-3, 4):
            if abs(dx) * 1.3 + abs(dy) * 0.9 < 5:
                hx = left_head_x + dx
                hy = left_head_y + dy
                if 0 <= hx < width and 0 <= hy < height:
                    canvas[hy][hx] = HEAD_DARK if dx < 0 else HEAD_GREEN
    
    # Left snout
    for i in range(4):
        sx = left_head_x - 3 - i
        sy = left_head_y + 1
        if 0 <= sx < width and 0 <= sy < height:
            canvas[sy][sx] = HEAD_DARK
            if sy + 1 < height:
                canvas[sy + 1][sx] = HEAD_GREEN
    
    # Left eye
    ex = left_head_x
    ey = left_head_y - 1
    if 0 <= ex < width and 0 <= ey < height:
        canvas[ey][ex] = EYE_RED
        if ex - 1 >= 0:
            canvas[ey][ex - 1] = EYE_DARK
    
    # Left fangs
    for fx in [left_head_x - 5, left_head_x - 3]:
        fy = left_head_y + 3
        if 0 <= fx < width and 0 <= fy < height:
            canvas[fy][fx] = FANG_WHITE
    
    # Right head (smaller, angled right and up)
    right_head_x = center_x + 10
    right_head_y = neck_base_y - 8
    
    # Right neck
    for dy in range(6):
        for dx in range(-2, 3):
            nx = right_head_x + dx
            ny = neck_base_y - 4 + dy
            if 0 <= nx < width and 0 <= ny < height:
                canvas[ny][nx] = HEAD_GREEN if dx > 0 else HEAD_DARK
    
    # Right head shape (smaller)
    for dy in range(-4, 5):
        for dx in range(-3, 4):
            if abs(dx) * 1.3 + abs(dy) * 0.9 < 5:
                hx = right_head_x + dx
                hy = right_head_y + dy
                if 0 <= hx < width and 0 <= hy < height:
                    canvas[hy][hx] = HEAD_DARK if dx < 0 else HEAD_GREEN
    
    # Right snout
    for i in range(4):
        sx = right_head_x + 3 + i
        sy = right_head_y + 1
        if 0 <= sx < width and 0 <= sy < height:
            canvas[sy][sx] = HEAD_GREEN
            if sy + 1 < height:
                canvas[sy + 1][sx] = HEAD_DARK
    
    # Right eye
    ex = right_head_x + 1
    ey = right_head_y - 1
    if 0 <= ex < width and 0 <= ey < height:
        canvas[ey][ex] = EYE_RED
        if ex + 1 < width:
            canvas[ey][ex + 1] = EYE_DARK
    
    # Right fangs
    for fx in [right_head_x + 3, right_head_x + 5]:
        fy = right_head_y + 3
        if 0 <= fx < width and 0 <= fy < height:
            canvas[fy][fx] = FANG_WHITE
    
    return canvas


def create_hydra_attack():
    """Create Hydra attack animation - all three heads striking forward"""
    width = 64
    height = 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Same color palette
    SCALE_DARK_GREEN = [40, 60, 45, 255]
    SCALE_GREEN = [60, 90, 65, 255]
    SCALE_LIGHT = [80, 110, 85, 255]
    
    BELLY_GRAY = [70, 75, 70, 255]
    BELLY_LIGHT = [90, 95, 90, 255]
    
    HEAD_DARK = [35, 55, 40, 255]
    HEAD_GREEN = [55, 80, 60, 255]
    
    EYE_RED = [180, 30, 30, 255]
    EYE_DARK = [100, 15, 15, 255]
    
    FANG_WHITE = [220, 215, 200, 255]
    FANG_YELLOW = [200, 190, 150, 255]
    
    TONGUE_RED = [160, 40, 40, 255]
    
    FIRE_ORANGE = [220, 100, 40, 200]
    FIRE_YELLOW = [240, 180, 60, 180]
    
    center_x = 38  # Shifted right for lunge
    base_y = 58
    
    # === TAIL (curved back for balance) ===
    tail_segments = [
        (center_x + 12, base_y - 2),
        (center_x + 16, base_y - 3),
        (center_x + 19, base_y - 5),
        (center_x + 21, base_y - 8),
    ]
    
    for i, (tx, ty) in enumerate(tail_segments):
        width_val = 5 - i // 2
        for dy in range(-width_val, width_val + 1):
            for dx in range(-width_val, width_val + 1):
                if abs(dx) + abs(dy) <= width_val:
                    if 0 <= tx + dx < width and 0 <= ty + dy < height:
                        canvas[ty + dy][tx + dx] = SCALE_DARK_GREEN if dy < 0 else SCALE_GREEN
    
    # === MAIN BODY (leaning forward) ===
    body_y = base_y - 18
    
    for dy in range(-10, 14):
        body_width = 12 - abs(dy) // 4
        for dx in range(-body_width, body_width + 1):
            bx = center_x + dx
            by = body_y + dy
            if 0 <= bx < width and 0 <= by < height:
                if abs(dx) < 5:
                    canvas[by][bx] = BELLY_GRAY if abs(dx) < 3 else BELLY_LIGHT
                else:
                    canvas[by][bx] = SCALE_GREEN if dx > 0 else SCALE_DARK_GREEN
    
    # Scale texture
    for sy in range(body_y - 8, body_y + 12, 3):
        for sx in range(center_x - 10, center_x + 11, 4):
            if 0 <= sx < width and 0 <= sy < height:
                canvas[sy][sx] = SCALE_LIGHT
    
    # === NECK BASE ===
    neck_base_y = body_y - 12
    for dy in range(6):
        neck_width = 8 - dy // 2
        for dx in range(-neck_width, neck_width + 1):
            nx = center_x + dx
            ny = neck_base_y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if abs(dx) < 3:
                    canvas[ny][nx] = BELLY_LIGHT
                else:
                    canvas[ny][nx] = SCALE_GREEN if dx > 0 else SCALE_DARK_GREEN
    
    # === THREE HEADS STRIKING FORWARD ===
    # Center head (lunging far forward)
    center_head_x = center_x - 12
    center_head_y = neck_base_y - 8
    
    # Center neck (extended forward)
    for i in range(10):
        for dx in range(-3, 4):
            nx = center_x - 2 - i
            ny = neck_base_y - 2 + i // 3
            if 0 <= nx < width and 0 <= ny < height:
                if abs(dx) < 2:
                    canvas[ny][nx] = BELLY_LIGHT
                else:
                    canvas[ny][nx] = HEAD_GREEN if dx > 0 else HEAD_DARK
    
    # Center head (open mouth attacking)
    for dy in range(-5, 7):
        for dx in range(-4, 5):
            if abs(dx) * 1.2 + abs(dy - 1) * 0.8 < 6:
                hx = center_head_x + dx
                hy = center_head_y + dy
                if 0 <= hx < width and 0 <= hy < height:
                    if dy < 0:
                        # Upper jaw
                        canvas[hy][hx] = HEAD_GREEN if dx > 0 else HEAD_DARK
                    else:
                        # Lower jaw (wide open)
                        canvas[hy][hx] = HEAD_DARK if dx < 0 else HEAD_GREEN
    
    # Center snout
    for i in range(6):
        sx = center_head_x - 4 - i
        sy = center_head_y
        if 0 <= sx < width and 0 <= sy < height:
            for dy in range(-1, 2):
                if 0 <= sy + dy < height:
                    canvas[sy + dy][sx] = HEAD_DARK if dy < 0 else HEAD_GREEN
    
    # Center eye (fierce)
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            ex = center_head_x + 1
            ey = center_head_y - 2
            if 0 <= ex + dx < width and 0 <= ey + dy < height:
                if abs(dx) + abs(dy) < 2:
                    canvas[ey + dy][ex + dx] = EYE_RED if abs(dx) + abs(dy) == 0 else EYE_DARK
    
    # Center open mouth interior
    for my in range(center_head_y + 1, center_head_y + 5):
        for mx in range(center_head_x - 3, center_head_x + 3):
            if 0 <= mx < width and 0 <= my < height:
                if (my - center_head_y) < 4:
                    canvas[my][mx] = SHADOW_BLACK = [20, 15, 15, 255]
    
    # Center fangs (large)
    for fx in [center_head_x - 7, center_head_x - 5, center_head_x - 3]:
        for dy in range(3):
            fy = center_head_y + 3 + dy
            if 0 <= fx < width and 0 <= fy < height:
                canvas[fy][fx] = FANG_WHITE if dy < 2 else FANG_YELLOW
    
    # Center tongue
    for i in range(4):
        tx = center_head_x - 6 - i
        ty = center_head_y + 3
        if 0 <= tx < width and 0 <= ty < height:
            canvas[ty][tx] = TONGUE_RED
    
    # Fire breath from center head
    fire_start_x = center_head_x - 10
    fire_start_y = center_head_y + 2
    for i in range(12):
        fx = fire_start_x - i
        fy = fire_start_y + (i // 4) - 1
        fire_width = 2 + i // 5
        for dy in range(-fire_width, fire_width + 1):
            if 0 <= fx < width and 0 <= fy + dy < height:
                if i < 6:
                    canvas[fy + dy][fx] = FIRE_YELLOW if abs(dy) < fire_width - 1 else FIRE_ORANGE
                else:
                    canvas[fy + dy][fx] = FIRE_ORANGE
    
    # Left head (striking diagonally)
    left_head_x = center_x - 16
    left_head_y = neck_base_y - 4
    
    # Left neck
    for i in range(8):
        for dx in range(-2, 3):
            nx = center_x - 6 - i
            ny = neck_base_y - i // 2
            if 0 <= nx < width and 0 <= ny < height:
                canvas[ny][nx] = HEAD_GREEN if dx > 0 else HEAD_DARK
    
    # Left head (open mouth)
    for dy in range(-4, 6):
        for dx in range(-3, 4):
            if abs(dx) * 1.3 + abs(dy) * 0.9 < 5:
                hx = left_head_x + dx
                hy = left_head_y + dy
                if 0 <= hx < width and 0 <= hy < height:
                    canvas[hy][hx] = HEAD_DARK if dx < 0 else HEAD_GREEN
    
    # Left snout
    for i in range(4):
        sx = left_head_x - 3 - i
        sy = left_head_y
        if 0 <= sx < width and 0 <= sy < height:
            canvas[sy][sx] = HEAD_DARK
            if sy + 1 < height:
                canvas[sy + 1][sx] = HEAD_GREEN
    
    # Left eye
    ex = left_head_x
    ey = left_head_y - 2
    if 0 <= ex < width and 0 <= ey < height:
        canvas[ey][ex] = EYE_RED
    
    # Left fangs
    for fx in [left_head_x - 5, left_head_x - 3]:
        for dy in range(2):
            fy = left_head_y + 3 + dy
            if 0 <= fx < width and 0 <= fy < height:
                canvas[fy][fx] = FANG_WHITE if dy == 0 else FANG_YELLOW
    
    # Right head (striking diagonally)
    right_head_x = center_x - 8
    right_head_y = neck_base_y - 4
    
    # Right neck
    for i in range(8):
        for dx in range(-2, 3):
            nx = center_x + 2 - i
            ny = neck_base_y - i // 2
            if 0 <= nx < width and 0 <= ny < height:
                canvas[ny][nx] = HEAD_GREEN if dx > 0 else HEAD_DARK
    
    # Right head (open mouth)
    for dy in range(-4, 6):
        for dx in range(-3, 4):
            if abs(dx) * 1.3 + abs(dy) * 0.9 < 5:
                hx = right_head_x + dx
                hy = right_head_y + dy
                if 0 <= hx < width and 0 <= hy < height:
                    canvas[hy][hx] = HEAD_DARK if dx < 0 else HEAD_GREEN
    
    # Right snout
    for i in range(4):
        sx = right_head_x - 3 - i
        sy = right_head_y
        if 0 <= sx < width and 0 <= sy < height:
            canvas[sy][sx] = HEAD_GREEN
            if sy + 1 < height:
                canvas[sy + 1][sx] = HEAD_DARK
    
    # Right eye
    ex = right_head_x + 1
    ey = right_head_y - 2
    if 0 <= ex < width and 0 <= ey < height:
        canvas[ey][ex] = EYE_RED
    
    # Right fangs
    for fx in [right_head_x - 5, right_head_x - 3]:
        for dy in range(2):
            fy = right_head_y + 3 + dy
            if 0 <= fx < width and 0 <= fy < height:
                canvas[fy][fx] = FANG_WHITE if dy == 0 else FANG_YELLOW
    
    return canvas


def main():
    """Create and save Hydra monster images"""
    print("Creating Hydra monster images...")
    
    # Create both images
    hydra_default = create_hydra_default()
    hydra_attack = create_hydra_attack()
    
    # Convert to PIL and scale up
    scale = 4
    
    # Default pose
    img_default = Image.fromarray(hydra_default, 'RGBA')
    img_default_scaled = img_default.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_default_scaled.save('../art/hydra_monster.png')
    print(f"✓ Saved: ../art/hydra_monster.png ({64 * scale}x{64 * scale})")
    
    # Attack animation
    img_attack = Image.fromarray(hydra_attack, 'RGBA')
    img_attack_scaled = img_attack.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_attack_scaled.save('../art/hydra_monster_attack.png')
    print(f"✓ Saved: ../art/hydra_monster_attack.png ({64 * scale}x{64 * scale})")
    
    print("\n✅ Hydra monster creation complete!")
    print("\nFeatures:")
    print("- Default: Three-headed serpent with menacing stance")
    print("- Attack: All three heads striking with fire breath from center head")
    print("\nStyle: Dark fantasy pixel art inspired by vampire aesthetic")
    print("Colors: Dark green scales, red glowing eyes, white fangs, gray belly")


if __name__ == '__main__':
    main()
