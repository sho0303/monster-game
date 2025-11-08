#!/usr/bin/env python3
"""
Create pixel-art style magician at 128x128 resolution with transparent background
Less realistic, more pixelated while maintaining enhanced details
"""

from PIL import Image, ImageDraw
import os
import math

def draw_pixelated_gradient(draw, x, y, width, height, color1, color2, direction='horizontal'):
    """Create a simple pixelated gradient effect"""
    steps = 8 if direction == 'horizontal' else 6
    step_size = width // steps if direction == 'horizontal' else height // steps
    
    for i in range(steps):
        ratio = i / (steps - 1)
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        
        if direction == 'horizontal':
            start_x = x + i * step_size
            end_x = x + (i + 1) * step_size if i < steps - 1 else x + width
            draw.rectangle([start_x, y, end_x, y + height], fill=(r, g, b))
        else:
            start_y = y + i * step_size
            end_y = y + (i + 1) * step_size if i < steps - 1 else y + height
            draw.rectangle([x, start_y, x + width, end_y], fill=(r, g, b))

def draw_pixelated_circle(draw, center_x, center_y, radius, fill_color, outline_color=None):
    """Draw a pixelated circle"""
    # Draw circle using rectangles for pixelated effect
    for y in range(-radius, radius + 1):
        for x in range(-radius, radius + 1):
            if x*x + y*y <= radius*radius:
                pixel_x = center_x + x
                pixel_y = center_y + y
                draw.rectangle([pixel_x, pixel_y, pixel_x + 1, pixel_y + 1], fill=fill_color)
    
    if outline_color:
        # Draw pixelated outline
        for angle in range(0, 360, 45):
            x = center_x + int(radius * math.cos(math.radians(angle)))
            y = center_y + int(radius * math.sin(math.radians(angle)))
            draw.rectangle([x, y, x + 1, y + 1], fill=outline_color)

