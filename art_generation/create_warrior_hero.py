"""
Create pixel art warrior hero images
Inspired by armored knight with sword and shield
"""
from PIL import Image
import numpy as np
import random

def create_warrior_default():
    """Create warrior standing ready with sword and shield"""
    width = 64
    height = 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette - armored knight theme
    ARMOR_SILVER = [180, 185, 195, 255]      # Silver armor
    ARMOR_DARK = [120, 125, 135, 255]        # Dark silver
    ARMOR_LIGHT = [220, 225, 235, 255]       # Light silver highlights
    
    CAPE_RED = [160, 40, 45, 255]            # Red cape
    CAPE_DARK = [110, 25, 30, 255]           # Dark red
    CAPE_LIGHT = [200, 60, 65, 255]          # Light red
    
    BELT_GOLD = [200, 170, 80, 255]          # Gold belt/trim
    BELT_DARK = [150, 120, 50, 255]          # Dark gold
    
    BOOT_DARK = [40, 40, 45, 255]            # Dark boots
    BOOT_SHADOW = [25, 25, 30, 255]          # Boot shadow
    
    SWORD_STEEL = [160, 170, 180, 255]       # Sword blade
    SWORD_EDGE = [200, 210, 220, 255]        # Sword edge
    HANDLE_BROWN = [80, 60, 40, 255]         # Sword handle
    HANDLE_DARK = [50, 40, 25, 255]          # Handle dark
    
    SHIELD_METAL = [140, 145, 155, 255]      # Shield metal
    SHIELD_RED = [140, 35, 40, 255]          # Shield red design
    
    SKIN_LIGHT = [220, 190, 160, 255]        # Skin (if visible)
    
    center_x = 32
    base_y = 62
    
    # === BOOTS ===
    left_foot_x = center_x - 5
    right_foot_x = center_x + 5
    
    for foot_x in [left_foot_x, right_foot_x]:
        for y in range(base_y - 6, base_y):
            for x in range(foot_x - 3, foot_x + 3):
                if 0 <= x < width and 0 <= y < height:
                    canvas[y][x] = BOOT_DARK if x < foot_x else BOOT_SHADOW
    
    # === LEGS (armored) ===
    for y in range(base_y - 20, base_y - 6):
        for x in range(left_foot_x - 3, left_foot_x + 3):
            if 0 <= x < width and 0 <= y < height:
                canvas[y][x] = ARMOR_DARK if x < left_foot_x else ARMOR_SILVER
    
    for y in range(base_y - 20, base_y - 6):
        for x in range(right_foot_x - 3, right_foot_x + 3):
            if 0 <= x < width and 0 <= y < height:
                canvas[y][x] = ARMOR_DARK if x < right_foot_x else ARMOR_SILVER
    
    # === TORSO (armored with cape) ===
    torso_y = base_y - 34
    
    # Cape behind
    for dy in range(-8, 18):
        cape_width = 14 - abs(dy) // 4
        for dx in range(-cape_width, cape_width + 1):
            if abs(dx) > 8:  # Only outer parts (behind armor)
                tx = center_x + dx
                ty = torso_y + dy
                if 0 <= tx < width and 0 <= ty < height:
                    if dx < 0:
                        canvas[ty][tx] = CAPE_DARK
                    else:
                        canvas[ty][tx] = CAPE_RED
    
    # Armor chest plate
    for dy in range(-12, 14):
        body_width = 10 - abs(dy) // 4
        for dx in range(-body_width, body_width + 1):
            tx = center_x + dx
            ty = torso_y + dy
            if 0 <= tx < width and 0 <= ty < height:
                if abs(dx) < 3:
                    canvas[ty][tx] = ARMOR_LIGHT
                elif dx < 0:
                    canvas[ty][tx] = ARMOR_DARK
                else:
                    canvas[ty][tx] = ARMOR_SILVER
    
    # Belt
    belt_y = base_y - 20
    for belt_row in range(3):
        for x in range(center_x - 9, center_x + 10):
            if 0 <= x < width and 0 <= belt_y + belt_row < height:
                if belt_row == 1:
                    canvas[belt_y + belt_row][x] = BELT_GOLD
                else:
                    canvas[belt_y + belt_row][x] = BELT_DARK
    
    # === LEFT ARM (holding shield) ===
    arm_y = torso_y - 4
    left_arm_x = center_x - 10
    
    for dy in range(0, 12):
        for dx in range(-3, 3):
            ax = left_arm_x + dx
            ay = arm_y + dy
            if 0 <= ax < width and 0 <= ay < height:
                canvas[ay][ax] = ARMOR_SILVER if dx > 0 else ARMOR_DARK
    
    # Shield
    shield_x = left_arm_x - 2
    shield_y = arm_y + 6
    
    for dy in range(-8, 9):
        for dx in range(-4, 5):
            if abs(dx) + abs(dy) * 0.8 < 8:
                sx = shield_x + dx
                sy = shield_y + dy
                if 0 <= sx < width and 0 <= sy < height:
                    # Shield design
                    if abs(dx) < 2 and abs(dy) < 6:
                        canvas[sy][sx] = SHIELD_RED
                    else:
                        canvas[sy][sx] = SHIELD_METAL if dx < 0 else ARMOR_SILVER
    
    # === RIGHT ARM (holding sword) ===
    right_arm_x = center_x + 10
    
    for dy in range(0, 12):
        for dx in range(-3, 3):
            ax = right_arm_x + dx
            ay = arm_y + dy
            if 0 <= ax < width and 0 <= ay < height:
                canvas[ay][ax] = ARMOR_DARK if dx < 0 else ARMOR_SILVER
    
    # Sword
    sword_x = right_arm_x + 2
    sword_y = arm_y + 4
    
    # Handle
    for i in range(6):
        if 0 <= sword_x < width and 0 <= sword_y + i < height:
            canvas[sword_y + i][sword_x] = HANDLE_BROWN if i % 2 == 0 else HANDLE_DARK
            if sword_x - 1 >= 0:
                canvas[sword_y + i][sword_x - 1] = HANDLE_BROWN if i % 2 == 0 else HANDLE_DARK
    
    # Blade pointing up
    for i in range(16):
        by = sword_y - i
        if 0 <= sword_x < width and 0 <= by < height:
            canvas[by][sword_x] = SWORD_EDGE
            if sword_x - 1 >= 0:
                canvas[by][sword_x - 1] = SWORD_STEEL
    
    # === HELMET ===
    head_y = torso_y - 18
    
    # Helmet shape
    for dy in range(-7, 6):
        for dx in range(-6, 7):
            dist = (dx * dx * 0.8 + dy * dy) ** 0.5
            if dist < 7:
                hx = center_x + dx
                hy = head_y + dy
                if 0 <= hx < width and 0 <= hy < height:
                    if dy < 0:
                        canvas[hy][hx] = ARMOR_LIGHT if abs(dx) < 3 else ARMOR_SILVER
                    else:
                        canvas[hy][hx] = ARMOR_SILVER if abs(dx) < 2 else ARMOR_DARK
    
    # Visor slit
    for x in range(center_x - 5, center_x + 6):
        if 0 <= x < width and 0 <= head_y < height:
            canvas[head_y][x] = BOOT_DARK
            if head_y + 1 < height:
                canvas[head_y + 1][x] = BOOT_SHADOW
    
    # Plume on helmet
    plume_y = head_y - 6
    for i in range(8):
        py = plume_y - i
        if 0 <= center_x < width and 0 <= py < height:
            canvas[py][center_x] = CAPE_RED if i % 2 == 0 else CAPE_DARK
            if center_x - 1 >= 0:
                canvas[py][center_x - 1] = CAPE_RED if i % 2 == 0 else CAPE_DARK
    
    return canvas


