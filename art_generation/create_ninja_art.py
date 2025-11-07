"""
Create a pixel art ninja character PNG
"""
from PIL import Image, ImageDraw
import numpy as np

def create_ninja():
    """Create a Minecraft-style ninja character"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette
    BLACK = [0, 0, 0, 255]           # Ninja outfit
    DARK_GRAY = [40, 40, 40, 255]    # Dark cloth
    GRAY = [100, 100, 100, 255]      # Cloth highlights
    SKIN = [255, 220, 177, 255]      # Skin tone for eyes
    RED = [180, 0, 0, 255]           # Dark red accents
    DARK_RED = [100, 0, 0, 255]      # Darker red
    SILVER = [192, 192, 192, 255]    # Weapons
    WHITE = [255, 255, 255, 255]     # Eye whites
    BROWN = [101, 67, 33, 255]       # Belt/accessories
    
    # HEAD (8x8, centered at top)
    head_start_x = 12
    head_start_y = 4
    
    # Black hood/mask (full coverage)
    for y in range(head_start_y, head_start_y + 8):
        for x in range(head_start_x, head_start_x + 8):
            canvas[y][x] = BLACK
    
    # Eyes only showing (ninja mask)
    # Left eye
    canvas[head_start_y + 3][head_start_x + 2] = WHITE
    canvas[head_start_y + 3][head_start_x + 3] = SKIN
    # Right eye  
    canvas[head_start_y + 3][head_start_x + 5] = SKIN
    canvas[head_start_y + 3][head_start_x + 6] = WHITE
    
    # Red headband accent
    canvas[head_start_y + 1][head_start_x + 1] = RED
    canvas[head_start_y + 1][head_start_x + 2] = RED
    canvas[head_start_y + 1][head_start_x + 3] = RED
    canvas[head_start_y + 1][head_start_x + 4] = RED
    canvas[head_start_y + 1][head_start_x + 5] = RED
    canvas[head_start_y + 1][head_start_x + 6] = RED
    
    # BODY (8x12)
    body_start_x = 12
    body_start_y = 12
    
    # Black ninja gi
    for y in range(body_start_y, body_start_y + 12):
        for x in range(body_start_x, body_start_x + 8):
            canvas[y][x] = BLACK
    
    # Dark gray shading on sides
    for y in range(body_start_y, body_start_y + 12):
        canvas[y][body_start_x] = DARK_GRAY
        canvas[y][body_start_x + 7] = DARK_GRAY
    
    # Red sash/belt
    for x in range(body_start_x + 1, body_start_x + 7):
        canvas[body_start_y + 5][x] = RED
        canvas[body_start_y + 6][x] = DARK_RED
    
    # Brown utility belt pouches
    canvas[body_start_y + 7][body_start_x + 2] = BROWN
    canvas[body_start_y + 7][body_start_x + 5] = BROWN
    
    # LEFT ARM (4x12) - holding kunai
    left_arm_x = 8
    left_arm_y = 12
    
    for y in range(left_arm_y, left_arm_y + 10):
        for x in range(left_arm_x, left_arm_x + 4):
            canvas[y][x] = BLACK
    
    # Kunai knife in left hand
    canvas[left_arm_y + 10][left_arm_x + 1] = SILVER
    canvas[left_arm_y + 11][left_arm_x + 1] = SILVER
    canvas[left_arm_y + 12][left_arm_x + 1] = SILVER
    canvas[left_arm_y + 11][left_arm_x + 2] = BROWN  # Handle
    
    # RIGHT ARM (4x12) - in attack pose
    right_arm_x = 20
    right_arm_y = 12
    
    for y in range(right_arm_y, right_arm_y + 10):
        for x in range(right_arm_x, right_arm_x + 4):
            canvas[y][x] = BLACK
    
    # Shuriken in right hand
    canvas[right_arm_y + 9][right_arm_x + 1] = SILVER
    canvas[right_arm_y + 9][right_arm_x + 2] = SILVER
    canvas[right_arm_y + 10][right_arm_x + 1] = SILVER
    canvas[right_arm_y + 10][right_arm_x + 2] = SILVER
    canvas[right_arm_y + 10][right_arm_x] = SILVER
    canvas[right_arm_y + 10][right_arm_x + 3] = SILVER
    
    # LEFT LEG (4x8)
    left_leg_x = 12
    left_leg_y = 24
    
    for y in range(left_leg_y, left_leg_y + 8):
        for x in range(left_leg_x, left_leg_x + 3):
            canvas[y][x] = BLACK
    
    # RIGHT LEG (4x8)
    right_leg_x = 17
    right_leg_y = 24
    
    for y in range(right_leg_y, right_leg_y + 8):
        for x in range(right_leg_x, right_leg_x + 3):
            canvas[y][x] = BLACK
    
    # Ninja shoes/boots (dark gray)
    for x in range(left_leg_x, left_leg_x + 3):
        canvas[left_leg_y + 6][x] = DARK_GRAY
        canvas[left_leg_y + 7][x] = DARK_GRAY
    
    for x in range(right_leg_x, right_leg_x + 3):
        canvas[right_leg_y + 6][x] = DARK_GRAY
        canvas[right_leg_y + 7][x] = DARK_GRAY
    
    # Add some highlights for depth
    canvas[body_start_y + 1][body_start_x + 3] = GRAY
    canvas[body_start_y + 1][body_start_x + 4] = GRAY
    canvas[head_start_y + 4][head_start_x + 3] = DARK_GRAY
    canvas[head_start_y + 4][head_start_x + 4] = DARK_GRAY
    
    # Convert numpy array to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 8x with nearest neighbor (pixel perfect)
    scale = 8
    img_scaled = img.resize((size * scale, size * scale), Image.NEAREST)
    
    # Save
    output_path = 'ascii_art/hero_ninja.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {size * scale}x{size * scale} pixels")
    print(f"   Style: Pixel art ninja with kunai and shuriken")
    print(f"   Features: Black outfit, red sash, weapons, stealth pose")

if __name__ == '__main__':
    create_ninja()
