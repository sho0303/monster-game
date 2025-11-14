#!/usr/bin/env python3
"""
Starfish Monster Art Generator - Creates pixel art for the starfish monster
Creates both regular and attack versions of the starfish
"""

import numpy as np
from PIL import Image
import os

def create_starfish_art():
    """Create regular starfish pixel art - chunky tube arms like reference image"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette for starfish - pink/orange tones from reference
    BLACK = [0, 0, 0, 255]
    WHITE = [255, 255, 255, 255]
    STAR_PINK = [255, 130, 150, 255]      # Pink body color
    STAR_ORANGE = [255, 160, 100, 255]    # Orange/peach tones
    STAR_DARK = [200, 80, 90, 255]        # Dark pink shading
    STAR_LIGHT = [255, 180, 180, 255]     # Light pink highlights
    BUMP_WHITE = [245, 245, 240, 255]     # Whitish bumps/tubercles
    
    # Center body of starfish
    center_x, center_y = 16, 16
    
    # Draw central body (rounded center disc)
    for y in range(13, 20):
        for x in range(13, 20):
            if (x - center_x)**2 + (y - center_y)**2 <= 12:
                canvas[y][x] = STAR_PINK
    
    # Draw 5 thick tubular arms (like reference image)
    # Arm 1 - Top (pointing up) - THICK cylindrical arm
    for i in range(9):
        y = center_y - 5 - i
        # Keep arms thick (3-4 pixels wide) throughout
        arm_width = 3 if i < 6 else 2
        for dx in range(-arm_width, arm_width + 1):
            x = center_x + dx
            if 0 <= y < size and 0 <= x < size:
                canvas[y][x] = STAR_PINK
    
    # Arm 2 - Upper Right (diagonal) - THICK
    for i in range(8):
        y = center_y - 3 - int(i * 0.6)
        x = center_x + 3 + i
        arm_width = 3 if i < 5 else 2
        for dy in range(-arm_width, arm_width + 1):
            for dx in range(-1, 2):
                ny, nx = y + dy, x + dx
                if 0 <= ny < size and 0 <= nx < size:
                    canvas[ny][nx] = STAR_PINK
    
    # Arm 3 - Lower Right - THICK
    for i in range(8):
        y = center_y + 3 + int(i * 0.5)
        x = center_x + 3 + i
        arm_width = 3 if i < 5 else 2
        for dy in range(-arm_width, arm_width + 1):
            for dx in range(-1, 2):
                ny, nx = y + dy, x + dx
                if 0 <= ny < size and 0 <= nx < size:
                    canvas[ny][nx] = STAR_PINK
    
    # Arm 4 - Lower Left - THICK
    for i in range(8):
        y = center_y + 3 + int(i * 0.5)
        x = center_x - 3 - i
        arm_width = 3 if i < 5 else 2
        for dy in range(-arm_width, arm_width + 1):
            for dx in range(-1, 2):
                ny, nx = y + dy, x + dx
                if 0 <= ny < size and 0 <= nx < size:
                    canvas[ny][nx] = STAR_PINK
    
    # Arm 5 - Upper Left - THICK
    for i in range(8):
        y = center_y - 3 - int(i * 0.6)
        x = center_x - 3 - i
        arm_width = 3 if i < 5 else 2
        for dy in range(-arm_width, arm_width + 1):
            for dx in range(-1, 2):
                ny, nx = y + dy, x + dx
                if 0 <= ny < size and 0 <= nx < size:
                    canvas[ny][nx] = STAR_PINK
    
    # Add dark shading on bottom/right sides of arms (3D tube effect)
    for y in range(size):
        for x in range(size):
            if canvas[y][x][3] > 0:
                # Shade the bottom and right sides
                if (y > center_y and x > center_x - 3) or (x > center_x and y > center_y - 3):
                    import random
                    if random.random() > 0.4:  # Add some texture
                        canvas[y][x] = STAR_DARK
    
    # Add light highlights on top/left (tubular 3D effect)
    for y in range(size):
        for x in range(size):
            if canvas[y][x][3] > 0 and canvas[y][x][0] == STAR_PINK[0]:
                if y < center_y and x < center_x:
                    import random
                    if random.random() > 0.6:
                        canvas[y][x] = STAR_LIGHT
    
    # Add bumpy texture (tubercles) - characteristic white/light bumps
    import random
    random.seed(42)  # Consistent pattern
    for y in range(6, 27):
        for x in range(6, 27):
            if canvas[y][x][3] > 0:
                if random.random() > 0.88:  # Scattered bumps
                    canvas[y][x] = BUMP_WHITE
    
    # Add eyes (simple black dots)
    canvas[15][14] = BLACK
    canvas[15][18] = BLACK
    # Eye highlights
    canvas[14][14] = WHITE
    canvas[14][18] = WHITE
    
    return canvas

def create_starfish_attack():
    """Create starfish attack animation - arms reaching/curling"""
    # Create a 32x32 canvas
    size = 32
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Color palette (same as regular)
    BLACK = [0, 0, 0, 255]
    WHITE = [255, 255, 255, 255]
    STAR_PINK = [255, 130, 150, 255]
    STAR_ORANGE = [255, 160, 100, 255]
    STAR_DARK = [200, 80, 90, 255]
    STAR_LIGHT = [255, 180, 180, 255]
    BUMP_WHITE = [245, 245, 240, 255]
    
    # Starfish in aggressive pose - arms curled/reaching
    center_x, center_y = 16, 15
    
    # Draw central body
    for y in range(13, 18):
        for x in range(13, 19):
            if (x - center_x)**2 + (y - center_y)**2 <= 9:
                canvas[y][x] = STAR_PINK
    
    # Draw arms in curled aggressive position - THICK tubes
    # Top arm - curled upward
    for i in range(8):
        y = center_y - 4 - i
        curve = int(i * 0.3) if i > 3 else 0
        arm_width = 3 if i < 5 else 2
        for dx in range(-arm_width, arm_width + 1):
            x = center_x + dx + curve
            if 0 <= y < size and 0 <= x < size:
                canvas[y][x] = STAR_PINK
    
    # Right arm - reaching out thick
    for i in range(7):
        y = center_y + int(i * 0.3)
        x = center_x + 3 + i
        arm_width = 3 if i < 4 else 2
        for dy in range(-arm_width, arm_width + 1):
            for dx in range(-1, 2):
                ny, nx = y + dy, x + dx
                if 0 <= ny < size and 0 <= nx < size:
                    canvas[ny][nx] = STAR_PINK
    
    # Left arm - reaching out thick
    for i in range(7):
        y = center_y + int(i * 0.3)
        x = center_x - 3 - i
        arm_width = 3 if i < 4 else 2
        for dy in range(-arm_width, arm_width + 1):
            for dx in range(-1, 2):
                ny, nx = y + dy, x + dx
                if 0 <= ny < size and 0 <= nx < size:
                    canvas[ny][nx] = STAR_PINK
    
    # Bottom right arm - curled
    for i in range(6):
        y = center_y + 3 + i
        x = center_x + 2 + int(i * 0.5)
        arm_width = 3 if i < 4 else 2
        for dy in range(-arm_width, arm_width + 1):
            for dx in range(-1, 2):
                ny, nx = y + dy, x + dx
                if 0 <= ny < size and 0 <= nx < size:
                    canvas[ny][nx] = STAR_PINK
    
    # Bottom left arm - curled
    for i in range(6):
        y = center_y + 3 + i
        x = center_x - 2 - int(i * 0.5)
        arm_width = 3 if i < 4 else 2
        for dy in range(-arm_width, arm_width + 1):
            for dx in range(-1, 2):
                ny, nx = y + dy, x + dx
                if 0 <= ny < size and 0 <= nx < size:
                    canvas[ny][nx] = STAR_PINK
    
    # Add 3D shading
    for y in range(size):
        for x in range(size):
            if canvas[y][x][3] > 0:
                if (y > center_y and x > center_x - 3) or (x > center_x and y > center_y - 3):
                    import random
                    if random.random() > 0.5:
                        canvas[y][x] = STAR_DARK
    
    # Add highlights
    for y in range(size):
        for x in range(size):
            if canvas[y][x][3] > 0 and canvas[y][x][0] == STAR_PINK[0]:
                if y < center_y and x < center_x:
                    import random
                    if random.random() > 0.7:
                        canvas[y][x] = STAR_LIGHT
    
    # Add bumpy texture
    import random
    random.seed(42)
    for y in range(5, 28):
        for x in range(5, 28):
            if canvas[y][x][3] > 0:
                if random.random() > 0.9:
                    canvas[y][x] = BUMP_WHITE
    
    # Eyes - more aggressive/wider
    canvas[14][14] = BLACK
    canvas[14][18] = BLACK
    canvas[13][14] = WHITE
    canvas[13][18] = WHITE
    
    return canvas

def main():
    """Generate starfish monster art files"""
    print("Creating Starfish Monster Art...")
    
    # Create output directory if it doesn't exist
    output_dir = "art"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate regular starfish
    print("  - Creating regular starfish...")
    starfish_canvas = create_starfish_art()
    starfish_img = Image.fromarray(starfish_canvas, 'RGBA')
    
    # Scale up 8x for better visibility (32 -> 256)
    starfish_scaled = starfish_img.resize((256, 256), Image.NEAREST)
    starfish_scaled.save(os.path.join(output_dir, "starfish_monster.png"))
    print(f"    ✓ Saved {output_dir}/starfish_monster.png")
    
    # Generate attack starfish
    print("  - Creating starfish attack animation...")
    attack_canvas = create_starfish_attack()
    attack_img = Image.fromarray(attack_canvas, 'RGBA')
    
    # Scale up 8x
    attack_scaled = attack_img.resize((256, 256), Image.NEAREST)
    attack_scaled.save(os.path.join(output_dir, "starfish_monster_attack.png"))
    print(f"    ✓ Saved {output_dir}/starfish_monster_attack.png")
    
    print("\n✅ Starfish Monster Art Generation Complete!")
    print(f"   Regular: {output_dir}/starfish_monster.png (256x256)")
    print(f"   Attack:  {output_dir}/starfish_monster_attack.png (256x256)")

if __name__ == "__main__":
    main()