def create_warrior_attack():
    """Create warrior attack animation - sword swing"""
    width = 64
    height = 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Same color palette
    ARMOR_SILVER = [180, 185, 195, 255]
    ARMOR_DARK = [120, 125, 135, 255]
    ARMOR_LIGHT = [220, 225, 235, 255]
    
    CAPE_RED = [160, 40, 45, 255]
    CAPE_DARK = [110, 25, 30, 255]
    
    BELT_GOLD = [200, 170, 80, 255]
    BELT_DARK = [150, 120, 50, 255]
    
    BOOT_DARK = [40, 40, 45, 255]
    BOOT_SHADOW = [25, 25, 30, 255]
    
    SWORD_STEEL = [160, 170, 180, 255]
    SWORD_EDGE = [200, 210, 220, 255]
    HANDLE_BROWN = [80, 60, 40, 255]
    HANDLE_DARK = [50, 40, 25, 255]
    
    SHIELD_METAL = [140, 145, 155, 255]
    
    MOTION_BLUR = [180, 180, 200, 120]
    
    center_x = 32
    base_y = 62
    
    # === BOOTS ===
    left_foot_x = center_x - 5
    right_foot_x = center_x + 5
    
    for foot_x in [left_foot_x, right_foot_x]:
        for y in range(base_y - 6, base_y):
            for x in range(foot_x - 3, foot_x + 3):
                if 0 <= x < width and 0 <= y < height:
                    canvas[y][x] = BOOT_DARK if x < foot_x else BOOT_SHADOW
    
    # === LEGS ===
    for y in range(base_y - 20, base_y - 6):
        for x in range(left_foot_x - 3, left_foot_x + 3):
            if 0 <= x < width and 0 <= y < height:
                canvas[y][x] = ARMOR_DARK if x < left_foot_x else ARMOR_SILVER
    
    for y in range(base_y - 20, base_y - 6):
        for x in range(right_foot_x - 3, right_foot_x + 3):
            if 0 <= x < width and 0 <= y < height:
                canvas[y][x] = ARMOR_DARK if x < right_foot_x else ARMOR_SILVER
    
    # === TORSO ===
    torso_y = base_y - 34
    
    # Cape flowing
    for dy in range(-8, 18):
        cape_width = 12 - abs(dy) // 4
        for dx in range(-cape_width, cape_width + 1):
            if abs(dx) > 7:
                tx = center_x + dx + (2 if dx > 0 else -2)  # Flowing
                ty = torso_y + dy
                if 0 <= tx < width and 0 <= ty < height:
                    canvas[ty][tx] = CAPE_DARK if dx < 0 else CAPE_RED
    
    # Armor
    for dy in range(-12, 14):
        body_width = 10 - abs(dy) // 4
        for dx in range(-body_width, body_width + 1):
            tx = center_x + dx
            ty = torso_y + dy
            if 0 <= tx < width and 0 <= ty < height:
                if abs(dx) < 3:
                    canvas[ty][tx] = ARMOR_LIGHT
                elif dx < 0:
                    canvas[ty][tx] = ARMOR_DARK
                else:
                    canvas[ty][tx] = ARMOR_SILVER
    
    # Belt
    belt_y = base_y - 20
    for belt_row in range(3):
        for x in range(center_x - 9, center_x + 10):
            if 0 <= x < width and 0 <= belt_y + belt_row < height:
                if belt_row == 1:
                    canvas[belt_y + belt_row][x] = BELT_GOLD
                else:
                    canvas[belt_y + belt_row][x] = BELT_DARK
    
    # === LEFT ARM (shield defensive) ===
    arm_y = torso_y - 4
    left_arm_x = center_x - 10
    
    for dy in range(0, 12):
        for dx in range(-3, 3):
            ax = left_arm_x + dx
            ay = arm_y + dy
            if 0 <= ax < width and 0 <= ay < height:
                canvas[ay][ax] = ARMOR_SILVER if dx > 0 else ARMOR_DARK
    
    # Shield
    shield_x = left_arm_x - 2
    shield_y = arm_y + 6
    
    for dy in range(-8, 9):
        for dx in range(-4, 5):
            if abs(dx) + abs(dy) * 0.8 < 8:
                sx = shield_x + dx
                sy = shield_y + dy
                if 0 <= sx < width and 0 <= sy < height:
                    canvas[sy][sx] = SHIELD_METAL
    
    # === RIGHT ARM (swinging sword down and out) ===
    right_arm_x = center_x + 10
    
    # Arm extending down and outward
    for i in range(16):
        ax = right_arm_x + i // 3
        ay = arm_y + i
        for dx in range(-3, 3):
            px = ax + dx
            if 0 <= px < width and 0 <= ay < height:
                canvas[ay][px] = ARMOR_SILVER if dx > 0 else ARMOR_DARK
    
    # Hand position
    hand_x = right_arm_x + 5
    hand_y = arm_y + 16
    
    # Sword swinging diagonally down
    sword_x = hand_x
    sword_y = hand_y
    
    # Handle
    for i in range(6):
        hx = sword_x + i // 2
        hy = sword_y + i
        if 0 <= hx < width and 0 <= hy < height:
            canvas[hy][hx] = HANDLE_BROWN if i % 2 == 0 else HANDLE_DARK
            if hx - 1 >= 0:
                canvas[hy][hx - 1] = HANDLE_BROWN if i % 2 == 0 else HANDLE_DARK
    
    # Blade extending down and out
    for i in range(16):
        bx = sword_x + (i + 6) // 2
        by = sword_y + i + 6
        if 0 <= bx < width and 0 <= by < height:
            canvas[by][bx] = SWORD_EDGE
            if bx - 1 >= 0:
                canvas[by][bx - 1] = SWORD_STEEL
            if bx + 1 < width:
                canvas[by][bx + 1] = SWORD_STEEL
    
    # Motion blur (adjusted for downward motion)
    for i in range(8):
        mx = hand_x - i
        my = hand_y - i * 2
        if 0 <= mx < width and 0 <= my < height:
            canvas[my][mx] = MOTION_BLUR
    
    # === HELMET ===
    head_y = torso_y - 18
    
    for dy in range(-7, 6):
        for dx in range(-6, 7):
            dist = (dx * dx * 0.8 + dy * dy) ** 0.5
            if dist < 7:
                hx = center_x + dx
                hy = head_y + dy
                if 0 <= hx < width and 0 <= hy < height:
                    if dy < 0:
                        canvas[hy][hx] = ARMOR_LIGHT if abs(dx) < 3 else ARMOR_SILVER
                    else:
                        canvas[hy][hx] = ARMOR_SILVER if abs(dx) < 2 else ARMOR_DARK
    
    # Visor
    for x in range(center_x - 5, center_x + 6):
        if 0 <= x < width and 0 <= head_y < height:
            canvas[head_y][x] = BOOT_DARK
            if head_y + 1 < height:
                canvas[head_y + 1][x] = BOOT_SHADOW
    
    # Plume
    plume_y = head_y - 6
    for i in range(8):
        py = plume_y - i
        if 0 <= center_x < width and 0 <= py < height:
            canvas[py][center_x] = CAPE_RED if i % 2 == 0 else CAPE_DARK
            if center_x - 1 >= 0:
                canvas[py][center_x - 1] = CAPE_RED if i % 2 == 0 else CAPE_DARK
    
    return canvas


