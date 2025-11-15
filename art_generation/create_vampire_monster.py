"""
Create pixel art Vampire monster images
Inspired by dark vampire lord with flowing cape and supernatural powers
"""
from PIL import Image
import numpy as np

def create_vampire_default():
    """Create vampire in standing pose with cape and aristocratic stance"""
    width = 64
    height = 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette - vampire lord theme
    SKIN_PALE = [220, 215, 210, 255]          # Pale vampire skin
    SKIN_SHADOW = [180, 175, 170, 255]        # Skin shadow
    SKIN_DARK = [140, 135, 130, 255]          # Dark skin shadow
    
    HAIR_BLACK = [20, 20, 25, 255]            # Black hair
    HAIR_DARK = [35, 35, 40, 255]             # Dark hair highlight
    
    CAPE_BLACK = [15, 15, 20, 255]            # Black cape outer
    CAPE_DARK = [25, 25, 30, 255]             # Cape shadow
    CAPE_RED = [120, 20, 25, 255]             # Red cape lining
    CAPE_RED_DARK = [80, 15, 20, 255]         # Dark red
    
    VEST_PURPLE = [60, 30, 70, 255]           # Purple vest
    VEST_DARK = [40, 20, 50, 255]             # Dark purple
    
    SHIRT_WHITE = [240, 235, 230, 255]        # White shirt
    SHIRT_SHADOW = [200, 195, 190, 255]       # Shirt shadow
    
    PANTS_BLACK = [20, 20, 25, 255]           # Black pants
    
    BOOT_BLACK = [15, 15, 20, 255]            # Black boots
    
    EYE_RED = [200, 40, 40, 255]              # Red glowing eyes
    EYE_DARK = [120, 20, 20, 255]             # Dark red
    
    FANG_WHITE = [240, 235, 230, 255]         # White fangs
    
    COLLAR_DARK = [10, 10, 15, 255]           # Dark collar
    
    center_x = 32
    base_y = 60
    
    # === CAPE (flowing behind) ===
    # Left cape wing
    for cy in range(20):
        cape_width = 8 + cy // 3
        for cx in range(cape_width):
            cape_x = center_x - 8 - cx
            cape_y = base_y - 45 + cy
            if 0 <= cape_x < width and 0 <= cape_y < height:
                if cx < 2:
                    canvas[cape_y][cape_x] = CAPE_RED if cy % 2 == 0 else CAPE_RED_DARK
                else:
                    canvas[cape_y][cape_x] = CAPE_BLACK if cx % 2 == 0 else CAPE_DARK
    
    # Right cape wing
    for cy in range(20):
        cape_width = 8 + cy // 3
        for cx in range(cape_width):
            cape_x = center_x + 8 + cx
            cape_y = base_y - 45 + cy
            if 0 <= cape_x < width and 0 <= cape_y < height:
                if cx < 2:
                    canvas[cape_y][cape_x] = CAPE_RED if cy % 2 == 0 else CAPE_RED_DARK
                else:
                    canvas[cape_y][cape_x] = CAPE_BLACK if cx % 2 == 0 else CAPE_DARK
    
    # Cape collar/shoulders
    for cy in range(8):
        for cx in range(-10, 11):
            collar_y = base_y - 38 + cy
            collar_x = center_x + cx
            if 0 <= collar_x < width and 0 <= collar_y < height:
                if abs(cx) > 5:
                    canvas[collar_y][collar_x] = COLLAR_DARK if cy < 3 else CAPE_BLACK
    
    # === BOOTS ===
    # Left boot
    for dy in range(6):
        for dx in range(-3, 4):
            boot_x = center_x - 4 + dx
            boot_y = base_y + dy
            if 0 <= boot_x < width and 0 <= boot_y < height:
                canvas[boot_y][boot_x] = BOOT_BLACK if dx < 0 else CAPE_DARK
    
    # Right boot
    for dy in range(6):
        for dx in range(-3, 4):
            boot_x = center_x + 4 + dx
            boot_y = base_y + dy
            if 0 <= boot_x < width and 0 <= boot_y < height:
                canvas[boot_y][boot_x] = BOOT_BLACK if dx < 0 else CAPE_DARK
    
    # === LEGS ===
    for dy in range(18):
        leg_width = 3
        # Left leg
        for dx in range(-leg_width, leg_width + 1):
            leg_x = center_x - 4 + dx
            leg_y = base_y - 6 + dy
            if 0 <= leg_x < width and 0 <= leg_y < height:
                canvas[leg_y][leg_x] = PANTS_BLACK
        
        # Right leg
        for dx in range(-leg_width, leg_width + 1):
            leg_x = center_x + 4 + dx
            leg_y = base_y - 6 + dy
            if 0 <= leg_x < width and 0 <= leg_y < height:
                canvas[leg_y][leg_x] = PANTS_BLACK
    
    # === TORSO ===
    torso_y = base_y - 28
    
    # Vest
    for dy in range(12):
        torso_width = 7 - dy // 5
        for dx in range(-torso_width, torso_width + 1):
            tx = center_x + dx
            ty = torso_y + dy
            if 0 <= tx < width and 0 <= ty < height:
                if abs(dx) < 3:
                    # Shirt front
                    canvas[ty][tx] = SHIRT_WHITE if abs(dx) < 2 else SHIRT_SHADOW
                else:
                    # Vest
                    canvas[ty][tx] = VEST_PURPLE if dx < 0 else VEST_DARK
    
    # Cape front drape
    for dy in range(15):
        for dx in [-8, -7, 7, 8]:
            drape_x = center_x + dx
            drape_y = torso_y + dy
            if 0 <= drape_x < width and 0 <= drape_y < height:
                canvas[drape_y][drape_x] = CAPE_BLACK if abs(dx) == 8 else CAPE_DARK
    
    # === ARMS ===
    # Left arm (slightly forward)
    for dy in range(14):
        for dx in range(-2, 3):
            arm_x = center_x - 8 + dx
            arm_y = torso_y + 2 + dy
            if 0 <= arm_x < width and 0 <= arm_y < height:
                if dy > 8:
                    # Hand/sleeve
                    canvas[arm_y][arm_x] = CAPE_BLACK
                else:
                    # Upper arm
                    canvas[arm_y][arm_x] = CAPE_BLACK if dx < 0 else CAPE_DARK
    
    # Left hand (pale skin)
    for dy in range(4):
        for dx in range(-2, 3):
            hand_x = center_x - 8 + dx
            hand_y = torso_y + 16 + dy
            if 0 <= hand_x < width and 0 <= hand_y < height:
                if abs(dx) + abs(dy) < 4:
                    canvas[hand_y][hand_x] = SKIN_PALE if dx > 0 else SKIN_SHADOW
    
    # Clawed fingers (left hand)
    for fx in [center_x - 9, center_x - 7]:
        for dy in range(2):
            finger_y = torso_y + 20 + dy
            if 0 <= fx < width and 0 <= finger_y < height:
                canvas[finger_y][fx] = SKIN_DARK
    
    # Right arm
    for dy in range(14):
        for dx in range(-2, 3):
            arm_x = center_x + 8 + dx
            arm_y = torso_y + 2 + dy
            if 0 <= arm_x < width and 0 <= arm_y < height:
                if dy > 8:
                    canvas[arm_y][arm_x] = CAPE_BLACK
                else:
                    canvas[arm_y][arm_x] = CAPE_BLACK if dx < 0 else CAPE_DARK
    
    # Right hand
    for dy in range(4):
        for dx in range(-2, 3):
            hand_x = center_x + 8 + dx
            hand_y = torso_y + 16 + dy
            if 0 <= hand_x < width and 0 <= hand_y < height:
                if abs(dx) + abs(dy) < 4:
                    canvas[hand_y][hand_x] = SKIN_PALE if dx > 0 else SKIN_SHADOW
    
    # Clawed fingers (right hand)
    for fx in [center_x + 7, center_x + 9]:
        for dy in range(2):
            finger_y = torso_y + 20 + dy
            if 0 <= fx < width and 0 <= finger_y < height:
                canvas[finger_y][fx] = SKIN_DARK
    
    # === NECK ===
    neck_y = torso_y - 2
    for dy in range(4):
        for dx in range(-2, 3):
            nx = center_x + dx
            ny = neck_y + dy
            if 0 <= nx < width and 0 <= ny < height:
                canvas[ny][nx] = SKIN_PALE if abs(dx) < 2 else SKIN_SHADOW
    
    # === HEAD ===
    head_y = neck_y - 8
    
    # Face
    for dy in range(-6, 8):
        for dx in range(-5, 6):
            if abs(dx) * 1.2 + abs(dy) * 0.9 < 7:
                hx = center_x + dx
                hy = head_y + dy
                if 0 <= hx < width and 0 <= hy < height:
                    if dy < 0:
                        # Upper face
                        canvas[hy][hx] = SKIN_PALE if abs(dx) < 3 else SKIN_SHADOW
                    else:
                        # Lower face
                        canvas[hy][hx] = SKIN_PALE if abs(dx) < 4 else SKIN_SHADOW
    
    # Hair (slicked back, dark)
    for dy in range(8):
        for dx in range(-5, 6):
            if abs(dx) * 1.3 + dy * 0.8 < 8:
                hair_x = center_x + dx
                hair_y = head_y - 6 + dy
                if 0 <= hair_x < width and 0 <= hair_y < height:
                    canvas[hair_y][hair_x] = HAIR_BLACK if dx < 0 else HAIR_DARK
    
    # Eyes (red glowing)
    # Left eye
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            eye_x = center_x - 2 + dx
            eye_y = head_y - 1 + dy
            if 0 <= eye_x < width and 0 <= eye_y < height:
                if abs(dx) + abs(dy) < 2:
                    canvas[eye_y][eye_x] = EYE_RED if dx == 0 and dy == 0 else EYE_DARK
    
    # Right eye
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            eye_x = center_x + 2 + dx
            eye_y = head_y - 1 + dy
            if 0 <= eye_x < width and 0 <= eye_y < height:
                if abs(dx) + abs(dy) < 2:
                    canvas[eye_y][eye_x] = EYE_RED if dx == 0 and dy == 0 else EYE_DARK
    
    # Nose
    for dy in range(2):
        nose_x = center_x
        nose_y = head_y + 1 + dy
        if 0 <= nose_x < width and 0 <= nose_y < height:
            canvas[nose_y][nose_x] = SKIN_DARK
    
    # Mouth (slight smirk with fangs)
    for mx in range(center_x - 2, center_x + 3):
        mouth_y = head_y + 4
        if 0 <= mx < width and 0 <= mouth_y < height:
            canvas[mouth_y][mx] = SKIN_DARK
    
    # Fangs
    fang_y = head_y + 5
    for fx in [center_x - 1, center_x + 1]:
        if 0 <= fx < width and 0 <= fang_y < height:
            canvas[fang_y][fx] = FANG_WHITE
    
    # High collar
    for dy in range(4):
        for dx in [-6, -5, 5, 6]:
            collar_x = center_x + dx
            collar_y = neck_y + 1 + dy
            if 0 <= collar_x < width and 0 <= collar_y < height:
                canvas[collar_y][collar_x] = COLLAR_DARK if abs(dx) == 6 else CAPE_BLACK
    
    return canvas


