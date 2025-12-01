"""
Flytrap Monster Creator
Creates pixel art for a carnivorous Venus flytrap with snapping jaws.
Recreated with a focus on the classic Venus Flytrap look: green exterior, red interior, and long teeth.

Resolution: 64x64 pixels (scaled 4x to 256x256)
Style: Pixel art
"""

from PIL import Image
import numpy as np
import random

def create_flytrap_default():
    """Create the default open flytrap pose."""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Palette
    GREEN_LIGHT = [140, 210, 60, 255]
    GREEN_MID = [90, 160, 30, 255]
    GREEN_DARK = [50, 100, 20, 255]
    
    RED_LIGHT = [220, 80, 80, 255]
    RED_MID = [180, 40, 50, 255]
    RED_DARK = [120, 20, 30, 255]
    
    TOOTH_COLOR = [230, 240, 180, 255]
    TOOTH_SHADOW = [180, 190, 100, 255]
    
    STEM_COLOR = [70, 130, 30, 255]
    STEM_SHADOW = [40, 80, 20, 255]
    
    FLY_BODY = [40, 40, 50, 255]
    FLY_WING = [200, 200, 220, 180]
    
    center_x = 32
    base_y = 60
    
    # --- Draw Stem ---
    # Curved stem
    for y in range(35, 64):
        # Curve calculation
        offset_x = int(2 * np.sin((y - 35) * 0.1))
        stem_w = 3
        if y > 55: stem_w = 4
        
        for x in range(center_x + offset_x - stem_w // 2, center_x + offset_x + stem_w // 2 + 1):
            if 0 <= x < width and 0 <= y < height:
                color = STEM_COLOR
                if x == center_x + offset_x + stem_w // 2:
                    color = STEM_SHADOW
                canvas[y, x] = color

    # --- Draw Leaves at Base ---
    # Simple jagged leaves
    for i in range(2):
        direction = 1 if i == 0 else -1
        start_x = center_x
        start_y = 58
        for l in range(12):
            lx = start_x + (l * direction * 2)
            ly = start_y - (l // 2)
            # Draw leaf segment
            for w in range(3 - (l//4)):
                px = lx
                py = ly + w
                if 0 <= px < width and 0 <= py < height:
                    canvas[py, px] = GREEN_MID
    
    # --- Draw Open Trap ---
    # The trap consists of two lobes.
    # Left Lobe (Top-Left to Bottom-Right tilt)
    # Right Lobe (Top-Right to Bottom-Left tilt)
    
    # We'll draw the back (interior) first, then the rim/teeth.
    
    trap_center_y = 30
    
    # Draw Interior (Red fleshy part)
    # Ellipse shape for the open mouth
    for y in range(15, 45):
        for x in range(10, 54):
            # Ellipse equation: ((x-h)^2 / a^2) + ((y-k)^2 / b^2) <= 1
            # Rotated slightly? Let's just do a simple wide ellipse for the open mouth
            dx = x - center_x
            dy = y - trap_center_y
            
            # Main mouth shape
            if (dx*dx)/(20*20) + (dy*dy)/(12*12) <= 1.0:
                # Gradient: Darker in center/bottom, lighter on top edges
                dist = np.sqrt(dx*dx + dy*dy)
                if dy > 0: # Bottom half of mouth
                    canvas[y, x] = RED_MID
                else:
                    canvas[y, x] = RED_DARK if dist < 8 else RED_MID
                
                # Add some texture/spots
                if (x + y) % 7 == 0 and (x * y) % 5 == 0:
                    canvas[y, x] = RED_LIGHT

    # Draw Exterior Shell (Green) - visible at the bottom/back of the lobes
    for y in range(15, 50):
        for x in range(8, 56):
            dx = x - center_x
            dy = y - trap_center_y
            
            # Slightly larger ellipse for the shell, but only draw if not overwriting the red interior (or draw behind)
            # Actually, let's draw the shell where the red isn't, to form the "cup"
            if (dx*dx)/(22*22) + (dy*dy)/(14*14) <= 1.0:
                if canvas[y, x][3] == 0: # If empty
                    canvas[y, x] = GREEN_MID
                    if y > trap_center_y + 5:
                        canvas[y, x] = GREEN_DARK # Shadow at bottom

    # --- Draw Teeth (Cilia) ---
    # Spikes along the top and bottom edges of the mouth
    
    # Top teeth
    for i in range(7):
        # Spread across the top arc
        tx = 14 + i * 6
        ty = 20 - abs(i - 3) * 2 # Arch
        
        # Draw tooth pointing up/out
        for h in range(6):
            px = tx
            py = ty - h
            if 0 <= px < width and 0 <= py < height:
                canvas[py, px] = TOOTH_COLOR
                # Side shading
                if h < 3:
                    if px+1 < width: canvas[py, px+1] = TOOTH_SHADOW

    # Bottom teeth
    for i in range(7):
        tx = 14 + i * 6
        ty = 40 + abs(i - 3) * 2 # Arch
        
        # Draw tooth pointing down/out
        for h in range(6):
            px = tx
            py = ty + h
            if 0 <= px < width and 0 <= py < height:
                canvas[py, px] = TOOTH_COLOR
                if h < 3:
                    if px+1 < width: canvas[py, px+1] = TOOTH_SHADOW

    # --- Trigger Hairs ---
    # Tiny black lines inside
    triggers = [(28, 30), (32, 32), (36, 30)]
    for tx, ty in triggers:
        if 0 <= tx < width and 0 <= ty < height:
            canvas[ty, tx] = [50, 0, 0, 255]
            canvas[ty-1, tx] = [50, 0, 0, 255]

    # --- A Fly! ---
    # Hovering near the trap
    fly_x = 45
    fly_y = 25
    
    # Wings
    canvas[fly_y-1, fly_x-2] = FLY_WING
    canvas[fly_y-2, fly_x-3] = FLY_WING
    canvas[fly_y-1, fly_x+2] = FLY_WING
    canvas[fly_y-2, fly_x+3] = FLY_WING
    
    # Body
    canvas[fly_y, fly_x] = FLY_BODY
    canvas[fly_y, fly_x-1] = FLY_BODY
    canvas[fly_y, fly_x+1] = FLY_BODY
    canvas[fly_y+1, fly_x] = FLY_BODY
    
    # Eyes
    canvas[fly_y, fly_x-1] = [200, 0, 0, 255] # Red eye

    return canvas

def create_flytrap_attack():
    """Create the attacking (closed) flytrap pose."""
    width, height = 64, 64
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Palette (Same as default)
    GREEN_LIGHT = [140, 210, 60, 255]
    GREEN_MID = [90, 160, 30, 255]
    GREEN_DARK = [50, 100, 20, 255]
    
    TOOTH_COLOR = [230, 240, 180, 255]
    TOOTH_SHADOW = [180, 190, 100, 255]
    
    STEM_COLOR = [70, 130, 30, 255]
    STEM_SHADOW = [40, 80, 20, 255]
    
    FLY_BODY = [40, 40, 50, 255]
    FLY_WING = [200, 200, 220, 180]
    
    center_x = 32
    base_y = 60
    
    # --- Draw Stem ---
    # Straighter, tense stem
    for y in range(35, 64):
        stem_w = 3
        if y > 55: stem_w = 4
        for x in range(center_x - stem_w // 2, center_x + stem_w // 2 + 1):
            if 0 <= x < width and 0 <= y < height:
                color = STEM_COLOR
                if x == center_x + stem_w // 2:
                    color = STEM_SHADOW
                canvas[y, x] = color

    # --- Draw Leaves at Base ---
    for i in range(2):
        direction = 1 if i == 0 else -1
        start_x = center_x
        start_y = 58
        for l in range(12):
            lx = start_x + (l * direction * 2)
            ly = start_y - (l // 2)
            for w in range(3 - (l//4)):
                px = lx
                py = ly + w
                if 0 <= px < width and 0 <= py < height:
                    canvas[py, px] = GREEN_MID

    # --- Draw Closed Trap ---
    # A solid green oval shape, slightly flattened
    trap_center_y = 30
    
    for y in range(18, 42):
        for x in range(12, 52):
            dx = x - center_x
            dy = y - trap_center_y
            
            # Ellipse for closed trap
            if (dx*dx)/(18*18) + (dy*dy)/(10*10) <= 1.0:
                # Main body color
                color = GREEN_MID
                
                # Shading
                if dy > 3: color = GREEN_DARK # Bottom shadow
                if dy < -3: color = GREEN_LIGHT # Top highlight
                
                # Seam in the middle
                if -1 <= dy <= 1:
                    color = GREEN_DARK
                
                canvas[y, x] = color

    # --- Draw Interlocked Teeth ---
    # Teeth crossing over the seam
    
    for i in range(8):
        tx = 16 + i * 4
        ty = trap_center_y
        
        # Upper tooth pointing down
        for h in range(5):
            if (i % 2 == 0): # Alternating
                px = tx
                py = ty + h - 2
                if 0 <= px < width and 0 <= py < height:
                    canvas[py, px] = TOOTH_COLOR
            else: # Lower tooth pointing up
                px = tx
                py = ty - h + 2
                if 0 <= px < width and 0 <= py < height:
                    canvas[py, px] = TOOTH_COLOR

    # --- Trapped Fly ---
    # Maybe a leg or wing sticking out?
    # Let's put a wing sticking out the side
    wing_x = 48
    wing_y = 30
    canvas[wing_y, wing_x] = FLY_WING
    canvas[wing_y-1, wing_x+1] = FLY_WING
    canvas[wing_y+1, wing_x+1] = FLY_WING
    
    # --- Motion Lines ---
    # Lines indicating snapping shut
    lines = [
        (10, 20, 15, 25),
        (54, 20, 49, 25),
        (10, 40, 15, 35),
        (54, 40, 49, 35)
    ]
    
    for x1, y1, x2, y2 in lines:
        # Simple line drawing
        points = max(abs(x2-x1), abs(y2-y1))
        for i in range(points + 1):
            t = i / points
            x = int(x1 + (x2-x1)*t)
            y = int(y1 + (y2-y1)*t)
            if 0 <= x < width and 0 <= y < height:
                canvas[y, x] = [255, 255, 255, 200]

    return canvas

def main():
    print("Creating flytrap monster images...")
    
    flytrap_default = create_flytrap_default()
    flytrap_attack = create_flytrap_attack()
    
    # Convert to PIL and scale up
    scale = 4
    
    # Default pose
    img_default = Image.fromarray(flytrap_default, 'RGBA')
    img_default_scaled = img_default.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_default_scaled.save('art/flytrap_monster_attack.png')
    print(f"✓ Saved: art/flytrap_monster_attack.png ({64 * scale}x{64 * scale})")
    
    # Attack animation
    img_attack = Image.fromarray(flytrap_attack, 'RGBA')
    img_attack_scaled = img_attack.resize((64 * scale, 64 * scale), Image.Resampling.NEAREST)
    img_attack_scaled.save('art/flytrap_monster.png')
    print(f"✓ Saved: art/flytrap_monster.png ({64 * scale}x{64 * scale})")
    
    print("\n✅ Flytrap monster creation complete!")

if __name__ == '__main__':
    main()
