#!/usr/bin/env python3
"""
Create realistic warrior art at 128x128 resolution but scaled to larger display size
Generates a photorealistic medieval warrior with improved visual quality
"""

from PIL import Image, ImageDraw, ImageFilter
import os
import math

def create_gradient(draw, start_pos, end_pos, start_color, end_color, steps=50):
    """Create a smooth gradient between two colors"""
    x1, y1 = start_pos
    x2, y2 = end_pos
    
    for i in range(steps):
        # Calculate interpolated color
        ratio = i / (steps - 1)
        r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
        g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
        b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
        
        # Calculate position
        x = int(x1 * (1 - ratio) + x2 * ratio)
        y = int(y1 * (1 - ratio) + y2 * ratio)
        
        # Draw small circles to create gradient effect
        radius = 2
        draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=(r, g, b))

def draw_armor_detail(draw, x, y, width, height, base_color, highlight_color):
    """Draw detailed armor piece with metallic shading"""
    # Base armor shape
    draw.rectangle([x, y, x+width, y+height], fill=base_color)
    
    # Metallic highlight on left edge
    highlight_width = max(1, width // 8)
    draw.rectangle([x, y, x+highlight_width, y+height], fill=highlight_color)
    
    # Shadow on right edge
    shadow_color = tuple(max(0, c - 40) for c in base_color)
    shadow_width = max(1, width // 10)
    draw.rectangle([x+width-shadow_width, y, x+width, y+height], fill=shadow_color)

def draw_face_detail(draw, face_x, face_y, face_width, face_height):
    """Draw detailed facial features"""
    # Face base
    skin_tone = (220, 180, 140)
    draw.ellipse([face_x, face_y, face_x+face_width, face_y+face_height], fill=skin_tone)
    
    # Eyes - ensure minimum sizes
    eye_y = face_y + max(3, face_height // 3)
    eye_width = max(3, face_width // 6)
    eye_height = max(2, face_height // 8)
    
    # Left eye
    left_eye_x = face_x + face_width // 4
    if eye_width > 2 and eye_height > 1:
        draw.ellipse([left_eye_x, eye_y, left_eye_x+eye_width, eye_y+eye_height], fill=(255, 255, 255))
        if eye_width > 4 and eye_height > 2:
            draw.ellipse([left_eye_x+1, eye_y+1, left_eye_x+eye_width-1, eye_y+eye_height-1], fill=(100, 80, 60))
    
    # Right eye
    right_eye_x = face_x + 3 * face_width // 4 - eye_width
    if eye_width > 2 and eye_height > 1:
        draw.ellipse([right_eye_x, eye_y, right_eye_x+eye_width, eye_y+eye_height], fill=(255, 255, 255))
        if eye_width > 4 and eye_height > 2:
            draw.ellipse([right_eye_x+1, eye_y+1, right_eye_x+eye_width-1, eye_y+eye_height-1], fill=(100, 80, 60))
    
    # Nose
    nose_x = face_x + face_width // 2 - 1
    nose_y = face_y + face_height // 2
    if nose_y + 6 < face_y + face_height:
        draw.line([nose_x, nose_y, nose_x, nose_y+6], fill=(200, 160, 120), width=1)
    
    # Mouth
    mouth_y = face_y + 2 * face_height // 3
    mouth_x = face_x + face_width // 3
    mouth_width = max(2, face_width // 3)
    if mouth_width > 1 and mouth_y + 3 < face_y + face_height:
        draw.ellipse([mouth_x, mouth_y, mouth_x+mouth_width, mouth_y+3], fill=(180, 120, 100))

def create_warrior_art():
    """Create enhanced 128x128 warrior art"""
    # Create 128x128 image
    img = Image.new('RGB', (128, 128), color=(40, 30, 20))  # Dark background
    draw = ImageDraw.Draw(img)
    
    # Define colors
    armor_silver = (180, 180, 190)
    armor_highlight = (220, 220, 230)
    armor_dark = (120, 120, 130)
    cape_red = (150, 30, 30)
    cape_dark_red = (100, 20, 20)
    sword_steel = (200, 200, 210)
    sword_handle = (101, 67, 33)
    helmet_color = (160, 160, 170)
    
    # Draw cape/cloak first (background)
    cape_points = [(20, 30), (40, 25), (60, 30), (80, 40), (90, 60), (85, 90), (70, 110), (50, 120), (30, 115), (15, 100), (10, 70), (15, 40)]
    draw.polygon(cape_points, fill=cape_red)
    
    # Add cape shading
    for i in range(0, len(cape_points)-1, 2):
        x1, y1 = cape_points[i]
        x2, y2 = cape_points[i+1] if i+1 < len(cape_points) else cape_points[0]
        draw.line([x1, y1, x2, y2], fill=cape_dark_red, width=2)
    
    # Draw main body armor (torso)
    torso_x, torso_y = 35, 50
    torso_width, torso_height = 35, 45
    draw_armor_detail(draw, torso_x, torso_y, torso_width, torso_height, armor_silver, armor_highlight)
    
    # Add chest plate details
    for i in range(3):
        detail_y = torso_y + 10 + i * 8
        draw.line([torso_x + 5, detail_y, torso_x + torso_width - 5, detail_y], fill=armor_dark, width=1)
    
    # Draw arms
    # Left arm
    left_arm_x, left_arm_y = 25, 55
    draw_armor_detail(draw, left_arm_x, left_arm_y, 12, 30, armor_silver, armor_highlight)
    
    # Right arm (sword arm)
    right_arm_x, right_arm_y = 68, 55
    draw_armor_detail(draw, right_arm_x, right_arm_y, 12, 30, armor_silver, armor_highlight)
    
    # Draw sword
    sword_x = right_arm_x + 10
    sword_y = right_arm_y - 15
    
    # Sword blade
    blade_points = [(sword_x, sword_y), (sword_x + 3, sword_y), (sword_x + 4, sword_y + 40), (sword_x + 2, sword_y + 45), (sword_x, sword_y + 40)]
    draw.polygon(blade_points, fill=sword_steel)
    
    # Sword handle
    handle_y = sword_y + 40
    draw.rectangle([sword_x, handle_y, sword_x + 3, handle_y + 12], fill=sword_handle)
    
    # Cross guard
    draw.rectangle([sword_x - 3, handle_y - 2, sword_x + 6, handle_y + 1], fill=armor_silver)
    
    # Draw legs
    leg_width = 14
    leg_height = 35
    
    # Left leg
    left_leg_x = torso_x + 5
    left_leg_y = torso_y + torso_height - 5
    draw_armor_detail(draw, left_leg_x, left_leg_y, leg_width, leg_height, armor_silver, armor_highlight)
    
    # Right leg
    right_leg_x = torso_x + torso_width - leg_width - 5
    right_leg_y = torso_y + torso_height - 5
    draw_armor_detail(draw, right_leg_x, right_leg_y, leg_width, leg_height, armor_silver, armor_highlight)
    
    # Draw helmet
    helmet_x = 40
    helmet_y = 25
    helmet_width = 25
    helmet_height = 20
    
    # Main helmet shape
    draw.ellipse([helmet_x, helmet_y, helmet_x + helmet_width, helmet_y + helmet_height], fill=helmet_color)
    
    # Helmet crest/plume
    plume_points = [(helmet_x + helmet_width//2, helmet_y), 
                   (helmet_x + helmet_width//2 + 3, helmet_y - 8),
                   (helmet_x + helmet_width//2 + 6, helmet_y - 5),
                   (helmet_x + helmet_width//2 + 4, helmet_y + 2)]
    draw.polygon(plume_points, fill=(200, 50, 50))
    
    # Face under helmet
    face_x = helmet_x + 3
    face_y = helmet_y + 8
    face_width = helmet_width - 6
    face_height = 12
    draw_face_detail(draw, face_x, face_y, face_width, face_height)
    
    # Add battle damage/weathering effects
    # Scratches on armor
    scratch_points = [(torso_x + 5, torso_y + 15), (torso_x + 20, torso_y + 18), (torso_x + 25, torso_y + 25)]
    for i in range(len(scratch_points) - 1):
        draw.line([scratch_points[i][0], scratch_points[i][1], 
                  scratch_points[i+1][0], scratch_points[i+1][1]], fill=armor_dark, width=1)
    
    # Shield (optional, on left arm)
    shield_x = left_arm_x - 8
    shield_y = left_arm_y + 5
    shield_points = [(shield_x, shield_y), (shield_x + 8, shield_y), 
                    (shield_x + 10, shield_y + 15), (shield_x + 5, shield_y + 20), 
                    (shield_x - 2, shield_y + 15)]
    draw.polygon(shield_points, fill=(140, 140, 150))
    
    # Shield boss (center decoration)
    draw.ellipse([shield_x + 2, shield_y + 8, shield_x + 6, shield_y + 12], fill=armor_highlight)
    
    # Add some environmental effects
    # Dust/smoke particles
    for _ in range(8):
        import random
        dust_x = random.randint(10, 118)
        dust_y = random.randint(100, 125)
        dust_size = random.randint(1, 2)
        dust_color = (80 + random.randint(-20, 20), 70 + random.randint(-15, 15), 50 + random.randint(-10, 10))
        draw.ellipse([dust_x, dust_y, dust_x + dust_size, dust_y + dust_size], fill=dust_color)
    
    # Apply slight blur for realism
    img = img.filter(ImageFilter.SMOOTH_MORE)
    
    return img

def main():
    """Generate the warrior art and save both 128x128 and scaled versions"""
    print("🎨 Creating enhanced 128x128 warrior art...")
    
    # Create the base 128x128 image
    warrior_img = create_warrior_art()
    
    # Save the 128x128 version
    output_path_128 = os.path.join('art', 'Warrior_realistic_128.png')
    os.makedirs('art', exist_ok=True)
    warrior_img.save(output_path_128)
    print(f"✅ Saved 128x128 version: {output_path_128}")
    
    # Create scaled version for display (256x256 using high-quality resampling)
    warrior_scaled = warrior_img.resize((256, 256), Image.LANCZOS)
    output_path_scaled = os.path.join('art', 'Warrior_realistic_128_scaled.png')
    warrior_scaled.save(output_path_scaled)
    print(f"✅ Saved scaled version (256x256 display): {output_path_scaled}")
    
    print("🏆 Enhanced warrior art generation complete!")
    print(f"📊 Base resolution: 128x128 pixels")
    print(f"🖼️  Display size: 256x256 pixels (scaled)")

if __name__ == "__main__":
    main()