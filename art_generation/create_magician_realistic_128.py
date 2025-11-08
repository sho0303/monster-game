#!/usr/bin/env python3
"""
Create enhanced realistic magician art at 128x128 resolution with transparent background
More detailed and realistic while maintaining the magical wizard aesthetic
"""

from PIL import Image, ImageDraw, ImageFilter
import os
import math

def create_gradient_circle(draw, center_x, center_y, radius, inner_color, outer_color):
    """Create a gradient circle for magical effects"""
    for r in range(radius, 0, -1):
        ratio = (radius - r) / radius
        color = tuple(int(inner_color[i] * ratio + outer_color[i] * (1 - ratio)) for i in range(3))
        draw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r], 
                    outline=color + (int(255 * (radius - r) / radius),))

def draw_fabric_texture(draw, x, y, width, height, base_color, highlight_color, shadow_color):
    """Draw fabric texture with shading"""
    # Base fill
    draw.rectangle([x, y, x + width, y + height], fill=base_color)
    
    # Add fabric fold highlights and shadows
    for i in range(0, width, 8):
        fold_x = x + i
        if fold_x < x + width:
            # Highlight line
            draw.line([fold_x, y, fold_x, y + height], fill=highlight_color, width=1)
            # Shadow line
            if fold_x + 3 < x + width:
                draw.line([fold_x + 3, y, fold_x + 3, y + height], fill=shadow_color, width=1)

def draw_magical_staff(draw, staff_x, staff_y, staff_length):
    """Draw detailed magical staff"""
    staff_width = 4
    
    # Wooden shaft gradient
    wood_base = (101, 67, 33)
    wood_highlight = (140, 95, 50)
    wood_shadow = (70, 45, 20)
    
    # Main shaft
    draw.rectangle([staff_x, staff_y, staff_x + staff_width, staff_y + staff_length], fill=wood_base)
    
    # Wood grain lines
    for i in range(0, staff_length, 8):
        grain_y = staff_y + i
        draw.line([staff_x, grain_y, staff_x + staff_width, grain_y], fill=wood_shadow, width=1)
    
    # Highlight edge
    draw.line([staff_x, staff_y, staff_x, staff_y + staff_length], fill=wood_highlight, width=1)
    
    # Crystal orb at top
    orb_center_x = staff_x + staff_width // 2
    orb_center_y = staff_y - 8
    orb_radius = 6
    
    # Orb glow effect
    glow_colors = [(0, 255, 255), (100, 200, 255), (200, 150, 255)]
    for i, color in enumerate(glow_colors):
        radius = orb_radius - i * 2
        if radius > 0:
            draw.ellipse([orb_center_x - radius, orb_center_y - radius, 
                         orb_center_x + radius, orb_center_y + radius], 
                        fill=color + (180 - i * 40,))
    
    # Crystal facets
    draw.polygon([(orb_center_x - 3, orb_center_y), (orb_center_x, orb_center_y - 4), 
                 (orb_center_x + 3, orb_center_y), (orb_center_x, orb_center_y + 4)], 
                fill=(255, 255, 255, 200))

