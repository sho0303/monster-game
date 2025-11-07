"""
Create an animated attack version of the warrior character
Shows the warrior in a powerful sword strike with dynamic motion and battle effects
"""
from PIL import Image, ImageDraw
import numpy as np

def create_warrior_attack():
    """Create a Minecraft-style warrior in sword attack animation"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette
    BROWN_HAIR = [101, 67, 33, 255]      # Hair
    DARK_BROWN = [70, 45, 20, 255]       # Hair shadow
    SKIN = [255, 220, 177, 255]          # Skin tone
    SKIN_SHADOW = [220, 180, 140, 255]   # Skin shadow
    RED_SHIRT = [200, 50, 50, 255]       # Red tunic
    DARK_RED = [140, 30, 30, 255]        # Tunic shadow
    BLUE_PANTS = [50, 80, 180, 255]      # Blue pants
    DARK_BLUE = [30, 50, 120, 255]       # Pants shadow
    GRAY_ARMOR = [140, 140, 140, 255]    # Armor plates
    DARK_GRAY = [80, 80, 80, 255]        # Armor shadow
    SILVER = [192, 192, 192, 255]        # Sword
    GOLD = [255, 215, 0, 255]            # Sword hilt
    BROWN_SHIELD = [139, 90, 43, 255]    # Shield
    BLACK = [0, 0, 0, 255]               # Eyes, outlines
    
    # Attack effect colors
    WHITE_FLASH = [255, 255, 255, 255]   # Sword flash
    YELLOW_SPARK = [255, 255, 0, 255]    # Impact sparks
    ORANGE_FIRE = [255, 165, 0, 255]     # Battle energy
    LIGHT_BLUE = [173, 216, 230, 180]    # Motion blur
    BRIGHT_SILVER = [220, 220, 220, 255] # Sword gleam
    RED_ENERGY = [255, 0, 0, 180]        # Battle aura
    
    # HEAD (8x8, intense battle focus)
    head_start_x = 11  # Shifted slightly for attack lean
    head_start_y = 3   # Higher for forward lean
    
    # Brown hair (windswept from battle motion)
    for y in range(head_start_y, head_start_y + 3):
        for x in range(head_start_x, head_start_x + 8):
            if x < size:
                canvas[y][x] = BROWN_HAIR
    
    # Hair flowing motion effect
    canvas[head_start_y][head_start_x + 8] = BROWN_HAIR if head_start_x + 8 < size else None
    canvas[head_start_y + 1][head_start_x + 8] = DARK_BROWN if head_start_x + 8 < size else None
    
    # Hair shadow/details with motion
    canvas[head_start_y][head_start_x] = DARK_BROWN
    canvas[head_start_y][head_start_x + 7] = DARK_BROWN
    canvas[head_start_y + 1][head_start_x] = DARK_BROWN
    if head_start_x + 7 < size:
        canvas[head_start_y + 1][head_start_x + 7] = DARK_BROWN
    
    # Face (skin tone, focused expression)
    for y in range(head_start_y + 3, head_start_y + 8):
        for x in range(head_start_x, head_start_x + 8):
            if x < size:
                canvas[y][x] = SKIN
    
    # Face shadow (more dramatic for battle intensity)
    canvas[head_start_y + 7][head_start_x] = SKIN_SHADOW
    if head_start_x + 7 < size:
        canvas[head_start_y + 7][head_start_x + 7] = SKIN_SHADOW
    
    # Eyes (intense battle focus)
    canvas[head_start_y + 4][head_start_x + 2] = BLACK
    canvas[head_start_y + 4][head_start_x + 5] = BLACK
    
    # Determined expression (gritted teeth)
    canvas[head_start_y + 6][head_start_x + 3] = BLACK
    canvas[head_start_y + 6][head_start_x + 4] = BLACK
    
    # BODY (8x12, leaning into attack)
    body_start_x = 11  # Shifted for attack stance
    body_start_y = 11
    
    # Red tunic base (flowing with motion)
    for y in range(body_start_y, body_start_y + 12):
        for x in range(body_start_x, body_start_x + 8):
            if x < size and y < size:
                canvas[y][x] = RED_SHIRT
    
    # Tunic flowing motion effect
    for i in range(3):
        trail_x = body_start_x + 8 + i
        if trail_x < size:
            canvas[body_start_y + 4 + i][trail_x] = DARK_RED
            canvas[body_start_y + 6 + i][trail_x] = RED_ENERGY
    
    # Tunic shadows
    for y in range(body_start_y, body_start_y + 12):
        if y < size:
            canvas[y][body_start_x] = DARK_RED
            if body_start_x + 7 < size:
                canvas[y][body_start_x + 7] = DARK_RED
    
    # Chest armor plate (gleaming in battle)
    for y in range(body_start_y + 1, body_start_y + 6):
        for x in range(body_start_x + 2, body_start_x + 6):
            if x < size and y < size:
                canvas[y][x] = GRAY_ARMOR
    
    # Enhanced armor details with battle gleam
    canvas[body_start_y + 1][body_start_x + 2] = BRIGHT_SILVER
    canvas[body_start_y + 1][body_start_x + 5] = DARK_GRAY
    canvas[body_start_y + 3][body_start_x + 3] = WHITE_FLASH  # Armor gleam
    canvas[body_start_y + 5][body_start_x + 2] = DARK_GRAY
    canvas[body_start_y + 5][body_start_x + 5] = DARK_GRAY
    
    # Belt (secured for battle)
    for x in range(body_start_x + 1, body_start_x + 7):
        if x < size:
            canvas[body_start_y + 7][x] = BROWN_SHIELD
    
    # Belt buckle (glinting)
    canvas[body_start_y + 7][body_start_x + 3] = YELLOW_SPARK  # Brighter gold
    canvas[body_start_y + 7][body_start_x + 4] = GOLD
    
    # LEFT ARM (raised with shield in defensive position)
    left_arm_x = 7   # Pulled back for defense
    left_arm_y = 9   # Raised higher for protection
    
    # Arm (red sleeve)
    for y in range(left_arm_y, left_arm_y + 8):
        for x in range(left_arm_x, left_arm_x + 4):
            if x < size and y < size:
                canvas[y][x] = RED_SHIRT
    
    # Motion blur behind shield arm
    for i in range(2):
        blur_x = left_arm_x - i - 1
        if blur_x >= 0:
            canvas[left_arm_y + 2][blur_x] = LIGHT_BLUE
            canvas[left_arm_y + 4][blur_x] = LIGHT_BLUE
    
    # Hand gripping shield
    canvas[left_arm_y + 7][left_arm_x + 2] = SKIN
    canvas[left_arm_y + 7][left_arm_x + 3] = SKIN
    
    # Shield (positioned defensively)
    for y in range(left_arm_y, left_arm_y + 8):
        if y < size:
            canvas[y][left_arm_x] = BROWN_SHIELD
            canvas[y][left_arm_x + 1] = BROWN_SHIELD
    
    # Shield boss (metallic gleam)
    canvas[left_arm_y + 3][left_arm_x] = BRIGHT_SILVER
    canvas[left_arm_y + 3][left_arm_x + 1] = SILVER
    canvas[left_arm_y + 4][left_arm_x] = SILVER
    canvas[left_arm_y + 4][left_arm_x + 1] = BRIGHT_SILVER
    
    # RIGHT ARM (extended in powerful sword strike)
    right_arm_x = 17  # Extended further for dramatic swing
    right_arm_y = 8   # Raised for overhead strike
    
    # Arm (red sleeve, extended)
    for y in range(right_arm_y, right_arm_y + 6):  # Shorter due to extension
        for x in range(right_arm_x, right_arm_x + 6):  # Extended reach
            if x < size and y < size:
                canvas[y][x] = RED_SHIRT
    
    # Motion trail behind sword arm
    for i in range(4):
        trail_x = right_arm_x - i - 1
        if trail_x >= 0:
            canvas[right_arm_y + 2][trail_x] = LIGHT_BLUE
            canvas[right_arm_y + 3][trail_x] = RED_ENERGY
    
    # Hand gripping sword (extended)
    canvas[right_arm_y + 5][right_arm_x + 4] = SKIN
    canvas[right_arm_y + 5][right_arm_x + 5] = SKIN
    
    # MASSIVE SWORD STRIKE EFFECT
    sword_x = right_arm_x + 6
    sword_y = right_arm_y + 3
    
    # Sword blade (angled in striking motion)
    sword_positions = [
        (sword_x, sword_y),
        (sword_x + 1, sword_y + 1),
        (sword_x + 2, sword_y + 2),
        (sword_x + 3, sword_y + 3),
        (sword_x + 4, sword_y + 4),
        (sword_x + 5, sword_y + 5),
        (sword_x + 6, sword_y + 6),
        (sword_x + 7, sword_y + 7),
    ]
    
    for sx, sy in sword_positions:
        if 0 <= sx < size and 0 <= sy < size:
            canvas[sy][sx] = SILVER
    
    # Sword gleam (bright highlight)
    gleam_positions = [
        (sword_x, sword_y - 1),
        (sword_x + 1, sword_y),
        (sword_x + 2, sword_y + 1),
        (sword_x + 3, sword_y + 2),
        (sword_x + 4, sword_y + 3),
    ]
    
    for gx, gy in gleam_positions:
        if 0 <= gx < size and 0 <= gy < size:
            canvas[gy][gx] = WHITE_FLASH
    
    # SWORD ENERGY TRAIL (speed lines and effects)
    trail_positions = [
        (sword_x + 8, sword_y + 8, YELLOW_SPARK),
        (sword_x + 9, sword_y + 9, ORANGE_FIRE),
        (sword_x + 7, sword_y + 6, WHITE_FLASH),
        (sword_x + 8, sword_y + 7, BRIGHT_SILVER),
        (sword_x + 9, sword_y + 8, YELLOW_SPARK),
    ]
    
    for tx, ty, color in trail_positions:
        if 0 <= tx < size and 0 <= ty < size:
            canvas[ty][tx] = color
    
    # Sword hilt/guard (golden gleam)
    hilt_x = right_arm_x + 5
    hilt_y = right_arm_y + 4
    
    canvas[hilt_y][hilt_x] = YELLOW_SPARK  # Brighter gold
    canvas[hilt_y][hilt_x + 1] = GOLD
    canvas[hilt_y + 1][hilt_x] = GOLD
    
    # IMPACT SPARKS around sword strike
    spark_positions = [
        (sword_x + 6, sword_y + 5, YELLOW_SPARK),
        (sword_x + 7, sword_y + 6, WHITE_FLASH),
        (sword_x + 8, sword_y + 7, ORANGE_FIRE),
        (sword_x + 5, sword_y + 7, YELLOW_SPARK),
        (sword_x + 9, sword_y + 6, WHITE_FLASH),
    ]
    
    for spx, spy, color in spark_positions:
        if 0 <= spx < size and 0 <= spy < size:
            canvas[spy][spx] = color
    
    # LEFT LEG (braced for powerful strike)
    left_leg_x = 10  # Wider stance for stability
    left_leg_y = 23
    
    for y in range(left_leg_y, min(left_leg_y + 8, size)):
        for x in range(left_leg_x, left_leg_x + 4):  # Wider leg
            if x < size:
                canvas[y][x] = BLUE_PANTS
    
    # Leg shadow
    for y in range(left_leg_y, min(left_leg_y + 8, size)):
        canvas[y][left_leg_x] = DARK_BLUE
    
    # RIGHT LEG (lunging forward in attack)
    right_leg_x = 16
    right_leg_y = 24
    
    for y in range(right_leg_y, min(right_leg_y + 8, size)):
        for x in range(right_leg_x, right_leg_x + 4):
            if x < size:
                canvas[y][x] = BLUE_PANTS
    
    # Leg shadow
    for y in range(right_leg_y, min(right_leg_y + 8, size)):
        canvas[y][right_leg_x] = DARK_BLUE
    
    # Battle boots (armored, with ground impact)
    for x in range(left_leg_x, left_leg_x + 4):
        if x < size and left_leg_y + 6 < size:
            canvas[left_leg_y + 6][x] = GRAY_ARMOR  # Brighter armor
            if left_leg_y + 7 < size:
                canvas[left_leg_y + 7][x] = DARK_GRAY
    
    for x in range(right_leg_x, right_leg_x + 4):
        if x < size and right_leg_y + 6 < size:
            canvas[right_leg_y + 6][x] = GRAY_ARMOR
            if right_leg_y + 7 < size:
                canvas[right_leg_y + 7][x] = DARK_GRAY
    
    # Ground impact effects (dust and debris)
    ground_effects = [
        (left_leg_x - 1, left_leg_y + 8, LIGHT_BLUE),
        (left_leg_x + 2, left_leg_y + 8, DARK_GRAY),
        (right_leg_x + 1, right_leg_y + 8, LIGHT_BLUE),
        (right_leg_x + 3, right_leg_y + 8, GRAY_ARMOR),
    ]
    
    for gx, gy, color in ground_effects:
        if 0 <= gx < size and 0 <= gy < size:
            canvas[gy][gx] = color
    
    # Enhanced shoulder armor (gleaming in battle)
    canvas[body_start_y][body_start_x + 1] = BRIGHT_SILVER
    canvas[body_start_y][body_start_x + 6] = GRAY_ARMOR
    canvas[body_start_y + 1][body_start_x + 1] = GRAY_ARMOR
    if body_start_x + 6 < size:
        canvas[body_start_y + 1][body_start_x + 6] = BRIGHT_SILVER
    
    # Battle aura surrounding the warrior
    aura_positions = [
        (head_start_x - 1, head_start_y + 2),
        (body_start_x - 1, body_start_y + 4),
        (body_start_x + 8, body_start_y + 6),
        (right_leg_x + 4, right_leg_y + 2),
    ]
    
    for ax, ay in aura_positions:
        if 0 <= ax < size and 0 <= ay < size:
            canvas[ay][ax] = RED_ENERGY
    
    # Convert numpy array to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 8x with nearest neighbor (pixel perfect)
    scale = 8
    img_scaled = img.resize((size * scale, size * scale), Image.NEAREST)
    
    # Save
    import os
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'art', 'warrior_attack.png')
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {size * scale}x{size * scale} pixels")
    print(f"   Style: Animated warrior sword attack with battle effects")
    print(f"   Features: Dynamic strike pose, sword energy trail, impact sparks")
    print(f"   Animation: Flowing cape, battle stance, ground impact, armor gleam")
    print(f"   Effects: Sword flash, motion blur, battle aura, sparks")

if __name__ == '__main__':
    create_warrior_attack()