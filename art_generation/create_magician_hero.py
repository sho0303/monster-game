"""
Create pixel art magician hero images
Inspired by blue wizard with pointed hat, flowing robes, and magical staff
"""
from PIL import Image
import numpy as np
import random

def create_magician_default():
    """Create default standing magician with staff and pointed wizard hat"""
    width = 64
    height = 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color palette - blue wizard theme
    ROBE_DARK = [20, 35, 70, 255]        # Dark blue robe
    ROBE_MID = [30, 60, 120, 255]        # Mid blue robe
    ROBE_LIGHT = [50, 90, 160, 255]      # Light blue highlights
    ROBE_SHADOW = [15, 25, 50, 255]      # Deep robe shadows
    
    HAT_DARK = [15, 25, 55, 255]         # Dark blue pointed hat
    HAT_MID = [25, 45, 95, 255]          # Mid blue hat
    HAT_LIGHT = [40, 70, 130, 255]       # Light blue hat
    HAT_STAR = [255, 215, 50, 255]       # Gold stars/moon on hat
    HAT_BRIM = [10, 20, 45, 255]         # Dark hat brim
    
    SKIN_LIGHT = [220, 190, 170, 255]    # Pale skin
    SKIN_SHADOW = [180, 150, 130, 255]   # Skin shadows
    
    BEARD_WHITE = [230, 230, 240, 255]   # White/gray beard
    BEARD_GRAY = [180, 180, 190, 255]    # Gray beard shadows
    
    STAFF_WOOD = [110, 80, 50, 255]      # Brown wooden staff
    STAFF_DARK = [70, 50, 30, 255]       # Staff shadows
    STAFF_TOP = [200, 150, 80, 255]      # Golden staff top
    
    MAGIC_GOLD = [255, 220, 100, 255]    # Gold magical glow
    MAGIC_ORANGE = [255, 160, 60, 255]   # Orange magic
    MAGIC_WHITE = [255, 255, 240, 255]   # Bright magic
    
    BELT_BROWN = [90, 65, 40, 255]       # Leather belt
    BELT_BUCKLE = [180, 160, 80, 255]    # Gold buckle
    
    # Position magician (centered, moved lower to fit hat)
    center_x = 32
    base_y = 60
    
    # === STAFF (left side) ===
    staff_x = center_x - 12
    staff_bottom = base_y - 8
    staff_top = base_y - 43
    
    # Staff shaft
    for y in range(staff_top, staff_bottom):
        canvas[y][staff_x] = STAFF_WOOD
        canvas[y][staff_x + 1] = STAFF_DARK
    
    # Ornate staff top with magical orb
    for dy in range(-4, 5):
        for dx in range(-3, 4):
            if abs(dx) + abs(dy) <= 4:
                orb_x = staff_x + dx
                orb_y = staff_top - 3 + dy
                if 0 <= orb_x < width and 0 <= orb_y < height:
                    if abs(dx) + abs(dy) <= 2:
                        canvas[orb_y][orb_x] = MAGIC_WHITE
                    elif abs(dx) + abs(dy) <= 3:
                        canvas[orb_y][orb_x] = MAGIC_GOLD
                    else:
                        canvas[orb_y][orb_x] = STAFF_TOP
    
    # Staff glow particles (kept within frame)
    glow_spots = [(staff_x - 2, staff_top - 2), (staff_x + 3, staff_top - 1), 
                  (staff_x, staff_top - 3), (staff_x + 1, staff_top - 2)]
    for gx, gy in glow_spots:
        if 0 <= gx < width and 0 <= gy < height:
            canvas[gy][gx] = MAGIC_ORANGE
    
    # === BODY (flowing blue robes) ===
    # Lower robe (wide and flowing)
    for y in range(base_y - 22, base_y):
        width_at_y = 10 + (y - (base_y - 22)) // 2
        for x in range(center_x - width_at_y, center_x + width_at_y):
            if 0 <= x < width:
                # Robe folds and shadows
                if (x - center_x) % 5 == 0:
                    canvas[y][x] = ROBE_SHADOW
                elif abs(x - center_x) < 4:
                    canvas[y][x] = ROBE_MID
                elif abs(x - center_x) < 8:
                    canvas[y][x] = ROBE_LIGHT if (x + y) % 3 == 0 else ROBE_MID
                else:
                    canvas[y][x] = ROBE_DARK
    
    # Upper torso
    for y in range(base_y - 38, base_y - 22):
        width_at_y = 11
        for x in range(center_x - width_at_y, center_x + width_at_y):
            if 0 <= x < width:
                if abs(x - center_x) < 5:
                    canvas[y][x] = ROBE_MID
                elif x < center_x:
                    canvas[y][x] = ROBE_DARK
                else:
                    canvas[y][x] = ROBE_LIGHT
    
    # Belt with buckle
    belt_y = base_y - 22
    for x in range(center_x - 11, center_x + 11):
        if 0 <= x < width:
            canvas[belt_y][x] = BELT_BROWN
            canvas[belt_y + 1][x] = BELT_BROWN
    
    # Belt buckle
    for dy in range(-1, 2):
        for dx in range(-2, 3):
            if abs(dx) + abs(dy) <= 2:
                canvas[belt_y + dy][center_x + dx] = BELT_BUCKLE
    
    # === RIGHT ARM (holding staff) ===
    arm_x = staff_x + 3
    arm_y = base_y - 32
    for y in range(arm_y, arm_y + 12):
        for x in range(arm_x, arm_x + 4):
            if 0 <= x < width and 0 <= y < height:
                canvas[y][x] = ROBE_DARK if x < arm_x + 2 else ROBE_MID
    
    # Hand gripping staff
    for dy in range(4):
        canvas[arm_y + 12 + dy][staff_x - 1] = SKIN_SHADOW
        canvas[arm_y + 12 + dy][staff_x - 2] = SKIN_LIGHT
    
    # === LEFT ARM (extended, casting) ===
    left_arm_x = center_x + 8
    left_arm_y = base_y - 30
    
    # Upper arm
    for y in range(left_arm_y, left_arm_y + 6):
        for x in range(left_arm_x - 2, left_arm_x + 2):
            if 0 <= x < width and 0 <= y < height:
                canvas[y][x] = ROBE_MID
    
    # Forearm extending
    for x in range(left_arm_x, left_arm_x + 8):
        for dy in range(4):
            if 0 <= x < width:
                canvas[left_arm_y + 6 + dy][x] = ROBE_DARK
    
    # Hand
    hand_x = left_arm_x + 8
    hand_y = left_arm_y + 7
    for dy in range(3):
        for dx in range(3):
            if 0 <= hand_x + dx < width:
                canvas[hand_y + dy][hand_x + dx] = SKIN_LIGHT if dx < 2 else SKIN_SHADOW
    
    # Small magic sparkle from hand
    for i in range(4):
        mx = hand_x + 4 + i
        my = hand_y + 1 + random.randint(-1, 1)
        if 0 <= mx < width and 0 <= my < height:
            canvas[my][mx] = MAGIC_GOLD if i % 2 == 0 else MAGIC_ORANGE
    
    # === HEAD & FACE ===
    head_y = base_y - 40
    
    # Face
    for dy in range(6):
        for dx in range(-3, 4):
            fx = center_x + dx
            fy = head_y + dy
            if 0 <= fx < width and 0 <= fy < height:
                if abs(dx) < 3:
                    canvas[fy][fx] = SKIN_LIGHT if abs(dx) < 2 else SKIN_SHADOW
    
    # Eyes
    canvas[head_y + 2][center_x - 1] = ROBE_DARK
    canvas[head_y + 2][center_x + 1] = ROBE_DARK
    
    # Mustache
    for dx in range(-2, 3):
        canvas[head_y + 4][center_x + dx] = BEARD_GRAY
    
    # Long flowing beard
    beard_y = head_y + 5
    for dy in range(14):
        beard_width = 3 + min(dy // 2, 4)
        for dx in range(-beard_width, beard_width + 1):
            bx = center_x + dx
            by = beard_y + dy
            if 0 <= bx < width and 0 <= by < height:
                if abs(dx) == beard_width or dy == 0:
                    canvas[by][bx] = BEARD_GRAY
                else:
                    canvas[by][bx] = BEARD_WHITE if (dx + dy) % 2 == 0 else BEARD_GRAY
    
    # === POINTED WIZARD HAT (shorter to fit in frame) ===
    hat_base_y = head_y - 2
    hat_tip_y = head_y - 20
    
    # Pointed cone
    for y in range(hat_tip_y, hat_base_y):
        progress = (y - hat_tip_y) / (hat_base_y - hat_tip_y)
        hat_width = int(2 + progress * 7)
        
        for x in range(center_x - hat_width, center_x + hat_width + 1):
            if 0 <= x < width and 0 <= y < height:
                # Hat texture with light and shadow
                if x == center_x - hat_width or x == center_x + hat_width:
                    canvas[y][x] = HAT_DARK
                elif x < center_x:
                    canvas[y][x] = HAT_MID if (x + y) % 3 != 0 else HAT_DARK
                else:
                    canvas[y][x] = HAT_LIGHT if (x + y) % 3 == 0 else HAT_MID
    
    # Hat brim
    for x in range(center_x - 10, center_x + 11):
        if 0 <= x < width:
            canvas[hat_base_y][x] = HAT_BRIM
            canvas[hat_base_y + 1][x] = HAT_BRIM
            if abs(x - center_x) < 9:
                canvas[hat_base_y - 1][x] = HAT_BRIM
    
    # Stars and moons on hat
    # Star 1
    star1_x = center_x - 2
    star1_y = hat_tip_y + 6
    canvas[star1_y][star1_x] = HAT_STAR
    canvas[star1_y - 1][star1_x] = HAT_STAR
    canvas[star1_y + 1][star1_x] = HAT_STAR
    canvas[star1_y][star1_x - 1] = HAT_STAR
    canvas[star1_y][star1_x + 1] = HAT_STAR
    
    # Star 2
    star2_x = center_x + 3
    star2_y = hat_tip_y + 12
    canvas[star2_y][star2_x] = HAT_STAR
    canvas[star2_y - 1][star2_x] = HAT_STAR
    canvas[star2_y][star2_x + 1] = HAT_STAR
    
    # Crescent moon near top
    moon_x = center_x
    moon_y = hat_tip_y + 2
    for dy in range(-2, 3):
        canvas[moon_y + dy][moon_x] = HAT_STAR
        if abs(dy) < 2:
            canvas[moon_y + dy][moon_x + 1] = HAT_STAR
    
    # === MAGICAL SPARKLES ===
    sparkles = [
        (staff_x - 3, staff_top - 7), (staff_x + 4, staff_top - 5),
        (center_x - 15, base_y - 28), (center_x + 18, base_y - 32),
        (hand_x + 6, hand_y - 2), (center_x - 8, base_y - 45),
    ]
    
    for sx, sy in sparkles:
        if 0 <= sx < width and 0 <= sy < height:
            canvas[sy][sx] = MAGIC_GOLD if random.random() < 0.6 else MAGIC_ORANGE
    
    return canvas


def create_magician_attack():
    """Create magician casting a spell attack with raised staff"""
    width = 64
    height = 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Blue wizard color palette
    ROBE_DARK = [20, 35, 70, 255]
    ROBE_MID = [30, 60, 120, 255]
    ROBE_LIGHT = [50, 90, 160, 255]
    ROBE_SHADOW = [15, 25, 50, 255]
    
    HAT_DARK = [15, 25, 55, 255]
    HAT_MID = [25, 45, 95, 255]
    HAT_LIGHT = [40, 70, 130, 255]
    HAT_STAR = [255, 215, 50, 255]
    HAT_BRIM = [10, 20, 45, 255]
    
    SKIN_LIGHT = [220, 190, 170, 255]
    SKIN_SHADOW = [180, 150, 130, 255]
    
    BEARD_WHITE = [230, 230, 240, 255]
    BEARD_GRAY = [180, 180, 190, 255]
    
    STAFF_WOOD = [110, 80, 50, 255]
    STAFF_DARK = [70, 50, 30, 255]
    STAFF_TOP = [200, 150, 80, 255]
    
    BELT_BROWN = [90, 65, 40, 255]
    
    # Bright attack magic
    MAGIC_BRIGHT = [255, 255, 255, 255]  # Pure white energy core
    MAGIC_GOLD = [255, 220, 100, 255]    # Gold glow
    MAGIC_ORANGE = [255, 160, 60, 255]   # Orange energy
    MAGIC_BLUE = [100, 200, 255, 255]    # Blue energy trails
    MAGIC_ENERGY = [255, 200, 255, 255]  # Pink/purple energy
    
    center_x = 28  # Shifted left for staff raise
    base_y = 58
    
    # === STAFF (raised high but not off frame) ===
    staff_x = center_x + 10
    staff_bottom = base_y - 28
    staff_top = base_y - 48
    
    # Staff shaft
    for y in range(staff_top, staff_bottom):
        if 0 <= y < height:
            canvas[y][staff_x] = STAFF_WOOD
            canvas[y][staff_x + 1] = STAFF_DARK
    
    # Ornate staff top with magical orb (sized to fit in frame)
    for dy in range(-5, 6):
        for dx in range(-4, 5):
            if abs(dx) + abs(dy) <= 6:
                orb_x = staff_x + dx
                orb_y = staff_top - 3 + dy
                if 0 <= orb_x < width and 0 <= orb_y < height:
                    if abs(dx) + abs(dy) <= 3:
                        canvas[orb_y][orb_x] = MAGIC_BRIGHT
                    elif abs(dx) + abs(dy) <= 4:
                        canvas[orb_y][orb_x] = MAGIC_GOLD
                    else:
                        canvas[orb_y][orb_x] = STAFF_TOP
    
    # === MASSIVE MAGICAL BLAST ===
    blast_start_x = staff_x
    blast_start_y = staff_top - 3
    
    # Main energy beam (thick and powerful)
    for i in range(22):
        beam_x = blast_start_x + i + 8
        beam_y = blast_start_y - i // 4
        if 0 <= beam_x < width and 0 <= beam_y < height:
            beam_width = 3 if i < 10 else 2
            for dy in range(-beam_width, beam_width + 1):
                if 0 <= beam_y + dy < height:
                    if abs(dy) == beam_width:
                        canvas[beam_y + dy][beam_x] = MAGIC_BLUE
                    elif abs(dy) == beam_width - 1:
                        canvas[beam_y + dy][beam_x] = MAGIC_GOLD
                    else:
                        canvas[beam_y + dy][beam_x] = MAGIC_BRIGHT
    
    # Energy swirls and particles
    for i in range(30):
        angle_offset = i * 0.6
        swirl_x = int(blast_start_x + 10 + i * 1.2)
        swirl_y = int(blast_start_y + 4 * np.sin(angle_offset))
        if 0 <= swirl_x < width and 0 <= swirl_y < height:
            canvas[swirl_y][swirl_x] = MAGIC_ENERGY if i % 3 == 0 else MAGIC_ORANGE
    
    # Explosive energy particles near orb (kept within frame)
    for i in range(15):
        px = blast_start_x + random.randint(-5, 5)
        py = blast_start_y + random.randint(-3, 5)
        if 0 <= px < width and 0 <= py < height:
            canvas[py][px] = MAGIC_GOLD if random.random() < 0.5 else MAGIC_BRIGHT
    
    # === BODY (dynamic casting pose) ===
    # Lower robe (flowing back from power)
    for y in range(base_y - 20, base_y):
        width_at_y = 8 + (y - (base_y - 20)) // 2
        for x in range(center_x - width_at_y, center_x + width_at_y):
            if 0 <= x < width:
                if (x - center_x) % 5 == 0:
                    canvas[y][x] = ROBE_SHADOW
                elif abs(x - center_x) < 4:
                    canvas[y][x] = ROBE_MID
                else:
                    canvas[y][x] = ROBE_LIGHT if (x + y) % 3 == 0 else ROBE_MID
    
    # Upper torso
    for y in range(base_y - 35, base_y - 20):
        for x in range(center_x - 10, center_x + 10):
            if 0 <= x < width:
                canvas[y][x] = ROBE_MID if abs(x - center_x) < 5 else ROBE_DARK
    
    # Belt
    for x in range(center_x - 10, center_x + 10):
        if 0 <= x < width:
            canvas[base_y - 20][x] = BELT_BROWN
            canvas[base_y - 19][x] = BELT_BROWN
    
    # === RIGHT ARM (raised holding staff) ===
    arm_x = staff_x - 2
    arm_y = base_y - 38
    for y in range(arm_y, arm_y + 15):
        for x in range(arm_x - 3, arm_x + 1):
            if 0 <= x < width and 0 <= y < height:
                canvas[y][x] = ROBE_DARK if x < arm_x - 1 else ROBE_MID
    
    # Hand gripping staff
    for dy in range(4):
        canvas[staff_bottom + dy][staff_x - 1] = SKIN_SHADOW
        canvas[staff_bottom + dy][staff_x - 2] = SKIN_LIGHT
    
    # === LEFT ARM (extended forward casting) ===
    left_arm_y = base_y - 32
    for x in range(center_x - 12, center_x - 2):
        for y in range(left_arm_y, left_arm_y + 4):
            if 0 <= x < width and 0 <= y < height:
                canvas[y][x] = ROBE_DARK
    
    # Hand with magical energy
    hand_x = center_x - 13
    hand_y = left_arm_y + 1
    for dy in range(3):
        for dx in range(3):
            hx = hand_x + dx
            hy = hand_y + dy
            if 0 <= hx < width and 0 <= hy < height:
                canvas[hy][hx] = SKIN_LIGHT if dx < 2 else SKIN_SHADOW
    
    # Magic emanating from hand
    for i in range(8):
        mx = hand_x - i - 2
        my = hand_y + 1 + random.randint(-2, 2)
        if 0 <= mx < width and 0 <= my < height:
            canvas[my][mx] = MAGIC_BRIGHT if i % 2 == 0 else MAGIC_BLUE
    
    # === HEAD & POINTED HAT ===
    head_y = base_y - 38
    
    # Face
    for dy in range(6):
        for dx in range(-3, 4):
            fx = center_x + dx
            fy = head_y + dy
            if 0 <= fx < width and 0 <= fy < height:
                if abs(dx) < 3:
                    canvas[fy][fx] = SKIN_LIGHT if abs(dx) < 2 else SKIN_SHADOW
    
    # Eyes (glowing with magic power)
    canvas[head_y + 2][center_x - 1] = MAGIC_BLUE
    canvas[head_y + 2][center_x + 1] = MAGIC_BLUE
    
    # Beard flowing with energy
    beard_y = head_y + 5
    for dy in range(10):
        beard_width = 3 + dy // 3
        for dx in range(-beard_width, beard_width + 1):
            bx = center_x + dx
            by = beard_y + dy
            if 0 <= bx < width and 0 <= by < height:
                if abs(dx) == beard_width or dy == 0:
                    canvas[by][bx] = BEARD_GRAY
                else:
                    canvas[by][bx] = BEARD_WHITE if (dx + dy) % 2 == 0 else BEARD_GRAY
    
    # === POINTED WIZARD HAT (shorter to match default) ===
    hat_base_y = head_y - 2
    hat_tip_y = head_y - 20
    
    # Pointed cone
    for y in range(hat_tip_y, hat_base_y):
        progress = (y - hat_tip_y) / (hat_base_y - hat_tip_y)
        hat_width = int(2 + progress * 7)
        
        for x in range(center_x - hat_width, center_x + hat_width + 1):
            if 0 <= x < width and 0 <= y < height:
                if x == center_x - hat_width or x == center_x + hat_width:
                    canvas[y][x] = HAT_DARK
                elif x < center_x:
                    canvas[y][x] = HAT_MID if (x + y) % 3 != 0 else HAT_DARK
                else:
                    canvas[y][x] = HAT_LIGHT if (x + y) % 3 == 0 else HAT_MID
    
    # Hat brim
    for x in range(center_x - 10, center_x + 11):
        if 0 <= x < width:
            canvas[hat_base_y][x] = HAT_BRIM
            canvas[hat_base_y + 1][x] = HAT_BRIM
            if abs(x - center_x) < 9:
                canvas[hat_base_y - 1][x] = HAT_BRIM
    
    # Star on hat
    star_x = center_x + 1
    star_y = hat_tip_y + 8
    canvas[star_y][star_x] = HAT_STAR
    canvas[star_y - 1][star_x] = HAT_STAR
    canvas[star_y][star_x + 1] = HAT_STAR
    
    # === MAGICAL EFFECTS (intense casting aura) ===
    # Sparkles everywhere
    for _ in range(35):
        sx = random.randint(10, width - 5)
        sy = random.randint(5, height - 20)
        if canvas[sy][sx][3] == 0:  # Only on empty space
            sparkle_color = random.choice([MAGIC_BRIGHT, MAGIC_BLUE, MAGIC_GOLD, MAGIC_ENERGY])
            canvas[sy][sx] = sparkle_color
    
    return canvas


def create_magician_death():
    """Create magician death animation - lying flat on ground with blood pool"""
    width = 64
    height = 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Blue wizard color palette
    ROBE_DARK = [20, 35, 70, 255]
    ROBE_MID = [30, 60, 120, 255]
    ROBE_LIGHT = [50, 90, 160, 255]
    ROBE_SHADOW = [15, 25, 50, 255]
    
    HAT_DARK = [15, 25, 55, 255]
    HAT_MID = [25, 45, 95, 255]
    HAT_LIGHT = [40, 70, 130, 255]
    HAT_STAR = [255, 215, 50, 255]
    HAT_BRIM = [10, 20, 45, 255]
    
    SKIN_LIGHT = [220, 190, 170, 255]
    SKIN_SHADOW = [180, 150, 130, 255]
    SKIN_PALE = [200, 170, 150, 255]  # Paler, lifeless
    
    BEARD_WHITE = [230, 230, 240, 255]
    BEARD_GRAY = [180, 180, 190, 255]
    
    STAFF_WOOD = [110, 80, 50, 255]
    STAFF_DARK = [70, 50, 30, 255]
    STAFF_TOP = [200, 150, 80, 255]
    
    BELT_BROWN = [90, 65, 40, 255]
    
    # Blood colors
    BLOOD_DARK = [100, 0, 0, 255]      # Dark blood
    BLOOD_MID = [140, 20, 20, 255]     # Mid blood
    BLOOD_BRIGHT = [180, 30, 30, 255]  # Bright blood
    
    # Fading magic effects
    MAGIC_FADE = [100, 120, 180, 150]   # Dim blue, more transparent
    MAGIC_DIM = [80, 100, 140, 100]     # Very dim
    
    center_x = 32
    base_y = 50  # Lying flat on ground
    
    # === BLOOD POOL (underneath body) ===
    # Large blood pool spreading from center
    blood_center_x = center_x
    blood_center_y = base_y + 2
    
    # Create irregular blood pool shape
    for y in range(base_y - 8, base_y + 8):
        for x in range(center_x - 20, center_x + 20):
            if 0 <= x < width and 0 <= y < height:
                # Distance from blood center
                dx = x - blood_center_x
                dy = (y - blood_center_y) * 1.5  # Elliptical
                dist = (dx*dx + dy*dy) ** 0.5
                
                # Irregular blood pool with variations
                blood_radius = 16 + random.randint(-3, 3)
                if dist < blood_radius:
                    # Create depth variation in blood pool
                    if dist < blood_radius * 0.3:
                        canvas[y][x] = BLOOD_DARK
                    elif dist < blood_radius * 0.6:
                        canvas[y][x] = BLOOD_MID if (x + y) % 3 != 0 else BLOOD_DARK
                    else:
                        canvas[y][x] = BLOOD_BRIGHT if (x + y) % 2 == 0 else BLOOD_MID
    
    # Blood splatters and drips
    splatter_positions = [
        (center_x - 18, base_y - 10), (center_x + 15, base_y - 8),
        (center_x - 12, base_y + 10), (center_x + 20, base_y + 5),
        (center_x - 22, base_y + 2), (center_x + 12, base_y - 12),
    ]
    
    for sx, sy in splatter_positions:
        if 0 <= sx < width and 0 <= sy < height:
            canvas[sy][sx] = BLOOD_BRIGHT
            # Small splatter around each spot
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    spx = sx + dx
                    spy = sy + dy
                    if 0 <= spx < width and 0 <= spy < height and random.random() < 0.4:
                        canvas[spy][spx] = BLOOD_MID
    
    # === FALLEN STAFF (lying beside body) ===
    staff_x = center_x + 18
    staff_y = base_y - 5
    
    # Staff shaft lying horizontal/diagonal
    for i in range(32):
        sx = staff_x + i
        sy = staff_y + i // 8
        if 0 <= sx < width and 0 <= sy < height:
            canvas[sy][sx] = STAFF_WOOD
            if sy + 1 < height:
                canvas[sy + 1][sx] = STAFF_DARK
    
    # Orb at staff end (dimmed)
    orb_x = staff_x + 3
    orb_y = staff_y - 1
    for dy in range(-3, 4):
        for dx in range(-3, 4):
            if abs(dx) + abs(dy) <= 4:
                ox = orb_x + dx
                oy = orb_y + dy
                if 0 <= ox < width and 0 <= oy < height:
                    if abs(dx) + abs(dy) <= 2:
                        canvas[oy][ox] = MAGIC_FADE
                    elif abs(dx) + abs(dy) <= 3:
                        canvas[oy][ox] = MAGIC_DIM
                    else:
                        canvas[oy][ox] = STAFF_TOP
    
    # === BODY (lying flat on back) ===
    # Torso flat on ground
    torso_y = base_y - 2
    
    # Main body/robe spread out
    for dy in range(-10, 10):
        body_width = 12 - abs(dy) // 3
        for dx in range(-body_width, body_width + 1):
            bx = center_x + dx
            by = torso_y + dy
            if 0 <= bx < width and 0 <= by < height:
                # Don't overdraw blood
                if canvas[by][bx][3] == 0:
                    if abs(dy) < 5:
                        canvas[by][bx] = ROBE_MID if abs(dx) < 6 else ROBE_DARK
                    else:
                        canvas[by][bx] = ROBE_DARK if abs(dx) < 4 else ROBE_SHADOW
    
    # Belt across body
    for x in range(center_x - 10, center_x + 10):
        if 0 <= x < width:
            belt_y = torso_y
            if canvas[belt_y][x][3] == 0:
                canvas[belt_y][x] = BELT_BROWN
                canvas[belt_y + 1][x] = BELT_BROWN
    
    # === LEFT ARM (extended out to side) ===
    left_arm_x = center_x - 12
    left_arm_y = torso_y - 2
    
    # Upper arm
    for x in range(left_arm_x - 8, left_arm_x):
        for dy in range(-2, 3):
            ax = x
            ay = left_arm_y + dy
            if 0 <= ax < width and 0 <= ay < height:
                if canvas[ay][ax][3] == 0:
                    canvas[ay][ax] = ROBE_DARK if dy == 0 else ROBE_MID
    
    # Left hand
    hand_x = left_arm_x - 9
    for dy in range(-2, 3):
        for dx in range(-3, 1):
            hx = hand_x + dx
            hy = left_arm_y + dy
            if 0 <= hx < width and 0 <= hy < height:
                if canvas[hy][hx][3] == 0:
                    canvas[hy][hx] = SKIN_PALE if abs(dy) < 2 else SKIN_SHADOW
    
    # === RIGHT ARM (extended out to other side) ===
    right_arm_x = center_x + 12
    right_arm_y = torso_y + 1
    
    # Upper arm
    for x in range(right_arm_x, right_arm_x + 8):
        for dy in range(-2, 3):
            ax = x
            ay = right_arm_y + dy
            if 0 <= ax < width and 0 <= ay < height:
                if canvas[ay][ax][3] == 0:
                    canvas[ay][ax] = ROBE_MID if abs(dy) < 2 else ROBE_DARK
    
    # Right hand
    hand_x = right_arm_x + 8
    for dy in range(-2, 3):
        for dx in range(0, 4):
            hx = hand_x + dx
            hy = right_arm_y + dy
            if 0 <= hx < width and 0 <= hy < height:
                if canvas[hy][hx][3] == 0:
                    canvas[hy][hx] = SKIN_PALE if abs(dy) < 2 else SKIN_SHADOW
    
    # === HEAD (lying flat, face up) ===
    head_y = torso_y - 12
    
    # Face
    for dy in range(-3, 4):
        for dx in range(-3, 4):
            fx = center_x + dx
            fy = head_y + dy
            if 0 <= fx < width and 0 <= fy < height:
                if abs(dx) + abs(dy) < 5:
                    if canvas[fy][fx][3] == 0:
                        canvas[fy][fx] = SKIN_PALE if abs(dx) < 2 else SKIN_SHADOW
    
    # Closed/dead eyes
    canvas[head_y - 1][center_x - 2] = ROBE_SHADOW
    canvas[head_y - 1][center_x - 1] = ROBE_SHADOW
    canvas[head_y - 1][center_x + 1] = ROBE_SHADOW
    canvas[head_y - 1][center_x + 2] = ROBE_SHADOW
    
    # Beard spread out on ground
    beard_y = head_y + 3
    for dy in range(12):
        beard_width = 4 + dy // 2
        for dx in range(-beard_width, beard_width + 1):
            bx = center_x + dx
            by = beard_y + dy
            if 0 <= bx < width and 0 <= by < height:
                if canvas[by][bx][3] == 0:
                    if abs(dx) == beard_width or dy == 0:
                        canvas[by][bx] = BEARD_GRAY
                    else:
                        canvas[by][bx] = BEARD_WHITE if (dx + dy) % 2 == 0 else BEARD_GRAY
    
    # === POINTED HAT (fallen off to the side) ===
    hat_x = center_x - 15
    hat_y = head_y - 8
    
    # Hat lying on its side
    for i in range(18):
        # Draw sideways cone
        hat_height = 5 - i // 5
        for dy in range(-hat_height, hat_height + 1):
            hx = hat_x - i
            hy = hat_y + dy
            if 0 <= hx < width and 0 <= hy < height:
                if canvas[hy][hx][3] == 0:
                    if abs(dy) == hat_height:
                        canvas[hy][hx] = HAT_DARK
                    elif dy < 0:
                        canvas[hy][hx] = HAT_MID if (hx + hy) % 3 != 0 else HAT_DARK
                    else:
                        canvas[hy][hx] = HAT_LIGHT if (hx + hy) % 3 == 0 else HAT_MID
    
    # Star on fallen hat
    star_x = hat_x - 8
    star_y = hat_y
    if 0 <= star_x < width and 0 <= star_y < height:
        canvas[star_y][star_x] = HAT_STAR
        if star_x - 1 >= 0:
            canvas[star_y][star_x - 1] = HAT_STAR
    
    # === FADING MAGIC EFFECTS (dying out) ===
    fade_positions = [
        (orb_x - 2, orb_y - 5), (orb_x + 3, orb_y - 4),
        (center_x - 18, head_y - 5), (center_x + 15, head_y - 6),
        (center_x - 8, torso_y - 18), (center_x + 10, torso_y - 20),
    ]
    
    for fx, fy in fade_positions:
        if 0 <= fx < width and 0 <= fy < height:
            if canvas[fy][fx][3] == 0:
                canvas[fy][fx] = MAGIC_DIM if random.random() < 0.6 else MAGIC_FADE
    
    return canvas


def main():
    """Create and save all three magician hero images"""
    print("Creating blue wizard hero images...")
    
    # Create all three images
    magician_default = create_magician_default()
    magician_attack = create_magician_attack()
    magician_death = create_magician_death()
    
    # Convert to PIL and scale up
    scale = 4
    
    # Default pose
    img_default = Image.fromarray(magician_default, 'RGBA')
    img_default_scaled = img_default.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_default_scaled.save("../art/magician_hero.png")
    print("✓ Saved: magician_hero.png (256x256)")
    
    # Attack animation
    img_attack = Image.fromarray(magician_attack, 'RGBA')
    img_attack_scaled = img_attack.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_attack_scaled.save("../art/magician_hero_attack.png")
    print("✓ Saved: magician_hero_attack.png (256x256)")
    
    # Death animation
    img_death = Image.fromarray(magician_death, 'RGBA')
    img_death_scaled = img_death.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_death_scaled.save("../art/magician_hero_death.png")
    print("✓ Saved: magician_hero_death.png (256x256)")
    
    print("\n✅ Blue wizard magician hero creation complete!")
    print("\nFeatures:")
    print("- Default: Standing wizard with pointed hat, staff with glowing orb, extended hand casting")
    print("- Attack: Massive magical blast from raised staff, glowing eyes, intense energy beam")
    print("- Death: Wizard lying flat on ground with blood pool, fallen staff beside, hat knocked off")
    print("\nStyle: Pixel art classic blue wizard")
    print("Colors: Blue robes & pointed hat with stars, white beard, wooden staff with golden orb")


if __name__ == "__main__":
    main()
