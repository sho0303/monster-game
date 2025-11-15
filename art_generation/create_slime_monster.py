"""
Slime Monster Generator
Creates pixel art images for the Slime monster (default and attack poses).
Inspired by: Translucent turquoise gelatinous blob with bubbles and cute face.
Resolution: 64x64 scaled to 256x256
"""

from PIL import Image
import numpy as np

# Color palette - translucent turquoise/cyan slime
SLIME_CORE = np.array([60, 180, 170, 255])        # Core slime color
SLIME_LIGHT = np.array([120, 220, 210, 255])      # Light slime highlights
SLIME_MID = np.array([80, 200, 190, 255])         # Mid-tone slime
SLIME_DARK = np.array([40, 140, 150, 255])        # Dark slime shadows

SLIME_TRANSPARENT = np.array([100, 210, 200, 180]) # Semi-transparent areas
SLIME_EDGE = np.array([50, 160, 160, 255])        # Edge outline

BUBBLE_LIGHT = np.array([200, 250, 250, 200])     # Light bubble
BUBBLE_BRIGHT = np.array([230, 255, 255, 230])    # Bright bubble highlight
BUBBLE_EDGE = np.array([150, 230, 230, 180])      # Bubble edge

SHINE_BRIGHT = np.array([240, 255, 255, 255])     # Bright shine spots
SHINE_GLOW = np.array([180, 240, 240, 220])       # Glow around shines

EYE_OUTER = np.array([40, 120, 130, 255])         # Eye outer ring
EYE_WHITE = np.array([200, 240, 240, 255])        # Eye white
EYE_IRIS = np.array([60, 160, 160, 255])          # Eye iris
EYE_PUPIL = np.array([20, 60, 70, 255])           # Eye pupil
EYE_SHINE = np.array([240, 255, 255, 255])        # Eye shine

MOUTH_LINE = np.array([30, 100, 110, 255])        # Mouth line
MOUTH_SHADOW = np.array([40, 120, 120, 200])      # Mouth shadow

MOTION_BLUR = np.array([80, 200, 190, 100])       # Motion blur effect