def create_warrior_death():
    """Create warrior death animation - fallen on ground"""
    width = 64
    height = 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette
    ARMOR_SILVER = [180, 185, 195, 255]
    ARMOR_DARK = [120, 125, 135, 255]
    ARMOR_LIGHT = [220, 225, 235, 255]
    
    CAPE_RED = [160, 40, 45, 255]
    CAPE_DARK = [110, 25, 30, 255]
    
    BELT_GOLD = [200, 170, 80, 255]
    BELT_DARK = [150, 120, 50, 255]
    
    BOOT_DARK = [40, 40, 45, 255]
    BOOT_SHADOW = [25, 25, 30, 255]
    
    SWORD_STEEL = [160, 170, 180, 255]
    SWORD_EDGE = [200, 210, 220, 255]
    HANDLE_BROWN = [80, 60, 40, 255]
    
    SHIELD_METAL = [140, 145, 155, 255]
    
    BLOOD_DARK = [100, 0, 0, 255]
    BLOOD_MID = [140, 20, 20, 255]
    BLOOD_LIGHT = [180, 40, 40, 255]
    
    center_x = 32
    base_y = 48
    
    # === BLOOD POOL ===
    blood_y = base_y + 6
    for y in range(blood_y - 3, blood_y + 10):
        for x in range(center_x - 16, center_x + 16):
            if 0 <= x < width and 0 <= y < height:
                dx = x - center_x
                dy = y - blood_y
                dist = (dx * dx * 0.4 + dy * dy) ** 0.5
                if dist < 11:
                    if dist < 4:
                        canvas[y][x] = BLOOD_DARK
                    elif dist < 7:
                        canvas[y][x] = BLOOD_MID if (x + y) % 2 == 0 else BLOOD_DARK
                    else:
                        canvas[y][x] = BLOOD_LIGHT if (x + y) % 3 == 0 else BLOOD_MID
    
    # === LEGS (fallen) ===
    left_leg_x = center_x - 6
    right_leg_x = center_x + 6
    
    for leg_x in [left_leg_x, right_leg_x]:
        for y in range(base_y + 4, base_y + 18):
            for x in range(leg_x - 3, leg_x + 3):
                if 0 <= x < width and 0 <= y < height:
                    canvas[y][x] = ARMOR_DARK if x < leg_x else ARMOR_SILVER
    
    # Boots
    for leg_x in [left_leg_x, right_leg_x]:
        for y in range(base_y + 18, min(base_y + 24, height)):
            for x in range(leg_x - 3, leg_x + 3):
                if 0 <= x < width and 0 <= y < height:
                    canvas[y][x] = BOOT_DARK if x < leg_x else BOOT_SHADOW
    
    # === TORSO (lying flat) ===
    torso_y = base_y - 6
    
    # Cape spread beneath
    for dy in range(-6, 12):
        cape_width = 16 - abs(dy) // 3
        for dx in range(-cape_width, cape_width + 1):
            if abs(dx) > 8:
                tx = center_x + dx
                ty = torso_y + dy
                if 0 <= tx < width and 0 <= ty < height:
                    canvas[ty][tx] = CAPE_DARK if dx < 0 else CAPE_RED
    
    # Armor chest
    for dy in range(-8, 10):
        body_width = 9 - abs(dy) // 3
        for dx in range(-body_width, body_width + 1):
            tx = center_x + dx
            ty = torso_y + dy
            if 0 <= tx < width and 0 <= ty < height:
                if abs(dx) < 2:
                    canvas[ty][tx] = ARMOR_LIGHT
                else:
                    canvas[ty][tx] = ARMOR_SILVER if dx > 0 else ARMOR_DARK
    
    # Belt
    for x in range(center_x - 8, center_x + 9):
        if 0 <= x < width and 0 <= torso_y + 4 < height:
            canvas[torso_y + 4][x] = BELT_GOLD
    
    # === ARMS (spread out) ===
    arm_y = torso_y - 2
    
    # Left arm
    left_arm_x = center_x - 8
    for i in range(10):
        ax = left_arm_x - i
        for dy in range(-2, 3):
            ay = arm_y + dy
            if 0 <= ax < width and 0 <= ay < height:
                canvas[ay][ax] = ARMOR_SILVER if abs(dy) <= 1 else ARMOR_DARK
    
    # Right arm
    right_arm_x = center_x + 8
    for i in range(10):
        ax = right_arm_x + i
        for dy in range(-2, 3):
            ay = arm_y + dy
            if 0 <= ax < width and 0 <= ay < height:
                canvas[ay][ax] = ARMOR_SILVER if abs(dy) <= 1 else ARMOR_DARK
    
    # === HELMET (lying on side) ===
    head_y = torso_y - 14
    
    for dy in range(-6, 7):
        for dx in range(-7, 8):
            dist = (dx * dx + dy * dy * 0.8) ** 0.5
            if dist < 7:
                hx = center_x + dx
                hy = head_y + dy
                if 0 <= hx < width and 0 <= hy < height:
                    canvas[hy][hx] = ARMOR_SILVER if abs(dy) < 3 else ARMOR_DARK
    
    # Visor (dark slit)
    for x in range(center_x - 4, center_x + 5):
        if 0 <= x < width and 0 <= head_y < height:
            canvas[head_y][x] = BOOT_SHADOW
    
    # === DROPPED SWORD ===
    sword_x = center_x + 14
    sword_y = base_y
    
    # Blade
    for i in range(12):
        if 0 <= sword_x + i < width and 0 <= sword_y < height:
            canvas[sword_y][sword_x + i] = SWORD_EDGE if i < 10 else SWORD_STEEL
            if sword_y + 1 < height:
                canvas[sword_y + 1][sword_x + i] = SWORD_STEEL
    
    # Handle
    for i in range(4):
        if 0 <= sword_x - i < width and 0 <= sword_y < height:
            canvas[sword_y][sword_x - i] = HANDLE_BROWN
            if sword_y + 1 < height:
                canvas[sword_y + 1][sword_x - i] = HANDLE_BROWN
    
    # === DROPPED SHIELD ===
    shield_x = center_x - 16
    shield_y = base_y + 2
    
    for dy in range(-5, 6):
        for dx in range(-3, 4):
            if abs(dx) + abs(dy) * 0.9 < 6:
                sx = shield_x + dx
                sy = shield_y + dy
                if 0 <= sx < width and 0 <= sy < height:
                    canvas[sy][sx] = SHIELD_METAL if abs(dx + dy) % 2 == 0 else ARMOR_DARK
    
    return canvas


