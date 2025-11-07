"""
Create a pixel art warrior character PNG - matches ninja style
"""
from PIL import Image, ImageDraw
import numpy as np

def create_warrior():
    """Create a Minecraft-style warrior character"""
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
    
    # HEAD (8x8, centered at top)
    head_start_x = 12
    head_start_y = 4
    
    # Brown hair
    for y in range(head_start_y, head_start_y + 3):
        for x in range(head_start_x, head_start_x + 8):
            canvas[y][x] = BROWN_HAIR
    
    # Hair shadow/details
    canvas[head_start_y][head_start_x] = DARK_BROWN
    canvas[head_start_y][head_start_x + 7] = DARK_BROWN
    canvas[head_start_y + 1][head_start_x] = DARK_BROWN
    canvas[head_start_y + 1][head_start_x + 7] = DARK_BROWN
    
    # Face (skin tone)
    for y in range(head_start_y + 3, head_start_y + 8):
        for x in range(head_start_x, head_start_x + 8):
            canvas[y][x] = SKIN
    
    # Face shadow
    canvas[head_start_y + 7][head_start_x] = SKIN_SHADOW
    canvas[head_start_y + 7][head_start_x + 7] = SKIN_SHADOW
    
    # Eyes
    canvas[head_start_y + 4][head_start_x + 2] = BLACK
    canvas[head_start_y + 4][head_start_x + 5] = BLACK
    
    # Nose
    canvas[head_start_y + 5][head_start_x + 4] = SKIN_SHADOW
    
    # Mouth (smile)
    canvas[head_start_y + 6][head_start_x + 3] = BLACK
    canvas[head_start_y + 6][head_start_x + 4] = BLACK
    
    # BODY (8x12) - Red tunic with armor
    body_start_x = 12
    body_start_y = 12
    
    # Red tunic base
    for y in range(body_start_y, body_start_y + 12):
        for x in range(body_start_x, body_start_x + 8):
            canvas[y][x] = RED_SHIRT
    
    # Tunic shadows
    for y in range(body_start_y, body_start_y + 12):
        canvas[y][body_start_x] = DARK_RED
        canvas[y][body_start_x + 7] = DARK_RED
    
    # Chest armor plate
    for y in range(body_start_y + 1, body_start_y + 6):
        for x in range(body_start_x + 2, body_start_x + 6):
            canvas[y][x] = GRAY_ARMOR
    
    # Armor details/shadows
    canvas[body_start_y + 1][body_start_x + 2] = DARK_GRAY
    canvas[body_start_y + 1][body_start_x + 5] = DARK_GRAY
    canvas[body_start_y + 5][body_start_x + 2] = DARK_GRAY
    canvas[body_start_y + 5][body_start_x + 5] = DARK_GRAY
    
    # Belt
    for x in range(body_start_x + 1, body_start_x + 7):
        canvas[body_start_y + 7][x] = BROWN_SHIELD
    
    # Belt buckle
    canvas[body_start_y + 7][body_start_x + 3] = GOLD
    canvas[body_start_y + 7][body_start_x + 4] = GOLD
    
    # LEFT ARM (4x12) - holding shield
    left_arm_x = 8
    left_arm_y = 12
    
    # Arm (red sleeve)
    for y in range(left_arm_y, left_arm_y + 10):
        for x in range(left_arm_x, left_arm_x + 4):
            canvas[y][x] = RED_SHIRT
    
    # Arm shadow
    for y in range(left_arm_y, left_arm_y + 10):
        canvas[y][left_arm_x + 3] = DARK_RED
    
    # Hand
    canvas[left_arm_y + 9][left_arm_x + 1] = SKIN
    canvas[left_arm_y + 9][left_arm_x + 2] = SKIN
    
    # Shield (large)
    for y in range(left_arm_y + 2, left_arm_y + 10):
        canvas[y][left_arm_x] = BROWN_SHIELD
        canvas[y][left_arm_x + 1] = BROWN_SHIELD
    
    # Shield boss (center)
    canvas[left_arm_y + 5][left_arm_x] = SILVER
    canvas[left_arm_y + 5][left_arm_x + 1] = SILVER
    canvas[left_arm_y + 6][left_arm_x] = SILVER
    canvas[left_arm_y + 6][left_arm_x + 1] = SILVER
    
    # RIGHT ARM (4x12) - holding sword
    right_arm_x = 20
    right_arm_y = 12
    
    # Arm (red sleeve)
    for y in range(right_arm_y, right_arm_y + 10):
        for x in range(right_arm_x, right_arm_x + 4):
            canvas[y][x] = RED_SHIRT
    
    # Arm shadow
    for y in range(right_arm_y, right_arm_y + 10):
        canvas[y][right_arm_x] = DARK_RED
    
    # Hand
    canvas[right_arm_y + 9][right_arm_x + 1] = SKIN
    canvas[right_arm_y + 9][right_arm_x + 2] = SKIN
    
    # Sword blade (extended down)
    for y in range(right_arm_y + 10, right_arm_y + 16):
        canvas[y][right_arm_x + 2] = SILVER
    
    # Sword highlight
    for y in range(right_arm_y + 10, right_arm_y + 15):
        canvas[y][right_arm_x + 1] = DARK_GRAY
    
    # Sword hilt/guard
    canvas[right_arm_y + 9][right_arm_x + 1] = GOLD
    canvas[right_arm_y + 9][right_arm_x + 2] = GOLD
    canvas[right_arm_y + 9][right_arm_x + 3] = GOLD
    
    # LEFT LEG (4x8) - Blue pants
    left_leg_x = 12
    left_leg_y = 24
    
    for y in range(left_leg_y, left_leg_y + 8):
        for x in range(left_leg_x, left_leg_x + 3):
            canvas[y][x] = BLUE_PANTS
    
    # Leg shadow
    for y in range(left_leg_y, left_leg_y + 8):
        canvas[y][left_leg_x] = DARK_BLUE
    
    # RIGHT LEG (4x8) - Blue pants
    right_leg_x = 17
    right_leg_y = 24
    
    for y in range(right_leg_y, right_leg_y + 8):
        for x in range(right_leg_x, right_leg_x + 3):
            canvas[y][x] = BLUE_PANTS
    
    # Leg shadow
    for y in range(right_leg_y, right_leg_y + 8):
        canvas[y][right_leg_x] = DARK_BLUE
    
    # Boots (dark gray/armor)
    for x in range(left_leg_x, left_leg_x + 3):
        canvas[left_leg_y + 6][x] = DARK_GRAY
        canvas[left_leg_y + 7][x] = DARK_GRAY
    
    for x in range(right_leg_x, right_leg_x + 3):
        canvas[right_leg_y + 6][x] = DARK_GRAY
        canvas[right_leg_y + 7][x] = DARK_GRAY
    
    # Boot highlights
    canvas[left_leg_y + 6][left_leg_x + 1] = GRAY_ARMOR
    canvas[right_leg_y + 6][right_leg_x + 1] = GRAY_ARMOR
    
    # Shoulder armor pads
    canvas[body_start_y][body_start_x + 1] = GRAY_ARMOR
    canvas[body_start_y][body_start_x + 6] = GRAY_ARMOR
    canvas[body_start_y + 1][body_start_x + 1] = GRAY_ARMOR
    canvas[body_start_y + 1][body_start_x + 6] = GRAY_ARMOR
    
    # Convert numpy array to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 8x with nearest neighbor (pixel perfect)
    scale = 8
    img_scaled = img.resize((size * scale, size * scale), Image.NEAREST)
    
    # Save
    output_path = 'ascii_art/hero_warrior_v2.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {size * scale}x{size * scale} pixels")
    print(f"   Style: Pixel art warrior with sword and shield")
    print(f"   Features: Brown hair, red tunic, blue pants, gray armor, sword, shield")

if __name__ == '__main__':
    create_warrior()
