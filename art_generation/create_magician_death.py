"""
Create a pixel art magician death image - dead magician laying horizontal on ground with blood pool
"""
from PIL import Image, ImageDraw
import numpy as np

def create_magician_death():
    """Create a dead magician laying on the ground with blood pool"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette
    GRAY_BEARD = [180, 180, 180, 255]    # Gray beard
    WHITE_BEARD = [240, 240, 240, 255]   # Beard highlight
    SKIN = [255, 220, 177, 255]          # Skin tone
    PALE_SKIN = [220, 200, 170, 255]     # Pale dead skin
    PURPLE_ROBE = [120, 50, 180, 255]    # Purple robe
    DARK_PURPLE = [70, 30, 110, 255]     # Robe shadow
    BLUE_ROBE = [50, 80, 200, 255]       # Blue accents
    GOLD = [255, 215, 0, 255]            # Gold trim
    BROWN_STAFF = [101, 67, 33, 255]     # Wooden staff
    DARK_BROWN = [70, 45, 20, 255]       # Staff shadow
    BLACK = [0, 0, 0, 255]               # Closed eyes
    PURPLE_HAT = [100, 40, 150, 255]     # Wizard hat
    DARK_RED = [139, 0, 0, 255]          # Dark blood
    RED_BLOOD = [180, 0, 0, 255]         # Blood
    LIGHT_BLOOD = [200, 50, 50, 255]     # Blood highlights
    
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
                canvas[y][x] = DARK_RED
    
    # Middle layer (brighter blood)
    for y in range(blood_center_y - 1, blood_center_y + 4):
        for x in range(blood_center_x - 6, blood_center_x + 6):
            dist_x = abs(x - blood_center_x)
            dist_y = abs(y - blood_center_y)
            if dist_x + dist_y < 8:
                canvas[y][x] = RED_BLOOD
    
    # Highlights (fresh blood)
    for y in range(blood_center_y, blood_center_y + 3):
        for x in range(blood_center_x - 4, blood_center_x + 4):
            dist_x = abs(x - blood_center_x)
            dist_y = abs(y - blood_center_y)
            if dist_x + dist_y < 5:
                canvas[y][x] = LIGHT_BLOOD
    
    # BODY LAYING HORIZONTAL (head to the left, feet to the right)
    body_y = 16  # Vertical center
    
    # HEAD (laying sideways) - leftmost part
    head_x = 4
    head_y = body_y - 3
    
    # Face (pale dead skin)
    for y in range(head_y, head_y + 6):
        for x in range(head_x, head_x + 6):
            canvas[y][x] = PALE_SKIN
    
    # Closed eyes (X marks)
    canvas[head_y + 2][head_x + 1] = BLACK
    canvas[head_y + 2][head_x + 2] = BLACK
    canvas[head_y + 3][head_x + 2] = BLACK
    
    canvas[head_y + 2][head_x + 4] = BLACK
    canvas[head_y + 2][head_x + 5] = BLACK
    canvas[head_y + 3][head_x + 4] = BLACK
    
    # Gray beard (sprawled out)
    for y in range(head_y + 3, head_y + 6):
        for x in range(head_x, head_x + 6):
            canvas[y][x] = GRAY_BEARD
    
    # Beard extends down
    for x in range(head_x + 1, head_x + 5):
        canvas[head_y + 6][x] = GRAY_BEARD
        canvas[head_y + 7][x] = GRAY_BEARD
    
    # Beard highlights
    canvas[head_y + 4][head_x + 2] = WHITE_BEARD
    canvas[head_y + 5][head_x + 3] = WHITE_BEARD
    
    # WIZARD HAT (fallen off, next to head)
    hat_x = head_x - 3
    hat_y = head_y - 2
    
    # Hat laying sideways (pointing left)
    for x in range(hat_x, hat_x + 4):
        canvas[hat_y + 2][x] = PURPLE_HAT
        canvas[hat_y + 3][x] = PURPLE_HAT
    
    canvas[hat_y + 1][hat_x + 1] = PURPLE_HAT
    canvas[hat_y + 1][hat_x + 2] = PURPLE_HAT
    canvas[hat_y + 4][hat_x + 1] = PURPLE_HAT
    canvas[hat_y + 4][hat_x + 2] = PURPLE_HAT
    
    canvas[hat_y][hat_x + 2] = PURPLE_HAT
    canvas[hat_y + 5][hat_x + 2] = PURPLE_HAT
    
    # Gold star on hat
    canvas[hat_y + 2][hat_x + 2] = GOLD
    
    # TORSO (purple robe, horizontal)
    torso_x = head_x + 6
    torso_y = body_y - 2
    torso_width = 8
    torso_height = 4
    
    for y in range(torso_y, torso_y + torso_height):
        for x in range(torso_x, torso_x + torso_width):
            canvas[y][x] = PURPLE_ROBE
    
    # Robe shadows (darker purple)
    for y in range(torso_y, torso_y + torso_height):
        canvas[y][torso_x] = DARK_PURPLE
        canvas[y][torso_x + torso_width - 1] = DARK_PURPLE
    
    for x in range(torso_x, torso_x + torso_width):
        canvas[torso_y + torso_height - 1][x] = DARK_PURPLE
    
    # Gold trim on robe
    for x in range(torso_x + 1, torso_x + torso_width - 1):
        canvas[torso_y][x] = GOLD
    
    # LEFT ARM (extended upward from body)
    left_arm_x = torso_x + 2
    left_arm_y = torso_y - 4
    
    # Purple sleeve
    for y in range(left_arm_y, torso_y):
        canvas[y][left_arm_x] = PURPLE_ROBE
        canvas[y][left_arm_x + 1] = PURPLE_ROBE
    
    # Sleeve shadow
    for y in range(left_arm_y, torso_y):
        canvas[y][left_arm_x] = DARK_PURPLE
    
    # Hand (pale)
    canvas[left_arm_y][left_arm_x] = PALE_SKIN
    canvas[left_arm_y][left_arm_x + 1] = PALE_SKIN
    canvas[left_arm_y - 1][left_arm_x] = PALE_SKIN
    
    # RIGHT ARM (extended downward from body)
    right_arm_x = torso_x + 5
    right_arm_y = torso_y + torso_height
    
    # Purple sleeve
    for y in range(right_arm_y, right_arm_y + 4):
        canvas[y][right_arm_x] = PURPLE_ROBE
        canvas[y][right_arm_x + 1] = PURPLE_ROBE
    
    # Sleeve shadow
    for y in range(right_arm_y, right_arm_y + 4):
        canvas[y][right_arm_x] = DARK_PURPLE
    
    # Hand (pale, laying limp)
    canvas[right_arm_y + 3][right_arm_x] = PALE_SKIN
    canvas[right_arm_y + 3][right_arm_x + 1] = PALE_SKIN
    canvas[right_arm_y + 4][right_arm_x] = PALE_SKIN
    
    # LEGS (horizontal, feet to the right)
    legs_x = torso_x + torso_width
    legs_y = torso_y
    legs_width = 6
    legs_height = 4
    
    # Purple robe continues for legs
    for y in range(legs_y, legs_y + legs_height):
        for x in range(legs_x, legs_x + legs_width):
            canvas[y][x] = PURPLE_ROBE
    
    # Leg shadows
    for y in range(legs_y, legs_y + legs_height):
        canvas[y][legs_x] = DARK_PURPLE
    
    # Feet (blue shoes, horizontal)
    feet_x = legs_x + legs_width
    canvas[legs_y][feet_x] = BLUE_ROBE
    canvas[legs_y + 1][feet_x] = BLUE_ROBE
    canvas[legs_y + 2][feet_x] = BLUE_ROBE
    canvas[legs_y + 3][feet_x] = BLUE_ROBE
    
    # STAFF (dropped beside the body)
    staff_x = torso_x + 3
    staff_y = torso_y - 8
    
    # Wooden staff laying diagonally
    for i in range(12):
        canvas[staff_y + i][staff_x + i // 3] = BROWN_STAFF
    
    # Staff shadow
    for i in range(12):
        canvas[staff_y + i][staff_x + i // 3 - 1] = DARK_BROWN
    
    # Staff broken at top (no magic crystal - it's dead)
    
    # Blood splatter near torso
    canvas[torso_y + 1][torso_x + 3] = RED_BLOOD
    canvas[torso_y + 2][torso_x + 4] = DARK_RED
    canvas[torso_y + 1][torso_x + 5] = RED_BLOOD
    
    # Convert numpy array to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 8x with nearest neighbor (pixel perfect)
    scale = 8
    img_scaled = img.resize((size * scale, size * scale), Image.NEAREST)
    
    # Save
    output_path = 'art/magician_death.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {size * scale}x{size * scale} pixels")
    print(f"   Style: Pixel art dead magician")
    print(f"   Features: Laying horizontal, fallen wizard hat, sprawled beard,")
    print(f"            purple robe, dropped broken staff, large blood pool,")
    print(f"            pale skin, closed eyes (X marks)")

if __name__ == '__main__':
    create_magician_death()