def main():
    """Create and save all three warrior hero images"""
    print("Creating warrior hero images...")
    
    # Create all three images
    warrior_default = create_warrior_default()
    warrior_attack = create_warrior_attack()
    warrior_death = create_warrior_death()
    
    # Convert to PIL and scale up
    scale = 4
    
    # Default pose
    img_default = Image.fromarray(warrior_default, 'RGBA')
    img_default_scaled = img_default.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_default_scaled.save('warrior_hero.png')
    print(f"✓ Saved: warrior_hero.png ({64 * scale}x{64 * scale})")
    
    # Attack animation
    img_attack = Image.fromarray(warrior_attack, 'RGBA')
    img_attack_scaled = img_attack.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_attack_scaled.save('warrior_hero_attack.png')
    print(f"✓ Saved: warrior_hero_attack.png ({64 * scale}x{64 * scale})")
    
    # Death animation
    img_death = Image.fromarray(warrior_death, 'RGBA')
    img_death_scaled = img_death.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_death_scaled.save('warrior_hero_death.png')
    print(f"✓ Saved: warrior_hero_death.png ({64 * scale}x{64 * scale})")
    
    print("\n✅ Armored warrior hero creation complete!")
    print("\nFeatures:")
    print("- Default: Warrior standing with sword and shield")
    print("- Attack: Dynamic sword swing with motion blur")
    print("- Death: Fallen warrior with blood pool and dropped equipment")
    print("\nStyle: Pixel art inspired by armored knight")
    print("Colors: Silver armor, red cape, gold trim, steel weapons")


if __name__ == '__main__':
    main()
