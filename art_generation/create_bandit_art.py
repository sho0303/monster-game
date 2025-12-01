"""
Create pixel art for the Bandit monster and its attack animation.
"""
from PIL import Image, ImageDraw
import numpy as np
import random

def create_bandit_art():
    # Image dimensions
    width = 64
    height = 64
    scale = 4
    
    # Colors
    SKIN = [180, 130, 100, 255]
    SKIN_SHADOW = [140, 100, 80, 255]
    HAIR = [30, 20, 20, 255] # Dark beard/hair
    BANDANA_BASE = [200, 50, 50, 255] # Red
    BANDANA_PATTERN = [255, 100, 50, 255] # Orange stripes
    COAT_BLUE = [40, 60, 100, 255]
    COAT_TRIM = [200, 180, 50, 255] # Gold
    PANTS_GREEN = [80, 90, 60, 255]
    BOOTS_BROWN = [100, 60, 40, 255]
    METAL_LIGHT = [200, 200, 210, 255]
    METAL_DARK = [100, 100, 110, 255]
    TATTOO_WHITE = [220, 220, 220, 200] # Semi-transparent white
    
    def draw_bandit(is_attack=False):
        canvas = np.zeros((height, width, 4), dtype=np.uint8)
        
        def draw_pixel(x, y, color):
            if 0 <= x < width and 0 <= y < height:
                canvas[y][x] = color
                
        def draw_rect(x, y, w, h, color):
            for i in range(w):
                for j in range(h):
                    draw_pixel(x + i, y + j, color)

        # Center position
        cx = width // 2
        cy = height // 2
        
        # Offset for attack lunge
        x_off = -5 if is_attack else 0
        
        # === LEGS ===
        # Left Leg
        draw_rect(cx - 8 + x_off, cy + 10, 6, 18, PANTS_GREEN)
        draw_rect(cx - 8 + x_off, cy + 20, 6, 12, BOOTS_BROWN) # Boot
        
        # Right Leg (stepped back if attacking)
        rx_off = 5 if is_attack else 0
        draw_rect(cx + 2 + x_off + rx_off, cy + 10, 6, 18, PANTS_GREEN)
        draw_rect(cx + 2 + x_off + rx_off, cy + 20, 6, 12, BOOTS_BROWN) # Boot
        
        # === TORSO ===
        # Blue Coat
        draw_rect(cx - 10 + x_off, cy - 5, 20, 18, COAT_BLUE)
        # Gold Buttons/Trim
        for y in range(cy - 5, cy + 13, 4):
            draw_pixel(cx - 4 + x_off, y, COAT_TRIM)
            draw_pixel(cx + 3 + x_off, y, COAT_TRIM)
            
        # Belt/Sash
        draw_rect(cx - 10 + x_off, cy + 10, 20, 3, [60, 40, 30, 255])
        
        # === HEAD ===
        head_y = cy - 18
        # Face shape
        draw_rect(cx - 7 + x_off, head_y, 14, 14, SKIN)
        
        # Beard (Dark, bushy)
        for x in range(cx - 7 + x_off, cx + 8 + x_off):
            for y in range(head_y + 8, head_y + 16):
                if (x - (cx + x_off))**2 + (y - (head_y + 8))**2 < 60: # Rounded beard
                    draw_pixel(x, y, HAIR)
                    
        # Bandana (Red with stripes)
        for x in range(cx - 8 + x_off, cx + 9 + x_off):
            for y in range(head_y - 4, head_y + 2):
                col = BANDANA_BASE
                if (x + y) % 4 == 0: col = BANDANA_PATTERN
                draw_pixel(x, y, col)
        # Bandana knot/tails on left
        draw_pixel(cx - 9 + x_off, head_y, BANDANA_BASE)
        draw_pixel(cx - 10 + x_off, head_y + 1, BANDANA_BASE)
        
        # Eyes
        draw_pixel(cx - 3 + x_off, head_y + 5, [255, 255, 255, 255])
        draw_pixel(cx - 3 + x_off, head_y + 5, [0, 0, 0, 255]) # Pupil
        draw_pixel(cx + 2 + x_off, head_y + 5, [255, 255, 255, 255])
        draw_pixel(cx + 2 + x_off, head_y + 5, [0, 0, 0, 255]) # Pupil
        
        # === ARMS ===
        # Left Arm (Viewer's Left) - Resting or clenched
        for x in range(cx - 16 + x_off, cx - 10 + x_off):
            for y in range(cy - 5, cy + 10):
                draw_pixel(x, y, SKIN)
                # Tattoos (White circles)
                if (x * y) % 17 == 0:
                    draw_pixel(x, y, TATTOO_WHITE)
        # Shoulder pad
        draw_rect(cx - 17 + x_off, cy - 7, 8, 5, COAT_BLUE)
        
        # Right Arm (Viewer's Right) - Holding Dagger
        # If attacking, arm is extended forward
        arm_x = cx + 10 + x_off
        arm_y = cy
        
        if is_attack:
            # Extended arm
            for x in range(cx + 10 + x_off, cx + 22 + x_off):
                for y in range(cy - 2, cy + 4):
                    draw_pixel(x, y, SKIN)
            hand_x = cx + 22 + x_off
            hand_y = cy
        else:
            # Bent arm holding dagger up
            for x in range(cx + 10 + x_off, cx + 16 + x_off):
                for y in range(cy - 5, cy + 5):
                    draw_pixel(x, y, SKIN)
            hand_x = cx + 14 + x_off
            hand_y = cy + 2
            
        # Shoulder pad
        draw_rect(cx + 9 + x_off, cy - 7, 8, 5, COAT_BLUE)
        
        # Tattoos on right arm
        if not is_attack:
            draw_pixel(cx + 12 + x_off, cy - 2, TATTOO_WHITE)
            draw_pixel(cx + 13 + x_off, cy + 2, TATTOO_WHITE)

        # === WEAPON (Dagger) ===
        # Handle
        draw_rect(hand_x, hand_y - 2, 3, 6, [100, 80, 20, 255]) # Gold/Wood handle
        
        # Blade
        if is_attack:
            # Pointing right/forward
            for i in range(10):
                draw_pixel(hand_x + 3 + i, hand_y, METAL_LIGHT)
                draw_pixel(hand_x + 3 + i, hand_y + 1, METAL_DARK) # Shadow
            # Tip
            draw_pixel(hand_x + 13, hand_y, METAL_LIGHT)
        else:
            # Pointing up/diagonal
            for i in range(8):
                draw_pixel(hand_x + 1 + i, hand_y - 3 + i, METAL_LIGHT) # Back edge
                draw_pixel(hand_x + 2 + i, hand_y - 3 + i, METAL_DARK) # Sharp edge
                
        # Scimitar on hip (Sheathed)
        # Curved shape on left hip
        for i in range(10):
            sx = cx - 8 + x_off - i
            sy = cy + 12 + (i // 2)
            draw_pixel(sx, sy, [50, 50, 60, 255]) # Sheath color
            
        return Image.fromarray(canvas, 'RGBA')

    # Generate and save images
    img_normal = draw_bandit(is_attack=False)
    img_normal = img_normal.resize((width * scale, height * scale), Image.Resampling.NEAREST)
    img_normal.save('art/bandit.png')
    print(f"Saved art/bandit.png")
    
    img_attack = draw_bandit(is_attack=True)
    img_attack = img_attack.resize((width * scale, height * scale), Image.Resampling.NEAREST)
    img_attack.save('art/bandit_attack.png')
    print(f"Saved art/bandit_attack.png")

if __name__ == "__main__":
    create_bandit_art()
