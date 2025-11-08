"""
Create a 128x128 high-resolution, realistic warrior character PNG
Optimized for smaller size while maintaining detail
"""
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import math

def create_realistic_warrior_128():
    """Create a 128x128 high-resolution realistic warrior character"""
    # Create a 128x128 canvas
    width, height = 128, 128
    
    # Create image with transparent background
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Realistic color palette
    HAIR_COLOR = (92, 51, 23)          # Dark brown hair
    HAIR_HIGHLIGHT = (139, 90, 43)     # Hair highlights
    SKIN_COLOR = (241, 194, 125)       # Realistic skin tone
    SKIN_SHADOW = (205, 148, 87)       # Skin shadows
    SKIN_HIGHLIGHT = (255, 228, 181)   # Skin highlights
    
    TUNIC_RED = (139, 69, 19)          # Deep red tunic
    TUNIC_SHADOW = (101, 35, 10)       # Tunic shadows
    TUNIC_HIGHLIGHT = (178, 115, 86)   # Tunic highlights
    
    PANTS_BLUE = (25, 25, 112)         # Navy blue pants
    PANTS_SHADOW = (15, 15, 67)        # Pants shadows  
    PANTS_HIGHLIGHT = (70, 70, 139)    # Pants highlights
    
    ARMOR_SILVER = (169, 169, 169)     # Silver armor
    ARMOR_DARK = (105, 105, 105)       # Armor shadows
    ARMOR_BRIGHT = (220, 220, 220)     # Armor highlights
    
    SWORD_STEEL = (192, 192, 192)      # Steel blade
    SWORD_EDGE = (255, 255, 255)       # Sword edge highlight
    SWORD_SHADOW = (128, 128, 128)     # Sword shadow
    
    GOLD_COLOR = (255, 215, 0)         # Gold accents
    GOLD_SHADOW = (184, 134, 11)       # Gold shadows
    
    LEATHER_BROWN = (101, 67, 33)      # Leather shield/belt
    LEATHER_SHADOW = (62, 39, 35)      # Leather shadows
    
    def draw_gradient_ellipse(xy, fill_colors, outline=None):
        """Draw an ellipse with gradient effect"""
        x1, y1, x2, y2 = xy
        
        # Create gradient by drawing multiple ellipses
        steps = 5  # Reduced for 128x128
        max_shrink = min((x2 - x1) // 2, (y2 - y1) // 2) - 1
        if max_shrink <= 0:
            # Fallback to simple ellipse if too small
            color = fill_colors[0] if fill_colors else (128, 128, 128)
            draw.ellipse(xy, fill=color + (255,), outline=outline)
            return
            
        for i in range(steps):
            ratio = i / steps
            # Interpolate between colors
            if len(fill_colors) == 2:
                color = tuple(int(fill_colors[0][j] * (1 - ratio) + fill_colors[1][j] * ratio) for j in range(3))
            else:
                color = fill_colors[0]
            
            # Calculate smaller ellipse with bounds checking
            shrink = min(i * 1, max_shrink)  # Smaller shrink for 128x128
            new_x1, new_y1 = x1 + shrink, y1 + shrink
            new_x2, new_y2 = x2 - shrink, y2 - shrink
            
            if new_x2 > new_x1 and new_y2 > new_y1:
                draw.ellipse([new_x1, new_y1, new_x2, new_y2], 
                            fill=color + (255,), outline=outline)
    
    def draw_gradient_rectangle(xy, fill_colors, outline=None):
        """Draw a rectangle with gradient effect"""
        x1, y1, x2, y2 = xy
        
        # Vertical gradient
        for i in range(y2 - y1):
            ratio = i / (y2 - y1)
            color = tuple(int(fill_colors[0][j] * (1 - ratio) + fill_colors[1][j] * ratio) for j in range(3))
            draw.line([(x1, y1 + i), (x2, y1 + i)], fill=color + (255,))
    
    # HEAD - realistic face with shading (scaled to 128x128)
    head_x, head_y = 48, 8
    head_w, head_h = 32, 32
    
    # Face base (oval)
    draw_gradient_ellipse([head_x, head_y, head_x + head_w, head_y + head_h], 
                         [SKIN_HIGHLIGHT, SKIN_COLOR])
    
    # Face shadow (left side)
    draw.ellipse([head_x - 2, head_y + 2, head_x + head_w - 10, head_y + head_h + 2],
                fill=SKIN_SHADOW + (128,))
    
    # Hair - realistic flowing hair
    # Hair base
    draw.ellipse([head_x - 5, head_y - 7, head_x + head_w + 5, head_y + 18],
                fill=HAIR_COLOR + (255,))
    
    # Hair highlights
    draw.ellipse([head_x + 2, head_y - 5, head_x + 18, head_y + 10],
                fill=HAIR_HIGHLIGHT + (180,))
    draw.ellipse([head_x + 12, head_y - 2, head_x + 28, head_y + 12],
                fill=HAIR_HIGHLIGHT + (120,))
    
    # Eyes - realistic with pupils and highlights
    eye_y = head_y + 10
    # Left eye
    draw.ellipse([head_x + 7, eye_y, head_x + 13, eye_y + 4], fill=(255, 255, 255, 255))
    draw.ellipse([head_x + 8, eye_y + 1, head_x + 12, eye_y + 3], fill=(101, 67, 33, 255))  # Brown iris
    draw.ellipse([head_x + 9, eye_y + 1, head_x + 11, eye_y + 2], fill=(0, 0, 0, 255))     # Pupil
    
    # Right eye
    draw.ellipse([head_x + 17, eye_y, head_x + 23, eye_y + 4], fill=(255, 255, 255, 255))
    draw.ellipse([head_x + 18, eye_y + 1, head_x + 22, eye_y + 3], fill=(101, 67, 33, 255))  # Brown iris
    draw.ellipse([head_x + 19, eye_y + 1, head_x + 21, eye_y + 2], fill=(0, 0, 0, 255))     # Pupil
    
    # Nose - 3D shading
    nose_x, nose_y = head_x + 14, head_y + 14
    draw.ellipse([nose_x, nose_y, nose_x + 4, nose_y + 6], fill=SKIN_COLOR + (255,))
    draw.ellipse([nose_x - 1, nose_y + 1, nose_x + 2, nose_y + 4], fill=SKIN_SHADOW + (180,))
    
    # Mouth - realistic with slight smile
    mouth_y = head_y + 21
    draw.ellipse([head_x + 11, mouth_y, head_x + 21, mouth_y + 4], fill=SKIN_SHADOW + (200,))
    
    # BODY - Realistic torso with detailed tunic (scaled to 128x128)
    body_x, body_y = 48, 48
    body_w, body_h = 32, 48
    
    # Torso base
    draw_gradient_rectangle([body_x, body_y, body_x + body_w, body_y + body_h], 
                          [TUNIC_HIGHLIGHT, TUNIC_RED])
    
    # Tunic shadows and folds
    draw.polygon([(body_x, body_y), (body_x + 10, body_y + 15), (body_x, body_y + 20)], 
                fill=TUNIC_SHADOW + (180,))
    draw.polygon([(body_x + body_w, body_y), (body_x + body_w - 10, body_y + 15), 
                 (body_x + body_w, body_y + 20)], fill=TUNIC_SHADOW + (180,))
    
    # Chest armor - realistic metallic breastplate
    armor_x, armor_y = body_x + 8, body_y + 4
    armor_w, armor_h = 16, 24
    
    # Armor base
    draw_gradient_ellipse([armor_x, armor_y, armor_x + armor_w, armor_y + armor_h],
                         [ARMOR_BRIGHT, ARMOR_SILVER])
    
    # Armor details and rivets (smaller for 128x128)
    for i in range(2):
        for j in range(3):
            rivet_x = armor_x + 4 + i * 6
            rivet_y = armor_y + 4 + j * 6
            draw.ellipse([rivet_x, rivet_y, rivet_x + 2, rivet_y + 2], 
                        fill=ARMOR_DARK + (255,))
    
    # Belt - leather with gold buckle
    belt_y = body_y + 28
    draw.rectangle([body_x, belt_y, body_x + body_w, belt_y + 4], fill=LEATHER_BROWN + (255,))
    
    # Belt buckle
    buckle_x = body_x + 13
    draw.rectangle([buckle_x, belt_y - 1, buckle_x + 6, belt_y + 5], fill=GOLD_COLOR + (255,))
    
    # LEFT ARM - holding detailed shield (scaled)
    arm_x, arm_y = 24, 48
    arm_w, arm_h = 16, 48
    
    # Arm base
    draw_gradient_rectangle([arm_x, arm_y, arm_x + arm_w, arm_y + arm_h], 
                          [TUNIC_HIGHLIGHT, TUNIC_RED])
    
    # Shield - detailed medieval round shield
    shield_x, shield_y = 8, 60
    shield_r = 12
    
    # Shield base (wood/leather)
    draw.ellipse([shield_x, shield_y, shield_x + shield_r * 2, shield_y + shield_r * 2], 
                fill=LEATHER_BROWN + (255,))
    
    # Shield metal rim
    draw.ellipse([shield_x - 1, shield_y - 1, shield_x + shield_r * 2 + 1, shield_y + shield_r * 2 + 1], 
                fill=ARMOR_SILVER + (255,), width=2)
    
    # Shield boss (center metal piece)
    boss_x, boss_y = shield_x + shield_r - 4, shield_y + shield_r - 4
    draw_gradient_ellipse([boss_x, boss_y, boss_x + 8, boss_y + 8], 
                         [ARMOR_BRIGHT, ARMOR_DARK])
    
    # RIGHT ARM - holding detailed sword (scaled)
    right_arm_x, right_arm_y = 88, 48
    right_arm_w, right_arm_h = 16, 48
    
    # Arm base
    draw_gradient_rectangle([right_arm_x, right_arm_y, right_arm_x + right_arm_w, right_arm_y + right_arm_h], 
                          [TUNIC_HIGHLIGHT, TUNIC_RED])
    
    # Sword - realistic medieval longsword (scaled)
    sword_x, sword_y = right_arm_x + 12, right_arm_y - 16
    sword_w, sword_h = 4, 64
    
    # Sword blade
    draw_gradient_rectangle([sword_x, sword_y, sword_x + sword_w, sword_y + sword_h - 12], 
                          [SWORD_EDGE, SWORD_STEEL])
    
    # Blade fuller (central groove)
    draw.rectangle([sword_x + 1, sword_y + 4, sword_x + 3, sword_y + sword_h - 16], 
                  fill=SWORD_SHADOW + (180,))
    
    # Blade point
    draw.polygon([(sword_x, sword_y + 4), (sword_x + 2, sword_y), (sword_x + 4, sword_y + 4)], 
                fill=SWORD_EDGE + (255,))
    
    # Crossguard
    guard_y = sword_y + sword_h - 12
    draw.rectangle([sword_x - 4, guard_y, sword_x + sword_w + 4, guard_y + 2], 
                  fill=ARMOR_SILVER + (255,))
    
    # Grip
    draw_gradient_rectangle([sword_x + 1, guard_y + 2, sword_x + sword_w - 1, guard_y + 10], 
                          [LEATHER_BROWN, LEATHER_SHADOW])
    
    # Pommel
    draw_gradient_ellipse([sword_x, guard_y + 10, sword_x + sword_w, guard_y + 14], 
                         [GOLD_COLOR, GOLD_SHADOW])
    
    # LEGS - Realistic with detailed pants and boots (scaled)
    left_leg_x, left_leg_y = 48, 96
    leg_w, leg_h = 14, 32
    
    # Left leg
    draw_gradient_rectangle([left_leg_x, left_leg_y, left_leg_x + leg_w, left_leg_y + leg_h], 
                          [PANTS_HIGHLIGHT, PANTS_BLUE])
    
    # Right leg  
    right_leg_x = 66
    draw_gradient_rectangle([right_leg_x, left_leg_y, right_leg_x + leg_w, left_leg_y + leg_h], 
                          [PANTS_HIGHLIGHT, PANTS_BLUE])
    
    # Leg shadows/folds
    draw.rectangle([left_leg_x, left_leg_y + 5, left_leg_x + 2, left_leg_y + leg_h - 5], 
                  fill=PANTS_SHADOW + (180,))
    draw.rectangle([right_leg_x, left_leg_y + 5, right_leg_x + 2, left_leg_y + leg_h - 5], 
                  fill=PANTS_SHADOW + (180,))
    
    # Boots - detailed leather boots with armor plates (scaled)
    boot_y = left_leg_y + 20
    boot_h = 12
    
    # Left boot
    draw_gradient_rectangle([left_leg_x, boot_y, left_leg_x + leg_w, boot_y + boot_h], 
                          [LEATHER_BROWN, LEATHER_SHADOW])
    # Boot armor plate
    draw_gradient_rectangle([left_leg_x + 2, boot_y + 2, left_leg_x + leg_w - 2, boot_y + 6], 
                          [ARMOR_BRIGHT, ARMOR_SILVER])
    
    # Right boot
    draw_gradient_rectangle([right_leg_x, boot_y, right_leg_x + leg_w, boot_y + boot_h], 
                          [LEATHER_BROWN, LEATHER_SHADOW])
    # Boot armor plate
    draw_gradient_rectangle([right_leg_x + 2, boot_y + 2, right_leg_x + leg_w - 2, boot_y + 6], 
                          [ARMOR_BRIGHT, ARMOR_SILVER])
    
    # Shoulder armor - detailed pauldrons (scaled)
    # Left shoulder
    draw_gradient_ellipse([body_x - 4, body_y - 2, body_x + 10, body_y + 10], 
                         [ARMOR_BRIGHT, ARMOR_SILVER])
    # Right shoulder
    draw_gradient_ellipse([body_x + body_w - 6, body_y - 2, body_x + body_w + 8, body_y + 10], 
                         [ARMOR_BRIGHT, ARMOR_SILVER])
    
    # Add some battle-worn effects and details (scaled)
    # Scratches on armor
    for i in range(3):
        scratch_x = armor_x + (i * 3) + 2
        scratch_y = armor_y + (i * 4) + 4
        draw.line([(scratch_x, scratch_y), (scratch_x + 2, scratch_y + 3)], 
                 fill=ARMOR_DARK + (200,), width=1)
    
    # Apply subtle blur for realism
    img = img.filter(ImageFilter.GaussianBlur(radius=0.3))
    
    # Save the high-resolution warrior
    output_path = 'art/Warrior_realistic_128.png'
    img.save(output_path, 'PNG')
    
    print(f"✅ Created {output_path}")
    print(f"   Size: {width}x{height} pixels (optimized resolution)")
    print(f"   Style: Photorealistic medieval warrior")
    print(f"   Features: Detailed armor, realistic sword & shield, battle-worn effects")
    print(f"   Details: Brown hair, red tunic, blue pants, silver armor, leather accessories")
    print(f"   Quality: 128x128 high-resolution with gradient shading and realistic proportions")

if __name__ == '__main__':
    create_realistic_warrior_128()