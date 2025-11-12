"""
Create a pixel art ninja death/defeated image
Ninja laying horizontal on the ground with blood pool
"""
from PIL import Image, ImageDraw
import numpy as np

def create_ninja_death():
    """Create a defeated ninja laying on ground with blood pool"""
    # Create a 32x32 canvas (same as ninja art)
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette (matching ninja art style)
    BLACK = [0, 0, 0, 255]           # Ninja outfit
    DARK_GRAY = [40, 40, 40, 255]    # Dark cloth
    GRAY = [100, 100, 100, 255]      # Cloth highlights
    SKIN = [255, 220, 177, 255]      # Skin tone for eyes
    RED = [180, 0, 0, 255]           # Red accents
    DARK_RED = [100, 0, 0, 255]      # Darker red
    BLOOD_RED = [139, 0, 0, 255]     # Blood pool
    DARK_BLOOD = [89, 0, 0, 255]     # Dark blood
    SILVER = [192, 192, 192, 255]    # Weapons
    BROWN = [101, 67, 33, 255]       # Belt/accessories
    
    # BLOOD POOL - spread across bottom of canvas
    # Create organic blood pool shape
    blood_pool_y_start = 20
    
    # Main blood pool (wider in middle, tapered at edges)
    blood_positions = [
        # Bottom layer (widest)
        (28, 8, 24),   # y, x_start, width
        (27, 7, 25),
        (26, 7, 24),
        (25, 8, 22),
        (24, 9, 20),
        (23, 10, 18),
        (22, 11, 16),
        (21, 12, 14),
        (20, 13, 12),
    ]
    
    for y, x_start, width in blood_positions:
        for x in range(x_start, x_start + width):
            if x < size:
                # Alternate between blood colors for texture
                if (x + y) % 3 == 0:
                    canvas[y][x] = DARK_BLOOD
                else:
                    canvas[y][x] = BLOOD_RED
    
    # NINJA BODY - laying horizontal (defeated pose)
    # Body positioned laying on side, horizontally across canvas
    
    # HEAD (laying on side) - positioned left side
    head_x_start = 4
    head_y_start = 14
    
    # Black hood/mask
    for y in range(head_y_start, head_y_start + 6):
        for x in range(head_x_start, head_x_start + 8):
            if x < size and y < size:
                canvas[y][x] = BLACK
    
    # Closed eyes (defeated/unconscious)
    canvas[head_y_start + 2][head_x_start + 2] = DARK_GRAY
    canvas[head_y_start + 2][head_x_start + 3] = DARK_GRAY
    canvas[head_y_start + 2][head_x_start + 5] = DARK_GRAY
    canvas[head_y_start + 2][head_x_start + 6] = DARK_GRAY
    
    # Red headband (partially visible)
    canvas[head_y_start][head_x_start + 2] = RED
    canvas[head_y_start][head_x_start + 3] = RED
    canvas[head_y_start][head_x_start + 4] = RED
    canvas[head_y_start][head_x_start + 5] = RED
    
    # TORSO (horizontal, laying on ground)
    torso_x_start = 11
    torso_y_start = 13
    torso_width = 10
    torso_height = 8
    
    # Black ninja gi (body laying horizontal)
    for y in range(torso_y_start, torso_y_start + torso_height):
        for x in range(torso_x_start, torso_x_start + torso_width):
            if x < size and y < size:
                canvas[y][x] = BLACK
    
    # Dark gray shading (depth)
    for y in range(torso_y_start + 1, torso_y_start + torso_height - 1):
        if torso_x_start < size:
            canvas[y][torso_x_start] = DARK_GRAY
        if torso_x_start + torso_width - 1 < size:
            canvas[y][torso_x_start + torso_width - 1] = DARK_GRAY
    
    # Red sash visible on torso
    for x in range(torso_x_start + 2, torso_x_start + 8):
        if x < size and torso_y_start + 4 < size:
            canvas[torso_y_start + 4][x] = RED
        if x < size and torso_y_start + 5 < size:
            canvas[torso_y_start + 5][x] = DARK_RED
    
    # LEFT ARM (extended outward, laying on ground)
    left_arm_x = 4
    left_arm_y = 18
    
    for x in range(left_arm_x, left_arm_x + 7):
        for y in range(left_arm_y, left_arm_y + 3):
            if x < size and y < size:
                canvas[y][x] = BLACK
    
    # Hand (fingers splayed)
    canvas[left_arm_y + 1][left_arm_x] = DARK_GRAY
    canvas[left_arm_y + 2][left_arm_x] = DARK_GRAY
    canvas[left_arm_y][left_arm_x + 1] = DARK_GRAY
    
    # RIGHT ARM (laying across body)
    right_arm_x = 18
    right_arm_y = 16
    
    for x in range(right_arm_x, right_arm_x + 6):
        for y in range(right_arm_y, right_arm_y + 3):
            if x < size and y < size:
                canvas[y][x] = BLACK
    
    # LEGS (extended, laying horizontal)
    # Left leg
    left_leg_x = 20
    left_leg_y = 19
    
    for x in range(left_leg_x, left_leg_x + 7):
        for y in range(left_leg_y, left_leg_y + 3):
            if x < size and y < size:
                canvas[y][x] = BLACK
    
    # Right leg (slightly offset)
    right_leg_x = 20
    right_leg_y = 17
    
    for x in range(right_leg_x, right_leg_x + 6):
        for y in range(right_leg_y, right_leg_y + 2):
            if x < size and y < size:
                canvas[y][x] = BLACK
    
    # Ninja boots/shoes
    for y in range(left_leg_y, left_leg_y + 3):
        if left_leg_x + 5 < size and y < size:
            canvas[y][left_leg_x + 5] = DARK_GRAY
        if left_leg_x + 6 < size and y < size:
            canvas[y][left_leg_x + 6] = DARK_GRAY
    
    # Dropped kunai near hand
    canvas[left_arm_y - 1][left_arm_x + 1] = SILVER
    canvas[left_arm_y - 2][left_arm_x + 1] = SILVER
    canvas[left_arm_y - 3][left_arm_x + 1] = SILVER
    canvas[left_arm_y - 2][left_arm_x + 2] = BROWN  # Handle
    
    # Add blood splatter on ninja (injury detail)
    canvas[torso_y_start + 3][torso_x_start + 5] = DARK_RED
    canvas[torso_y_start + 3][torso_x_start + 6] = BLOOD_RED
    canvas[torso_y_start + 4][torso_x_start + 6] = DARK_RED
    
    # Convert numpy array to PIL Image
    img = Image.fromarray(canvas, 'RGBA')
    
    # Scale up 8x with nearest neighbor (pixel perfect)
    scale = 8
    img_scaled = img.resize((size * scale, size * scale), Image.NEAREST)
    
    # Save to parent directory's art folder
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    output_path = os.path.join(parent_dir, 'art', 'ninja_death.png')
    
    img_scaled.save(output_path, 'PNG')
    print(f"✅ Created {output_path}")
    print(f"   Size: {size * scale}x{size * scale} pixels")
    print(f"   Style: Pixel art defeated ninja")
    print(f"   Features: Laying horizontal, blood pool, dropped weapon")
    print(f"   State: Defeated/unconscious pose")

if __name__ == '__main__':
    create_ninja_death()
