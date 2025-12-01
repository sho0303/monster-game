import numpy as np
from PIL import Image, ImageDraw
import os
import math

def create_sand_wyrm_art():
    width = 64
    height = 64
    
    # === COLORS ===
    TRANSPARENT = [0, 0, 0, 0]
    
    # Sand/Environment
    SAND_LIGHT = [240, 230, 160, 255]
    SAND_MID = [210, 190, 120, 255]
    SAND_DARK = [170, 150, 90, 255]
    SAND_SHADOW = [130, 110, 70, 255]
    
    # Wyrm Armor (Gold/Chitin)
    ARMOR_HIGHLIGHT = [255, 250, 200, 255] # Bright specular
    ARMOR_LIGHT = [255, 215, 0, 255]       # Gold
    ARMOR_MID = [218, 165, 32, 255]        # Goldenrod
    ARMOR_DARK = [184, 134, 11, 255]       # Dark Goldenrod
    ARMOR_SHADOW = [101, 67, 33, 255]      # Dark Brown/Bronze
    ARMOR_OUTLINE = [60, 40, 20, 255]      # Very dark brown
    
    # Flesh/Underbelly
    FLESH_LIGHT = [200, 150, 100, 255]
    FLESH_DARK = [150, 100, 60, 255]
    
    # Details
    EYE_COLOR = [0, 200, 255, 255]         # Glowing Cyan/Blue
    EYE_GLOW = [150, 230, 255, 150]        # Transparent glow
    MOUTH_DARK = [40, 10, 10, 255]
    TOOTH_COLOR = [240, 240, 220, 255]
    
    # Initialize canvases
    canvas_default = np.zeros((height, width, 4), dtype=np.uint8)
    canvas_attack = np.zeros((height, width, 4), dtype=np.uint8)
    
    # === HELPER FUNCTIONS ===
    def draw_pixel(canvas, x, y, color):
        if 0 <= x < width and 0 <= y < height:
            # Alpha blending if color is not fully opaque
            if len(color) == 4 and color[3] < 255:
                current = canvas[y][x]
                alpha = color[3] / 255.0
                for c in range(3):
                    canvas[y][x][c] = int(current[c] * (1 - alpha) + color[c] * alpha)
                canvas[y][x][3] = max(current[3], color[3]) # Keep max alpha
            else:
                canvas[y][x] = color

    def draw_circle(canvas, cx, cy, r, color):
        for y in range(int(cy - r), int(cy + r + 1)):
            for x in range(int(cx - r), int(cx + r + 1)):
                if (x - cx)**2 + (y - cy)**2 <= r**2:
                    draw_pixel(canvas, x, y, color)

    def draw_segment(canvas, cx, cy, r, angle_deg=0):
        # Draw a segmented body part with shading
        # Angle determines the rotation of the segment plates
        
        for y in range(int(cy - r), int(cy + r + 1)):
            for x in range(int(cx - r), int(cx + r + 1)):
                if 0 <= x < width and 0 <= y < height:
                    dist = ((x - cx)**2 + (y - cy)**2)**0.5
                    if dist <= r:
                        # Outline
                        if dist > r - 1.5:
                            draw_pixel(canvas, x, y, ARMOR_OUTLINE)
                            continue
                            
                        # Calculate lighting
                        # Light comes from top-left
                        dx = x - cx
                        dy = y - cy
                        
                        # Rotate coordinates for texture alignment
                        rad = math.radians(angle_deg)
                        rot_x = dx * math.cos(rad) - dy * math.sin(rad)
                        rot_y = dx * math.sin(rad) + dy * math.cos(rad)
                        
                        # Base color logic
                        col = ARMOR_MID
                        
                        # Cylindrical shading (highlight on top-left side)
                        # We use the rotated Y to simulate the segment ridges
                        
                        # Ridge at the "top" of the segment (relative to rotation)
                        if rot_y < -r * 0.5:
                            col = ARMOR_LIGHT
                        elif rot_y > r * 0.5:
                            col = ARMOR_DARK
                        
                        # Specular highlight
                        if dist < r * 0.8 and rot_x < -r * 0.2 and rot_y < -r * 0.2:
                            col = ARMOR_HIGHLIGHT
                            
                        # Deep shadow at bottom right
                        if rot_x > r * 0.3 and rot_y > r * 0.3:
                            col = ARMOR_SHADOW
                            
                        # Segment line (the gap between plates)
                        # We simulate this by making the very bottom of the rotated segment dark
                        if rot_y > r * 0.7:
                            col = ARMOR_OUTLINE
                            
                        draw_pixel(canvas, x, y, col)
                        
                        # Texture spots (weathering)
                        if (x * y * 13) % 47 < 2:
                            draw_pixel(canvas, x, y, ARMOR_SHADOW)

    def draw_spike(canvas, tip_x, tip_y, base_x, base_y, width_base):
        # Simple triangle spike
        # Vector from base to tip
        vx = tip_x - base_x
        vy = tip_y - base_y
        length = (vx**2 + vy**2)**0.5
        if length == 0: return
        
        # Perpendicular vector
        px = -vy / length * width_base
        py = vx / length * width_base
        
        # Triangle points: Tip, BaseLeft, BaseRight
        p1 = (tip_x, tip_y)
        p2 = (base_x + px, base_y + py)
        p3 = (base_x - px, base_y - py)
        
        # Bounding box
        min_x = int(min(p1[0], p2[0], p3[0]))
        max_x = int(max(p1[0], p2[0], p3[0]))
        min_y = int(min(p1[1], p2[1], p3[1]))
        max_y = int(max(p1[1], p2[1], p3[1]))
        
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                # Barycentric coordinates or simple check
                # Using simple check for pixel art
                if 0 <= x < width and 0 <= y < height:
                    # Check if point is inside triangle
                    def sign(p1, p2, p3):
                        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
                    
                    d1 = sign((x, y), p1, p2)
                    d2 = sign((x, y), p2, p3)
                    d3 = sign((x, y), p3, p1)
                    
                    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
                    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
                    
                    if not (has_neg and has_pos):
                        draw_pixel(canvas, x, y, ARMOR_LIGHT)

    # === DEFAULT POSE GENERATION ===
    # Giant worm arching out of the sand
    
    # 1. Draw Sand Mound at bottom (REMOVED for transparency)
    # Sand background removed to allow sprite to be placed on any background
    pass

    # 2. Draw Body Segments (Back to Front order)
    # Path: Emerges at (15, 60), Arches up to (32, 10), Comes down to (50, 35)
    
    # Define path points (x, y, radius, angle)
    path = []
    
    # Rising part (Left side)
    for i in range(10):
        t = i / 10.0
        x = 15 + t * 10
        y = 65 - t * 40
        r = 12 - t * 2 # Gets slightly smaller
        angle = 10 + t * 20
        path.append((x, y, r, angle))
        
    # Arch top
    for i in range(8):
        t = i / 8.0
        x = 25 + t * 15
        y = 25 - math.sin(t * 3.14) * 10
        r = 10
        angle = 30 + t * 60
        path.append((x, y, r, angle))
        
    # Descending part (Right side - Head area)
    for i in range(6):
        t = i / 6.0
        x = 40 + t * 12
        y = 25 + t * 15
        r = 10 + t * 1 # Head gets slightly bigger/armored
        angle = 90 + t * 45
        path.append((x, y, r, angle))

    # Draw segments
    for i, (cx, cy, r, angle) in enumerate(path):
        draw_segment(canvas_default, cx, cy, r, angle)
        
        # Add spikes on the outer curve
        if i > 5: # Don't put spikes on the buried part
            # Calculate outer edge position
            rad = math.radians(angle - 90) # Perpendicular to segment angle
            spike_base_x = cx + math.cos(rad) * (r - 2)
            spike_base_y = cy + math.sin(rad) * (r - 2)
            spike_tip_x = cx + math.cos(rad) * (r + 6)
            spike_tip_y = cy + math.sin(rad) * (r + 6)
            draw_spike(canvas_default, spike_tip_x, spike_tip_y, spike_base_x, spike_base_y, 4)

    # 3. Draw Head (at the end of the path)
    head_x, head_y, head_r, head_angle = path[-1]
    
    # Mandibles
    # Left Mandible
    draw_spike(canvas_default, head_x - 5, head_y + 15, head_x - 2, head_y + 5, 3)
    # Right Mandible
    draw_spike(canvas_default, head_x + 10, head_y + 12, head_x + 4, head_y + 5, 3)
    
    # Face Plate
    draw_segment(canvas_default, head_x, head_y, head_r + 1, head_angle)
    
    # Eyes (Glowing Blue)
    # Left Eye
    draw_pixel(canvas_default, int(head_x - 3), int(head_y + 2), EYE_COLOR)
    draw_pixel(canvas_default, int(head_x - 2), int(head_y + 2), EYE_COLOR)
    # Right Eye
    draw_pixel(canvas_default, int(head_x + 4), int(head_y + 1), EYE_COLOR)
    draw_pixel(canvas_default, int(head_x + 5), int(head_y + 1), EYE_COLOR)
    
    # Eye Glow
    draw_pixel(canvas_default, int(head_x - 3), int(head_y + 3), EYE_GLOW)
    draw_pixel(canvas_default, int(head_x + 4), int(head_y + 2), EYE_GLOW)

    # === ATTACK POSE GENERATION ===
    # Lunging straight forward, mouth wide open
    
    # 1. Sand Explosion at bottom (REMOVED for transparency)
    # Sand background removed to allow sprite to be placed on any background
    pass
    
    # 2. Body Segments (Lunging forward)
    # Stacked vertically, getting larger towards top (perspective)
    
    for i in range(10):
        y = 60 - i * 4
        x = 32 + math.sin(i * 0.5) * 5 # Slight wiggle
        r = 10 + i * 0.5 # Getting closer/larger
        
        draw_segment(canvas_attack, x, y, r, 0)
        
        # Spikes on both sides
        draw_spike(canvas_attack, x - r - 4, y, x - r + 2, y, 3)
        draw_spike(canvas_attack, x + r + 4, y, x + r - 2, y, 3)

    # 3. Open Mouth Head
    head_cx = 32
    head_cy = 20
    head_r = 16
    
    # Draw open mouth interior (dark void)
    draw_circle(canvas_attack, head_cx, head_cy, head_r - 2, MOUTH_DARK)
    
    # Draw teeth ring
    num_teeth = 8
    for i in range(num_teeth):
        angle = (i / num_teeth) * 2 * math.pi
        tx = head_cx + math.cos(angle) * (head_r - 6)
        ty = head_cy + math.sin(angle) * (head_r - 6)
        
        # Tooth pointing inward
        tip_x = head_cx + math.cos(angle) * (head_r - 10)
        tip_y = head_cy + math.sin(angle) * (head_r - 10)
        
        draw_spike(canvas_attack, tip_x, tip_y, tx, ty, 2)
        
    # Draw Mandibles (Large, outer)
    # Left
    draw_spike(canvas_attack, head_cx - 10, head_cy + 15, head_cx - 18, head_cy, 5)
    # Right
    draw_spike(canvas_attack, head_cx + 10, head_cy + 15, head_cx + 18, head_cy, 5)
    # Top
    draw_spike(canvas_attack, head_cx, head_cy - 15, head_cx, head_cy - 18, 5)
    
    # Eyes on the side of the head
    draw_pixel(canvas_attack, int(head_cx - 12), int(head_cy - 5), EYE_COLOR)
    draw_pixel(canvas_attack, int(head_cx + 12), int(head_cy - 5), EYE_COLOR)
    
    # Motion lines
    for i in range(5):
        lx = 10 + i * 10
        ly = 10 + i * 5
        draw_pixel(canvas_attack, lx, ly, [255, 255, 255, 100])
        draw_pixel(canvas_attack, lx+1, ly+1, [255, 255, 255, 100])

    # === SAVE IMAGES ===
    
    # Scale up 4x
    img_default = Image.fromarray(canvas_default, 'RGBA')
    img_default = img_default.resize((width * 4, height * 4), Image.Resampling.NEAREST)
    img_default.save('art/sand_wyrm_monster.png')
    print(f"✓ Saved: art/sand_wyrm_monster.png ({width*4}x{height*4})")
    
    img_attack = Image.fromarray(canvas_attack, 'RGBA')
    img_attack = img_attack.resize((width * 4, height * 4), Image.Resampling.NEAREST)
    img_attack.save('art/sand_wyrm_monster_attack.png')
    print(f"✓ Saved: art/sand_wyrm_monster_attack.png ({width*4}x{height*4})")

if __name__ == "__main__":
    print("Creating Sand Wyrm monster images...")
    create_sand_wyrm_art()
    print("✅ Sand Wyrm creation complete!")
