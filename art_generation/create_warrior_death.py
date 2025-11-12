"""
Create a pixel art warrior death image - dead warrior laying horizontal on ground with blood pool
"""
from PIL import Image, ImageDraw
import numpy as np

def create_warrior_death():
    """Create a dead warrior laying on the ground with blood pool"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette
    BROWN_HAIR = [101, 67, 33, 255]      # Hair
    DARK_BROWN = [70, 45, 20, 255]       # Hair shadow
    SKIN = [255, 220, 177, 255]          # Skin tone
    PALE_SKIN = [220, 200, 170, 255]     # Pale dead skin
    RED_SHIRT = [200, 50, 50, 255]       # Red tunic
    DARK_RED = [140, 30, 30, 255]        # Tunic shadow
    BLUE_PANTS = [50, 80, 180, 255]      # Blue pants
    DARK_BLUE = [30, 50, 120, 255]       # Pants shadow
    GRAY_ARMOR = [140, 140, 140, 255]    # Armor plates
    DARK_GRAY = [80, 80, 80, 255]        # Armor shadow
    SILVER = [192, 192, 192, 255]        # Sword
    GOLD = [255, 215, 0, 255]            # Sword hilt
    BLACK = [0, 0, 0, 255]               # Closed eyes
    BLOOD_DARK = [139, 0, 0, 255]        # Dark blood
    BLOOD_RED = [180, 0, 0, 255]         # Blood
    BLOOD_LIGHT = [200, 50, 50, 255]     # Blood highlights
    
    # BLOOD POOL (underneath the body)
    blood_center_x = 16
    blood_center_y = 24
    
    # Large irregular blood pool
    # Bottom layer (darkest)
    for y in range(blood_center_y - 2, blood_center_y + 6):
        for x in range(blood_center_x - 8, blood_center_x + 8):
            # Create irregular pool shape
            dist_x = abs(x - blood_center_x)
            dist_y = abs(y - blood_center_y)
            if dist_x + dist_y < 10:
                canvas[y][x] = BLOOD_DARK
    
    # Middle layer (brighter blood)
    for y in range(blood_center_y - 1, blood_center_y + 4):
        for x in range(blood_center_x - 6, blood_center_x + 6):
            dist_x = abs(x - blood_center_x)
            dist_y = abs(y - blood_center_y)
            if dist_x + dist_y < 8:
                canvas[y][x] = BLOOD_RED
    
    # Highlights (fresh blood)
    for y in range(blood_center_y, blood_center_y + 3):
        for x in range(blood_center_x - 4, blood_center_x + 4):
            dist_x = abs(x - blood_center_x)
            dist_y = abs(y - blood_center_y)
            if dist_x + dist_y < 5:
                canvas[y][x] = BLOOD_LIGHT
    
    # BODY LAYING HORIZONTAL (head to the left, feet to the right)
    body_y = 16  # Vertical center
    
    # HEAD (laying sideways) - leftmost part
    head_x = 4
    head_y = body_y - 3
    
    # Brown hair (side profile)
    for y in range(head_y, head_y + 3):
        for x in range(head_x, head_x + 6):
            canvas[y][x] = BROWN_HAIR
    
    # Hair shadow
    canvas[head_y][head_x] = DARK_BROWN
    canvas[head_y + 1][head_x] = DARK_BROWN
    
    # Face (pale dead skin)
    for y in range(head_y + 3, head_y + 6):
        for x in range(head_x, head_x + 6):
            canvas[y][x] = PALE_SKIN
    
    # Closed eyes (X marks - dead)
    canvas[head_y + 4][head_x + 1] = BLACK
    canvas[head_y + 4][head_x + 2] = BLACK
    canvas[head_y + 5][head_x + 2] = BLACK
    
    canvas[head_y + 4][head_x + 4] = BLACK
    canvas[head_y + 4][head_x + 5] = BLACK
    canvas[head_y + 5][head_x + 4] = BLACK
    
    # TORSO (red tunic with armor, horizontal)
    torso_x = head_x + 6
    torso_y = body_y - 2
    torso_width = 8
    torso_height = 4
    
    # Red tunic base
    for y in range(torso_y, torso_y + torso_height):
        for x in range(torso_x, torso_x + torso_width):
            canvas[y][x] = RED_SHIRT
    
    # Tunic shadows
    for y in range(torso_y, torso_y + torso_height):
        canvas[y][torso_x] = DARK_RED
        canvas[y][torso_x + torso_width - 1] = DARK_RED
    
    for x in range(torso_x, torso_x + torso_width):
        canvas[torso_y + torso_height - 1][x] = DARK_RED
    
    # Chest armor plate (damaged/cracked)
    canvas[torso_y + 1][torso_x + 2] = GRAY_ARMOR
    canvas[torso_y + 1][torso_x + 3] = GRAY_ARMOR
    canvas[torso_y + 1][torso_x + 5] = GRAY_ARMOR
    canvas[torso_y + 2][torso_x + 2] = GRAY_ARMOR
    canvas[torso_y + 2][torso_x + 5] = GRAY_ARMOR
    
    # Armor shadows
    canvas[torso_y + 1][torso_x + 2] = DARK_GRAY
    canvas[torso_y + 2][torso_x + 2] = DARK_GRAY
    
    # LEFT ARM (extended upward from body)
    left_arm_x = torso_x + 1
    left_arm_y = torso_y - 4
    
    # Red sleeve
    for y in range(left_arm_y, torso_y):
        canvas[y][left_arm_x] = RED_SHIRT
        canvas[y][left_arm_x + 1] = RED_SHIRT
    
    # Sleeve shadow
    for y in range(left_arm_y, torso_y):
        canvas[y][left_arm_x] = DARK_RED
    
    # Hand (pale, limp)
    canvas[left_arm_y][left_arm_x] = PALE_SKIN
    canvas[left_arm_y][left_arm_x + 1] = PALE_SKIN
    canvas[left_arm_y - 1][left_arm_x] = PALE_SKIN
    
    # Shoulder armor
    canvas[torso_y][left_arm_x] = GRAY_ARMOR
    canvas[torso_y][left_arm_x + 1] = GRAY_ARMOR
    
    # RIGHT ARM (extended downward from body)
    right_arm_x = torso_x + 6
    right_arm_y = torso_y + torso_height
    
    # Red sleeve
    for y in range(right_arm_y, right_arm_y + 4):
        canvas[y][right_arm_x] = RED_SHIRT
        canvas[y][right_arm_x + 1] = RED_SHIRT
    
    # Sleeve shadow
    for y in range(right_arm_y, right_arm_y + 4):
        canvas[y][right_arm_x] = DARK_RED
    
    # Hand (pale, laying limp)
    canvas[right_arm_y + 3][right_arm_x] = PALE_SKIN
    canvas[right_arm_y + 3][right_arm_x + 1] = PALE_SKIN
    canvas[right_arm_y + 4][right_arm_x] = PALE_SKIN
    
    # Shoulder armor
    canvas[torso_y][right_arm_x] = GRAY_ARMOR
    canvas[torso_y][right_arm_x + 1] = GRAY_ARMOR
    
    # LEGS (horizontal, blue pants, feet to the right)
    legs_x = torso_x + torso_width
    legs_y = torso_y
    legs_width = 6
    legs_height = 4
    
    # Blue pants
    for y in range(legs_y, legs_y + legs_height):
        for x in range(legs_x, legs_x + legs_width):
            canvas[y][x] = BLUE_PANTS
    
    # Pants shadows
    for y in range(legs_y, legs_y + legs_height):
        canvas[y][legs_x] = DARK_BLUE
    
    # Boots (dark gray, horizontal)
    feet_x = legs_x + legs_width
    for y in range(legs_y, legs_y + legs_height):
        canvas[y][feet_x] = DARK_GRAY
        canvas[y][feet_x + 1] = DARK_GRAY
    
    # Boot highlights
    canvas[legs_y][feet_x] = GRAY_ARMOR
    canvas[legs_y + 1][feet_x] = GRAY_ARMOR
    
    # SWORD (dropped beside the body)
    sword_x = torso_x + 3
    sword_y = torso_y - 7
    
    # Silver blade (laying diagonally)
    for i in range(10):
        canvas[sword_y + i][sword_x + i // 3] = SILVER
        canvas[sword_y + i][sword_x + i // 3 + 1] = SILVER
    
    # Sword edge (darker)
    for i in range(10):
        canvas[sword_y + i][sword_x + i // 3] = DARK_GRAY
    
    # Gold hilt/guard
    canvas[sword_y + 9][sword_x + 2] = GOLD
    canvas[sword_y + 9][sword_x + 3] = GOLD
    canvas[sword_y + 9][sword_x + 4] = GOLD
    canvas[sword_y + 10][sword_x + 3] = GOLD
    
    # SHIELD (fallen beside body)
    shield_x = head_x - 3
    shield_y = head_y + 2
    
    # Brown shield (small, laying down)
    for y in range(shield_y, shield_y + 4):
        for x in range(shield_x, shield_x + 3):
            canvas[y][x] = DARK_BROWN
    
    # Shield rim (darker)
    canvas[shield_y][shield_x] = BLACK
    canvas[shield_y][shield_x + 2] = BLACK
    canvas[shield_y + 3][shield_x] = BLACK
    canvas[shield_y + 3][shield_x + 2] = BLACK
    
    # Blood splatters on torso
    canvas[torso_y + 1][torso_x + 4] = BLOOD_RED
    canvas[torso_y + 2][torso_x + 3] = BLOOD_DARK
    canvas[torso_y + 2][torso_x + 4] = BLOOD_RED
    canvas[torso_y + 2][torso_x + 5] = BLOOD_RED
    canvas[torso_y + 3][torso_x + 4] = BLOOD_DARK
    
    # Blood drip from wound
    canvas[torso_y + 3][torso_x + 4] = BLOOD_RED
    canvas[right_arm_y][right_arm_x] = BLOOD_DARK
    
    # Convert numpy array to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 8x with nearest neighbor (pixel perfect)
    scale = 8
    img_scaled = img.resize((size * scale, size * scale), Image.NEAREST)
    
    # Save
    output_path = 'art/warrior_death.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {size * scale}x{size * scale} pixels")
    print(f"   Style: Pixel art dead warrior")
    print(f"   Features: Laying horizontal, brown hair, pale skin, closed eyes (X marks),")
    print(f"            red tunic with damaged armor, blue pants, dark boots,")
    print(f"            dropped sword and shield, large blood pool, blood splatters on chest")

if __name__ == '__main__':
    create_warrior_death()