def create_vampire_attack():
    """Create vampire attack animation - lunging with claws and supernatural energy"""
    width = 64
    height = 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Same color palette
    SKIN_PALE = [220, 215, 210, 255]
    SKIN_SHADOW = [180, 175, 170, 255]
    SKIN_DARK = [140, 135, 130, 255]
    
    HAIR_BLACK = [20, 20, 25, 255]
    HAIR_DARK = [35, 35, 40, 255]
    
    CAPE_BLACK = [15, 15, 20, 255]
    CAPE_DARK = [25, 25, 30, 255]
    CAPE_RED = [120, 20, 25, 255]
    CAPE_RED_DARK = [80, 15, 20, 255]
    
    VEST_PURPLE = [60, 30, 70, 255]
    VEST_DARK = [40, 20, 50, 255]
    
    SHIRT_WHITE = [240, 235, 230, 255]
    SHIRT_SHADOW = [200, 195, 190, 255]
    
    PANTS_BLACK = [20, 20, 25, 255]
    BOOT_BLACK = [15, 15, 20, 255]
    
    EYE_RED = [200, 40, 40, 255]
    EYE_DARK = [120, 20, 20, 255]
    
    FANG_WHITE = [240, 235, 230, 255]
    COLLAR_DARK = [10, 10, 15, 255]
    
    ENERGY_RED = [200, 50, 50, 200]           # Red energy
    ENERGY_DARK = [150, 30, 30, 180]          # Dark energy
    
    center_x = 32
    base_y = 60
    
    # === CAPE (billowing dramatically) ===
    # Left cape wing (swept back)
    for cy in range(22):
        cape_width = 10 + cy // 2
        for cx in range(cape_width):
            cape_x = center_x - 6 - cx
            cape_y = base_y - 48 + cy
            if 0 <= cape_x < width and 0 <= cape_y < height:
                if cx < 3:
                    canvas[cape_y][cape_x] = CAPE_RED if cy % 2 == 0 else CAPE_RED_DARK
                else:
                    canvas[cape_y][cape_x] = CAPE_BLACK if cx % 2 == 0 else CAPE_DARK
    
    # Right cape wing (swept back)
    for cy in range(22):
        cape_width = 10 + cy // 2
        for cx in range(cape_width):
            cape_x = center_x + 6 + cx
            cape_y = base_y - 48 + cy
            if 0 <= cape_x < width and 0 <= cape_y < height:
                if cx < 3:
                    canvas[cape_y][cape_x] = CAPE_RED if cy % 2 == 0 else CAPE_RED_DARK
                else:
                    canvas[cape_y][cape_x] = CAPE_BLACK if cx % 2 == 0 else CAPE_DARK
    
    # === LEGS (in lunge position) ===
    # Left leg forward
    for dy in range(20):
        leg_width = 3
        for dx in range(-leg_width, leg_width + 1):
            leg_x = center_x - 6 + dx
            leg_y = base_y - 8 + dy
            if 0 <= leg_x < width and 0 <= leg_y < height:
                canvas[leg_y][leg_x] = PANTS_BLACK
    
    # Right leg back
    for dy in range(18):
        leg_width = 3
        for dx in range(-leg_width, leg_width + 1):
            leg_x = center_x + 8 + dx
            leg_y = base_y - 6 + dy
            if 0 <= leg_x < width and 0 <= leg_y < height:
                canvas[leg_y][leg_x] = PANTS_BLACK
    
    # Boots
    for boot_offset in [-6, 8]:
        for dy in range(6):
            for dx in range(-3, 4):
                boot_x = center_x + boot_offset + dx
                boot_y = base_y + dy
                if 0 <= boot_x < width and 0 <= boot_y < height:
                    canvas[boot_y][boot_x] = BOOT_BLACK if dx < 0 else CAPE_DARK
    
    # === TORSO (leaning forward) ===
    torso_y = base_y - 28
    
    for dy in range(12):
        torso_width = 7 - dy // 5
        for dx in range(-torso_width, torso_width + 1):
            tx = center_x + dx
            ty = torso_y + dy
            if 0 <= tx < width and 0 <= ty < height:
                if abs(dx) < 3:
                    canvas[ty][tx] = SHIRT_WHITE if abs(dx) < 2 else SHIRT_SHADOW
                else:
                    canvas[ty][tx] = VEST_PURPLE if dx < 0 else VEST_DARK
    
    # === ARMS (reaching forward aggressively) ===
    # Left arm (extended forward with claws)
    for i in range(16):
        for dx in range(-2, 3):
            arm_x = center_x - 10 - i // 2
            arm_y = torso_y + i
            if 0 <= arm_x < width and 0 <= arm_y < height:
                if i > 10:
                    canvas[arm_y][arm_x] = SKIN_PALE if dx > 0 else SKIN_SHADOW
                else:
                    canvas[arm_y][arm_x] = CAPE_BLACK if dx < 0 else CAPE_DARK
    
    # Left hand/claws
    left_hand_x = center_x - 18
    left_hand_y = torso_y + 16
    for dy in range(4):
        for dx in range(-2, 3):
            hx = left_hand_x + dx
            hy = left_hand_y + dy
            if 0 <= hx < width and 0 <= hy < height:
                if abs(dx) + abs(dy) < 4:
                    canvas[hy][hx] = SKIN_PALE if dx > 0 else SKIN_SHADOW
    
    # Claws extended
    for claw_offset in [-2, 0, 2]:
        for dy in range(3):
            claw_x = left_hand_x + claw_offset
            claw_y = left_hand_y + 4 + dy
            if 0 <= claw_x < width and 0 <= claw_y < height:
                canvas[claw_y][claw_x] = SKIN_DARK
    
    # Right arm
    for i in range(16):
        for dx in range(-2, 3):
            arm_x = center_x - 8 - i // 2
            arm_y = torso_y + 2 + i
            if 0 <= arm_x < width and 0 <= arm_y < height:
                if i > 10:
                    canvas[arm_y][arm_x] = SKIN_PALE if dx > 0 else SKIN_SHADOW
                else:
                    canvas[arm_y][arm_x] = CAPE_BLACK if dx < 0 else CAPE_DARK
    
    # Right hand/claws
    right_hand_x = center_x - 16
    right_hand_y = torso_y + 18
    for dy in range(4):
        for dx in range(-2, 3):
            hx = right_hand_x + dx
            hy = right_hand_y + dy
            if 0 <= hx < width and 0 <= hy < height:
                if abs(dx) + abs(dy) < 4:
                    canvas[hy][hx] = SKIN_PALE if dx > 0 else SKIN_SHADOW
    
    # Claws extended
    for claw_offset in [-2, 0, 2]:
        for dy in range(3):
            claw_x = right_hand_x + claw_offset
            claw_y = right_hand_y + 4 + dy
            if 0 <= claw_x < width and 0 <= claw_y < height:
                canvas[claw_y][claw_x] = SKIN_DARK
    
    # === NECK ===
    neck_y = torso_y - 2
    for dy in range(4):
        for dx in range(-2, 3):
            nx = center_x + dx
            ny = neck_y + dy
            if 0 <= nx < width and 0 <= ny < height:
                canvas[ny][nx] = SKIN_PALE if abs(dx) < 2 else SKIN_SHADOW
    
    # === HEAD (fierce expression) ===
    head_y = neck_y - 8
    
    # Face
    for dy in range(-6, 8):
        for dx in range(-5, 6):
            if abs(dx) * 1.2 + abs(dy) * 0.9 < 7:
                hx = center_x + dx
                hy = head_y + dy
                if 0 <= hx < width and 0 <= hy < height:
                    canvas[hy][hx] = SKIN_PALE if abs(dx) < 3 else SKIN_SHADOW
    
    # Hair
    for dy in range(8):
        for dx in range(-5, 6):
            if abs(dx) * 1.3 + dy * 0.8 < 8:
                hair_x = center_x + dx
                hair_y = head_y - 6 + dy
                if 0 <= hair_x < width and 0 <= hair_y < height:
                    canvas[hair_y][hair_x] = HAIR_BLACK if dx < 0 else HAIR_DARK
    
    # Eyes (intense red glow)
    for eye_offset in [-2, 2]:
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                eye_x = center_x + eye_offset + dx
                eye_y = head_y - 1 + dy
                if 0 <= eye_x < width and 0 <= eye_y < height:
                    if abs(dx) + abs(dy) < 2:
                        canvas[eye_y][eye_x] = EYE_RED if dx == 0 and dy == 0 else EYE_DARK
    
    # Mouth (open with fangs)
    for my in range(3):
        for mx in range(center_x - 3, center_x + 4):
            mouth_y = head_y + 3 + my
            if 0 <= mx < width and 0 <= mouth_y < height:
                if my == 0:
                    canvas[mouth_y][mx] = SKIN_DARK
                else:
                    canvas[mouth_y][mx] = HAIR_BLACK
    
    # Large fangs
    for fx in [center_x - 2, center_x + 2]:
        for dy in range(3):
            fang_y = head_y + 5 + dy
            if 0 <= fx < width and 0 <= fang_y < height:
                canvas[fang_y][fx] = FANG_WHITE if dy < 2 else SKIN_SHADOW
    
    # === SUPERNATURAL ENERGY ===
    # Red energy around hands
    for hand_x in [left_hand_x, right_hand_x]:
        for energy_offset in range(8):
            for angle in range(0, 360, 45):
                import math
                ex = int(hand_x + math.cos(math.radians(angle)) * (3 + energy_offset // 2))
                ey = int((left_hand_y if hand_x == left_hand_x else right_hand_y) + 
                        math.sin(math.radians(angle)) * (3 + energy_offset // 2))
                if 0 <= ex < width and 0 <= ey < height:
                    if energy_offset < 4:
                        canvas[ey][ex] = ENERGY_RED
                    elif energy_offset < 6:
                        canvas[ey][ex] = ENERGY_DARK
    
    return canvas


def main():
    """Create and save vampire monster images"""
    print("Creating vampire monster images...")
    
    # Create both images
    vampire_default = create_vampire_default()
    vampire_attack = create_vampire_attack()
    
    # Convert to PIL and scale up
    scale = 4
    
    # Default pose
    img_default = Image.fromarray(vampire_default, 'RGBA')
    img_default_scaled = img_default.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_default_scaled.save('../art/vampire_monster.png')
    print(f"✓ Saved: ../art/vampire_monster.png ({64 * scale}x{64 * scale})")
    
    # Attack animation
    img_attack = Image.fromarray(vampire_attack, 'RGBA')
    img_attack_scaled = img_attack.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_attack_scaled.save('../art/vampire_monster_attack.png')
    print(f"✓ Saved: ../art/vampire_monster_attack.png ({64 * scale}x{64 * scale})")
    
    print("\n✅ Vampire monster creation complete!")
    print("\nFeatures:")
    print("- Default: Aristocratic vampire lord with flowing black cape and red lining")
    print("- Attack: Aggressive lunge with extended claws and supernatural red energy")
    print("\nStyle: Dark fantasy pixel art inspired by classic vampire lord")
    print("Colors: Pale skin, black cape with red lining, purple vest, red glowing eyes")


if __name__ == '__main__':
    main()