def create_slime_default():
    """Create default Slime pose - blob sitting with cute face"""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    center_x = 32
    center_y = 40
    
    # === MAIN SLIME BODY (rounded blob shape) ===
    # Bottom portion (wider, flatter)
    for y in range(15):
        # Create rounded bottom
        width_at_y = int(20 - (y * 0.3))
        height_y = center_y + 10 - y
        
        for x in range(-width_at_y, width_at_y + 1):
            body_x = center_x + x
            body_y = height_y
            
            if 0 <= body_x < width and 0 <= body_y < height:
                # Distance from center for shading
                dist_from_center = abs(x)
                
                # Outer edge
                if dist_from_center == width_at_y or y == 0:
                    canvas[body_y][body_x] = SLIME_EDGE
                # Left side (lighter)
                elif x < -width_at_y // 2:
                    if y < 5:
                        canvas[body_y][body_x] = SLIME_LIGHT
                    else:
                        canvas[body_y][body_x] = SLIME_MID
                # Right side (darker)
                elif x > width_at_y // 2:
                    canvas[body_y][body_x] = SLIME_DARK
                # Center
                else:
                    if y < 8:
                        canvas[body_y][body_x] = SLIME_CORE
                    else:
                        canvas[body_y][body_x] = SLIME_LIGHT
    
    # Top portion (rounded dome)
    for y in range(20):
        # Elliptical top
        width_at_y = int(20 - (y ** 1.3) / 3.5)
        if width_at_y < 1:
            break
        height_y = center_y - 5 - y
        
        for x in range(-width_at_y, width_at_y + 1):
            body_x = center_x + x
            body_y = height_y
            
            if 0 <= body_x < width and 0 <= body_y < height:
                dist_from_center = abs(x)
                
                # Outer edge
                if dist_from_center == width_at_y or y == 19:
                    canvas[body_y][body_x] = SLIME_EDGE
                # Top highlight area
                elif y > 12 and dist_from_center < 8:
                    canvas[body_y][body_x] = SLIME_LIGHT
                # Left side (lighter)
                elif x < 0:
                    canvas[body_y][body_x] = SLIME_MID
                # Right side (darker)
                elif x > 5:
                    canvas[body_y][body_x] = SLIME_DARK
                # Center
                else:
                    canvas[body_y][body_x] = SLIME_CORE
    
    # === LARGE SHINE SPOT (top left) ===
    shine_positions = [
        (center_x - 8, center_y - 15), (center_x - 7, center_y - 15),
        (center_x - 9, center_y - 14), (center_x - 8, center_y - 14), (center_x - 7, center_y - 14), (center_x - 6, center_y - 14),
        (center_x - 8, center_y - 13), (center_x - 7, center_y - 13), (center_x - 6, center_y - 13),
        (center_x - 7, center_y - 12)
    ]
    
    for sx, sy in shine_positions:
        if 0 <= sx < width and 0 <= sy < height:
            canvas[sy][sx] = SHINE_BRIGHT
    
    # Shine glow
    shine_glow_positions = [
        (center_x - 10, center_y - 15), (center_x - 10, center_y - 14), (center_x - 10, center_y - 13),
        (center_x - 9, center_y - 16), (center_x - 8, center_y - 16), (center_x - 7, center_y - 16),
        (center_x - 6, center_y - 15), (center_x - 5, center_y - 14), (center_x - 5, center_y - 13)
    ]
    
    for sx, sy in shine_glow_positions:
        if 0 <= sx < width and 0 <= sy < height:
            if canvas[sy][sx][3] < 200:  # Don't overwrite existing bright areas
                canvas[sy][sx] = SHINE_GLOW
    
    # === INTERNAL BUBBLES ===
    # Large bubble (left side)
    large_bubble_x = center_x - 10
    large_bubble_y = center_y - 5
    
    for by in range(5):
        bubble_width = 3 - by // 2
        for bx in range(-bubble_width, bubble_width + 1):
            b_x = large_bubble_x + bx
            b_y = large_bubble_y - by
            if 0 <= b_x < width and 0 <= b_y < height:
                if by == 0 or abs(bx) == bubble_width:
                    canvas[b_y][b_x] = BUBBLE_EDGE
                elif by < 2 and bx <= 0:
                    canvas[b_y][b_x] = BUBBLE_BRIGHT
                else:
                    canvas[b_y][b_x] = BUBBLE_LIGHT
    
    # Small bubble highlights on large bubble
    if 0 <= large_bubble_x - 1 < width and 0 <= large_bubble_y - 3 < height:
        canvas[large_bubble_y - 3][large_bubble_x - 1] = SHINE_BRIGHT
    
    # Medium bubble (right side)
    med_bubble_x = center_x + 8
    med_bubble_y = center_y - 2
    
    for by in range(4):
        bubble_width = 2 - by // 2
        for bx in range(-bubble_width, bubble_width + 1):
            b_x = med_bubble_x + bx
            b_y = med_bubble_y - by
            if 0 <= b_x < width and 0 <= b_y < height:
                if by == 0 or abs(bx) == bubble_width:
                    canvas[b_y][b_x] = BUBBLE_EDGE
                elif by < 2:
                    canvas[b_y][b_x] = BUBBLE_LIGHT
                else:
                    canvas[b_y][b_x] = BUBBLE_BRIGHT
    
    # Small bubbles scattered
    small_bubble_positions = [
        (center_x - 5, center_y + 2), (center_x + 3, center_y - 8),
        (center_x - 12, center_y - 12), (center_x + 10, center_y - 10),
        (center_x, center_y + 5), (center_x + 6, center_y + 3)
    ]
    
    for sbx, sby in small_bubble_positions:
        if 0 <= sbx < width and 0 <= sby < height:
            canvas[sby][sbx] = BUBBLE_BRIGHT
            if sbx + 1 < width:
                canvas[sby][sbx + 1] = BUBBLE_LIGHT
            if sby - 1 >= 0:
                canvas[sby - 1][sbx] = BUBBLE_LIGHT
    
    # === EYES (cute round eyes) ===
    eye_y = center_y - 8
    left_eye_x = center_x - 6
    right_eye_x = center_x + 6
    
    for eye_x in [left_eye_x, right_eye_x]:
        # Outer ring
        for ey in range(-3, 4):
            for ex in range(-3, 4):
                e_x = eye_x + ex
                e_y = eye_y + ey
                if 0 <= e_x < width and 0 <= e_y < height:
                    dist = (ex ** 2 + ey ** 2) ** 0.5
                    if 2.5 < dist < 3.5:
                        canvas[e_y][e_x] = EYE_OUTER
                    elif dist <= 2.5:
                        if dist < 1.5:
                            # Pupil
                            if ey >= 0:
                                canvas[e_y][e_x] = EYE_PUPIL
                            else:
                                canvas[e_y][e_x] = EYE_IRIS
                        else:
                            # White
                            canvas[e_y][e_x] = EYE_WHITE
        
        # Eye shine
        if 0 <= eye_x - 1 < width and 0 <= eye_y - 2 < height:
            canvas[eye_y - 2][eye_x - 1] = EYE_SHINE
            canvas[eye_y - 1][eye_x - 1] = EYE_SHINE
    
    # === MOUTH (simple smile) ===
    mouth_y = center_y - 2
    
    # Curved smile
    mouth_positions = [
        (center_x - 4, mouth_y), (center_x - 3, mouth_y + 1),
        (center_x - 2, mouth_y + 1), (center_x - 1, mouth_y + 1),
        (center_x, mouth_y + 1), (center_x + 1, mouth_y + 1),
        (center_x + 2, mouth_y + 1), (center_x + 3, mouth_y + 1),
        (center_x + 4, mouth_y)
    ]
    
    for mx, my in mouth_positions:
        if 0 <= mx < width and 0 <= my < height:
            canvas[my][mx] = MOUTH_LINE
    
    # === SMALL SHINE SPOTS (scattered on surface) ===
    tiny_shine_positions = [
        (center_x - 14, center_y - 8), (center_x + 12, center_y - 12),
        (center_x - 4, center_y + 4), (center_x + 8, center_y + 2),
        (center_x, center_y - 18)
    ]
    
    for tsx, tsy in tiny_shine_positions:
        if 0 <= tsx < width and 0 <= tsy < height:
            canvas[tsy][tsx] = SHINE_BRIGHT
    
    return canvas


