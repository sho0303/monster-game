"""
Viper Monster Creator
Creates pixel art for a dangerous desert viper with distinctive rattlesnake patterns.
Inspired by the coiled rattlesnake with segmented scales and warning rattle.

Resolution: 64x64 pixels (scaled 4x to 256x256)
Style: Pixel art with detailed scale patterns
Palette: Brown, tan, cream scales with darker diamond patterns
"""

from PIL import Image
import numpy as np


def create_viper_default():
    """Create the default coiled viper pose."""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette - inspired by rattlesnake
    SCALE_BROWN = [139, 90, 43, 255]      # Dark brown scales
    SCALE_TAN = [180, 140, 90, 255]       # Medium tan
    SCALE_LIGHT = [210, 180, 140, 255]    # Light tan/cream
    SCALE_CREAM = [230, 210, 170, 255]    # Belly cream
    SCALE_DARK = [90, 60, 30, 255]        # Very dark brown
    PATTERN_BLACK = [40, 30, 20, 255]     # Diamond pattern
    RATTLE_TAN = [200, 170, 120, 255]     # Rattle segments
    RATTLE_DARK = [120, 90, 50, 255]      # Rattle shadows
    EYE_YELLOW = [220, 200, 60, 255]      # Yellow eye
    EYE_BLACK = [20, 20, 20, 255]         # Pupil
    TONGUE_RED = [200, 50, 50, 255]       # Forked tongue
    
    center_x = 32
    center_y = 32
    
    # === BODY COILS (three main coils) ===
    # Bottom coil (largest)
    for angle in range(360):
        rad = np.radians(angle)
        for r in range(18, 26):
            x = int(center_x + r * np.cos(rad))
            y = int(center_y + 12 + r * 0.4 * np.sin(rad))
            if 0 <= x < width and 0 <= y < height:
                # Scale pattern
                pattern_val = (x + y) % 6
                if pattern_val < 2:
                    canvas[y][x] = SCALE_BROWN
                elif pattern_val < 4:
                    canvas[y][x] = SCALE_TAN
                else:
                    canvas[y][x] = SCALE_LIGHT
                
                # Diamond patterns
                if (x // 4 + y // 4) % 3 == 0 and abs(x - center_x) > 10:
                    canvas[y][x] = PATTERN_BLACK
    
    # Middle coil
    for angle in range(360):
        rad = np.radians(angle)
        for r in range(15, 22):
            x = int(center_x + r * 0.7 * np.cos(rad))
            y = int(center_y + r * 0.4 * np.sin(rad))
            if 0 <= x < width and 0 <= y < height:
                pattern_val = (x + y) % 6
                if pattern_val < 2:
                    canvas[y][x] = SCALE_BROWN
                elif pattern_val < 4:
                    canvas[y][x] = SCALE_TAN
                else:
                    canvas[y][x] = SCALE_LIGHT
                
                if (x // 4 + y // 3) % 3 == 0:
                    canvas[y][x] = PATTERN_BLACK
    
    # Top coil (head area)
    for angle in range(180, 360):
        rad = np.radians(angle)
        for r in range(12, 18):
            x = int(center_x - 5 + r * 0.6 * np.cos(rad))
            y = int(center_y - 8 + r * 0.3 * np.sin(rad))
            if 0 <= x < width and 0 <= y < height:
                pattern_val = (x + y) % 6
                if pattern_val < 3:
                    canvas[y][x] = SCALE_TAN
                else:
                    canvas[y][x] = SCALE_LIGHT
    
    # === HEAD (triangular viper head) ===
    head_x = center_x - 8
    head_y = center_y - 12
    
    # Head base (wide triangular shape)
    for dy in range(12):
        head_width = 8 - dy // 2
        for dx in range(-head_width, head_width + 1):
            hx = head_x + dx
            hy = head_y + dy
            if 0 <= hx < width and 0 <= hy < height:
                if dy < 4:
                    # Top of head - darker
                    canvas[hy][hx] = SCALE_BROWN if abs(dx) > 2 else SCALE_TAN
                else:
                    # Snout area
                    canvas[hy][hx] = SCALE_TAN if abs(dx) > 1 else SCALE_LIGHT
    
    # Eyes (distinctive pit viper eyes)
    for eye_offset in [-4, 4]:
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                eye_x = head_x + eye_offset + dx
                eye_y = head_y + 3 + dy
                if 0 <= eye_x < width and 0 <= eye_y < height:
                    if abs(dx) + abs(dy) < 3:
                        canvas[eye_y][eye_x] = EYE_YELLOW if abs(dx) + abs(dy) < 2 else SCALE_DARK
                    if abs(dx) < 2 and abs(dy) < 2:
                        canvas[eye_y][eye_x] = EYE_BLACK
    
    # Nostrils
    for nostril_x in [head_x - 2, head_x + 2]:
        nostril_y = head_y + 8
        if 0 <= nostril_x < width and 0 <= nostril_y < height:
            canvas[nostril_y][nostril_x] = SCALE_DARK
    
    # === RATTLE (distinctive segmented rattle tail) ===
    rattle_start_x = center_x + 20
    rattle_start_y = center_y - 8
    
    # Rattle segments (8 segments)
    for segment in range(8):
        seg_x = rattle_start_x + segment * 3
        seg_y = rattle_start_y - segment // 2
        
        # Each segment is roughly oval
        for dy in range(-3, 4):
            for dx in range(-2, 3):
                rx = seg_x + dx
                ry = seg_y + dy
                if 0 <= rx < width and 0 <= ry < height:
                    if abs(dx) * 1.5 + abs(dy) < 4:
                        # Alternating light/dark segments
                        if segment % 2 == 0:
                            canvas[ry][rx] = RATTLE_TAN if abs(dy) < 2 else RATTLE_DARK
                        else:
                            canvas[ry][rx] = RATTLE_DARK if abs(dy) < 2 else SCALE_BROWN
    
    # Rattle tip (pointed end)
    tip_x = rattle_start_x + 24
    tip_y = rattle_start_y - 4
    for dy in range(-2, 3):
        for dx in range(2):
            tx = tip_x + dx
            ty = tip_y + dy
            if 0 <= tx < width and 0 <= ty < height and abs(dy) <= 2 - dx:
                canvas[ty][tx] = RATTLE_TAN
    
    # === BELLY SCALES (visible on coils) ===
    for y in range(center_y + 8, center_y + 20):
        for x in range(center_x - 12, center_x + 12):
            if 0 <= x < width and 0 <= y < height:
                # Check if we're on the body
                dist_sq = (x - center_x) ** 2 + ((y - center_y - 12) * 2) ** 2
                if dist_sq < 400 and dist_sq > 300:
                    # Segmented belly scales
                    if y % 2 == 0:
                        canvas[y][x] = SCALE_CREAM
    
    return canvas


def create_viper_attack():
    """Create the striking viper attack animation - same coiled body with head raised and mouth open."""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette - same as default
    SCALE_BROWN = [139, 90, 43, 255]
    SCALE_TAN = [180, 140, 90, 255]
    SCALE_LIGHT = [210, 180, 140, 255]
    SCALE_CREAM = [230, 210, 170, 255]
    SCALE_DARK = [90, 60, 30, 255]
    PATTERN_BLACK = [40, 30, 20, 255]
    RATTLE_TAN = [200, 170, 120, 255]
    RATTLE_DARK = [120, 90, 50, 255]
    EYE_YELLOW = [220, 200, 60, 255]
    EYE_BLACK = [20, 20, 20, 255]
    TONGUE_RED = [200, 50, 50, 255]
    FANG_WHITE = [240, 240, 230, 255]
    MOUTH_DARK = [30, 20, 15, 255]
    
    center_x = 32
    center_y = 32
    
    # === BODY COILS (same as default - three main coils) ===
    # Bottom coil (largest)
    for angle in range(360):
        rad = np.radians(angle)
        for r in range(18, 26):
            x = int(center_x + r * np.cos(rad))
            y = int(center_y + 12 + r * 0.4 * np.sin(rad))
            if 0 <= x < width and 0 <= y < height:
                # Scale pattern
                pattern_val = (x + y) % 6
                if pattern_val < 2:
                    canvas[y][x] = SCALE_BROWN
                elif pattern_val < 4:
                    canvas[y][x] = SCALE_TAN
                else:
                    canvas[y][x] = SCALE_LIGHT
                
                # Diamond patterns
                if (x // 4 + y // 4) % 3 == 0 and abs(x - center_x) > 10:
                    canvas[y][x] = PATTERN_BLACK
    
    # Middle coil
    for angle in range(360):
        rad = np.radians(angle)
        for r in range(15, 22):
            x = int(center_x + r * 0.7 * np.cos(rad))
            y = int(center_y + r * 0.4 * np.sin(rad))
            if 0 <= x < width and 0 <= y < height:
                pattern_val = (x + y) % 6
                if pattern_val < 2:
                    canvas[y][x] = SCALE_BROWN
                elif pattern_val < 4:
                    canvas[y][x] = SCALE_TAN
                else:
                    canvas[y][x] = SCALE_LIGHT
                
                if (x // 4 + y // 3) % 3 == 0:
                    canvas[y][x] = PATTERN_BLACK
    
    # Top coil (neck area - but no head here)
    for angle in range(180, 360):
        rad = np.radians(angle)
        for r in range(12, 18):
            x = int(center_x - 5 + r * 0.6 * np.cos(rad))
            y = int(center_y - 8 + r * 0.3 * np.sin(rad))
            if 0 <= x < width and 0 <= y < height:
                pattern_val = (x + y) % 6
                if pattern_val < 3:
                    canvas[y][x] = SCALE_TAN
                else:
                    canvas[y][x] = SCALE_LIGHT
    
    # === NECK EXTENSION (connecting to raised head) ===
    # Extend neck upward and to the left
    for ny in range(12):
        neck_width = 4 - ny // 4
        for nx in range(-neck_width, neck_width + 1):
            neck_x = center_x - 8 - ny // 2 + nx
            neck_y = center_y - 12 - ny
            if 0 <= neck_x < width and 0 <= neck_y < height:
                canvas[neck_y][neck_x] = SCALE_TAN if abs(nx) < 2 else SCALE_BROWN
    
    # === HEAD (raised up and to the left with open mouth) ===
    head_x = center_x - 14
    head_y = center_y - 28
    
    # Upper jaw (triangular)
    for dy in range(8):
        head_width = 6 - dy // 2
        for dx in range(-head_width, head_width + 1):
            hx = head_x + dx
            hy = head_y + dy
            if 0 <= hx < width and 0 <= hy < height:
                if dy < 3:
                    canvas[hy][hx] = SCALE_BROWN if abs(dx) > 2 else SCALE_TAN
                else:
                    canvas[hy][hx] = SCALE_TAN if abs(dx) > 1 else SCALE_LIGHT
    
    # Lower jaw (open mouth)
    for dy in range(6):
        jaw_width = 5 - dy // 2
        for dx in range(-jaw_width, jaw_width + 1):
            jx = head_x + dx
            jy = head_y + 8 + dy
            if 0 <= jx < width and 0 <= jy < height:
                if dy < 2:
                    # Mouth interior (dark)
                    canvas[jy][jx] = MOUTH_DARK if abs(dx) < 3 else SCALE_TAN
                else:
                    # Lower jaw scales
                    canvas[jy][jx] = SCALE_TAN if abs(dx) > 1 else SCALE_LIGHT
    
    # Eyes (fierce, yellow)
    for eye_offset in [-3, 3]:
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                eye_x = head_x + eye_offset + dx
                eye_y = head_y + 2 + dy
                if 0 <= eye_x < width and 0 <= eye_y < height:
                    if abs(dx) + abs(dy) < 3:
                        canvas[eye_y][eye_x] = EYE_YELLOW if abs(dx) + abs(dy) < 2 else SCALE_DARK
                    if abs(dx) < 2 and abs(dy) < 2:
                        canvas[eye_y][eye_x] = EYE_BLACK
    
    # Fangs (prominent, pointing down)
    for fang_offset in [-2, 2]:
        for fy in range(5):
            fang_x = head_x + fang_offset
            fang_y = head_y + 8 + fy
            if 0 <= fang_x < width and 0 <= fang_y < height:
                canvas[fang_y][fang_x] = FANG_WHITE if fy < 4 else SCALE_DARK
    
    # Forked tongue (extended from mouth)
    tongue_x = head_x
    tongue_y = head_y + 10
    # Main tongue
    for ty in range(6):
        for tx in range(-1, 2):
            tong_x = tongue_x + tx
            tong_y = tongue_y + ty
            if 0 <= tong_x < width and 0 <= tong_y < height:
                canvas[tong_y][tong_x] = TONGUE_RED
    
    # Fork tips
    for fork_offset in [-2, 2]:
        for fy in range(2):
            fork_x = tongue_x + fork_offset
            fork_y = tongue_y + 5 + fy
            if 0 <= fork_x < width and 0 <= fork_y < height:
                canvas[fork_y][fork_x] = TONGUE_RED
    
    # === RATTLE (same as default) ===
    rattle_start_x = center_x + 20
    rattle_start_y = center_y - 8
    
    # Rattle segments (8 segments)
    for segment in range(8):
        seg_x = rattle_start_x + segment * 3
        seg_y = rattle_start_y - segment // 2
        
        # Each segment is roughly oval
        for dy in range(-3, 4):
            for dx in range(-2, 3):
                rx = seg_x + dx
                ry = seg_y + dy
                if 0 <= rx < width and 0 <= ry < height:
                    if abs(dx) * 1.5 + abs(dy) < 4:
                        # Alternating light/dark segments
                        if segment % 2 == 0:
                            canvas[ry][rx] = RATTLE_TAN if abs(dy) < 2 else RATTLE_DARK
                        else:
                            canvas[ry][rx] = RATTLE_DARK if abs(dy) < 2 else SCALE_BROWN
    
    # Rattle tip (pointed end)
    tip_x = rattle_start_x + 24
    tip_y = rattle_start_y - 4
    for dy in range(-2, 3):
        for dx in range(2):
            tx = tip_x + dx
            ty = tip_y + dy
            if 0 <= tx < width and 0 <= ty < height and abs(dy) <= 2 - dx:
                canvas[ty][tx] = RATTLE_TAN
    
    # === BELLY SCALES (visible on coils) ===
    for y in range(center_y + 8, center_y + 20):
        for x in range(center_x - 12, center_x + 12):
            if 0 <= x < width and 0 <= y < height:
                # Check if we're on the body
                dist_sq = (x - center_x) ** 2 + ((y - center_y - 12) * 2) ** 2
                if dist_sq < 400 and dist_sq > 300:
                    # Segmented belly scales
                    if y % 2 == 0:
                        canvas[y][x] = SCALE_CREAM
    
    return canvas


def main():
    print("Creating viper monster images...")
    
    viper_default = create_viper_default()
    viper_attack = create_viper_attack()
    
    # Convert to PIL and scale up
    scale = 4
    
    # Default pose
    img_default = Image.fromarray(viper_default, 'RGBA')
    img_default_scaled = img_default.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_default_scaled.save('art/viper_monster.png')
    print(f"✓ Saved: art/viper_monster.png ({64 * scale}x{64 * scale})")
    
    # Attack animation
    img_attack = Image.fromarray(viper_attack, 'RGBA')
    img_attack_scaled = img_attack.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_attack_scaled.save('art/viper_monster_attack.png')
    print(f"✓ Saved: art/viper_monster_attack.png ({64 * scale}x{64 * scale})")
    
    print("\n✅ Viper monster creation complete!")
    print("\nFeatures:")
    print("- Default: Coiled defensive pose with segmented rattle tail")
    print("- Attack: Lightning-fast strike with open mouth, fangs, and venom spray")
    print("\nStyle: Desert rattlesnake-inspired pixel art")
    print("Colors: Brown, tan, cream scales with diamond patterns and yellow eyes")


if __name__ == '__main__':
    main()
