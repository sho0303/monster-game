"""
Create pixel art caveman monster images
Inspired by barbaric warrior with spear and skull trophy
"""
from PIL import Image
import numpy as np

def create_caveman_default():
    """Create caveman standing ready with spear"""
    width = 64
    height = 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette - barbaric caveman theme
    SKIN_TAN = [160, 120, 90, 255]          # Tan skin
    SKIN_DARK = [120, 90, 70, 255]          # Dark tan
    SKIN_LIGHT = [190, 150, 110, 255]       # Light tan
    
    HAIR_BROWN = [60, 45, 35, 255]          # Dark brown hair
    HAIR_DARK = [40, 30, 25, 255]           # Darker brown
    HAIR_LIGHT = [80, 60, 45, 255]          # Lighter brown
    
    FUR_DARK = [70, 60, 50, 255]            # Dark fur clothing
    FUR_LIGHT = [100, 85, 70, 255]          # Light fur
    FUR_SHADOW = [50, 45, 40, 255]          # Fur shadow
    
    BLOOD_RED = [140, 30, 30, 255]          # Blood stains
    BLOOD_DARK = [100, 20, 20, 255]         # Dark blood
    
    BONE_WHITE = [220, 210, 195, 255]       # Bone/skull
    BONE_SHADOW = [180, 170, 155, 255]      # Bone shadow
    
    SPEAR_WOOD = [100, 75, 50, 255]         # Wooden spear
    SPEAR_DARK = [70, 55, 40, 255]          # Dark wood
    STONE_GRAY = [120, 115, 110, 255]       # Stone spearhead
    
    HORN_CREAM = [200, 190, 170, 255]       # Horns
    HORN_DARK = [160, 150, 135, 255]        # Horn shadow
    
    EYE_DARK = [30, 25, 20, 255]            # Eyes
    
    center_x = 32
    base_y = 62
    
    # === FEET (bare, large) ===
    left_foot_x = center_x - 6
    right_foot_x = center_x + 6
    
    for foot_x in [left_foot_x, right_foot_x]:
        for y in range(base_y - 4, base_y):
            for x in range(foot_x - 4, foot_x + 4):
                if 0 <= x < width and 0 <= y < height:
                    canvas[y][x] = SKIN_DARK if x < foot_x else SKIN_TAN
    
    # === LEGS (muscular with fur wraps) ===
    # Left leg
    for y in range(base_y - 18, base_y - 4):
        leg_width = 4 if y < base_y - 10 else 5
        for x in range(left_foot_x - leg_width, left_foot_x + leg_width):
            if 0 <= x < width and 0 <= y < height:
                canvas[y][x] = SKIN_TAN if x < left_foot_x else SKIN_LIGHT
    
    # Right leg
    for y in range(base_y - 18, base_y - 4):
        leg_width = 4 if y < base_y - 10 else 5
        for x in range(right_foot_x - leg_width, right_foot_x + leg_width):
            if 0 <= x < width and 0 <= y < height:
                canvas[y][x] = SKIN_TAN if x < right_foot_x else SKIN_LIGHT
    
    # Fur wraps on legs
    for wrap_y in [base_y - 16, base_y - 8]:
        for x in range(left_foot_x - 5, left_foot_x + 5):
            if 0 <= x < width and 0 <= wrap_y < height:
                for dy in range(3):
                    if 0 <= wrap_y + dy < height:
                        canvas[wrap_y + dy][x] = FUR_DARK if dy == 1 else FUR_SHADOW
        
        for x in range(right_foot_x - 5, right_foot_x + 5):
            if 0 <= x < width and 0 <= wrap_y < height:
                for dy in range(3):
                    if 0 <= wrap_y + dy < height:
                        canvas[wrap_y + dy][x] = FUR_DARK if dy == 1 else FUR_SHADOW
    
    # === LOINCLOTH (fur with blood stains) ===
    loin_y = base_y - 20
    for dy in range(8):
        cloth_width = 8 - abs(dy - 4) // 2
        for dx in range(-cloth_width, cloth_width + 1):
            lx = center_x + dx
            ly = loin_y + dy
            if 0 <= lx < width and 0 <= ly < height:
                if dy < 3:
                    canvas[ly][lx] = FUR_LIGHT if abs(dx) < 3 else FUR_DARK
                else:
                    canvas[ly][lx] = FUR_DARK if abs(dx) % 2 == 0 else FUR_SHADOW
                
                # Blood stains
                if dy > 2 and abs(dx) < 4 and (dx + dy) % 3 == 0:
                    canvas[ly][lx] = BLOOD_DARK
    
    # === TORSO (muscular, bare chest) ===
    torso_y = base_y - 34
    
    for dy in range(-10, 12):
        body_width = 11 - abs(dy) // 3
        for dx in range(-body_width, body_width + 1):
            tx = center_x + dx
            ty = torso_y + dy
            if 0 <= tx < width and 0 <= ty < height:
                if abs(dx) < 3:
                    canvas[ty][tx] = SKIN_LIGHT
                elif dx < 0:
                    canvas[ty][tx] = SKIN_DARK
                else:
                    canvas[ty][tx] = SKIN_TAN
    
    # Muscle definition
    for muscle_y in [torso_y - 4, torso_y + 2, torso_y + 8]:
        for x in range(center_x - 6, center_x + 7):
            if 0 <= x < width and 0 <= muscle_y < height:
                if abs(x - center_x) > 1:
                    canvas[muscle_y][x] = SKIN_DARK
    
    # Fur shoulder piece
    shoulder_y = torso_y - 8
    for dy in range(6):
        for dx in range(-10, 11):
            if abs(dx) > 5 or dy < 2:
                sx = center_x + dx
                sy = shoulder_y + dy
                if 0 <= sx < width and 0 <= sy < height:
                    canvas[sy][sx] = FUR_LIGHT if dy % 2 == 0 else FUR_DARK
    
    # === LEFT ARM (holding spear) ===
    arm_y = torso_y - 2
    left_arm_x = center_x - 10
    
    for dy in range(0, 16):
        for dx in range(-3, 4):
            ax = left_arm_x + dx
            ay = arm_y + dy
            if 0 <= ax < width and 0 <= ay < height:
                canvas[ay][ax] = SKIN_TAN if dx > 0 else SKIN_DARK
    
    # Hand
    hand_y = arm_y + 16
    for dy in range(4):
        for dx in range(-3, 4):
            hx = left_arm_x + dx
            hy = hand_y + dy
            if 0 <= hx < width and 0 <= hy < height:
                canvas[hy][hx] = SKIN_TAN if abs(dx) < 2 else SKIN_DARK
    
    # Spear in hand
    spear_x = left_arm_x
    for i in range(35):
        sy = hand_y - i
        if 0 <= spear_x < width and 0 <= sy < height and sy >= 5:
            if i < 8:
                # Stone spearhead
                canvas[sy][spear_x] = STONE_GRAY
                if spear_x - 1 >= 0:
                    canvas[sy][spear_x - 1] = STONE_GRAY
                if i < 6 and spear_x + 1 < width:
                    canvas[sy][spear_x + 1] = STONE_GRAY
                # Blood on spearhead
                if i > 2 and i < 6:
                    canvas[sy][spear_x] = BLOOD_RED
            else:
                # Wooden shaft
                canvas[sy][spear_x] = SPEAR_WOOD if i % 3 != 0 else SPEAR_DARK
    
    # === RIGHT ARM (holding skull trophy) ===
    right_arm_x = center_x + 10
    
    for dy in range(0, 12):
        for dx in range(-3, 4):
            ax = right_arm_x + dx
            ay = arm_y + dy
            if 0 <= ax < width and 0 <= ay < height:
                canvas[ay][ax] = SKIN_DARK if dx < 0 else SKIN_TAN
    
    # Hand holding skull
    hand_x = right_arm_x
    hand_y = arm_y + 12
    for dy in range(3):
        for dx in range(-2, 3):
            hx = hand_x + dx
            hy = hand_y + dy
            if 0 <= hx < width and 0 <= hy < height:
                canvas[hy][hx] = SKIN_TAN
    
    # Skull trophy
    skull_x = hand_x + 2
    skull_y = hand_y + 4
    
    for dy in range(-5, 6):
        for dx in range(-4, 5):
            if abs(dx) + abs(dy) < 7:
                skx = skull_x + dx
                sky = skull_y + dy
                if 0 <= skx < width and 0 <= sky < height:
                    canvas[sky][skx] = BONE_WHITE if abs(dx) < 3 else BONE_SHADOW
    
    # Skull eye sockets
    for eye_dx in [-2, 2]:
        for dy in range(-2, 1):
            for dx in range(-1, 2):
                ex = skull_x + eye_dx + dx
                ey = skull_y + dy
                if 0 <= ex < width and 0 <= ey < height:
                    if abs(dx) + abs(dy) < 2:
                        canvas[ey][ex] = EYE_DARK
    
    # Small horns on skull
    for horn_dx in [-4, 4]:
        for i in range(4):
            hx = skull_x + horn_dx + (i // 2 if horn_dx < 0 else -i // 2)
            hy = skull_y - 5 - i
            if 0 <= hx < width and 0 <= hy < height:
                canvas[hy][hx] = HORN_CREAM if i < 2 else HORN_DARK
    
    # === HEAD (bearded, wild hair) ===
    head_y = torso_y - 16
    
    # Wild hair/beard
    for dy in range(-10, 8):
        for dx in range(-9, 10):
            dist = (dx * dx * 0.7 + dy * dy) ** 0.5
            if dist < 10:
                hx = center_x + dx
                hy = head_y + dy
                if 0 <= hx < width and 0 <= hy < height:
                    if abs(dx) > 6 or dy < -6 or (dy > 3 and abs(dx) > 3):
                        # Hair/beard
                        canvas[hy][hx] = HAIR_BROWN if dist < 8 else HAIR_DARK
                    elif dy > -5 and abs(dx) < 6:
                        # Face
                        canvas[hy][hx] = SKIN_TAN if abs(dx) < 3 else SKIN_DARK
    
    # Eyes (fierce)
    for eye_dx in [-3, 3]:
        for dy in range(-2, 1):
            for dx in range(-1, 2):
                ex = center_x + eye_dx + dx
                ey = head_y + dy
                if 0 <= ex < width and 0 <= ey < height:
                    if abs(dx) + abs(dy) < 2:
                        canvas[ey][ex] = EYE_DARK
    
    # Nose
    for dy in range(2):
        if 0 <= center_x < width and 0 <= head_y + 1 + dy < height:
            canvas[head_y + 1 + dy][center_x] = SKIN_DARK
    
    # Mouth (grimace)
    for x in range(center_x - 2, center_x + 3):
        if 0 <= x < width and 0 <= head_y + 4 < height:
            canvas[head_y + 4][x] = HAIR_DARK
    
    # Horned headpiece
    for horn_side in [-1, 1]:
        for i in range(8):
            horn_x = center_x + horn_side * (6 + i // 2)
            horn_y = head_y - 8 - i
            if 0 <= horn_x < width and 0 <= horn_y < height:
                canvas[horn_y][horn_x] = HORN_CREAM if i < 5 else HORN_DARK
                if horn_x + horn_side >= 0 and horn_x + horn_side < width:
                    canvas[horn_y][horn_x + horn_side] = HORN_CREAM if i < 5 else HORN_DARK
    
    return canvas


def create_caveman_attack():
    """Create caveman attack animation - spear thrust"""
    width = 64
    height = 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Same color palette
    SKIN_TAN = [160, 120, 90, 255]
    SKIN_DARK = [120, 90, 70, 255]
    SKIN_LIGHT = [190, 150, 110, 255]
    
    HAIR_BROWN = [60, 45, 35, 255]
    HAIR_DARK = [40, 30, 25, 255]
    
    FUR_DARK = [70, 60, 50, 255]
    FUR_LIGHT = [100, 85, 70, 255]
    FUR_SHADOW = [50, 45, 40, 255]
    
    BLOOD_RED = [140, 30, 30, 255]
    BLOOD_DARK = [100, 20, 20, 255]
    
    SPEAR_WOOD = [100, 75, 50, 255]
    SPEAR_DARK = [70, 55, 40, 255]
    STONE_GRAY = [120, 115, 110, 255]
    
    HORN_CREAM = [200, 190, 170, 255]
    HORN_DARK = [160, 150, 135, 255]
    
    EYE_DARK = [30, 25, 20, 255]
    
    MOTION_BLUR = [140, 120, 100, 100]
    
    center_x = 32
    base_y = 62
    
    # === FEET ===
    left_foot_x = center_x - 6
    right_foot_x = center_x + 6
    
    for foot_x in [left_foot_x, right_foot_x]:
        for y in range(base_y - 4, base_y):
            for x in range(foot_x - 4, foot_x + 4):
                if 0 <= x < width and 0 <= y < height:
                    canvas[y][x] = SKIN_DARK if x < foot_x else SKIN_TAN
    
    # === LEGS ===
    for y in range(base_y - 18, base_y - 4):
        leg_width = 4 if y < base_y - 10 else 5
        for x in range(left_foot_x - leg_width, left_foot_x + leg_width):
            if 0 <= x < width and 0 <= y < height:
                canvas[y][x] = SKIN_TAN if x < left_foot_x else SKIN_LIGHT
    
    for y in range(base_y - 18, base_y - 4):
        leg_width = 4 if y < base_y - 10 else 5
        for x in range(right_foot_x - leg_width, right_foot_x + leg_width):
            if 0 <= x < width and 0 <= y < height:
                canvas[y][x] = SKIN_TAN if x < right_foot_x else SKIN_LIGHT
    
    # Fur wraps
    for wrap_y in [base_y - 16, base_y - 8]:
        for x in range(left_foot_x - 5, left_foot_x + 5):
            if 0 <= x < width and 0 <= wrap_y < height:
                for dy in range(3):
                    if 0 <= wrap_y + dy < height:
                        canvas[wrap_y + dy][x] = FUR_DARK if dy == 1 else FUR_SHADOW
        
        for x in range(right_foot_x - 5, right_foot_x + 5):
            if 0 <= x < width and 0 <= wrap_y < height:
                for dy in range(3):
                    if 0 <= wrap_y + dy < height:
                        canvas[wrap_y + dy][x] = FUR_DARK if dy == 1 else FUR_SHADOW
    
    # === LOINCLOTH ===
    loin_y = base_y - 20
    for dy in range(8):
        cloth_width = 8 - abs(dy - 4) // 2
        for dx in range(-cloth_width, cloth_width + 1):
            lx = center_x + dx
            ly = loin_y + dy
            if 0 <= lx < width and 0 <= ly < height:
                if dy < 3:
                    canvas[ly][lx] = FUR_LIGHT if abs(dx) < 3 else FUR_DARK
                else:
                    canvas[ly][lx] = FUR_DARK if abs(dx) % 2 == 0 else FUR_SHADOW
                
                if dy > 2 and abs(dx) < 4 and (dx + dy) % 3 == 0:
                    canvas[ly][lx] = BLOOD_DARK
    
    # === TORSO ===
    torso_y = base_y - 34
    
    for dy in range(-10, 12):
        body_width = 11 - abs(dy) // 3
        for dx in range(-body_width, body_width + 1):
            tx = center_x + dx
            ty = torso_y + dy
            if 0 <= tx < width and 0 <= ty < height:
                if abs(dx) < 3:
                    canvas[ty][tx] = SKIN_LIGHT
                elif dx < 0:
                    canvas[ty][tx] = SKIN_DARK
                else:
                    canvas[ty][tx] = SKIN_TAN
    
    # Muscle definition
    for muscle_y in [torso_y - 4, torso_y + 2, torso_y + 8]:
        for x in range(center_x - 6, center_x + 7):
            if 0 <= x < width and 0 <= muscle_y < height:
                if abs(x - center_x) > 1:
                    canvas[muscle_y][x] = SKIN_DARK
    
    # Fur shoulder
    shoulder_y = torso_y - 8
    for dy in range(6):
        for dx in range(-10, 11):
            if abs(dx) > 5 or dy < 2:
                sx = center_x + dx
                sy = shoulder_y + dy
                if 0 <= sx < width and 0 <= sy < height:
                    canvas[sy][sx] = FUR_LIGHT if dy % 2 == 0 else FUR_DARK
    
    # === LEFT ARM (thrusting spear forward) ===
    arm_y = torso_y - 2
    left_arm_x = center_x - 10
    
    # Arm extending forward and down
    for i in range(18):
        ax = left_arm_x - i // 2
        ay = arm_y + i
        for dx in range(-3, 4):
            px = ax + dx
            if 0 <= px < width and 0 <= ay < height:
                canvas[ay][px] = SKIN_TAN if dx > 0 else SKIN_DARK
    
    # Hand position
    hand_x = left_arm_x - 9
    hand_y = arm_y + 18
    
    for dy in range(4):
        for dx in range(-3, 4):
            hx = hand_x + dx
            hy = hand_y + dy
            if 0 <= hx < width and 0 <= hy < height:
                canvas[hy][hx] = SKIN_TAN if abs(dx) < 2 else SKIN_DARK
    
    # Spear thrusting diagonally
    spear_x = hand_x - 2
    spear_y = hand_y
    
    for i in range(25):
        sx = spear_x - i // 2
        sy = spear_y + i
        if 0 <= sx < width and 0 <= sy < height:
            if i < 8:
                # Stone spearhead with blood
                canvas[sy][sx] = BLOOD_RED if i > 2 else STONE_GRAY
                if sx - 1 >= 0 and i < 6:
                    canvas[sy][sx - 1] = STONE_GRAY
                if sx + 1 < width and i < 6:
                    canvas[sy][sx + 1] = STONE_GRAY
            else:
                # Wooden shaft
                canvas[sy][sx] = SPEAR_WOOD if i % 3 != 0 else SPEAR_DARK
    
    # Motion blur
    for i in range(6):
        mx = hand_x + i
        my = hand_y - i * 2
        if 0 <= mx < width and 0 <= my < height:
            canvas[my][mx] = MOTION_BLUR
    
    # === RIGHT ARM (pulling back) ===
    right_arm_x = center_x + 10
    
    for dy in range(0, 12):
        for dx in range(-3, 4):
            ax = right_arm_x + dx
            ay = arm_y + dy
            if 0 <= ax < width and 0 <= ay < height:
                canvas[ay][ax] = SKIN_DARK if dx < 0 else SKIN_TAN
    
    # Hand clenched
    hand_x = right_arm_x
    hand_y = arm_y + 12
    for dy in range(3):
        for dx in range(-2, 3):
            hx = hand_x + dx
            hy = hand_y + dy
            if 0 <= hx < width and 0 <= hy < height:
                canvas[hy][hx] = SKIN_TAN if abs(dx) < 2 else SKIN_DARK
    
    # === HEAD ===
    head_y = torso_y - 16
    
    # Wild hair/beard
    for dy in range(-10, 8):
        for dx in range(-9, 10):
            dist = (dx * dx * 0.7 + dy * dy) ** 0.5
            if dist < 10:
                hx = center_x + dx
                hy = head_y + dy
                if 0 <= hx < width and 0 <= hy < height:
                    if abs(dx) > 6 or dy < -6 or (dy > 3 and abs(dx) > 3):
                        canvas[hy][hx] = HAIR_BROWN if dist < 8 else HAIR_DARK
                    elif dy > -5 and abs(dx) < 6:
                        canvas[hy][hx] = SKIN_TAN if abs(dx) < 3 else SKIN_DARK
    
    # Eyes (intense)
    for eye_dx in [-3, 3]:
        for dy in range(-2, 1):
            for dx in range(-1, 2):
                ex = center_x + eye_dx + dx
                ey = head_y + dy
                if 0 <= ex < width and 0 <= ey < height:
                    if abs(dx) + abs(dy) < 2:
                        canvas[ey][ex] = EYE_DARK
    
    # Nose
    for dy in range(2):
        if 0 <= center_x < width and 0 <= head_y + 1 + dy < height:
            canvas[head_y + 1 + dy][center_x] = SKIN_DARK
    
    # Mouth (battle cry)
    for x in range(center_x - 3, center_x + 4):
        if 0 <= x < width and 0 <= head_y + 4 < height:
            canvas[head_y + 4][x] = HAIR_DARK
            if head_y + 5 < height:
                canvas[head_y + 5][x] = EYE_DARK
    
    # Horned headpiece
    for horn_side in [-1, 1]:
        for i in range(8):
            horn_x = center_x + horn_side * (6 + i // 2)
            horn_y = head_y - 8 - i
            if 0 <= horn_x < width and 0 <= horn_y < height:
                canvas[horn_y][horn_x] = HORN_CREAM if i < 5 else HORN_DARK
                if horn_x + horn_side >= 0 and horn_x + horn_side < width:
                    canvas[horn_y][horn_x + horn_side] = HORN_CREAM if i < 5 else HORN_DARK
    
    return canvas


def main():
    """Create and save caveman monster images"""
    print("Creating caveman monster images...")
    
    # Create both images
    caveman_default = create_caveman_default()
    caveman_attack = create_caveman_attack()
    
    # Convert to PIL and scale up
    scale = 4
    
    # Default pose
    img_default = Image.fromarray(caveman_default, 'RGBA')
    img_default_scaled = img_default.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_default_scaled.save('caveman_monster.png')
    print(f"✓ Saved: caveman_monster.png ({64 * scale}x{64 * scale})")
    
    # Attack animation
    img_attack = Image.fromarray(caveman_attack, 'RGBA')
    img_attack_scaled = img_attack.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_attack_scaled.save('caveman_monster_attack.png')
    print(f"✓ Saved: caveman_monster_attack.png ({64 * scale}x{64 * scale})")
    
    print("\n✅ Caveman monster creation complete!")
    print("\nFeatures:")
    print("- Default: Barbaric caveman with spear and skull trophy")
    print("- Attack: Aggressive spear thrust with motion blur")
    print("\nStyle: Pixel art inspired by barbaric warrior")
    print("Colors: Tan skin, dark fur, brown hair, bone trophy, bloody spear")


if __name__ == '__main__':
    main()
