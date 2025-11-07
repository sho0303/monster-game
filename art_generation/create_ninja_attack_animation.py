"""
Create an animated attack version of the ninja character
Shows the ninja in mid-attack with motion effects and dynamic pose
"""
from PIL import Image, ImageDraw
import numpy as np

def create_ninja_attack():
    """Create a Minecraft-style ninja in attack animation"""
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
    LIGHT_BLUE = [150, 200, 255, 180]  # Motion blur effect
    YELLOW = [255, 255, 0, 255]      # Attack sparkle
    ORANGE = [255, 165, 0, 255]      # Attack flash
    
    # HEAD (8x8, tilted forward in attack pose)
    head_start_x = 11  # Slightly shifted for dynamic pose
    head_start_y = 3   # Higher for leaning forward
    
    # Black hood/mask (full coverage)
    for y in range(head_start_y, head_start_y + 8):
        for x in range(head_start_x, head_start_x + 8):
            if x < size and y < size:
                canvas[y][x] = BLACK
    
    # Eyes showing intensity (focused attack)
    # Left eye (narrowed in concentration)
    canvas[head_start_y + 3][head_start_x + 2] = WHITE
    canvas[head_start_y + 4][head_start_x + 2] = SKIN
    # Right eye  
    canvas[head_start_y + 3][head_start_x + 5] = SKIN
    canvas[head_start_y + 4][head_start_x + 5] = WHITE
    
    # Red headband fluttering in motion
    canvas[head_start_y + 1][head_start_x + 1] = RED
    canvas[head_start_y + 1][head_start_x + 2] = RED
    canvas[head_start_y + 1][head_start_x + 3] = RED
    canvas[head_start_y + 1][head_start_x + 4] = RED
    canvas[head_start_y + 1][head_start_x + 5] = RED
    canvas[head_start_y][head_start_x + 6] = RED  # Flowing motion
    canvas[head_start_y][head_start_x + 7] = DARK_RED  # Trail effect
    
    # BODY (8x12, leaning forward in attack)
    body_start_x = 11
    body_start_y = 11
    
    # Black ninja gi
    for y in range(body_start_y, body_start_y + 12):
        for x in range(body_start_x, body_start_x + 8):
            if x < size and y < size:
                canvas[y][x] = BLACK
    
    # Dark gray shading on sides with motion effect
    for y in range(body_start_y, body_start_y + 12):
        if y < size:
            canvas[y][body_start_x] = DARK_GRAY
            if body_start_x + 7 < size:
                canvas[y][body_start_x + 7] = DARK_GRAY
    
    # Red sash/belt flowing in motion
    for x in range(body_start_x + 1, min(body_start_x + 8, size)):
        canvas[body_start_y + 5][x] = RED
        canvas[body_start_y + 6][x] = DARK_RED
    
    # Motion trail of sash
    canvas[body_start_y + 5][body_start_x + 8] = DARK_RED if body_start_x + 8 < size else DARK_RED
    
    # LEFT ARM (extended in attack) - dramatically repositioned
    left_arm_x = 6   # Extended outward
    left_arm_y = 10  # Higher for attack pose
    
    # Arm in striking position
    for y in range(left_arm_y, left_arm_y + 8):
        for x in range(left_arm_x, left_arm_x + 6):  # Longer arm for extension
            if x < size and y < size:
                canvas[y][x] = BLACK
    
    # Motion blur trail behind arm
    for i in range(3):
        trail_x = left_arm_x - i - 1
        if trail_x >= 0:
            canvas[left_arm_y + 2][trail_x] = LIGHT_BLUE
            canvas[left_arm_y + 3][trail_x] = LIGHT_BLUE
    
    # Kunai extended forward with attack effect
    kunai_x = left_arm_x + 6
    kunai_y = left_arm_y + 3
    
    # Kunai blade
    for i in range(4):
        if kunai_x + i < size:
            canvas[kunai_y][kunai_x + i] = SILVER
    
    # Attack sparkles around kunai
    canvas[kunai_y - 1][kunai_x + 3] = YELLOW
    canvas[kunai_y + 1][kunai_x + 3] = YELLOW
    canvas[kunai_y][kunai_x + 4] = WHITE
    canvas[kunai_y - 1][kunai_x + 4] = ORANGE
    canvas[kunai_y + 1][kunai_x + 4] = ORANGE
    
    # Speed lines showing attack motion
    for i in range(5):
        speed_x = kunai_x + 5 + i
        if speed_x < size:
            canvas[kunai_y][speed_x] = LIGHT_BLUE
            if i % 2 == 0:
                canvas[kunai_y - 1][speed_x] = LIGHT_BLUE
                canvas[kunai_y + 1][speed_x] = LIGHT_BLUE
    
    # RIGHT ARM (4x12) - pulled back for balance
    right_arm_x = 19
    right_arm_y = 13
    
    for y in range(right_arm_y, right_arm_y + 8):
        for x in range(right_arm_x, right_arm_x + 4):
            if x < size and y < size:
                canvas[y][x] = BLACK
    
    # Shuriken ready to throw
    canvas[right_arm_y + 2][right_arm_x + 1] = SILVER
    canvas[right_arm_y + 2][right_arm_x + 2] = SILVER
    canvas[right_arm_y + 3][right_arm_x + 1] = SILVER
    canvas[right_arm_y + 3][right_arm_x + 2] = SILVER
    
    # LEFT LEG (4x8) - in lunge position
    left_leg_x = 10  # Forward lunge
    left_leg_y = 23
    
    for y in range(left_leg_y, min(left_leg_y + 8, size)):
        for x in range(left_leg_x, left_leg_x + 4):
            if x < size:
                canvas[y][x] = BLACK
    
    # RIGHT LEG (4x8) - back leg for stability
    right_leg_x = 16
    right_leg_y = 24
    
    for y in range(right_leg_y, min(right_leg_y + 8, size)):
        for x in range(right_leg_x, right_leg_x + 4):
            if x < size:
                canvas[y][x] = BLACK
    
    # Ninja shoes/boots with ground effect
    for x in range(left_leg_x, left_leg_x + 4):
        if x < size and left_leg_y + 6 < size:
            canvas[left_leg_y + 6][x] = DARK_GRAY
            canvas[left_leg_y + 7][x] = DARK_GRAY
    
    # Dust kick-up effect from movement
    canvas[left_leg_y + 8][left_leg_x - 1] = GRAY if left_leg_x - 1 >= 0 else None
    canvas[left_leg_y + 8][left_leg_x] = GRAY if left_leg_y + 8 < size else None
    
    for x in range(right_leg_x, right_leg_x + 4):
        if x < size and right_leg_y + 6 < size:
            canvas[right_leg_y + 6][x] = DARK_GRAY
            if right_leg_y + 7 < size:
                canvas[right_leg_y + 7][x] = DARK_GRAY
    
    # Add dramatic highlights for attack intensity
    canvas[body_start_y + 1][body_start_x + 3] = GRAY
    canvas[body_start_y + 1][body_start_x + 4] = GRAY
    canvas[head_start_y + 4][head_start_x + 3] = GRAY  # Lighter for intensity
    canvas[head_start_y + 4][head_start_x + 4] = GRAY
    
    # Attack aura effect around the ninja
    aura_positions = [
        (head_start_y - 1, head_start_x + 2),
        (head_start_y - 1, head_start_x + 5),
        (body_start_y + 2, body_start_x - 1),
        (body_start_y + 8, body_start_x - 1),
    ]
    
    for y, x in aura_positions:
        if 0 <= x < size and 0 <= y < size:
            canvas[y][x] = LIGHT_BLUE
    
    # Convert numpy array to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 8x with nearest neighbor (pixel perfect)
    scale = 8
    img_scaled = img.resize((size * scale, size * scale), Image.NEAREST)
    
    # Save
    output_path = '../art/ninja_attack.png'
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {size * scale}x{size * scale} pixels")
    print(f"   Style: Animated ninja attack with motion effects")
    print(f"   Features: Attack pose, motion blur, speed lines, sparkles")
    print(f"   Animation: Kunai strike, flowing cloth, dust effects")

if __name__ == '__main__':
    create_ninja_attack()