def draw_realistic_face(draw, face_x, face_y, face_width, face_height):
    """Draw detailed facial features"""
    # Face base with skin tone
    skin_color = (235, 195, 160)
    draw.ellipse([face_x, face_y, face_x + face_width, face_y + face_height], fill=skin_color)
    
    # Facial shading
    shadow_color = (200, 160, 125)
    if face_width > 4 and face_height > 8:
        draw.ellipse([face_x + 2, face_y + face_height//4, face_x + face_width - 2, face_y + face_height], 
                    fill=shadow_color)
    
    # Eyes - ensure minimum sizes
    eye_width = max(4, face_width // 5)
    eye_height = max(3, face_height // 6)
    eye_y = face_y + face_height // 3
    
    # Left eye
    left_eye_x = face_x + face_width // 4
    if eye_width > 2 and eye_height > 2:
        draw.ellipse([left_eye_x, eye_y, left_eye_x + eye_width, eye_y + eye_height], fill=(255, 255, 255))
        if eye_width > 4 and eye_height > 3:
            draw.ellipse([left_eye_x + 1, eye_y + 1, left_eye_x + eye_width - 1, eye_y + eye_height - 1], 
                        fill=(70, 130, 180))  # Wise blue eyes
        if eye_width > 6 and eye_height > 4:
            draw.ellipse([left_eye_x + 2, eye_y + 2, left_eye_x + eye_width - 2, eye_y + eye_height - 2], 
                        fill=(20, 20, 20))  # Pupil
    
    # Right eye
    right_eye_x = face_x + 3 * face_width // 4 - eye_width
    if eye_width > 2 and eye_height > 2:
        draw.ellipse([right_eye_x, eye_y, right_eye_x + eye_width, eye_y + eye_height], fill=(255, 255, 255))
        if eye_width > 4 and eye_height > 3:
            draw.ellipse([right_eye_x + 1, eye_y + 1, right_eye_x + eye_width - 1, eye_y + eye_height - 1], 
                        fill=(70, 130, 180))
        if eye_width > 6 and eye_height > 4:
            draw.ellipse([right_eye_x + 2, eye_y + 2, right_eye_x + eye_width - 2, eye_y + eye_height - 2], 
                        fill=(20, 20, 20))
    
    # Eyebrows (gray)
    brow_color = (160, 160, 160)
    if eye_y > 4:
        draw.ellipse([left_eye_x - 2, eye_y - 4, left_eye_x + eye_width + 2, eye_y], fill=brow_color)
        draw.ellipse([right_eye_x - 2, eye_y - 4, right_eye_x + eye_width + 2, eye_y], fill=brow_color)
    
    # Nose
    nose_x = face_x + face_width // 2 - 2
    nose_y = face_y + face_height // 2
    if nose_y + 6 <= face_y + face_height:
        draw.polygon([(nose_x, nose_y), (nose_x + 4, nose_y), (nose_x + 2, nose_y + 6)], fill=shadow_color)
    
    # Mouth
    mouth_y = face_y + 2 * face_height // 3
    mouth_x = face_x + face_width // 3
    mouth_width = max(3, face_width // 3)
    if mouth_y + 4 <= face_y + face_height and mouth_width > 2:
        draw.ellipse([mouth_x, mouth_y, mouth_x + mouth_width, mouth_y + 4], fill=(160, 100, 80))

def draw_wizard_beard(draw, beard_x, beard_y, beard_width, beard_height):
    """Draw flowing wizard beard"""
    beard_base = (220, 220, 220)  # Light gray
    beard_shadow = (180, 180, 180)  # Darker gray
    beard_highlight = (250, 250, 250)  # White highlights
    
    # Main beard shape (flowing)
    beard_points = [
        (beard_x, beard_y),
        (beard_x + beard_width, beard_y),
        (beard_x + beard_width + 5, beard_y + beard_height // 3),
        (beard_x + beard_width - 2, beard_y + 2 * beard_height // 3),
        (beard_x + beard_width - 8, beard_y + beard_height),
        (beard_x + 8, beard_y + beard_height - 3),
        (beard_x - 2, beard_y + 2 * beard_height // 3),
        (beard_x - 5, beard_y + beard_height // 3)
    ]
    draw.polygon(beard_points, fill=beard_base)
    
    # Beard texture lines
    for i in range(0, beard_height, 4):
        line_y = beard_y + i
        wave_offset = int(3 * math.sin(i * 0.5))
        draw.line([beard_x + wave_offset, line_y, 
                  beard_x + beard_width + wave_offset, line_y], 
                 fill=beard_shadow, width=1)
        
        # Highlights
        if i % 8 == 0:
            draw.line([beard_x + wave_offset + 2, line_y, 
                      beard_x + beard_width + wave_offset - 2, line_y], 
                     fill=beard_highlight, width=1)

def create_enhanced_magician():
    """Create 128x128 enhanced magician with transparent background"""
    
    # Create 128x128 image with transparent background
    img = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Define enhanced color palette
    wizard_hat_purple = (85, 26, 139)
    hat_highlight = (123, 63, 177)
    hat_shadow = (60, 20, 100)
    robe_purple = (106, 90, 205)
    robe_highlight = (138, 122, 230)
    robe_shadow = (75, 60, 145)
    gold_trim = (255, 215, 0)
    gold_shadow = (200, 165, 0)
    staff_orb_blue = (0, 191, 255)
    magic_glow = (127, 255, 212)
    
    # Draw wizard hat
    hat_x, hat_y = 35, 5
    hat_width, hat_height = 35, 45
    
    # Hat main shape (tall and pointed)
    hat_points = [
        (hat_x + hat_width // 2, hat_y),  # Top point
        (hat_x + hat_width // 2 + 8, hat_y + 15),
        (hat_x + hat_width, hat_y + hat_height),
        (hat_x, hat_y + hat_height)
    ]
    draw.polygon(hat_points, fill=wizard_hat_purple)
    
    # Hat brim
    draw.ellipse([hat_x - 8, hat_y + hat_height - 5, hat_x + hat_width + 8, hat_y + hat_height + 8], 
                fill=wizard_hat_purple)
    
    # Hat decorations - stars and moons
    star_points = [(hat_x + 15, hat_y + 20), (hat_x + 17, hat_y + 25), (hat_x + 22, hat_y + 25), 
                   (hat_x + 18, hat_y + 28), (hat_x + 20, hat_y + 33), (hat_x + 15, hat_y + 30),
                   (hat_x + 10, hat_y + 33), (hat_x + 12, hat_y + 28), (hat_x + 8, hat_y + 25),
                   (hat_x + 13, hat_y + 25)]
    draw.polygon(star_points, fill=gold_trim)
    
    # Crescent moon
    draw.ellipse([hat_x + 20, hat_y + 10, hat_x + 28, hat_y + 18], fill=gold_trim)
    draw.ellipse([hat_x + 22, hat_y + 8, hat_x + 30, hat_y + 16], fill=wizard_hat_purple)
    
    # Draw face
    face_x, face_y = 42, 45
    face_width, face_height = 25, 20
    draw_realistic_face(draw, face_x, face_y, face_width, face_height)
    
    # Draw flowing beard
    beard_x, beard_y = 35, 60
    beard_width, beard_height = 35, 40
    draw_wizard_beard(draw, beard_x, beard_y, beard_width, beard_height)
    
    # Draw robe body
    robe_x, robe_y = 30, 85
    robe_width, robe_height = 45, 40
    draw_fabric_texture(draw, robe_x, robe_y, robe_width, robe_height, 
                       robe_purple, robe_highlight, robe_shadow)
    
    # Gold trim on robe
    draw.rectangle([robe_x, robe_y, robe_x + robe_width, robe_y + 3], fill=gold_trim)
    draw.rectangle([robe_x, robe_y + 3, robe_x + robe_width, robe_y + 5], fill=gold_shadow)
    
    # Mystical belt
    belt_y = robe_y + 15
    draw.rectangle([robe_x + 5, belt_y, robe_x + robe_width - 5, belt_y + 4], fill=gold_trim)
    
    # Draw arms
    # Left arm (holding magic orb)
    left_arm_x, left_arm_y = 15, 90
    draw_fabric_texture(draw, left_arm_x, left_arm_y, 18, 25, 
                       robe_purple, robe_highlight, robe_shadow)
    
    # Magic orb in left hand
    orb_x, orb_y = left_arm_x + 5, left_arm_y + 25
    create_gradient_circle(draw, orb_x, orb_y, 8, magic_glow, staff_orb_blue)
    
    # Magical energy swirls around orb
    for angle in range(0, 360, 45):
        x_offset = int(12 * math.cos(math.radians(angle)))
        y_offset = int(12 * math.sin(math.radians(angle)))
        spark_x = orb_x + x_offset
        spark_y = orb_y + y_offset
        draw.ellipse([spark_x - 1, spark_y - 1, spark_x + 1, spark_y + 1], 
                    fill=magic_glow + (150,))
    
    # Right arm (holding staff)
    right_arm_x, right_arm_y = 70, 90
    draw_fabric_texture(draw, right_arm_x, right_arm_y, 18, 25, 
                       robe_purple, robe_highlight, robe_shadow)
    
    # Draw magical staff
    staff_x = right_arm_x + 8
    staff_y = right_arm_y - 30
    draw_magical_staff(draw, staff_x, staff_y, 60)
    
    # Draw legs/lower robe
    leg_width = 20
    # Left leg area
    draw_fabric_texture(draw, robe_x + 5, robe_y + robe_height - 5, leg_width, 8, 
                       robe_purple, robe_highlight, robe_shadow)
    
    # Right leg area  
    draw_fabric_texture(draw, robe_x + robe_width - leg_width - 5, robe_y + robe_height - 5, 
                       leg_width, 8, robe_purple, robe_highlight, robe_shadow)
    
    # Mystical shoes
    shoe_color = (25, 25, 112)  # Midnight blue
    draw.ellipse([robe_x + 2, robe_y + robe_height + 5, robe_x + 18, robe_y + robe_height + 12], 
                fill=shoe_color)
    draw.ellipse([robe_x + robe_width - 18, robe_y + robe_height + 5, 
                 robe_x + robe_width - 2, robe_y + robe_height + 12], fill=shoe_color)
    
    # Add magical sparkles around the character
    import random
    for _ in range(12):
        sparkle_x = random.randint(10, 118)
        sparkle_y = random.randint(10, 118)
        sparkle_size = random.randint(1, 3)
        sparkle_color = random.choice([magic_glow, staff_orb_blue, gold_trim])
        draw.ellipse([sparkle_x, sparkle_y, sparkle_x + sparkle_size, sparkle_y + sparkle_size], 
                    fill=sparkle_color + (random.randint(100, 200),))
    
    # Apply slight smoothing filter for more realistic look
    img = img.filter(ImageFilter.SMOOTH)
    
    return img

def main():
    """Generate the enhanced magician art"""
    print("🧙 Creating enhanced 128x128 magician art with transparent background...")
    
    # Create the enhanced magician
    magician_img = create_enhanced_magician()
    
    # Save the 128x128 version
    output_path_128 = os.path.join('art', 'Magician_realistic_128.png')
    os.makedirs('art', exist_ok=True)
    magician_img.save(output_path_128)
    print(f"✅ Saved 128x128 version: {output_path_128}")
    
    # Create scaled version for larger display (using high-quality resampling)
    magician_scaled = magician_img.resize((256, 256), Image.LANCZOS)
    output_path_scaled = os.path.join('art', 'Magician_realistic_128_scaled.png')
    magician_scaled.save(output_path_scaled)
    print(f"✅ Saved scaled version (256x256 display): {output_path_scaled}")
    
    print("🌟 Enhanced magician art generation complete!")
    print(f"📊 Base resolution: 128x128 pixels")
    print(f"🖼️  Display size: 256x256 pixels (scaled)")
    print(f"✨ Features: Transparent background, realistic shading, magical effects")
    print(f"🎭 Details: Wizard hat with stars/moon, flowing beard, magical staff with crystal orb,")
    print(f"          purple robes with gold trim, magical energy effects, mystical sparkles")

if __name__ == "__main__":
    main()