def create_pixelated_magician():
    """Create 128x128 pixelated Gandalf-inspired magician with transparent background"""
    
    # Create 128x128 image with transparent background
    img = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Define Gandalf-inspired color palette
    wizard_hat_gray = (120, 120, 130)       # Gray wizard hat
    hat_shadow = (80, 80, 90)               # Dark gray shadow
    hat_highlight = (160, 160, 170)         # Light gray highlight
    robe_white = (240, 240, 245)            # White/light gray robes
    robe_shadow = (200, 200, 210)           # Robe shadow
    robe_highlight = (255, 255, 255)        # Pure white highlight
    belt_brown = (101, 67, 33)              # Brown leather belt
    belt_shadow = (68, 45, 22)              # Dark brown
    beard_white = (250, 250, 250)           # Pure white beard
    beard_gray = (220, 220, 220)            # Light gray beard
    beard_shadow = (180, 180, 180)          # Gray beard shadow
    skin_color = (240, 210, 180)            # Aged skin tone
    staff_brown = (101, 67, 33)             # Wood brown staff
    staff_highlight = (140, 95, 50)         # Light wood
    staff_shadow = (68, 45, 22)             # Dark brown
    magic_white = (255, 255, 255)           # Bright white magic
    magic_blue = (200, 220, 255)            # Soft blue magic
    eye_gray = (100, 120, 140)              # Wise gray eyes
    
    # Draw Gandalf-style pointed hat (tall and gray)
    hat_x, hat_y = 42, 5
    hat_width, hat_height = 28, 38
    
    # Hat main triangle shape - Gandalf's classic pointed hat
    hat_points = [
        (hat_x + hat_width // 2, hat_y),           # Sharp top point
        (hat_x + hat_width // 2 + 4, hat_y + 15), # Slight right curve
        (hat_x + hat_width - 1, hat_y + hat_height), # Bottom right
        (hat_x + 1, hat_y + hat_height)            # Bottom left
    ]
    draw.polygon(hat_points, fill=wizard_hat_gray)
    
    # Add shading to hat (right side shadow)
    shadow_points = [
        (hat_x + hat_width // 2 + 1, hat_y + 3),
        (hat_x + hat_width // 2 + 4, hat_y + 15),
        (hat_x + hat_width - 1, hat_y + hat_height),
        (hat_x + hat_width // 2 + 1, hat_y + hat_height)
    ]
    draw.polygon(shadow_points, fill=hat_shadow)
    
    # Hat brim (small, Gandalf-style)
    brim_y = hat_y + hat_height - 1
    draw.rectangle([hat_x - 4, brim_y, hat_x + hat_width + 4, brim_y + 4], fill=wizard_hat_gray)
    draw.rectangle([hat_x - 2, brim_y + 2, hat_x + hat_width + 2, brim_y + 4], fill=hat_shadow)
    
    # Simple hat decoration (no stars/moons - Gandalf's hat is plain)
    # Just add a subtle band
    band_y = hat_y + hat_height - 8
    draw.rectangle([hat_x + 2, band_y, hat_x + hat_width - 2, band_y + 2], fill=hat_shadow)
    
    # Draw Gandalf's wise face (pixelated)
    face_x, face_y = 47, 38
    face_width, face_height = 18, 14
    
    # Face base (aged skin)
    draw.rectangle([face_x, face_y, face_x + face_width, face_y + face_height], fill=skin_color)
    
    # Eyes (wise and piercing - Gandalf style)
    eye_y = face_y + 4
    # Left eye (slightly larger for wisdom)
    draw.rectangle([face_x + 3, eye_y, face_x + 6, eye_y + 3], fill=(255, 255, 255))
    draw.rectangle([face_x + 4, eye_y + 1, face_x + 5, eye_y + 2], fill=eye_gray)
    
    # Right eye
    draw.rectangle([face_x + face_width - 6, eye_y, face_x + face_width - 3, eye_y + 3], fill=(255, 255, 255))
    draw.rectangle([face_x + face_width - 5, eye_y + 1, face_x + face_width - 4, eye_y + 2], fill=eye_gray)
    
    # Bushy gray eyebrows (Gandalf's signature feature)
    draw.rectangle([face_x + 2, eye_y - 2, face_x + 7, eye_y - 1], fill=beard_gray)
    draw.rectangle([face_x + 1, eye_y - 3, face_x + 5, eye_y - 2], fill=beard_white)  # Extra bushy
    draw.rectangle([face_x + face_width - 7, eye_y - 2, face_x + face_width - 2, eye_y - 1], fill=beard_gray)
    draw.rectangle([face_x + face_width - 5, eye_y - 3, face_x + face_width - 1, eye_y - 2], fill=beard_white)
    
    # Nose (prominent)
    nose_y = face_y + 7
    draw.rectangle([face_x + face_width//2 - 1, nose_y, face_x + face_width//2 + 1, nose_y + 3], fill=(220, 190, 160))
    
    # Mouth (barely visible under mustache)
    mouth_y = face_y + 10
    draw.rectangle([face_x + 6, mouth_y, face_x + 12, mouth_y], fill=(210, 180, 150))
    
    # Show visible neck area (skin tone)
    neck_x, neck_y = face_x + 3, face_y + face_height
    neck_width, neck_height = face_width - 6, 8
    draw.rectangle([neck_x, neck_y, neck_x + neck_width, neck_y + neck_height], fill=skin_color)
    
    # Draw Gandalf's flowing beard (starting lower, leaving face and neck visible)
    beard_x, beard_y = 38, neck_y + neck_height - 2  # Start below the neck
    beard_width, beard_height = 30, 28
    
    # Main beard shape (flowing downward from chin area)
    draw.rectangle([beard_x, beard_y, beard_x + beard_width, beard_y + beard_height], fill=beard_white)
    
    # Beard flow pattern (wider at top, narrower at bottom like natural beards)
    # Upper beard (fuller at chin)
    draw.rectangle([beard_x - 2, beard_y, beard_x + beard_width + 2, beard_y + 12], fill=beard_white)
    # Lower flowing part (tapered)
    draw.rectangle([beard_x + 4, beard_y + 12, beard_x + beard_width - 4, beard_y + beard_height + 3], fill=beard_white)
    
    # Beard texture (flowing strands)
    for i in range(0, beard_height + 3, 4):
        line_y = beard_y + i
        # Wavy texture lines
        wave_offset = 1 if i % 8 == 0 else 0
        draw.rectangle([beard_x + 2 + wave_offset, line_y, beard_x + beard_width - 2 + wave_offset, line_y], fill=beard_gray)
        if i % 8 == 0:  # Bright white highlights
            draw.rectangle([beard_x + 4, line_y + 1, beard_x + beard_width - 4, line_y + 1], fill=(255, 255, 255))
    
    # Mustache (separate from main beard, just above mouth)
    mustache_y = face_y + 9
    draw.rectangle([face_x + 3, mustache_y, face_x + face_width - 3, mustache_y + 2], fill=beard_white)
    draw.rectangle([face_x + 2, mustache_y + 1, face_x + face_width - 2, mustache_y + 1], fill=beard_gray)
    
    # Draw Gandalf's white/gray robes (flowing and majestic)
    robe_x, robe_y = 30, 78
    robe_width, robe_height = 42, 38
    
    # Main robe rectangle (white/light gray like Gandalf the White)
    draw.rectangle([robe_x, robe_y, robe_x + robe_width, robe_y + robe_height], fill=robe_white)
    
    # Robe shading (subtle gray shadows)
    draw.rectangle([robe_x, robe_y, robe_x + 3, robe_y + robe_height], fill=robe_shadow)
    draw.rectangle([robe_x + robe_width - 3, robe_y, robe_x + robe_width, robe_y + robe_height], fill=robe_shadow)
    
    # Robe highlights (pure white center)
    draw.rectangle([robe_x + 6, robe_y, robe_x + robe_width - 6, robe_y + 6], fill=robe_highlight)
    
    # Simple brown leather belt (Gandalf style)
    belt_y = robe_y + 18
    draw.rectangle([robe_x + 8, belt_y, robe_x + robe_width - 8, belt_y + 4], fill=belt_brown)
    draw.rectangle([robe_x + 10, belt_y + 1, robe_x + robe_width - 10, belt_y + 3], fill=belt_shadow)
    
    # Belt buckle (simple rectangle)
    buckle_x = robe_x + robe_width // 2 - 3
    draw.rectangle([buckle_x, belt_y, buckle_x + 6, belt_y + 4], fill=belt_shadow)
    
    # Draw left arm (gesturing - Gandalf often gestures with his left hand)
    left_arm_x, left_arm_y = 18, 88
    arm_width, arm_height = 15, 22
    
    # White robe sleeve
    draw.rectangle([left_arm_x, left_arm_y, left_arm_x + arm_width, left_arm_y + arm_height], fill=robe_white)
    draw.rectangle([left_arm_x, left_arm_y, left_arm_x + 2, left_arm_y + arm_height], fill=robe_shadow)
    
    # Hand (aged but strong)
    draw.rectangle([left_arm_x + 4, left_arm_y + arm_height - 4, left_arm_x + 11, left_arm_y + arm_height], fill=skin_color)
    
    # Subtle white magic glow (Gandalf's power is more subtle)
    magic_x, magic_y = left_arm_x + 7, left_arm_y + arm_height + 1
    draw_pixelated_circle(draw, magic_x, magic_y, 4, magic_white)
    draw_pixelated_circle(draw, magic_x, magic_y, 2, magic_blue)
    
    # Gentle magic sparkles (white light)
    sparkle_positions = [(magic_x - 6, magic_y - 1), (magic_x + 6, magic_y + 1), (magic_x - 2, magic_y - 6)]
    for sx, sy in sparkle_positions:
        draw.rectangle([sx, sy, sx + 1, sy + 1], fill=magic_white)
    
    # Draw right arm (holding Gandalf's staff)
    right_arm_x, right_arm_y = 72, 88
    
    # White robe sleeve
    draw.rectangle([right_arm_x, right_arm_y, right_arm_x + arm_width, right_arm_y + arm_height], fill=robe_white)
    draw.rectangle([right_arm_x + arm_width - 2, right_arm_y, right_arm_x + arm_width, right_arm_y + arm_height], fill=robe_shadow)
    
    # Hand gripping staff
    draw.rectangle([right_arm_x + 5, right_arm_y + arm_height - 4, right_arm_x + 11, right_arm_y + arm_height], fill=skin_color)
    
    # Gandalf's iconic staff (tall and wooden)
    staff_x = right_arm_x + 7
    staff_y = right_arm_y - 35
    staff_width = 4
    staff_length = 65
    
    # Main wooden staff (gnarled and natural)
    draw.rectangle([staff_x, staff_y, staff_x + staff_width, staff_y + staff_length], fill=staff_brown)
    draw.rectangle([staff_x, staff_y, staff_x + 1, staff_y + staff_length], fill=staff_highlight)
    draw.rectangle([staff_x + staff_width - 1, staff_y, staff_x + staff_width, staff_y + staff_length], fill=staff_shadow)
    
    # Wood grain and knots (natural wood texture)
    for i in range(0, staff_length, 8):
        draw.rectangle([staff_x + 1, staff_y + i, staff_x + staff_width - 1, staff_y + i], fill=staff_shadow)
    
    # Staff knots (Gandalf's staff has natural wood knots)
    knot_positions = [staff_y + 15, staff_y + 35, staff_y + 50]
    for knot_y in knot_positions:
        draw.rectangle([staff_x - 1, knot_y, staff_x + staff_width + 1, knot_y + 2], fill=staff_brown)
        draw.rectangle([staff_x, knot_y + 1, staff_x + staff_width, knot_y + 1], fill=staff_shadow)
    
    # Gandalf's staff top (more like a natural crystal/orb)
    crystal_x, crystal_y = staff_x - 1, staff_y - 6
    
    # White crystal (like Gandalf's staff light)
    draw.rectangle([crystal_x, crystal_y, crystal_x + 6, crystal_y + 8], fill=magic_white)
    draw.rectangle([crystal_x + 1, crystal_y + 1, crystal_x + 5, crystal_y + 7], fill=(245, 245, 255))
    draw.rectangle([crystal_x + 2, crystal_y + 2, crystal_x + 4, crystal_y + 6], fill=magic_blue)
    
    # Soft glow around crystal
    draw.rectangle([crystal_x - 1, crystal_y + 2, crystal_x, crystal_y + 6], fill=(240, 240, 255, 128))
    draw.rectangle([crystal_x + 6, crystal_y + 2, crystal_x + 7, crystal_y + 6], fill=(240, 240, 255, 128))
    
    # Draw legs/feet (under flowing robes)
    # Left leg (mostly hidden under white robes)
    draw.rectangle([robe_x + 10, robe_y + robe_height - 5, robe_x + 20, robe_y + robe_height + 6], fill=robe_white)
    # Left boot (Gandalf's sturdy boots)
    draw.rectangle([robe_x + 8, robe_y + robe_height + 3, robe_x + 22, robe_y + robe_height + 8], fill=(101, 67, 33))
    
    # Right leg (mostly hidden under white robes)
    draw.rectangle([robe_x + robe_width - 20, robe_y + robe_height - 5, robe_x + robe_width - 10, robe_y + robe_height + 6], fill=robe_white)
    # Right boot
    draw.rectangle([robe_x + robe_width - 22, robe_y + robe_height + 3, robe_x + robe_width - 8, robe_y + robe_height + 8], fill=(101, 67, 33))
    
    # Add subtle magical aura (white light around Gandalf)
    aura_positions = [
        (30, 35), (85, 40), (25, 75), (90, 80), (35, 105), (80, 100),
        (50, 30), (70, 110), (28, 55), (88, 60)
    ]
    
    for sx, sy in aura_positions:
        # Soft white/blue magical aura (like Gandalf's subtle power)
        color = magic_white if (sx + sy) % 3 == 0 else magic_blue
        draw.rectangle([sx, sy, sx + 1, sy + 1], fill=color)
    
    return img

def main():
    """Generate the pixelated magician art"""
    print("🧙 Creating pixelated 128x128 magician art with transparent background...")
    
    # Create the pixelated magician
    magician_img = create_pixelated_magician()
    
    # Save the 128x128 version
    output_path_128 = os.path.join('art', 'Magician_pixelated_128.png')
    os.makedirs('art', exist_ok=True)
    magician_img.save(output_path_128)
    print(f"✅ Saved 128x128 version: {output_path_128}")
    
    # Create scaled version for larger display (using nearest neighbor for pixel perfect scaling)
    magician_scaled = magician_img.resize((256, 256), Image.NEAREST)
    output_path_scaled = os.path.join('art', 'Magician_pixelated_128_scaled.png')
    magician_scaled.save(output_path_scaled)
    print(f"✅ Saved scaled version (256x256 display): {output_path_scaled}")
    
    print("🎮 Pixelated magician art generation complete!")
    print(f"📊 Base resolution: 128x128 pixels")
    print(f"🖼️  Display size: 256x256 pixels (pixel-perfect scaled)")
    print(f"✨ Features: Transparent background, pixelated style, magical effects")
    print(f"🎭 Details: Blocky wizard hat with pixel stars, rectangular beard, chunky robes,")
    print(f"          pixelated staff with diamond crystal, simple magic orb, retro sparkles")

if __name__ == "__main__":
    main()