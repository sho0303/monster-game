"""
Create a pixel art magician character PNG - matches ninja/warrior style
"""
from PIL import Image, ImageDraw
import numpy as np

def create_magician():
    """Create a Minecraft-style magician/wizard character"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette
    GRAY_BEARD = [180, 180, 180, 255]    # Gray beard
    WHITE_BEARD = [240, 240, 240, 255]   # Beard highlight
    SKIN = [255, 220, 177, 255]          # Skin tone
    PURPLE_ROBE = [120, 50, 180, 255]    # Purple robe
    DARK_PURPLE = [70, 30, 110, 255]     # Robe shadow
    BLUE_ROBE = [50, 80, 200, 255]       # Blue accents
    DARK_BLUE = [30, 50, 130, 255]       # Blue shadow
    GOLD = [255, 215, 0, 255]            # Gold trim
    DARK_GOLD = [200, 160, 0, 255]       # Gold shadow
    BROWN_STAFF = [101, 67, 33, 255]     # Wooden staff
    DARK_BROWN = [70, 45, 20, 255]       # Staff shadow
    CYAN_MAGIC = [0, 255, 255, 255]      # Magic glow
    BLUE_MAGIC = [100, 150, 255, 255]    # Magic orb
    BLACK = [0, 0, 0, 255]               # Eyes, outlines
    PURPLE_HAT = [100, 40, 150, 255]     # Wizard hat
    
    # WIZARD HAT (tall pointy hat)
    hat_start_x = 12
    hat_start_y = 0
    
    # Hat tip (pointy top)
    canvas[hat_start_y][hat_start_x + 3] = PURPLE_HAT
    canvas[hat_start_y][hat_start_x + 4] = PURPLE_HAT
    
    canvas[hat_start_y + 1][hat_start_x + 2] = PURPLE_HAT
    canvas[hat_start_y + 1][hat_start_x + 3] = PURPLE_HAT
    canvas[hat_start_y + 1][hat_start_x + 4] = PURPLE_HAT
    canvas[hat_start_y + 1][hat_start_x + 5] = PURPLE_HAT
    
    canvas[hat_start_y + 2][hat_start_x + 1] = PURPLE_HAT
    canvas[hat_start_y + 2][hat_start_x + 2] = PURPLE_HAT
    canvas[hat_start_y + 2][hat_start_x + 3] = PURPLE_HAT
    canvas[hat_start_y + 2][hat_start_x + 4] = PURPLE_HAT
    canvas[hat_start_y + 2][hat_start_x + 5] = PURPLE_HAT
    canvas[hat_start_y + 2][hat_start_x + 6] = PURPLE_HAT
    
    # Hat brim
    for x in range(hat_start_x, hat_start_x + 8):
        canvas[hat_start_y + 3][x] = PURPLE_HAT
    
    # Gold stars on hat
    canvas[hat_start_y + 2][hat_start_x + 3] = GOLD
    canvas[hat_start_y + 1][hat_start_x + 4] = GOLD
    
    # HEAD (8x8)
    head_start_x = 12
    head_start_y = 4
    
    # Face (skin tone) - only top part visible
    for y in range(head_start_y, head_start_y + 5):
        for x in range(head_start_x, head_start_x + 8):
            canvas[y][x] = SKIN
    
    # Eyes (wise old wizard)
    canvas[head_start_y + 2][head_start_x + 2] = BLACK
    canvas[head_start_y + 2][head_start_x + 5] = BLACK
    
    # Gray eyebrows
    canvas[head_start_y + 1][head_start_x + 2] = GRAY_BEARD
    canvas[head_start_y + 1][head_start_x + 5] = GRAY_BEARD
    
    # Long gray beard (covers lower face and chest)
    for y in range(head_start_y + 4, head_start_y + 8):
        for x in range(head_start_x + 1, head_start_x + 7):
            canvas[y][x] = GRAY_BEARD
    
    # Beard highlights
    canvas[head_start_y + 5][head_start_x + 3] = WHITE_BEARD
    canvas[head_start_y + 6][head_start_x + 4] = WHITE_BEARD
    canvas[head_start_y + 5][head_start_x + 4] = WHITE_BEARD
    
    # BODY (8x12) - Purple robe
    body_start_x = 12
    body_start_y = 12
    
    # Beard continues down chest
    for y in range(body_start_y, body_start_y + 4):
        for x in range(body_start_x + 2, body_start_x + 6):
            canvas[y][x] = GRAY_BEARD
    
    # Purple robe base
    for y in range(body_start_y, body_start_y + 12):
        for x in range(body_start_x, body_start_x + 8):
            if canvas[y][x][3] == 0:  # Don't overwrite beard
                canvas[y][x] = PURPLE_ROBE
    
    # Robe shadows on sides
    for y in range(body_start_y + 4, body_start_y + 12):
        canvas[y][body_start_x] = DARK_PURPLE
        canvas[y][body_start_x + 7] = DARK_PURPLE
    
    # Gold trim on robe
    for x in range(body_start_x + 1, body_start_x + 7):
        canvas[body_start_y + 4][x] = GOLD
        canvas[body_start_y + 5][x] = DARK_GOLD
    
    # Blue accent on robe center
    canvas[body_start_y + 7][body_start_x + 3] = BLUE_ROBE
    canvas[body_start_y + 7][body_start_x + 4] = BLUE_ROBE
    canvas[body_start_y + 8][body_start_x + 3] = BLUE_ROBE
    canvas[body_start_y + 8][body_start_x + 4] = BLUE_ROBE
    
    # LEFT ARM (4x12) - holding magic orb
    left_arm_x = 8
    left_arm_y = 12
    
    # Purple sleeve
    for y in range(left_arm_y, left_arm_y + 10):
        for x in range(left_arm_x, left_arm_x + 4):
            canvas[y][x] = PURPLE_ROBE
    
    # Sleeve shadow
    for y in range(left_arm_y, left_arm_y + 10):
        canvas[y][left_arm_x + 3] = DARK_PURPLE
    
    # Hand
    canvas[left_arm_y + 9][left_arm_x + 1] = SKIN
    canvas[left_arm_y + 9][left_arm_x + 2] = SKIN
    
    # Magic orb (glowing blue sphere)
    canvas[left_arm_y + 10][left_arm_x + 1] = CYAN_MAGIC
    canvas[left_arm_y + 10][left_arm_x + 2] = CYAN_MAGIC
    canvas[left_arm_y + 11][left_arm_x + 1] = BLUE_MAGIC
    canvas[left_arm_y + 11][left_arm_x + 2] = BLUE_MAGIC
    canvas[left_arm_y + 12][left_arm_x + 1] = BLUE_MAGIC
    canvas[left_arm_y + 12][left_arm_x + 2] = BLUE_MAGIC
    
    # Orb glow effect
    canvas[left_arm_y + 10][left_arm_x] = CYAN_MAGIC
    canvas[left_arm_y + 10][left_arm_x + 3] = CYAN_MAGIC
    canvas[left_arm_y + 11][left_arm_x] = BLUE_MAGIC
    canvas[left_arm_y + 11][left_arm_x + 3] = BLUE_MAGIC
    
    # RIGHT ARM (4x12) - holding staff
    right_arm_x = 20
    right_arm_y = 12
    
    # Purple sleeve
    for y in range(right_arm_y, right_arm_y + 10):
        for x in range(right_arm_x, right_arm_x + 4):
            canvas[y][x] = PURPLE_ROBE
    
    # Sleeve shadow
    for y in range(right_arm_y, right_arm_y + 10):
        canvas[y][right_arm_x] = DARK_PURPLE
    
    # Hand
    canvas[right_arm_y + 9][right_arm_x + 1] = SKIN
    canvas[right_arm_y + 9][right_arm_x + 2] = SKIN
    
    # Wooden staff (long, extends beyond character)
    for y in range(right_arm_y - 2, right_arm_y + 18):
        canvas[y][right_arm_x + 2] = BROWN_STAFF
    
    # Staff shadow
    for y in range(right_arm_y - 2, right_arm_y + 18):
        canvas[y][right_arm_x + 1] = DARK_BROWN
    
    # Magic crystal on top of staff
    canvas[right_arm_y - 3][right_arm_x + 2] = CYAN_MAGIC
    canvas[right_arm_y - 2][right_arm_x + 1] = BLUE_MAGIC
    canvas[right_arm_y - 2][right_arm_x + 2] = CYAN_MAGIC
    canvas[right_arm_y - 2][right_arm_x + 3] = BLUE_MAGIC
    canvas[right_arm_y - 1][right_arm_x + 2] = BLUE_MAGIC
    
    # LEFT LEG (4x8) - Purple robe continues
    left_leg_x = 12
    left_leg_y = 24
    
    for y in range(left_leg_y, left_leg_y + 8):
        for x in range(left_leg_x, left_leg_x + 3):
            canvas[y][x] = PURPLE_ROBE
    
    # Robe shadow
    for y in range(left_leg_y, left_leg_y + 8):
        canvas[y][left_leg_x] = DARK_PURPLE
    
    # RIGHT LEG (4x8) - Purple robe
    right_leg_x = 17
    right_leg_y = 24
    
    for y in range(right_leg_y, right_leg_y + 8):
        for x in range(right_leg_x, right_leg_x + 3):
            canvas[y][x] = PURPLE_ROBE
    
    # Robe shadow
    for y in range(right_leg_y, right_leg_y + 8):
        canvas[y][right_leg_x] = DARK_PURPLE
    
    # Shoes (dark blue/mystical)
    for x in range(left_leg_x, left_leg_x + 3):
        canvas[left_leg_y + 6][x] = DARK_BLUE
        canvas[left_leg_y + 7][x] = DARK_BLUE
    
    for x in range(right_leg_x, right_leg_x + 3):
        canvas[right_leg_y + 6][x] = DARK_BLUE
        canvas[right_leg_y + 7][x] = DARK_BLUE
    
    # Gold trim on sleeves
    canvas[left_arm_y + 1][left_arm_x + 1] = GOLD
    canvas[left_arm_y + 1][left_arm_x + 2] = GOLD
    canvas[right_arm_y + 1][right_arm_x + 1] = GOLD
    canvas[right_arm_y + 1][right_arm_x + 2] = GOLD
    
    # Convert numpy array to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 8x with nearest neighbor (pixel perfect)
    scale = 8
    img_scaled = img.resize((size * scale, size * scale), Image.NEAREST)
    
    # Save
    output_path = 'ascii_art/hero_magician.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {size * scale}x{size * scale} pixels")
    print(f"   Style: Pixel art wizard/magician")
    print(f"   Features: Purple wizard hat, long gray beard, purple robe with gold trim,")
    print(f"            wooden staff with magic crystal, glowing magic orb")

if __name__ == '__main__':
    create_magician()