def create_slime_attack():
    """Create attack Slime pose - lunging forward with determined face"""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    center_x = 28  # Shifted for lunge
    center_y = 38
    
    # === MAIN SLIME BODY (stretched/lunging forward) ===
    # Bottom portion (stretched forward)
    for y in range(12):
        width_at_y = int(22 - (y * 0.4))
        height_y = center_y + 8 - y
        
        for x in range(-width_at_y, width_at_y + 1):
            body_x = center_x + x
            body_y = height_y
            
            if 0 <= body_x < width and 0 <= body_y < height:
                dist_from_center = abs(x)
                
                # Outer edge
                if dist_from_center == width_at_y or y == 0:
                    canvas[body_y][body_x] = SLIME_EDGE
                # Left side
                elif x < -width_at_y // 2:
                    canvas[body_y][body_x] = SLIME_MID
                # Right side
                elif x > width_at_y // 2:
                    canvas[body_y][body_x] = SLIME_DARK
                # Center
                else:
                    canvas[body_y][body_x] = SLIME_CORE
    
    # Top portion (tilted forward for lunge)
    for y in range(22):
        width_at_y = int(22 - (y ** 1.2) / 3.2)
        if width_at_y < 1:
            break
        height_y = center_y - 4 - y
        # Shift forward as we go up
        x_shift = -y // 3
        
        for x in range(-width_at_y, width_at_y + 1):
            body_x = center_x + x + x_shift
            body_y = height_y
            
            if 0 <= body_x < width and 0 <= body_y < height:
                dist_from_center = abs(x)
                
                # Outer edge
                if dist_from_center == width_at_y or y == 21:
                    canvas[body_y][body_x] = SLIME_EDGE
                # Top highlight
                elif y > 15 and dist_from_center < 8:
                    canvas[body_y][body_x] = SLIME_LIGHT
                # Left side
                elif x < 0:
                    canvas[body_y][body_x] = SLIME_MID
                # Right side
                elif x > 8:
                    canvas[body_y][body_x] = SLIME_DARK
                # Center
                else:
                    canvas[body_y][body_x] = SLIME_CORE
    
    # === FRONT EXTENSION (pseudopod reaching) ===
    for ext in range(10):
        ext_x = center_x - 12 - ext
        ext_y = center_y - 2 + ext // 3
        ext_height = 4 - ext // 4
        
        for ey in range(-ext_height, ext_height + 1):
            e_x = ext_x
            e_y = ext_y + ey
            if 0 <= e_x < width and 0 <= e_y < height:
                if abs(ey) == ext_height or ext == 9:
                    canvas[e_y][e_x] = SLIME_EDGE
                elif ey < 0:
                    canvas[e_y][e_x] = SLIME_MID
                else:
                    canvas[e_y][e_x] = SLIME_LIGHT
    
    # === LARGE SHINE SPOT (top, shifted for angle) ===
    shine_positions = [
        (center_x - 12, center_y - 18), (center_x - 11, center_y - 18),
        (center_x - 13, center_y - 17), (center_x - 12, center_y - 17), (center_x - 11, center_y - 17), (center_x - 10, center_y - 17),
        (center_x - 12, center_y - 16), (center_x - 11, center_y - 16), (center_x - 10, center_y - 16),
        (center_x - 11, center_y - 15)
    ]
    
    for sx, sy in shine_positions:
        if 0 <= sx < width and 0 <= sy < height:
            canvas[sy][sx] = SHINE_BRIGHT
    
    # Shine glow
    shine_glow_positions = [
        (center_x - 14, center_y - 18), (center_x - 14, center_y - 17), (center_x - 14, center_y - 16),
        (center_x - 13, center_y - 19), (center_x - 12, center_y - 19), (center_x - 11, center_y - 19),
        (center_x - 10, center_y - 18), (center_x - 9, center_y - 17), (center_x - 9, center_y - 16)
    ]
    
    for sx, sy in shine_glow_positions:
        if 0 <= sx < width and 0 <= sy < height:
            if canvas[sy][sx][3] < 200:
                canvas[sy][sx] = SHINE_GLOW
    
    # === INTERNAL BUBBLES (distorted from motion) ===
    # Large bubble
    large_bubble_x = center_x - 8
    large_bubble_y = center_y - 6
    
    for by in range(6):
        bubble_width = 3 - by // 3
        for bx in range(-bubble_width, bubble_width + 1):
            b_x = large_bubble_x + bx
            b_y = large_bubble_y - by
            if 0 <= b_x < width and 0 <= b_y < height:
                if by == 0 or abs(bx) == bubble_width:
                    canvas[b_y][b_x] = BUBBLE_EDGE
                elif by < 2:
                    canvas[b_y][b_x] = BUBBLE_BRIGHT
                else:
                    canvas[b_y][b_x] = BUBBLE_LIGHT
    
    # Medium bubbles
    med_bubble_positions = [(center_x + 6, center_y - 4), (center_x - 3, center_y + 2)]
    
    for mbx, mby in med_bubble_positions:
        for by in range(3):
            bubble_width = 2 - by // 2
            for bx in range(-bubble_width, bubble_width + 1):
                b_x = mbx + bx
                b_y = mby - by
                if 0 <= b_x < width and 0 <= b_y < height:
                    if by == 0 or abs(bx) == bubble_width:
                        canvas[b_y][b_x] = BUBBLE_EDGE
                    else:
                        canvas[b_y][b_x] = BUBBLE_LIGHT
    
    # Small bubbles
    small_bubble_positions = [
        (center_x - 14, center_y - 10), (center_x + 8, center_y - 12),
        (center_x + 2, center_y + 4), (center_x + 10, center_y - 2),
        (center_x - 6, center_y - 14)
    ]
    
    for sbx, sby in small_bubble_positions:
        if 0 <= sbx < width and 0 <= sby < height:
            canvas[sby][sbx] = BUBBLE_BRIGHT
    
    # === EYES (determined expression) ===
    eye_y = center_y - 10
    left_eye_x = center_x - 8
    right_eye_x = center_x + 4
    
    for eye_x in [left_eye_x, right_eye_x]:
        # Outer ring (slightly narrowed for determination)
        for ey in range(-3, 3):
            for ex in range(-3, 4):
                e_x = eye_x + ex
                e_y = eye_y + ey
                if 0 <= e_x < width and 0 <= e_y < height:
                    dist = (ex ** 2 + ey ** 2) ** 0.5
                    if 2.3 < dist < 3.5:
                        canvas[e_y][e_x] = EYE_OUTER
                    elif dist <= 2.3:
                        if dist < 1.5:
                            # Pupil (looking forward)
                            if ex < 0:
                                canvas[e_y][e_x] = EYE_PUPIL
                            else:
                                canvas[e_y][e_x] = EYE_IRIS
                        else:
                            canvas[e_y][e_x] = EYE_WHITE
        
        # Eye shine
        if 0 <= eye_x - 1 < width and 0 <= eye_y - 2 < height:
            canvas[eye_y - 2][eye_x - 1] = EYE_SHINE
    
    # === MOUTH (determined/attacking expression) ===
    mouth_y = center_y - 3
    
    # Oval attacking mouth
    mouth_positions = [
        (center_x - 6, mouth_y), (center_x - 5, mouth_y - 1), (center_x - 4, mouth_y - 1),
        (center_x - 3, mouth_y - 1), (center_x - 2, mouth_y - 1), (center_x - 1, mouth_y - 1),
        (center_x, mouth_y - 1), (center_x + 1, mouth_y),
        (center_x - 5, mouth_y + 1), (center_x - 4, mouth_y + 2), (center_x - 3, mouth_y + 2),
        (center_x - 2, mouth_y + 2), (center_x - 1, mouth_y + 1), (center_x, mouth_y + 1)
    ]
    
    for mx, my in mouth_positions:
        if 0 <= mx < width and 0 <= my < height:
            canvas[my][mx] = MOUTH_LINE
    
    # Mouth interior shadow
    for mx in range(center_x - 4, center_x):
        for my in range(mouth_y, mouth_y + 2):
            if 0 <= mx < width and 0 <= my < height:
                if canvas[my][mx][3] == 0:
                    canvas[my][mx] = MOUTH_SHADOW
    
    # === MOTION BLUR (trailing behind) ===
    for mb in range(12):
        blur_x = center_x + 15 + mb
        blur_y = center_y - 5 + mb // 4
        blur_height = 8 - mb // 3
        
        for by in range(-blur_height, blur_height + 1):
            b_x = blur_x
            b_y = blur_y + by
            if 0 <= b_x < width and 0 <= b_y < height:
                if canvas[b_y][b_x][3] == 0:
                    canvas[b_y][b_x] = MOTION_BLUR
    
    # === SMALL SHINE SPOTS ===
    tiny_shine_positions = [
        (center_x - 16, center_y - 12), (center_x + 10, center_y - 14),
        (center_x - 4, center_y + 3), (center_x + 8, center_y),
        (center_x - 8, center_y - 20)
    ]
    
    for tsx, tsy in tiny_shine_positions:
        if 0 <= tsx < width and 0 <= tsy < height:
            canvas[tsy][tsx] = SHINE_BRIGHT
    
    return canvas


def main():
    print("Creating Slime monster images...")
    
    # Create both poses
    slime_default = create_slime_default()
    slime_attack = create_slime_attack()
    
    # Scale up 4x (64x64 -> 256x256) using nearest neighbor
    img_default = Image.fromarray(slime_default, 'RGBA')
    img_default = img_default.resize((256, 256), Image.Resampling.NEAREST)
    img_default.save('art/slime_monster.png')
    print("✓ Saved: art/slime_monster.png (256x256)")
    
    img_attack = Image.fromarray(slime_attack, 'RGBA')
    img_attack = img_attack.resize((256, 256), Image.Resampling.NEAREST)
    img_attack.save('art/slime_monster_attack.png')
    print("✓ Saved: art/slime_monster_attack.png (256x256)")
    
    print("\n✅ Slime monster creation complete!")
    print("\nFeatures:")
    print("- Default: Cute blob sitting with round eyes and smile, internal bubbles")
    print("- Attack: Lunging forward with determined face, pseudopod reaching, motion blur")
    print("\nStyle: Gelatinous translucent blob")
    print("Colors: Turquoise/cyan with bubbles, shine spots, and glowing highlights")


if __name__ == "__main__":
    main()
